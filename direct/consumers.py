from .models import *
from channels.generic.websocket import WebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Q
import json


class ChatConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.room = None

    def connect(self):
        self.user = self.scope['user']
        self.receiver = self.scope['url_route']['kwargs']['receiver']
        author_user = User.object.filter(username=self.user.username)[0]
        receiver_user = User.objects.filter(username=self.receiver)[0]
        if Room.objects.filter(
                Q(sender=author_user, receiver=receiver_user) | Q(sender=receiver_user, receiver=author_user)).exists():
            self.room = Room.objects.filter(
                Q(sender=author_user, receiver=receiver_user) | Q(sender=receiver_user, receiver=author_user))[0]
        else:
            self.room = Room.objects.create(sender=author_user, receiver=receiver_user)
        self.room_group_name = 'chat_%s' % str(self.room.id)
        async_to_sync(self.channel_layer.group_add)(
            self.room.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))

    def typing_start(self, data):
        sender = data['from']
        content = {
            'command': 'typing_start',
            'message': sender
        }
        return self.send_chat_message(content)

    def typing_stop(self, data):
        content = {
            'command': 'typing_stop'
        }
        return self.send_chat_message(content)

    def new_message(self, data):
        sender = data['from']
        receiver = data['receiver']
        sender_user = User.objects.filter(username=sender)[0]
        receiver_user = User.objects.filter(username=receiver)[0]
        message = Message.objects.create(
            sender=sender_user,
            receiver=receiver_user,
            room=self.room,
            message=data['message']
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def fetch_messages(self, data):
        sender = User.objects.get(username=data['sender'])
        receiver = User.objects.get(username=data['receiver'])
        messages = Message.objects.filter(Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender)) \
                       .order_by('time_stamp')[:20]
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'typing_start': typing_start,
        'typing_stop': typing_stop,
    }

    @staticmethod
    def message_to_json(message):
        return {
            'sender': message.sender.username,
            'receiver': message.receiver.username,
            'content': message.message,
            'time_stamp': str(message.time_stamp)
        }

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result
