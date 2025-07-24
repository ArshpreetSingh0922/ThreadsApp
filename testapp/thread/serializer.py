from rest_framework import serializers
from .models import ThreadPost

class ThreadPostSerializer(serializers.ModelSerializer):
    total_upvotes = serializers.SerializerMethodField()
    total_downvotes = serializers.SerializerMethodField()
    owner = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = ThreadPost
        fields = [
            'postid',
            'owner',
            'content',
            'total_upvotes',
            'total_downvotes',
        ]

    def get_total_upvotes(self, obj):
        return len(obj.upvotes)

    def get_total_downvotes(self, obj):
        return len(obj.downvotes)
