from views import *
import redis 
redis = redis.Redis()
#data = b"https://api.covid19api.com/total/country/italy/status/confirmed"
def read_redis(data):
    for d in redis.scan_iter():
        if data==d:
            v = redis.get(data)
            v = str(v)
    return v


if __name__ == "__main__":
    data = b"https://api.covid19api.com/total/country/poland/status/confirmed"
    (read_redis(data))
