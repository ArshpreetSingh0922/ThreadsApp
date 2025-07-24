from django.db import models
import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User


class ThreadPost(models.Model):
    postid=models.UUIDField(primary_key=True,default=uuid.uuid1,editable=False)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.CharField(max_length=2000)
    upvotes = models.JSONField(default=list, blank=True)
    downvotes = models.JSONField(default=list, blank=True)

    def total_upvotes(self):
        return len(self.upvotes)

    def total_downvotes(self):
        return len(self.downvotes)

    def vote(self, user_id: int, vote_type: str):
        if vote_type == "upvote":
            if user_id not in self.upvotes:
                self.upvotes.append(user_id)
                if user_id in self.downvotes:
                    self.downvotes.remove(user_id)
        elif vote_type == "downvote":
            if user_id not in self.downvotes:
                self.downvotes.append(user_id)
                if user_id in self.upvotes:
                    self.upvotes.remove(user_id)
        self.save()


class Comment(models.Model):
    commentid=models.UUIDField(primary_key=True,default=uuid.uuid1,editable=False)
    post=models.ForeignKey(ThreadPost,on_delete=models.CASCADE,related_name='comments')
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    commenttext=models.CharField(max_length=2000)
