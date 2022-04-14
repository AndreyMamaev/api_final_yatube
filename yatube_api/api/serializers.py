from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post', 'author')


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('user',)
        model = Follow

    def validate_following(self, value):
        if self.context.get('request').user == value:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя!"
            )
        elif Follow.objects.filter(
            user=self.context.get('request').user, following=value
        ).exists():
            raise serializers.ValidationError(
                "Нельзя подписаться на уже подписанного автора!"
            )
        return value
