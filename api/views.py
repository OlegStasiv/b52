from django.db import IntegrityError
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, permissions, authentication
from zoltan.models import User, Task, TaskCandidates
from api.serializers import UserSerializer, TaskDetailSerializer, TaskCreateSerializer, TaskCandidateSerializer, \
    CandidateSerializer, TaskDetailCandidateSerializer
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

APP_VERSION = '0.2'  # CHANGE APP VERSION HERE


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        if request.data['version'] != APP_VERSION:
            return Response({"actual": False})
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


obtain_auth_token = ObtainAuthToken.as_view()


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
        try:
            serializer.save(candidate=candidate)
            request.user.update_points()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'detail': 'Already exists this relation'}, status=status.HTTP_409_CONFLICT)


class CandidateProfile(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailCandidateSerializer
    authentication_classes = (MyAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        relation_id = self.kwargs['pk']
        return TaskCandidates.objects.filter(id=relation_id)

    def patch(self, request, *args, **kwargs):
        request.user.update_points()
        return self.partial_update(request, *args, **kwargs)


class TaskDetailCandidate(generics.ListCreateAPIView):
    serializer_class = TaskDetailCandidateSerializer
    authentication_classes = (MyAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        task = self.kwargs['pk']
        return TaskCandidates.objects.filter(task_id=task)


@api_view()
def check_version(request):
    """Method to check actual version of app from request.

    :parameter: version -- version from app
    """
    if request.GET.get('version') == APP_VERSION:
        return Response({"actual": True})
    else:
        return Response({"actual": False})
