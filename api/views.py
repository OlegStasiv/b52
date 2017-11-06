from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, generics, permissions, authentication
from zoltan.models import User, Task, TaskCandidates, Candidate
from api.serializers import UserSerializer, TaskDetailSerializer, TaskCreateSerializer, TaskCandidateSerializer, \
    CandidateSerializer, TaskDetailCandidateSerializer


class MyAuthentication(authentication.TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            return None, ''
        return token.user, token


class UserViewSet(generics.CreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (MyAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method == 'POST':
            return permissions.AllowAny(),
        return permissions.IsAuthenticated(),

    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class TaskViewSet(generics.ListCreateAPIView):
    """This view should return a list of all the purchases for the currently authenticated user."""
    queryset = Task.objects.filter()
    serializer_class = TaskCreateSerializer
    authentication_classes = (MyAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user_id=user)

    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailSerializer
    authentication_classes = (MyAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user_id=user)


class TaskCandidateViewSet(generics.ListCreateAPIView):
    queryset = TaskCandidates.objects.all()
    serializer_class = TaskCandidateSerializer
    authentication_classes = (MyAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        candidate = CandidateSerializer(data=request.data['candidate'])
        candidate.is_valid(raise_exception=True)
        candidate = candidate.save()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(candidate=candidate)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CandidateProfile(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailCandidateSerializer
    authentication_classes = (MyAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        relation_id = self.kwargs['pk']
        return TaskCandidates.objects.filter(id=relation_id)


class TaskDetailCandidate(generics.ListCreateAPIView):
    serializer_class = TaskDetailCandidateSerializer
    authentication_classes = (MyAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        task = self.kwargs['pk']
        return TaskCandidates.objects.filter(task_id=task)


