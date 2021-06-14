from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .serializers import *
from .allfunctions import *

# from rest_framework.permissions import AllowAny
# from rest_framework import permissions

# Create your views here.
