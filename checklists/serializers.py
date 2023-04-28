from rest_framework import serializers
from checklists.models import Todolist

class TodolistSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Todolist
        fields = '__all__'


class TodolistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todolist
        fields = ("title", "is_complete")
    

class TodolistListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email
    
    class Meta:
        model = Todolist
        fields = ("pk", "title", "user", "created_at", "updated_at", "is_complete")