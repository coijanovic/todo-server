from flask import Flask, Response, request, redirect, url_for
import os.path
import yaml
import fileinput

if os.path.exists('config.yaml'):
    configfile = 'config.yaml'
else:
    configfile = 'defaultconfig.yaml'

with open(configfile, 'r') as f:
    try:
        config = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(exc)

app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def index():
    msg = 'web version wip'
    return Response(msg, mimetype='text/plain')

@app.route('/tasks')
def get_tasks():
    todofile = open(config['todopath'], 'r')
    todos = [ line for line in todofile if '[ ]' in line ]
    todos.sort(reverse=True)
    return Response(todos, mimetype='text/plain')

@app.route('/add', methods = ['GET', 'POST'])
def add_task():
    todo = request.json
    
    todofile = open(config['todopath'], 'a')
    todofile.write("[{prio}] - {content} - [ ]\n".format(prio=todo['prio'], content=todo['content']))
    todofile.close()
    return Response('done', mimetype='text/plain')

if __name__ == '__main__':
    app.run(debug=False, host=config['hostip'], port=config['hostport'])
