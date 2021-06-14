from datetime import datetime as dt
from rest_framework import serializers
from django.db.models import Q
# from django.contrib.auth.hashers import make_password, check_password

from .models import *
from common.allfunctions import *
from common.authsetup import *

class UsersSerializer(serializers.ModelSerializer):
	user_id = serializers.CharField(required=False, error_messages={'blank':"User Id can't be blank"}, help_text="Provide User Id")
	email = serializers.CharField(required=True, validators=[RegexValidator(
		regex=r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$',
		message=('Please provide a valid email'),
		)], error_messages={'blank':"Email can't be blank"})

	firstname = serializers.CharField(required=True, max_length=250, error_messages={'blank':"First name can't be blank"})
	lastname = serializers.CharField(required=True, max_length=250, error_messages={'blank':"Last name can't be blank"})
	role_id = serializers.IntegerField(required=True, validators=[RegexValidator(regex=r'^[0-9]*$',
					message=('Role id must be numerical'),)],
					help_text="Provide Role")
	company_id = serializers.CharField(required=True,error_messages={"blank": "Company ids can't be blank can't be blank"})
	address = serializers.CharField(required=False,error_messages={"blank": "Address can't be blank"})
	country_id = serializers.IntegerField(required=False, validators=[RegexValidator(regex=r'^[0-9]*$',
					message=('Company id must be numerical'),)],
					help_text="Provide Company id")
	state_id = serializers.IntegerField(required=False, validators=[RegexValidator(regex=r'^[0-9]*$',
					message=('State id must be numerical'),)],
					help_text="Provide State id")
	city_id = serializers.IntegerField(required=False, validators=[RegexValidator(regex=r'^[0-9]*$',
					message=('City id must be numerical'),)],
					help_text="Provide City id")
	zip = serializers.CharField(required=False,validators=[RegexValidator(
				regex=r'^[0-9]*$',
				message=('Pincode contains only numeric values'),
				) ], min_length=6, max_length=6, error_messages={'blank':"Pincode can't be blank"}
			)
	phone = serializers.CharField(required=False, validators=[RegexValidator(
				regex=r'^[0-9 ]*$',
				message=('Cellphone contains only space and numeric values'),
				) ], 
				min_length=8, max_length=11, 
				error_messages={'blank':"Phone can't be blank"}
			)
	last_login_ip = serializers.CharField(required=False,error_messages={"blank": "IP can't be blank"})

	status = serializers.ChoiceField(required=False, choices=(('1', 'Active'),  ('0', 'Inactive') ), error_messages={'blank':"Status can't be blank"})
	# role_perms = serializers.SerializerMethodField()

	class Meta:
		model = Admins
		fields = '__all__'

	# def get_child(self, Admins):
	# 	menu_id = Admins.id
	# 	return objchild

	@classmethod
	def validate(self, data):
		errors={}
		username = data.get('username')
		# users_data = Admins.objects.filter(Q(username__iexact = username), is_active=True, is_deleted=False, status='1').last()
		# if not users_data:
		# 	errors['username'] = "This account does not exist"

		company_id = data.get('company_id')
		if company_id:
			company_id = formatted_company_id_for_mysql(self, company_id)
			data["company_id"] = company_id

		user_id = data.get('user_id')
		if user_id:
			users_data = Admins.objects.filter(Q(email = data.get('email')), is_active=True, is_deleted=False).exclude(id=decode_str(data.get('user_id')))
			if users_data:
				errors['email'] = "This email already exists"

			get_password = Admins.objects.filter(Q(id = decode_str(user_id)), is_active=True, is_deleted=False)[0].password
			if data.get('password')==get_password:
				data['password']=data.get('password')
			else:
				data['password']=make_password(data.get('password'))

			if data.get('phone',None) is not None:
				pass
			else:
				data['phone']='1234567890'

			data['modified']=dt.now()

		if not user_id:
			users_data = Admins.objects.filter(Q(email = data.get('email')), is_active=True, is_deleted=False).last()
			if users_data:
				errors['email'] = "This email already exists"

			users_data = Admins.objects.filter(Q(username = username), is_active=True, is_deleted=False).last()
			if users_data:
				errors['username'] = "This account already exists"

			data["phone"]="1234567890"
			data["last_login"]=dt.now()
			data["created"]=dt.now()
			data["modified"]=dt.now()
			data["last_activity"]=dt.now()

		if errors:
			raise serializers.ValidationError(errors)
		return super(UsersSerializer, self).validate(self, data)

class UserLoginSerializers(serializers.ModelSerializer):
	username = serializers.CharField(required=True, max_length=250, error_messages={'blank':"Username can't be blank"})
	password = serializers.CharField(required=True, max_length=250, error_messages={'blank':"Password can't be blank"})

	class Meta:
	    model = Admins
	    fields = ('password','username')

	@classmethod
	def validate(self, data):
		errors={}
		username = data.get('username')
		findUser = Admins.objects.filter(username = username, is_active=True, is_deleted=False, status='1').last()

		if findUser is None:
			errors['username'] = "This account doesn't exist"
		# if findUser:
		# 	user = Admins.objects.filter(Q(username = username),is_active=1).values('id')[0]
		# 	user = Admins.objects.filter(id=user['id'])[0]

		# 	password = data.get('password')

		# 	# if not user.check_password(password):
		# 	if not check_password(user.password,password):
		# 		errors['password'] = "Invalid password"

		if errors:
			raise serializers.ValidationError(errors)
		return super(UserLoginSerializers, self).validate(self, data)

class UserIdentitySerializer(serializers.Serializer):
	user_id = serializers.CharField(required=True, error_messages={'blank':"User Identity can't be blank"}, help_text="Provide User Identity")

	# @classmethod
	# def validate(self, data):
	# 	errors = {}
	# 	user_validate = False
	# 	if data.get('user_id') is None or data.get('user_id') is "":
	# 		data['user_id'] = 0
	# 	else:
	# 		try:
	# 			data['user_id'] = int(decode_str(data.get('user_id')))
	# 			user_validate = True
	# 		except ValueError:
	# 			errors['user_id'] = "User Identity isn't valid."

	# 	if user_validate:
	# 		user_id=data.get('user_id')
	# 		checkuser = Admins.objects.filter(id=user_id, is_active=True).count()
	# 		if checkuser == 0:
	# 			errors['user_id'] = "User Identity isn't valid."

	# 	if errors:
	# 		raise serializers.ValidationError(errors)

	# 	return super(UserIdentitySerializer, self).validate(self, data)
