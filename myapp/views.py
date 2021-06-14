from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import permissions
# from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, logout
import datetime
from datetime import datetime as dt

from .models import *
from .serializers import *
# from common.allfunctions import *
from common.authsetup import *
import hashlib
from common.background import postpone
from django.utils import timezone

# Create your views here.
class UserSignin(GenericAPIView):
	"""
	This Functionality is used for Users Registration
	"""
	serializer_class = UsersSerializer
	permission_classes = [
		permissions.AllowAny # Or anon users can't register
	]

	@classmethod
	def post(self, request):
		response={}
		postData = UsersSerializer(data=request.data)
		# postData.is_valid(raise_exception=True)
		if postData.is_valid():
			username = postData.data["username"]
			password = postData.data["password"]
			hash_password =make_password(password)

			fetch_ip = get_client_ip(request)
			if fetch_ip:
				last_login_ip = fetch_ip
			else:
				last_login_ip = ''
			company_id = postData.data["company_id"]
			# company_id = formatted_company_id_for_mysql(self, company_id)

			User = Admins.objects.create(username=username, password=hash_password, email=postData.data["email"],
										firstname=postData.data["firstname"],lastname=postData.data["lastname"],
										company_id=company_id,role_id=postData.data["role_id"],
										phone=postData.data["phone"] if postData.data["phone"] else '',
										last_login=postData.data["last_login"], last_login_ip=last_login_ip,
										created=postData.data["created"], modified=postData.data["modified"],
										status=postData.data["status"], last_activity=postData.data["last_activity"],
										is_active=1
										)
			User.save()
			token, _ = Token.objects.get_or_create(user=User)
			# elastic = save_data_to_elastic(User.id,'users','Admins')
			# saving_status = save_to_elastic(User.id)

			result = {}
			if User:
				result['id']=User.id
				result['raw_id']=encode_str(User.id)
				result['username'] = username
				result['email'] = postData.data["email"]
				# result['role'] = role
				# result['company'] = company
				response['token']=token.key

				response['data'] = result
				response['status'] = 1
			else:
				response["errors"] = get_json_errors(postData.errors)
				response["status"] = 0			

		else:
			response['errors'] = get_json_errors(postData.errors)
			response['status'] = 0
		return Response(response)

# User Login
class UserLogin(GenericAPIView):
	"""
	This Functionality is used for Users Login
	"""
	serializer_class = UserLoginSerializers
	permission_classes = [
		permissions.AllowAny # Or anon users can't register
	]

	@classmethod
	def post(self, request):
		response = {}
		user = {}
		comp_list = []

		postData = UserLoginSerializers(data=request.data)
		# postData.is_valid(raise_exception=True)
		if postData.is_valid():
			username = postData.data['username']
			password = postData.data['password']
			# print(username, password)

			userAuth = UserAuthentication.user_authenticate(username=username, password=password)

			if userAuth is not None:

				# get_id = Admins.objects.filter(username=username).values('id','last_login','email','firstname','lastname','company_id')
				last_login = userAuth.last_login
				userAuth.last_activity = last_login
				userAuth.save()
				# get_ins = Admins.objects.filter(username=username)
				# get_id = get_ins.values('id','last_login','email','firstname','lastname','company_id')
				# get_ins.update(last_activity=get_id[0]['last_login'])
				# update_time = Admins.objects.filter(username=username).update(last_activity=get_id[0]['last_login'])
				ids = userAuth.id #get_id[0]['id']
				user_id = encode_str(ids)

				# AdminLoginLogs.objects.create(admin_id=get_id[0]['id'],start_date_time=dt.now())
				UserLogin.adminlog(ids)
				user['id'] = ids
				user['user_id'] = user_id
				user['username'] = username
				user['email']=userAuth.email
				user['firstname']=userAuth.firstname
				user['lastname']=userAuth.lastname

				# company_id = get_id[0]['company_id']
				# company_ids = decode_multi_value_for_mysql(self, company_id)
				# for comp in company_ids:
				# 	company = {}
				# 	dets = Companies.objects.filter(id=comp).first()
				# 	if dets:
				# 		company['id']=dets.id
				# 		company['name']=dets.name
				# 		comp_list.append(company)

				response['result'] = user
				response['token']= get_authentication_token(userAuth.id)
				response['company_data'] = comp_list
				response['status'] = 1
			else:
				response['errors'] = {"_error":'Wrong username or password'}
				response['status'] = 0
		else:
			response['errors'] = get_json_errors(postData.errors)
			response['status'] = 0
		return Response(response)

	@classmethod
	@postpone
	def adminlog(self,get_id):
		AdminLoginLogs.objects.create(admin_id=get_id,start_date_time=dt.now())
		return True
class Signout(GenericAPIView):
	"""
	This Functionality is used for user signout
	"""
	# authentication_classes = ()
	# permission_classes = ()

	serializer_class = UserIdentitySerializer

	@classmethod
	def post(self, request):
		response = {}
		post_data = UserIdentitySerializer(data=request.data)
		# post_data.is_valid(raise_exception=True)
		if post_data.is_valid():
			Signout.signoutfunc(request,post_data.data)

			if request.user.is_authenticated:
				logout(request)
				response['message'] = "You have successfully logged out."
			else:
				response['message'] = "You have successfully logged out."

			response['status'] = 1
		else:
			response['errors'] = get_json_errors(post_data.errors)
			response['status'] = 0
		return Response(response)

	@classmethod
	@postpone
	def signoutfunc(self,request,data):
		user = Admins.objects.filter(id=data.get('user_id')).last()
		fetch_ip = get_client_ip(request)
		if fetch_ip:
			last_login_ip = fetch_ip
		else:
			last_login_ip = ''
		user.last_login=timezone.now()
		user.last_login_ip=last_login_ip
		user.save()
		# update_ip = Admins.objects.filter(username=user).update(last_login_ip=last_login_ip)
		rec = AdminLoginLogs.objects.filter(admin_id=data.get('user_id')).last()
		if rec:
			# AdminLoginLogs.objects.filter(id=rec.id).update(end_date_time=dt.now())
			rec.end_date_time=dt.now()
			rec.save()
		return True
