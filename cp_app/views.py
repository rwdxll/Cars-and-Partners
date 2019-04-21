from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework import status
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.views import APIView

from cp_app.models import Partner
from cp_app.serializers import PartnerSerializer, UserSerializer
from django.contrib.auth.models import User

from functools import wraps
from time import time

# Create your views here.
def authorizeUser(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        user=request.user.id
        if request.user.is_authenticated:
            response = fn(request, *args)

        else:
            response = Response(
                "This action requires login!",
                status=status.HTTP_400_BAD_REQUEST)
        return response
    return wrapper

def root(request): 
    response = {}
    response['logged_in'] = False
    if request.user.is_authenticated():
        response['logged_in'] = True
        response['id'] = request.user.id
        response['username'] = request.user.username
    return JsonResponse(response)

@api_view(['POST'])
def user_add(request):
    """Create new user"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def partner_list(request):
    """List all partners"""
    partners = Partner.objects.all()
    serializer = PartnerSerializer(partners, many=True)
    return JsonResponse(serializer.data, safe=False)

class PartnerList(APIView):
    """List all partners"""
    def get(self, request):
        partners = Partner.objects.all()
        serializer = PartnerSerializer(partners, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['POST'])
@authorizeUser
def partner_add(request):
    """Create new partner"""
    serializer = PartnerSerializer(data=request.data)
    if serializer.is_valid():
        try:
            id = Partner.objects.latest('id').id +1
        except Partner.DoesNotExist:
            id = 1
        user = User.objects.get(id=request.user.id)
        serializer.save(id=id, user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def partner_detail(request, id):
    """Retrieve a particular partner"""
    try:
        partner = Partner.objects.get(id=id)
    except Partner.DoesNotExist:
        return HttpResponse("The requested item was not found", status=404)

    serializer = PartnerSerializer(partner)
    return JsonResponse(serializer.data)

@api_view(['DELETE'])
@authorizeUser
def partner_delete(request, id):
    """Delete partner"""
    try:
        partner = Partner.objects.get(id=id)
        if partner.deleted_at == 0:
            data = {"deleted_at": time()}
            serializer = PartnerSerializer(partner, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            "The requested item was already deleted",
            status=status.HTTP_404_NOT_FOUND
            )
    except Partner.DoesNotExist:
        return Response(
        "The requested item was not found",
        status=status.HTTP_404_NOT_FOUND
        )

    