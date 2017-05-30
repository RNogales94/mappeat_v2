from django.http import HttpResponseRedirect

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from registration_api import utils
from registration_api.serializers import UserSerializer


VALID_USER_FIELDS = utils.get_valid_user_fields()


@api_view(['POST'])
@permission_classes((AllowAny, ))
def register(request):
    """
    Example valid JSON:
    {"username": "john", "email": "john@example.com", "password": "verylongpassword"}
    """
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        user_data = utils.get_user_data(request.data)
        utils.create_inactive_user(**user_data)
        return Response(utils.USER_CREATED_RESPONSE_DATA,
                        status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((AllowAny, ))
def activate(request, activation_key=None):
    """
    Given an an activation key, look up and activate the user
    account corresponding to that key (if possible).

    """
    utils.activate_user(activation_key)
    # if not activated
    success_url = utils.get_settings('REGISTRATION_API_ACTIVATION_SUCCESS_URL')
    if success_url is not None:
        return Response(data={"message": "User activated"}, status=status.HTTP_200_OK)
