from rest_framework import serializers

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


class CandidateSerializer(serializers.ModelSerializer):
    awards = serializers.JSONField(allow_null=True)
    educations = serializers.JSONField(allow_null=True)
    courses = serializers.JSONField(allow_null=True)
    languages = serializers.JSONField(allow_null=True)
    projects = serializers.JSONField(allow_null=True)
    skills = serializers.ListField(child=serializers.CharField(allow_null=True), allow_null=True)

    class Meta:
        model = Candidate
        fields = '__all__'

    def create(self, validated_data):
        candidate = Candidate.objects.create(**validated_data)
        return candidate


class TaskCandidateSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    candidate = CandidateSerializer(read_only=True)

    class Meta:
        model = TaskCandidates
        exclude = ('candidate',)


class TaskDetailCandidateSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    candidate = CandidateSerializer(read_only=True)

    class Meta:
        model = TaskCandidates
        fields = '__all__'
        extra_kwargs = {'pk': {'read_only': True}}
