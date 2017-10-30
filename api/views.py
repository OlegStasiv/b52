from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, generics, permissions, authentication
from zoltan.models import User, Task
from api.serializers import UserSerializer, TaskDetailSerializer, \
    TaskCreateSerializer


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
    queryset = Task.objects.filter()
    serializer_class = TaskCreateSerializer
    authentication_classes = (MyAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Task.objects.filter(user_id=user)

    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class TaskDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskDetailSerializer
    authentication_classes = (MyAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(user_id=user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


# class TaskCandidateViewSet(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Task.objects.filter()
#     serializer_class = TaskCandidateSerializer
#     authentication_classes = (MyAuthentication,)
#     permission_classes = (IsAuthenticated,)
#
#     def get_queryset(self):
#         user = self.request.user
#         return TaskCandidates.objects.filter(user_id=user)
#
#     def put(self, request, *args, **kwargs):
#         pass



