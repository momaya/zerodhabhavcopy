from django.shortcuts import render
from django.http import JsonResponse
import redis
import json

REDIS_HOST = "redis-19587.c8.us-east-1-3.ec2.cloud.redislabs.com"
REDIS_PORT = 19587
REDIS_PWD = "08Xa5WeIMWNdm51WKgDW620TzfKvehJg"

# Create your views here.
def index(request):

    return render(request, 'search.html')
    
def api(request):

    if request.method == "POST":

        data = json.loads(request.body)
        stock = data['stock']
        if stock:
        
            r = redis.StrictRedis(host = REDIS_HOST, port = REDIS_PORT, decode_responses=True, db=0, password = REDIS_PWD)
            stacks = []
            for key in r.keys('STOCK:*'+str(stock).upper()+'*'):
                reg = r.hgetall(key)
                stacks.append(reg)
            
            context = { "redis" : stacks}

            return JsonResponse(context)

        else:
            response = "Stock Search is empty"
            return JsonResponse({"err":response}, status=400)
            