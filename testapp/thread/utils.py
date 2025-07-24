from .models import ThreadPost,Vote

def handle_vote(user,post,vote_type):
    """
    vote_type: 1 (upvote) or -1 (downvote)
    """
    try:
        vote = Vote.objects.get(user=user, post=post)
        if vote.value == vote_type:
            vote.delete()
            return "removed"
        else:
            vote.value = vote_type
            vote.save()
            return "switched"
    except Vote.DoesNotExist:
        Vote.objects.create(user=user, post=post, value=vote_type)
        return "created"
