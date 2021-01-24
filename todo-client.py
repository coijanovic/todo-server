import requests
import json
import os.path
import sys

if os.path.exists('config.json'):
    configfile = 'config.json'
else:
    configfile = 'defaultconfig.json'

with open(configfile, 'r') as f:
    config = json.load(f)

server_url = "http://{i}:{j}".format(
        i = config['hostip'],
        j = config['hostport']
        )

def todo_str(todo):
    ret = "[{p}] - {c}".format(p=todo['prio'],c=todo['content'])
    return ret

def show_todos():
    url = server_url + "/todos/open"
    todos = requests.get(url).text
    for t in json.loads(todos):
        print(todo_str(t))

def add_todo():
    url = server_url + "/add"
    content = input("What needs to be done? ")
    prio = input("How urgent is it? [0-5] ")
    todo = {'prio': int(prio), 'content': content}
    r = requests.post(url, json = todo)
    print(r)

def do_todo():
    url = server_url + "/todos/open"
    todos = json.loads(requests.get(url).text)
    i = 0
    for t in todos:
        print(f"\033[94m{i}.\033[0m | {todo_str(t)}")
        i += 1
    index = int(input("Which one is done? "))
    url = server_url + f"/done/{todos[index]['id']}"
    requests.get(url)

if sys.argv[-1] == "add":
    add_todo()
elif sys.argv[-1] == "done":
    do_todo()
else:
    show_todos()
