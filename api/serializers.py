from rest_framework import serializers, request

from zoltan.models import User, Task, Candidate, TaskCandidates


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')


class TaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}


class TaskDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}


# class TaskCandidateSerializer(serializers.ModelSerializer):
#     tasks = serializers.PrimaryKeyRelatedField(
#         many=True, read_only=True, queryset=Task.objects.all())
#     candidates = serializers.PrimaryKeyRelatedField(
#         many=True, queryset=Candidate.objects.all())
#
#     class Meta:
#         model = TaskCandidates
#         fields = '__all__'