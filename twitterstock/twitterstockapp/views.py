from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
import json
from django.http import JsonResponse
from email.header import decode_header
import os
# Create your views here.

@api_view(['GET'])
def get_myasset(request):
    return JsonResponse({
        'success': 1,
        'result': 1,
    })