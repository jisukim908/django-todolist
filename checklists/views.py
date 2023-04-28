from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from checklists.models import Todolist
from checklists.serializers import TodolistSerializer, TodolistCreateSerializer, TodolistListSerializer
from django.utils import timezone

# Create your views here.
class TodolistView(APIView):
    # 전체 조회
    def get(self, request):
        checklists = Todolist.objects.all()
        serializer = TodolistListSerializer(checklists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 추가하기
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"message":"로그인해주세요."},401)
        
        serializer = TodolistCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class TodolistDetailView(APIView):
    # 로그인한 사용자의 todolist 조회
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"message":"로그인해주세요."},401)
        current_user = request.user
        # 여러개의 todolist를 가지고와야하니까 get_object를 쓰면 오류가 난다.
        # get_object 는 한 개를 가지고온다.
        todolists = Todolist.objects.filter(user_id = current_user.id)
        serializer = TodolistListSerializer(todolists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    # 로그인한 사용자의 todolist 수정
    def put(self, request, todolist_id):
        if not request.user.is_authenticated:
            return Response({"message":"로그인해주세요."},401)
        todolist = get_object_or_404(Todolist, id=todolist_id)
        if request.user == todolist.user:
            serializer = TodolistCreateSerializer(todolist, data=request.data)
            if serializer.is_valid():
                if request.data.get("is_complete") == "True":
                    serializer.save(completion_at=timezone.now())
                else:
                    serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)
        

    # 로그인한 사용자 todolist 삭제
    def delete(self, request, todolist_id):
        if not request.user.is_authenticated:
            return Response({"message":"로그인해주세요."},401)
        todolist = get_object_or_404(Todolist, id=todolist_id)
        if request.user == todolist.user:
            todolist.delete()
            return Response("삭제되었습니다.",status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

    
