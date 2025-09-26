# from rest_framework import serializers

# from chats.utils import encrypt_message, decrypt_message
# from chats.models import Chat, Message
# from users.serializers import UserSerializer


# class ChatSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     is_group = serializers.BooleanField()
#     title = serializers.CharField(max_length=100)
#     users = serializers.ListField(child=serializers.IntegerField())

#     def create(self, validated_data: dict):
#         chat = Chat(
#             is_group=validated_data.get("is_group"),
#             title=validated_data.get("title"),
#         )
#         chat.save()
#         users = validated_data.get("users")
#         chat.users.set(users)
#         return chat

#     def update(self, instance: Chat, validated_data: dict):
#         # users = validated_data.pop("users")
#         for key, value in validated_data.items():
#             if key == "users":
#                 instance.users.set(value)
#                 continue
#             setattr(instance, key, value)
#         # if users:
#         #     instance.users.set(users)
#         instance.save()
#         return instance


# class MessageViewSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     text = serializers.SerializerMethodField(
#         method_name="get_decrypted_message"
#     )
#     parent = serializers.IntegerField(required=False)
#     sender = UserSerializer()

#     def get_decrypted_message(self, obj: Message):
#         return decrypt_message(encrypted_text=obj.text)


# class ChatViewSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     is_group = serializers.BooleanField()
#     title = serializers.CharField(max_length=100)
#     users = UserSerializer(many=True)
#     chat_messages = MessageViewSerializer(many=True)


# class MessageSerializer(serializers.Serializer):
#     text = serializers.CharField(max_length=2000)
#     chat = serializers.IntegerField()
#     parent = serializers.IntegerField(required=False)

#     def create(self, validated_data: dict):
#         validated_data["sender"] = self.context.get("user")
#         validated_data["chat"] = self.context.get("chat")
#         validated_data["text"] = encrypt_message(
#             text=validated_data.get("text")
#         )
#         message = Message(**validated_data)
#         message.save()
#         return message

#     def update(self, instance: Message, validated_data: dict):
#         validated_data["text"] = encrypt_message(
#             text=validated_data.get("text")
#         )
#         return super().update(instance, validated_data)
