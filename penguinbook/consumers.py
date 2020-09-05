# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message 
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        print('connection established')
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room /group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user_id']
        message_receiver_id=text_data_json['message_receiver_id']
        print("user_id:",user_id)
        print("message:", message)
        print("message_receiver_id:", message_receiver_id)
        Message.objects.create(user_id=user_id, message=message, message_receiver_id=message_receiver_id)
        # obj = Message(message=self.scope['url_route']['kwargs']['room_name'])
        # obj.message=message
        # obj.save()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id':user_id,
            }
        )
        print('socket receive')
    # Receive message from room/ group
    def chat_message(self, event):

        message = event['message']
        user_id = event['user_id']
        # room_name = event['roomName']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'user_id': user_id,
        }))
        print('socket chat_receive')

    # def fetch_messages(self):
    #     pass

