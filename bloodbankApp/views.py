from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect
# from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from bloodbankApp.models import *
# from events.models import/ EventNew
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect,Http404,HttpResponse, JsonResponse
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import difflib
import json
from django.http import JsonResponse
import requests
import datetime
from itertools import chain
from pyfcm import FCMNotification
from django.utils import timezone

# Create your views here.
@csrf_exempt
def register(request):
	if request.method == "POST":
		try:
			json_data = json.loads(request.body.decode("utf-8"))
			#print(json_data)
			emp_id = json_data['emp_id']
			email_id = json_data['email_id']
			full_name = json_data['name']
			phone = json_data['phone']
			gender = json_data['gender']
			blood_group = json_data['blood_group']
			address = json_data['address']
			city = json_data['city']
			fit_for_donation = json_data['fit_for_donation']
			password = json_data['password']
			device_token = json_data['token']
			u = User.objects.get(emp_id=int(emp_id))
			return JsonResponse({'status':'false','message':"User already exists"})
		except:
			user = User()
			user.emp_id=int(emp_id)
			user.email_id=email_id
			user.full_name=full_name
			user.phone=phone
			user.gender=gender
			user.blood_group=blood_group
			user.password=password
			user.address=address
			user.city=city
			user.fit_for_donation=fit_for_donation
			user.device_token = device_token
			try:
				user.save()
			except:
				return JsonResponse({'status':'false','message':"Bad request"})
			return JsonResponse({'status':'true','message':"Registration Successful"})
	else:
		return JsonResponse({'status':'false','message':"This is a post api"})

@csrf_exempt
def login(request):
	if request.method == "POST":
		try:
			json_data = json.loads(request.body.decode("utf-8"))
			email_id = json_data['email_id']
			password = json_data['password']
			user = User.objects.get(email_id=email_id, password=password)
			if user:
				return JsonResponse({'status':'true','message':"Login Successful"})
			else:
				return JsonResponse({'status':'false','message':"Login Failed"})
		except:
			return JsonResponse({'status':'false','message':"Login Failed"})
	else:
		return JsonResponse({'status':'false','message':"This is a post api"})

@csrf_exempt
def updateUser(request):
	if request.method == "POST":
		try:
			json_data = json.loads(request.body.decode("utf-8"))
			email_id = json_data['email_id']
			full_name = json_data['name']
			phone = json_data['phone']
			gender = json_data['gender']
			blood_group = json_data['blood_group']
			address = json_data['address']
			city = json_data['city']
			fit_for_donation = json_data['fit_for_donation']
			password = json_data['password']

			user = User.objects.get(email_id=email_id)
			user.full_name=full_name
			user.phone=phone
			user.gender=gender
			user.blood_group=blood_group
			user.password=password
			user.address=address
			user.city=city
			user.fit_for_donation=fit_for_donation
			try:
				user.save()
			except:
				return JsonResponse({'status':'false','message':"Bad request"})
			return JsonResponse({'status':'true','message':"Update Successful"})
		except:
			return JsonResponse({'status':'false','message':"Bad request"})
	else:
		return JsonResponse({'status':'false','message':"This is a post api"})

@csrf_exempt
def getUser(request):
	if request.method == 'GET':
		email_id = request.GET['email_id']
		user = User.objects.get(email_id=email_id)
		user.password = "xxxxx"
		data = serializers.serialize('json', [user,])
		struct = json.loads(data)
		return JsonResponse(struct[0], safe=False)
	else:
		return JsonResponse({'status':'false','message':"This is a get api"})

@csrf_exempt
def queryUsers(request):
	if request.method == 'GET':
		blood_group = request.GET['blood_group']
		city = request.GET['city']
		users = User.objects.filter(blood_group=blood_group,city=city)
		struct = []
		for user in users:
			user.password = "xxxxx"
			struct.append(json.loads(serializers.serialize('json', [user,]))[0]['fields'])
		
		return JsonResponse(struct, safe=False)
	else:
		return JsonResponse({'status':'false','message':"This is a get api"})


