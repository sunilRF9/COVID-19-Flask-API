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
    try:
        url = config.url.format(country)
        url_enc = url.encode()
        redis_data = read_redis(url_enc)
        redis_data = str(redis_data)
        cached_val = jsonify(redis_data)
        print('Serving From Redis')
        formatted_table = json2html.convert(json =redis_data)
        with open("templates/index.html","w") as f:
            f.write(formatted_table)
        return render_template('index.html')
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
        formatted_table = json2html.convert(json = latest_val)
        with open("templates/index.html","w") as f:
            f.write(formatted_table)
    return render_template('index.html')

#This route provides JSON data 
@app.route('/json/<country>/')
def get_json(country):
    print(f"served from {os.getpid()}")
    try:
        url = config.url.format(country)
        url_enc = url.encode()
        redis_data = read_redis(url_enc)
        print(redis_data.decode('utf-8'))
        cached_val = jsonify(redis_data)
        print('Serving From Redis')
        return cached_val
    except Exception as e:
        print(e)
        print('not found in cache')
        val = requests.get(url).text
        val = json.loads(val)
        cache[url] = val
        latest_val = val[-1]
        #CELERY TASK
        temp = json.dumps(latest_val)
        red.delay(url,temp)
        print('task loaded') 
    except:
        print('invalid country')
        print(config.url)
    return jsonify(latest_val)

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0',port=5000)
