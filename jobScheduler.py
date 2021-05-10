from apscheduler.schedulers.blocking import BlockingScheduler
import time
import requests
import zipfile
import io
import os
import redis
import csv

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=18, timezone="Asia/Kolkata")
def scheduled_job():

    REDIS_HOST = "redis-19587.c8.us-east-1-3.ec2.cloud.redislabs.com"
    REDIS_PORT = 19587
    REDIS_PWD = "08Xa5WeIMWNdm51WKgDW620TzfKvehJg"

    r = redis.StrictRedis(host = REDIS_HOST, port = REDIS_PORT, decode_responses=True, db=0, password = REDIS_PWD)

    timestr = time.strftime("EQ%d%m%y_CSV.ZIP")
    url = "https://www.bseindia.com/download/BhavCopy/Equity/"+timestr
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers)
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))
    zip_file.extractall(path = 'data/')
    filename = zip_file.namelist()[0]
    csv_list = csv.DictReader(open('data/'+filename, 'r'))

    redis_pipeline = r.pipeline(transaction=True)
    redis_pipeline.flushdb()
    for row in csv_list:
        stripped_key = "STOCK:"+row['SC_CODE'].rstrip()+":"+row['SC_NAME'].rstrip()
        value = {'name': row['SC_NAME'].rstrip(), 'code': row['SC_CODE'], 'open': float(row['OPEN']),
                 'close': float(row['CLOSE']), 'high': float(row['HIGH']), 'low': float(row['LOW'])}
        percentage = round(((value['close'] - value['open']) / value['open']) * 100, 2)
        value['percentage'] = round(percentage, 2)
        redis_pipeline.hmset(stripped_key, dict(value))
    redis_pipeline.execute()
    
sched.start()
