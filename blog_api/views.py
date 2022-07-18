from lib2to3.pytree import Base
from rest_framework import generics
from blog.models import Post
from  .serializers import PostSerializer
from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission, 
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    DjangoModelPermissions, 
    DjangoModelPermissionsOrAnonReadOnly,
)

class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        
        return obj.author == request.user # if the author(creator) of a Post is the user making the request, then return True

class PostList(generics.ListCreateAPIView):
    # permission_classes = (IsAdminUser, ) # need to make the object iterable by either making it into a list or tuple
    # permission_classes = (DjangoModelPermissions, )
    permission_classes = (IsAuthenticatedOrReadOnly, )
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer


class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
    permission_classes = (PostUserWritePermission, )
    queryset = Post.objects.all()
    serializer_class = PostSerializer


""" Concrete View Classes
#CreateAPIView
Used for create-only endpoints.
#ListAPIView
Used for read-only endpoints to represent a collection of model instances.
#RetrieveAPIView
Used for read-only endpoints to represent a single model instance.
#DestroyAPIView
Used for delete-only endpoints for a single model instance.
#UpdateAPIView
Used for update-only endpoints for a single model instance.
##ListCreateAPIView
Used for read-write endpoints to represent a collection of model instances.
RetrieveUpdateAPIView
Used for read or update endpoints to represent a single model instance.
#RetrieveDestroyAPIView
Used for read or delete endpoints to represent a single model instance.
#RetrieveUpdateDestroyAPIView
Used for read-write-delete endpoints to represent a single model instance.
"""