@csrf_exempt
def createRequest(request):
	if request.method == 'POST':
		try:
			json_data = json.loads(request.body.decode("utf-8"))
			print(json_data)
			email_id = json_data['email_id']
			blood_group = json_data['blood_group']
			quantity = json_data['quantity']
			location = json_data['location']
			city = json_data['city']
			deadline = json_data['deadline']
			story = json_data['story']
			provideCab = json_data['provideCab']
			#status is by default active
			blood_request = BloodRequest()
			blood_request.email_id = email_id
			blood_request.blood_group = blood_group
			blood_request.quantity = quantity
			blood_request.location = location
			blood_request.city = city
			blood_request.deadline = deadline#datetime.datetime.strptime(str(deadline), "%Y-%m-%d").date()
			blood_request.story = story
			blood_request.provideCab = provideCab
			blood_request.creationDate = timezone.now()
			blood_request.save()
			send_notifications(blood_request)
			return JsonResponse({"status": 'true', "request_id" : str(blood_request.id)})
		except:
			return JsonResponse({'status':'false','message':"Bad request"})
	else:
		return JsonResponse({'status':'false','message':"This is a post api"})

@csrf_exempt
def updateRequest(request):
	if request.method == 'POST':
		try:
			json_data = json.loads(request.body.decode("utf-8"))
			print(json_data)
			request_id = json_data['request_id']
			quantity = json_data['quantity']
			location = json_data['location']
			city = json_data['city']
			deadline = json_data['deadline']
			story = json_data['story']
			provideCab = json_data['provideCab']
			#status is by default active
			blood_request = BloodRequest.objects.get(id=int(request_id))
			print("blood_request")
			print(blood_request)
			blood_request.quantity = quantity
			blood_request.location = location
			blood_request.city = city
			blood_request.deadline = deadline#datetime.datetime.strptime(str(deadline), "%Y-%m-%d").date()
			blood_request.story = story
			blood_request.provideCab = provideCab
			blood_request.save()
			return JsonResponse({"status": 'true', "request_id" : str(blood_request.id)})
		except:
			return JsonResponse({'status':'false','message':"Bad request"})
	else:
		return JsonResponse({'status':'false','message':"This is a post api"})

@csrf_exempt
def deleteRequest(request):
	if request.method == 'POST':
		try:
			json_data = json.loads(request.body.decode("utf-8"))
			request_id = json_data['request_id']
			
			blood_request = BloodRequest.objects.get(id=int(request_id))
			
			blood_request.delete()
			return JsonResponse({"status": 'true', "message" : "Delete Successful"})
		except:
			return JsonResponse({'status':'false','message':"Bad request"})
	else:
		return JsonResponse({'status':'false','message':"This is a post api"})

@csrf_exempt
def getRequestById(request):
	if request.method == 'GET':
		request_id = request.GET['request_id']
		blood_request = BloodRequest.objects.get(id=request_id)
		data = serializers.serialize('json', [blood_request,])
		struct = json.loads(data)
		return JsonResponse(struct[0]['fields'], safe=False)
	else:
		return JsonResponse({'status':'false','message':"This is a get api"})

@csrf_exempt
def getRequestByUser(request):
	if request.method == 'GET':
		email_id = request.GET['email_id']
		blood_requests = BloodRequest.objects.filter(email_id=email_id)
		struct = []
		i = 0
		for blood_request in blood_requests:
			struct.append(json.loads(serializers.serialize('json', [blood_request,]))[0]['fields'])
			struct[i]['id'] = blood_request.id
			i = i+1
		
		return JsonResponse(struct, safe=False)
	else:
		return JsonResponse({'status':'false','message':"This is a get api"})

