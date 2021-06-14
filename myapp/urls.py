from django.urls import path
from django.conf.urls import include

from . import views

urlpatterns = [

	path('signup/', views.UserSignin.as_view(), name='signup'),
	path('login/', views.UserLogin.as_view(), name='login'),
	path('logout/', views.Signout.as_view(), name='logout'),

	# path(
	# 	'admin/',
	# 	include('users.admin_management.urls')
	# ),

	# path(
	# 	'menu/',
	# 	include('users.menu_management.urls')
	# ),

	# path(
	# 	'role/',
	# 	include('users.role_management.urls')
	# ),

	# path(
	# 	'company/',
	# 	include('users.company_management.urls')
	# ),

	# path(
	# 	'site/',
	# 	include('users.site_management.urls')
	# ),

	# path(
	# 	'global_settings/',
	# 	include('users.global_management.urls')
	# ),

]