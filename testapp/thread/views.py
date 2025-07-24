from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from .models import (
    ThreadPost,
    Comment
)
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from .serializer import ThreadPostSerializer

@permission_classes([AllowAny])
class MyTokenObtainPairView(TokenObtainPairView):
    pass


class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User(username=username)
            user.set_password(password)
            user.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(password):
            return Response({"message": "Login successful", "user_id": user.id})
        else:
            return Response({"error": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True,methods=['post'],url_name='upvote')
    def upvote(self,request,pk=None):
        print(request.data)
        post = get_object_or_404(ThreadPost, postid=pk)
        user=User.objects.get(username=request.user)
        post.vote(user_id=user.id,vote_type="upvote")
        serializer = ThreadPostSerializer(post)

        return Response({
            "message": "Post upvoted",
            "data":serializer.data,
        }, status=201)

    @action(detail=True,methods=['post'],url_name='downvote')
    def downvote(self,request,pk=None):
        print(request.data)
        post = get_object_or_404(ThreadPost, postid=pk)
        user=User.objects.get(username=request.user)
        post.vote(user_id=user.id,vote_type="downvote")

        serializer = ThreadPostSerializer(post)

        return Response({
            "message": "Post downvoted",
            "data":serializer.data,
        }, status=201)


    @action(detail=False, methods=["post"], url_path="create-post")
    def create_post(self, request):
        content = request.data.get("content")
        if not content:
            return Response({"error": "Content is required"}, status=400)

        post = ThreadPost.objects.create(owner=User.objects.get(username=request.user), content=content)
        return Response({
            "message": "Post created",
            "post_id": str(post.postid),
            "owner": post.owner.username,
            "content": post.content
        }, status=201)
    

    @action(detail=False, methods=["get"], url_path="all-posts")
    def list_posts(self, request):
        posts = ThreadPost.objects.all()
        serializer = ThreadPostSerializer(posts, many=True)
        data =serializer.data
        return Response(data, status=200)
    
    @action(detail=False,methods=['post'],url_path='comment')
    def comment(self,request,pk=None):
        user=get_object_or_404(User, username=request.user)
        post=get_object_or_404(ThreadPost, postid=pk)
        comment= request.data.get("comment")
        if not comment:
            return Response({"error": "comment body is required"}, status=400)
  
        comment =Comment.objects.create(
            post=post,
            owner=user,
            commenttext=comment
        )

        return Response(
            {
            "message": "comment created",
            "post_id": str(post.postid),
            "user": user.username,
            "content": comment.commenttext
            }, status=201)
    