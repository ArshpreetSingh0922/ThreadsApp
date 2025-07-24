from django.urls import path
from .views import (
    UserViewSet,
    MyTokenObtainPairView,
    TokenRefreshView,
    PostViewSet
)




urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'register'}), name='user-register'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='user-login'),
    path('auth/login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('thread-post/create-post/', PostViewSet.as_view({'post': 'create_post'}), name="create_post"),
    path('thread-post/all-posts/', PostViewSet.as_view({'get': 'list_posts'}), name="list_posts"),

    path('thread-post/<uuid:pk>/upvote/', PostViewSet.as_view({'post': 'upvote'}), name="upvote_post"),
    path('thread-post/<uuid:pk>/downvote/', PostViewSet.as_view({'post': 'downvote'}), name="downvote_post"),
    path('thread-post/<uuid:pk>/add-comment/', PostViewSet.as_view({'post': 'comment'}), name="comment"),

]
