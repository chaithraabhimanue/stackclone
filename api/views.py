from django.shortcuts import render
from django.contrib.auth.models import User
from api.serializers import UserSerializer,QuestionSerializer,AnswerSerializers,ProfileSerializer
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from stack.models import UserProfile,Questions,Answers
from rest_framework import authentication,permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action


class UsersView(GenericViewSet,CreateModelMixin):
    serializer_class=UserSerializer
    queryset=User.objects.all()
                
class ProfileView(ModelViewSet):
    serializer_class=ProfileSerializer
    queryset=UserProfile.objects.all()
    #authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def get_queryset(self):
    #     return UserProfile.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        prof=self.get_object()
        if prof.user!=request.user:
            raise serializers.ValidationError("not allowed to perform")
        else:
            return super().destroy(request,*args,**kwargs)

class QuestionsView(ModelViewSet):
    serializer_class=QuestionSerializer
    queryset=Questions.objects.all()
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        qus=self.get_object()
        if qus.user!=request.user:
            raise serializers.ValidationError("not allowed to perform")
        else:
            return super().destroy(request,*args,**kwargs)


    
    @action(methods=["post"],detail=True)
    def add_answer(self,request,*args,**kwargs):
        serializer=AnswerSerializers(data=request.data)
        quest=self.get_object()
        user=request.user
        if serializer.is_valid():
            serializer.save(question=quest,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


from rest_framework import serializers
class AnswersView(ModelViewSet):
    serializer_class=AnswerSerializers
    queryset=Answers.objects.all()
    # authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def create(self,request,*args,**kwargs):
        raise serializers.ValidationError("method not allowed")
    
    @action(methods=["post"],detail=True)
    def add_upvote(self,request,*args,**kwargs):
        answer=self.get_object()
        answer.up_vote.add(request.user)
        answer.save()
        return Response(data="upvoted")
    
    @action(methods=["post"],detail=True)
    def down_vote(self,request,*args,**kwargs):
        answer=self.get_object()
        answer.up_vote.remove(request.user)
        answer.save()
        return Response(data="upvote removed")
    
    def destroy(self, request, *args, **kwargs):
        ans=self.get_object()
        if ans.user!=request.user:
            raise serializers.ValidationError("not allowed to perform")
        else:
            return super().destroy(request,*args,**kwargs)




