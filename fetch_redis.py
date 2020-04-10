from views import *
import redis 
redis = redis.Redis()
'''def cache_red(url):
    print("[INFO]: READING FROM REDIS")
    return redis.get(url)
'''
#if __name__=="__main__":
data = b"https://api.covid19api.com/total/country/italy/status/confirmed"
for d in redis.scan_iter():
    if data==d:
        v = redis.get(data)
        print(str(v))
