from rest_framework.decorators import APIView, api_view, permission_classes
from roboproject.serializers import PostSerializer, CommentSerializer
from roboproject.models import Post
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class PostAPI(APIView):
    
    parser_class = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = PostSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request):
        if request.user.is_admin:
            data = request.data
            obj=Post.objects.get(id = data['id'])
            obj.delete()
            return Response({'message':'Post deleted'})
        else: 
            return Response({
                'status' : 'False',
                'message': 'Pehli fursat mein nikal'
                }, status.HTTP_400_BAD_REQUEST)
            


@api_view(['GET'])    
def get_projects(request):
    objs = Post.objects.filter(is_verified = True)
    try:
        page = request.GET.get('page',1)
        page_size = 10
        paginator  = Paginator(objs, page_size)
        serializer = PostSerializer(paginator.page(page), many = True)
    except Exception as e:
        return Response({
            'status' : 'False',
            'message': 'Empty Page'
            }, status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data)

@api_view(['POST'])
def post_comment(request, pk):
        data = request.data
        data= {"post": pk, "commentText" : data['commentText']}
        serializer = CommentSerializer(data=data)
        print("hello")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        
@api_view(['PUT'])
def react(request, pk, arg, num):
    obj=Post.objects.get(id = pk)
    data= {arg : num}
    serializer = PostSerializer(obj, data= data, partial = True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def verify(request, pk):
    if request.user.is_admin:
        obj=Post.objects.get(id = pk)
        data= {"is_verified": True}
        serializer = PostSerializer(obj, data= data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    else: 
        return Response({
            'status' : 'False',
            'message': 'Admin bnja phle ***'
            }, status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unverified(request):
    if request.user.is_admin:
        objs = Post.objects.filter(is_verified =False)
        serializer = PostSerializer(objs, many = True)
        return Response(serializer.data)
    else: 
        return Response({
            'status' : 'False',
            'message': 'Pehli fursat mein nikal'
            }, status.HTTP_400_BAD_REQUEST)