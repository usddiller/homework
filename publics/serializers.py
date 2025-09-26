# from rest_framework import serializers

# from publics.models import Public, PublicInvite
# from users.serializers import UserSerializer


# class PublicSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=200)
#     is_private = serializers.BooleanField(default=False)
#     members = serializers.ListField(
#         required=False,
#         child=serializers.IntegerField()
#     )
#     delete_members = serializers.ListField(
#         required=False,
#         child=serializers.IntegerField()
#     )

#     def validate(self, attrs: dict):
#         title = attrs.get("title")
#         if Public.objects.filter(title=title).exists():
#             raise serializers.ValidationError(
#                 detail=f"Public with title: {title} already exist!"
#             )
#         return super().validate(attrs)

#     def create(self, validated_data: dict):
#         public = Public(
#             owner=self.context.get("owner"),
#             title=validated_data.get("title"),
#             is_private=validated_data.get("is_private")
#         )
#         public.save()
#         public.members.set(objs=validated_data.get("members"))
#         return public
    
#     def update(self, instance: Public, validated_data: dict):
#         for key, value in validated_data.items():
#             if key == "delete_members":
#                 instance.members.remove(*value)
#                 continue
#             elif key == "members":
#                 instance.members.add(*value)
#                 continue
#             setattr(instance, key, value)
#         instance.save()
#         return instance


# class PublicViewSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(read_only=True, max_length=200)
#     owner = UserSerializer()
#     members = UserSerializer(many=True)
#     is_private = serializers.BooleanField(read_only=True)
