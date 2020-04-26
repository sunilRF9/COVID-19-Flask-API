from __future__ import absolute_import
import json
from celery_app import app
import os
import redis
#DOCKER COMPOSE VERSION#
#redis = redis.Redis(host = 'redis',port = 6379, decode_responses=True)
redis = redis.Redis()

@app.task
def red(url,val):
    val = json.loads(val)
    #df = pd.DataFrame(val,index=[0])
    #print(df) 
    redis.setex(url,3600,str(val))
    #res = redis.get(url)
    return 'Wrote to cache'