@csrf_exempt
def queryRequestForDonor(request):
	if request.method == 'GET':
		email_id = request.GET['email_id']

		user = None
		try:
			user = User.objects.get(email_id=email_id)
		except:
			return JsonResponse([], safe=False)

		blood_requests = BloodRequest.objects.filter(blood_group=user.blood_group,city=user.city)
		struct = []
		i=0
		for blood_request in blood_requests:
			response = Response.objects.filter(email_id=email_id,request_id=blood_request.id)
			requester = None
			if response.count() == 0:
				response = Response()
				requester = User()
			else:
				response = response[0]
				requester = User.objects.get(email_id=response.email_id)

			#combined = list(chain(blood_request,response))
			struct.append(json.loads(serializers.serialize('json', [blood_request,]))[0]['fields'])
			struct[i]['id'] = blood_request.id
			struct[i]['user_response'] = response.user_response
			struct[i]['name'] = requester.full_name
			struct[i]['phone'] = requester.phone

			i = i+1
		
		return JsonResponse(struct, safe=False)
	else:
		return JsonResponse({'status':'false','message':"This is a get api"})

@csrf_exempt
def createResponse(request):
	if request.method == 'POST':
		try:
			json_data = json.loads(request.body.decode("utf-8"))
			print(json_data)
			request_id = json_data['request_id']
			email_id = json_data['email_id']
			user_response = json_data['user_response']
			time = json_data['time']
			cab_needed = json_data['cab_needed']

			user = User.objects.filter(email_id=email_id)
			blood_request = BloodRequest.objects.filter(id=request_id)
			if user.count() == 0 or blood_request.count() == 0:
				return JsonResponse({'status':'false','message':"User or request does not exist"})

			res = Response()
			res.email_id = email_id
			res.request_id = request_id
			res.user_response = user_response
			res.cab_needed = cab_needed
			res.time = time#datetime.datetime.strptime(str(time), "%Y-%m-%d").date()
			res.save()
			return JsonResponse({"status": 'true', "message" : "Response Registered"})
		except:
			return JsonResponse({'status':'false','message':"Bad request"})
	else:
		return JsonResponse({'status':'false','message':"This is a post api"})

@csrf_exempt
def getResponse(request):
	if request.method == 'GET':
		request_id = request.GET['request_id']
		email_id = request.GET['email_id']
		responses = Response.objects.filter(request_id=request_id,email_id=email_id)

		user = User.objects.filter(email_id=email_id)
		blood_request = BloodRequest.objects.filter(id=request_id)
		if user.count() == 0 or blood_request.count() == 0:
			return JsonResponse({'status':'false','message':"User or request does not exist"})

		response = None
		if responses.count() == 0:
			response = Response()
		else:
			response = responses[0]

		data = serializers.serialize('json', [response,])
		struct = json.loads(data)
		return JsonResponse(struct[0], safe=False)
	else:
		return JsonResponse({'status':'false','message':"This is a get api"})

@csrf_exempt
def getResponsesByRequest(request):
	if request.method == 'GET':
		request_id = request.GET['request_id']
		responses = Response.objects.filter(request_id=request_id,user_response=True)

		blood_request = BloodRequest.objects.filter(id=request_id)
		if blood_request.count() == 0:
			return JsonResponse({'status':'false','message':"Request does not exist"})

		struct = []
		for response in responses:
			user = User.objects.get(email_id=response.email_id)
			struct.append({"email_id": response.email_id, "name": user.full_name, "phone": user.phone, "cab_needed": response.cab_needed})

		return JsonResponse(struct, safe=False)
	else:
		return JsonResponse({'status':'false','message':"This is a get api"})

def send_notifications(blood_request): 
	path_to_fcm = "https://fcm.googleapis.com"
	server_key = 'AAAA8ktmpX8:APA91bGN_-VRDbHOuvZkVNsZ0RnpKrHO8BTxl8bHNvadtGnfA52PAhxm6C0TIQwpMQjljFdFPYKRv09kRc9dzmo9QXdyt3d7LHN0PEq_tVNZBH9s7zqLj01Va2Tja3tUNkRdQcSiLl9I4aaGA7h8gzEIHtdn9iY7vQ'
	reg_ids = []
	users = User.objects.filter(blood_group=blood_request.blood_group,city=blood_request.city)
	for user in users:
		reg_ids.append(user.device_token)

	message_title = "New Blood request"
	message_body = "Someone is dying"
	result = FCMNotification(api_key=server_key).notify_multiple_devices(registration_ids=reg_ids, message_title=message_title, message_body=message_body)
	return
			