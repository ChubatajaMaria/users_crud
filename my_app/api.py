from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import UserSerializer, LoginSerializer
from .models import User


class BaseManageView(APIView):
    """
    The base class for ManageViews
        A ManageView is a view which is used to dispatch the requests to the appropriate views
        This is done so that we can use one URL with different methods (GET, PUT, etc)
    """
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'VIEWS_BY_METHOD'):
            raise Exception('VIEWS_BY_METHOD static dictionary variable must be defined on a ManageView class!')
        if request.method in self.VIEWS_BY_METHOD:
            return self.VIEWS_BY_METHOD[request.method]()(request, *args, **kwargs)

        return Response(status=405)


class UserCreateApi(generics.CreateAPIView):

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.request.method == 'POST':
            context['create_method'] = True
        return context

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserApi(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRUDApi(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserManageView(BaseManageView):
    VIEWS_BY_METHOD = {
        'POST': UserCreateApi.as_view,
        'GET': UserApi.as_view,
    }


class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
