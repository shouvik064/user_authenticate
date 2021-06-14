import requests, os, sys
import json
import uuid
import hashlib
import base64
from common.models import *
from rest_framework.authtoken.models import Token
import math
from django.db.models import Avg, Q
from decimal import *
from django.conf import settings
from datetime import date, datetime, timedelta
import pytz
from rest_framework import serializers
from os import urandom
from common.authsetup import *

from django.db import connection, reset_queries
import time
import functools
from common.background import postpone
from django.core import mail
from django.core.mail import EmailMessage
import pytz
import random
import time


def query_debugger(func):
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        reset_queries()
        start_queries = len(connection.queries)
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        end_queries = len(connection.queries)
        # print(f"Function : {func.__name__}")
        # print(f"Number of Queries : {end_queries - start_queries}")
        # print(f"Finished in : {(end - start):.2f}s")
        print("Function :" + func.__name__)
        print("Number of Queries: "+str(end_queries - start_queries))
        print((end - start))
        return result
    return inner_func

def replace_all(text, dic):
	for i, j in dic.items():
		text = text.replace(i, j)
	return text
	
def check_password(hashed_password, user_password):
	# pro_pass = hash_md5(user_password)
	# return hashed_password == pro_pass
	try:
		password, salt = hashed_password.split(':')
		print(password,'password')
		return password == hashlib.sha256(
				salt.encode() + user_password.encode()
			).hexdigest()
	except Exception as e:
		print(e)
		return False

def get_authentication_token(userid):
	user = Admins.objects.get(pk=userid)
	token, created = Token.objects.get_or_create(user=user)
	if created:
		token_key = created.key
	else:
		token_key = token.key
	return token_key

def get_json_errors(error_list_data):
	__field_errors = {}

	field_errors = [(k, v[0]) for k, v in error_list_data.items()]

	for key, error_list in field_errors:
		__field_errors[key] = error_list

	return __field_errors;

def collect_allErrors(errors1=None, errors2=None):
	errors1 = get_json_errors(errors1)
	errors2 = get_json_errors(errors2)

	errors = merge(errors1, errors2)

	return errors

def encode_str(text):
	string = str(text)
	encode = base64.b64encode(string.encode('ascii'))
	return str(encode.decode('ascii'))


def decode_str(encrypt_text):
	# string = str(encrypt_text)
	decode = base64.b64decode(encrypt_text).decode('ascii')
	return decode

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip

def decode_multi_value(self, value):
	if value:
		value = value.split(",")
		try:
			value = [int(x) for x in value]
		except ValueError:
			value = []
	else:
		value = []
	return value

def decode_multi_value_for_mysql(self, value):
	if value:
		value = value.replace("::",',').replace(':','')
		value = value.split(',')
		try:
			value = [int(x) for x in value]
		except ValueError:
			value = []
	else:
		value = []
	return value

def formatted_company_id_for_mysql(self, value):
	if value:
		value = ':' + value.replace(",",'::')+ ':'
	else:
		value = ':'
	return value

def decode_multi_value_array(self, value):
	value_list = []
	if value:
		if ',' in value:
			result = [x.strip() for x in value.split(',')]
			for i in result:
				rec_id = decode_str(i)
				value_list.append(rec_id)
		else:
			rec_id = decode_str(value)
			value_list.append(rec_id)			
	return value_list

def decode_multi_value_stringarray(self, value):
	value_list = []
	if value:
		if ',' in value:
			result = [x.strip() for x in value.split(',')]
			for i in result:
				value_list.append(i)
		else:
			rec_id = value
			value_list.append(rec_id)
	return value_list

def decode_multi_value_stringarray_for_invoice(self, value):
	value_list = []
	if value:
		if ',' in value:
			result = [x.strip() for x in value.split(',')]
			for i in result:
				value_list.append(decode_str(i))
		else:
			rec_id = decode_str(value)
			value_list.append(rec_id)
	return value_list

def convert_datetime_to_timestampformat(field):
	get_timezone = 'UTC'
	tz = pytz.timezone(get_timezone)
	if field:
		new_date=parser.parse(field)
		new_date=tz.localize(new_date)
		print("final",new_date)
		sa
	else:
		new_date="1900-04-07 06:02:27.748631+00"
	return new_date

def convert_datetime_format(field):
	try:
		date = field[:10]
		suffix =''
		d = datetime.strptime(date, '%Y-%m-%d')
		new_date = datetime.date.strftime(d, "%d %b, %Y")
		date_split = new_date.split(" ")
		suffix = get_suffix(int(date_split[0]))
		date1 = date_split[0]+suffix
		date_split[0] = date1
		new_date = ' '.join(date_split)
	except:
		new_date=''
		print('date error')	
	return new_date

def convert_date_format(field):

	d = datetime.strptime(field, '%Y-%m-%d')
	new_date = datetime.date.strftime(d, "%d %b, %Y")
	date_split = new_date.split(" ")
	suffix = get_suffix(int(date_split[0]))
	date1 = date_split[0]+suffix
	date_split[0] = date1
	new_date = ' '.join(date_split)
	return new_date	

def get_suffix(d):
	return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')


def fetch_column_names(self, table_name):
	cols = []
	for field in table_name._meta.fields:
		# field.get_attname_column()
		cols.append(field.name)

	return cols

def number_genarator():

	secure_random = random.SystemRandom()
	number_list  = [x for x in range(100, 500000)]
	result = secure_random.choice(number_list)

	return result

def number_genarator_large():

	secure_random = random.SystemRandom()
	number_list  = [x for x in range(10000000, 99999999)]
	result = secure_random.choice(number_list)

	return result	

from threading import Thread

def postpone(function):
	def decorator(*args, **kwargs):
		t = Thread(target = function, args=args, kwargs=kwargs)
		t.daemon = True
		t.start()
	return decorator