from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.conf import settings
from myapp.models import *
from django.db.models.functions import Concat
# from .allfunctions import check_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.authtoken.models import Token
# from datetime import date,timedelta, time, datetime
# from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from .allfunctions import *

def make_password(password):
    assert password
    hash = hashlib.md5(password.encode()).hexdigest()
    return hash
    
def check_password(hash, password):
    """Generates the hash for a password and compares it."""
    generated_hash = make_password(password)
    return hash == generated_hash

# , usertype=None, loginType=0
class UserAuthentication(ModelBackend):
	# def authenticate(self, request, username=None, password=None, **kwargs):
	@staticmethod
	def user_authenticate(request=None, **credentials):
		# print(credentials)

		loginType = 0
		usertype = None
		username = ""
		u_pw = ""

		# if "username" in credentials:
		# 	username = credentials["username"]
		if "username" in credentials:
			username = credentials["username"]

		if "password" in credentials:
			u_pw = credentials["password"]

		try:
			user = Admins.objects.filter(username__exact = username, is_active=True).get(username__exact = username)
			# Users.objects.filter(email__exact = username, is_active=True).update(is_online=True)

			# success = check_password(user.password, u_pw)

			# success=user.check_password(u_pw)
			success=check_password(user.password,u_pw)
			if success:
				return user
		except user.DoesNotExist:
			pass

		return None

	# @staticmethod
	# def user_get_user(self, uid):
	# 	try:
	# 		return Users.objects.get(pk=uid)
	# 	except ObjectDoesNotExist:
	# 		return None


def logoutactivity(request, instance=None):

	Admins.objects.filter(id=instance.id).update(last_login=timezone.now())


# from django.utils.deprecation import MiddleWareMixin

# class Middlewares3bucketSetup(MiddleWareMixin):
# 	print("=======================enter")
# 	def __init__(self, get_response):
# 		settings.AMAZON_IMAGE_URL = 'https://megha-demo-testing.s3.us-east-2.amazonaws.com/'
# 		settings.AMAZON_ACCESS_KEY = 'AKIA4H42A4CD2MWLHR6L'
# 		settings.AMAZON_SECRET_KEY = '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'
# 		settings.AMAZON_BUCKET = 'megha-demo-testing'
# 		self.get_response = get_response


# 	def __call__(self, request):
# 		# print("callllllllllllllll",request)
# 		return self.get_response(request)