from django.http import HttpResponseRedirect
from django.shortcuts import render


from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from registration_api import utils
from registration_api.serializers import UserSerializer

"""
Extension propia para asociar un Staff al nuevo usuario registrado
Este Staff será un Manager por defecto
"""
from mainRest.models import Staff, Restaurant, Owner



VALID_USER_FIELDS = utils.get_valid_user_fields()


@api_view(['POST'])
@permission_classes((AllowAny, ))
def register(request):
    """
    Example valid JSON:
    {"username": "john", "email": "john@example.com", "password": "pass", "restaurant": "My Pub"}
    """
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        #default code: create new_user
        user_data = utils.get_user_data(request.data)
        new_user = utils.create_inactive_user(**user_data)

        #Crear el restaurante del nuevo usuario:
        new_owner = Owner(user=new_user, name=new_user.username)
        new_owner.save()
        print("Owner " + new_owner.name + " created. [OK]")
        restaurant_name = request.data.pop('restaurant')
        new_restaurant = Restaurant(owner = new_owner, name=restaurant_name)
        new_restaurant.save()
        print("Restaurant " + new_restaurant.name + " created. [OK]")

        #Crear el staff
        staff_name = new_user.username
        new_staff = Staff(user=new_user, first_name=staff_name, restaurant=new_restaurant) #Manager por defecto
        new_staff.save()
        print("Staff " + new_staff.first_name + " created. [OK]")

        return Response(utils.USER_CREATED_RESPONSE_DATA,
                        status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_409_CONFLICT)


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
        return render(request, 'mainRest/activation.html', status=status.HTTP_200_OK)
