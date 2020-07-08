from views import *
#data = b"https://api.covid19api.com/total/country/italy/status/confirmed"
def read_redis(data):

    import redis 
    #redis = redis.Redis(host = 'redis',port = 6379, decode_responses=True)
    redis = redis.Redis()
    for d in redis.scan_iter():
        if data==d:return redis.get(data)
            
    return redis.get(data)
