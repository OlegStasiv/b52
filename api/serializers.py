from rest_framework import serializers
from zoltan.models import User, Task, Candidate, TaskCandidates, Notification


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'points')


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
    awards = serializers.JSONField(allow_null=True, required=False)
    educations = serializers.JSONField(allow_null=True, required=False)
    courses = serializers.JSONField(allow_null=True, required=False)
    languages = serializers.JSONField(allow_null=True, required=False)
    projects = serializers.JSONField(allow_null=True, required=False)
    skills = serializers.ListField(child=serializers.CharField(allow_null=True), allow_null=True, required=False)
    linkedin_url = serializers.URLField(allow_null=True, required=False)

    class Meta:
        model = Candidate
        fields = '__all__'

    def create(self, validated_data):
        if validated_data.get('linkedin_url', None):
            candidate, created = Candidate.objects.update_or_create(linkedin_url=validated_data['linkedin_url'], defaults=validated_data)
        else:
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


class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = '__all__'
