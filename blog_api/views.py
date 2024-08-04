from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Blog
from .serializers import BlogSerializer
from django.db.models import Q

class BlogListApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the Blog items for given requested user
        '''
        search_query = request.query_params.get('search', None)
        
        # Use search query parameter to filter blogs
        if search_query:
            Blogs = Blog.objects.filter(
                Q(title__icontains=search_query) | Q(auther__name__icontains=search_query)
            )
        else:
            Blogs = Blog.objects.all()

        serializer = BlogSerializer(Blogs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Blog with given Blog data
        '''
        data = request.data
        
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetailApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, blog_id):
        '''
        Helper method to get the object with given blog_id, and user_id
        '''
        try:
            return Blog.objects.get(id=blog_id)
        except Blog.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, blog_id, *args, **kwargs):
        '''
        Retrieves the Blog with given blog_id
        '''
        blog_instance = self.get_object(blog_id)
        if not blog_instance:
            return Response(
                {"res": "Object with Blog id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BlogSerializer(blog_instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, blog_id, *args, **kwargs):
        '''
        Updates the blog item with given blog_id if exists
        '''
        blog_instance = self.get_object(blog_id)
        if not blog_instance:
            return Response(
                {"res": "Object with blog id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = request.data

        serializer = BlogSerializer(instance = blog_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, blog_id, *args, **kwargs):
        '''
        Deletes the blog item with given blog_id if exists
        '''
        blog_instance = self.get_object(blog_id)
        if not blog_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        blog_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )