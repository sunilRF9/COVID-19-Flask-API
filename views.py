from flask import Flask,render_template,jsonify
import config
import os
from tasks import red
import json
from json2html import *
from fetch_redis import *
import requests
app = Flask(__name__)
cache={}
global url
@app.route('/html/<country>/')
def get(country):
    #print(f"served from {os.getpid()}")
    try:
        url = config.url.format(country)
        url_enc = url.encode()
        #print(url_enc)
        #cache_red(url)
        redis_data = read_redis(url_enc)
        #print(redis_data.decode('utf-8'))
        redis_data = str(redis_data)
        #print(type(redis_data))
        #print(redis_data)
        cached_val = jsonify(redis_data)
        #print(cached_val)
        #print(type(cached_val))
        print('Serving From Redis')
        #if url in cache_red(url):
            #print('FROM CACHE:\n')
        #cached_val = {"Cached":"True","Data":redis_data}#cache[url][-1]}
        #print(cached_val)
        formatted_table = json2html.convert(json =redis_data)
        with open("templates/index.html","w") as f:
            f.write(formatted_table)
        return render_template('index.html')
    #print(app.config)
    except Exception as e:
        print(e)
        print('not found in cache')
        val = requests.get(url).text
        val = json.loads(val)
        cache[url] = val
        latest_val = val[-1]
        #CELERY TASK
        temp = json.dumps(latest_val)
        #print('initiating cel task')
        red.delay(url,temp)
        print('task loaded') 
        #print(latest_val)
        formatted_table = json2html.convert(json = latest_val)
        with open("templates/index.html","w") as f:
            f.write(formatted_table)
    #finally:
    #    print('invalid country')
    #    print(config.url)
        #index= open("templates/index.html","w")
        #index.write(formatted_table)
        #index.close()
    return render_template('index.html')
    #return {"cached":"False","data":val[-1]}

#This route provides JSON data 
@app.route('/json/<country>/')
def get_json(country):
    print(f"served from {os.getpid()}")
    try:
        url = config.url.format(country)
        url_enc = url.encode()
        #print(url_enc)
        #cache_red(url)
        redis_data = read_redis(url_enc)
        print(redis_data.decode('utf-8'))
        #print(redis_data)
        cached_val = jsonify(redis_data)
        print('Serving From Redis')
        return cached_val
    #url = config.url.format(country)
    #if url in cache:
    #    #print('FROM CACHE:\n')
    #    cached_val = {"Cached":"True","Data":cache[url][-1]}
    #    print(cached_val)
    #print(app.config)
    except Exception as e:
        print(e)
        print('not found in cache')
        val = requests.get(url).text
        val = json.loads(val)
        cache[url] = val
        latest_val = val[-1]
        #CELERY TASK
        temp = json.dumps(latest_val)
        #print('initiating cel task')
        red.delay(url,temp)
        print('task loaded') 
        #print(latest_val)
    except:
        print('invalid country')
        print(config.url)
    return jsonify(latest_val)

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0',port=5000)
