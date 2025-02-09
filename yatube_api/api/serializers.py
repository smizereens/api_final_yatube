from rest_framework import serializers
from rest_framework.relations import SlugRelatedField as SRField
from posts.models import Comment, Post, User, Follow, Group


class PostSerializer(serializers.ModelSerializer):
    author = SRField(
        slug_field='username',
        read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = SRField(
        read_only=True,
        slug_field='username')
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = SRField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )

    class Meta:
        model = Follow
        fields = ('id', 'user', 'following')

    def validate(self, data):
        user = self.context['request'].user
        following = data['following']
        if user == following:
            raise serializers.ValidationError("You cannot follow yourself.")
        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                "You are already following this user.")
        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
