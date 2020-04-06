from flask import Flask,render_template,jsonify
import config
import os
from tasks import red
import json
from json2html import *
import requests
app = Flask(__name__)
cache={}
@app.route('/html/<country>/')
def get(country):
    #print(f"served from {os.getpid()}")
    url = config.url.format(country)
    if url in cache:
        #print('FROM CACHE:\n')
        cached_val = {"Cached":"True","Data":cache[url][-1]}
        print(cached_val)
        formatted_table = json2html.convert(json = cached_val)
        with open("templates/index.html","w") as f:
            f.write(formatted_table)
        return render_template('index.html')
    #print(app.config)
    try:
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
    except:
        print('invalid country')
        print(config.url)
        #index= open("templates/index.html","w")
        #index.write(formatted_table)
        #index.close()
    return render_template('index.html')
    #return {"cached":"False","data":val[-1]}

#This route provides JSON data 
@app.route('/json/<country>/')
def get_json(country):
    print(f"served from {os.getpid()}")
    url = config.url.format(country)
    if url in cache:
        #print('FROM CACHE:\n')
        cached_val = {"Cached":"True","Data":cache[url][-1]}
        print(cached_val)
    #print(app.config)
    try:
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
    app.run(debug=True,host='localhost',port='1111') 
