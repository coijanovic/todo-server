from flask import Flask, Response, request, redirect, url_for, jsonify
import os.path
import json
import time
import fileinput

if os.path.exists('config.json'):
    configfile = 'config.json'
else:
    configfile = 'defaultconfig.json'

with open(configfile, 'r') as f:
    config = json.load(f)

app = Flask(__name__)
app.static_folder = 'static'

def get_todos():
    with open(config['todofile'], 'r') as f:
        todos = json.load(f)
    return todos

def write_todos(data):
    with open(config['todofile'], "w") as f:
        json.dump(data, f)

def format_todos(todos):
    ret = ""
    for i in todos:
        ret += "[{p}] - {c}\n".format(p=i['prio'],c=i['content'])
    return ret

@app.route('/')
def index():
    msg = 'web version wip'
    return Response(msg, mimetype='text/plain')

@app.route('/todos/open')
def get_open_todos():
    todos = get_todos()
    open_todos = [ t for t in todos if t['done'] == False ]
    open_todos.sort(key=lambda k: k['prio'], reverse=True)
    return format_todos(open_todos)

@app.route('/add', methods = ['GET', 'POST'])
def add_task():
    r = request.json
    todo = {
        "prio": r['prio'],
        "content": r['content'],
        "done": False,
        "time": {
            "created": int(time.time()),
            "edited": int(time.time())
        }
    }
    todos = get_todos()
    todos.append(todo)
    write_todos(todos)
    return Response('done\n', mimetype='text/plain')

@app.route('/done/<content>')
def mark_done(content):
    todos = get_todos()
    for t in todos:
        if t['content'] == content:
            t['done'] = True
            t['time']['edited'] = int(time.time())
    write_todos(todos)
    return Response('done\n', mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=False, host=config['hostip'], port=config['hostport'])
