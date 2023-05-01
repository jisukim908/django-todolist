from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer, UserUpdateSerializer, UserListSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)
from users.models import User

# Create your views here.
class UserView(APIView):
    # 전체조회
    def get(self, request):
        alluser = User.objects.all()
        serializer = UserListSerializer(alluser, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 가입
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status= status.HTTP_400_BAD_REQUEST)


class UserInformationView(APIView):  
    # 로그인한 사용자 정보 조회  
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"message":"로그인해주세요."},401)
        return Response(UserListSerializer(request.user).data, status=status.HTTP_200_OK)

    # 로그인한 사용자 정보 수정
    def put(self, request, user_id):
        if not request.user.is_authenticated:
            return Response({"message":"로그인해주세요."},401)
        
        user = get_object_or_404(User,id=user_id)
        if (request.user).id == user_id:
            serializer = UserUpdateSerializer(user, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

    # 로그인한 사용자 정보 탈퇴(삭제)
    def delete(self, request, user_id):
        if not request.user.is_authenticated:
            return Response({"message":"로그인해주세요."},401)
        
        if (request.user).id == user_id:
           user = request.user
           user.is_active == False
           user.save()
           # 회원 탈퇴한다고 유저정보를 삭제하지는 않는다..!
           # user = get_object_or_404(User,id=user_id)
           # user.delete() 
           # 이렇게 사용하지 않는다.
           # 보통 비활성화를 한다.
           return Response("탈퇴했습니다.", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)
            
    # 휴면계정과 탈퇴계정 구분하는 것도 생각해볼만 하다.

# customize token
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# 실제로 로그인이 되었는지 확인
class mockView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response("get 요청")