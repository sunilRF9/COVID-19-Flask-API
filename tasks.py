from __future__ import absolute_import
import json
import cv2
from celery_app import app
import os
import redis
import pandas as pd
redis = redis.Redis()

@app.task
def red(url,val):
    val = json.loads(val)
    df = pd.DataFrame(val,index=[0])
    #print(df) 
    redis.setex(url,3600,str(df))
    res = redis.get(url)
    return (str(res))
