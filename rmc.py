#!/usr/bin/env python3

import json
import requests
import pendulum
import urllib3
import sys
import os
from time import gmtime, strftime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

login_uri = "/rest/rm-central/v1/login-sessions"
tasks_uri = "/rest/rm-central/v2/tasks"
TZ = "Europe/Kiev"
hours = 24

def date_parse(date):
    return pendulum.parse(date.strip('Z'))


def date_print(date):
    date = date_parse(date)
    return date.in_tz(tz=TZ).to_datetime_string()

def get_failed_tasks(ip,login,password):
    cred = {
        "auth": {
            "passwordCredentials": {
                "username": login,
                "password": password
            }
        }
    }

    past = pendulum.now().subtract(hours=hours)
    host = "https://"+ip
    login_response = requests.post((host + login_uri), json=cred, verify=False)
    token = login_response.json()['loginSession']['access']['token']['id']
    headers = {"X-Auth-Token": token}
    tasks_response = requests.get((host + tasks_uri),
                                  headers=headers,
                                  verify=False)
    tasks = tasks_response.json()
    counter = 0
    messag = []
    for task in tasks['tasks']:
        if task['taskStatus'] != "Ok" and date_parse(task['createdAt']) >= past:
            task_uri = (task['taskUri'])
            task_response = requests.get((host + task_uri),
                                         headers=headers,
                                         verify=False)
            result = task_response.json()
            counter +=1
            if task['taskStatus'] == "Error":
                error = (result['task']['taskErrors'][0]['errorDetails'])
            else:
                error = task['taskStatus']
            msg= "Name: {}, Initiator: {}, Parent: {}, Resource: {}, createdAt: {}, updatedAt: {}, {} ]".format(
                 task['name'],str(task['initiator']), str(task['parentResourceName']),
                 str(task['associatedResource']['resourceName']),
                 date_print(task['createdAt']), date_print(task['updatedAt']), error)
            messag.append((ip,'ERROR',msg))
    return messag
if __name__ == '__main__':
    try:
        ip = "###-rmc1"
        login = "libre"
        password = "###"
        resp = get_failed_tasks(ip,login,password)
        if resp != "":
                print(resp)
        else:
                print('Nothing to send')

    except KeyboardInterrupt:
        print('Bye-Bye...')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
