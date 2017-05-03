from flask import Flask
from flask import render_template
from flask import send_from_directory
from invoke_ansible import run_playbook 
import json
import ansible
import os
app = Flask(__name__,static_url_path='/static')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('./static/js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('./static/css', path)


@app.route('/')
def index():
    return 'Index Page'

@app.route('/run')
def run():
    result = run_playbook(playbook_path="/home/ubuntu/workspace/flasksampleapp/playbooks/test.yml", console=False)
    return json.dumps(result[0].__dict__['_result'])

@app.route('/runasync')
def runasync():
    result = run_playbook(playbook_path="/home/ubuntu/workspace/flasksampleapp/playbooks/async.yml", console=False)
    return json.dumps({"job_id": result[0].__dict__['_result']['ansible_job_id']})

@app.route('/status')
def status():
    evars = { "job_id": "362518481715.4888"}
    result = open("/home/ubuntu/.ansible_async/"+evars["job_id"], "r").read()
    return result

@app.route('/listjobs')
def listjobs():
    evars = { "job_id": "362518481715.4888"}
    dirname = "/home/ubuntu/.ansible_async/"
    return json.dumps(os.listdir(dirname))

@app.route('/listvms')
def listvms():
    evars = [
            { "id":1, "ip":"10.0.0.1", "username": "ubuntu", "keyname": "testkey.pem"},
            { "id":2, "ip":"10.0.0.2", "username": "fedora", "keyname": "testkey.pem"},
            { "id":3, "ip":"10.0.0.3", "username": "centos", "keyname": "testkey.pem"},
            ]
    return json.dumps(evars)

@app.route('/listsshkeys')
def listsshkeys():
    evars = [
            { "id":1, "name":"testkey1.pem"},
            { "id":2, "name":"testkey2.pem"},
            { "id":1, "name":"testkey3.pem"},
            ]
    return json.dumps(evars)

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=8080)
