import http.client
import json

import requests
from flask import Flask,jsonify,request
from requests.auth import HTTPBasicAuth

app=Flask(__name__)

@app.route('/', methods=["POST"])


def abc():
  flag = 0
  input_json = request.get_json(force=True)
  conn = http.client.HTTPSConnection("log-analysis.atlassian.net")
  url = "https://log-analysis.atlassian.net/rest/api/3/search"

  auth = HTTPBasicAuth("keerthanadm.is20@rvce.edu.in",
                       "ATATT3xFfGF009VqyVnK0BEhhC_mZ1iIqqLm0fumX8TETxokzVLh76Jvdv77_-EczE7o-QfLBSsSCbNngW8Lehn2OI7HV930JDPlt3D0CsoCZ0h_uLk4med8Gf9dJrHT86mXMG1__5gUU_EfBAhJAjBXoMee9SY5fgKZyW5Tcxh6nblRiHCWDuw=800C4A75")

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic a2VlcnRoYW5hZG0uaXMyMEBydmNlLmVkdS5pbjpBVEFUVDN4RmZHRjAwOVZxeVZuSzBCRWhoQ19tWjFpSXFxTG0wZnVtWDhURVR4b2t6VkxoNzZKdmR2NzdfLUVjekU3by1RZkxCU3NTQ2JObmdXOExlaG4yT0k3SFY5MzBKRFBsdDNEMENzb0NaMGhfdUxrNG1lZDhHZjlkSnJIVDg2bVhNRzFfXzVnVVVfRWZCQWhKQWpCWG9NZWU5U1k1ZmdLWnlXNVRjeGg2bmJsUmlIQ1dEdXc9ODAwQzRBNzU=',
    'Cookie': 'atlassian.xsrf.token=2ce4f5e8-4fa2-44be-a47e-9a2b5b3c24f0_4e22051a201d1b197a173c602d4d6cbf789df1c4_lin'
  }

  query = {
    'jql': '',
    'maxResults': 1000
  }

  response = requests.request(
    "GET",
    url,
    headers=headers,
    params=query,
    auth=auth
  )
  a = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
  a = json.loads(a)
  a = a['issues']
  # print(a[0]['fields']['description']['content'][0]['content'][0]['text'])
  for each in a:
    if(each['fields']['issuetype']['name']=='Sub-task'):
      continue
    elif (each['fields']['description']['content'][0]['content'][0]['text'] == input_json["text"] ):
      if each['fields']['status']['name']=='Done':
        flag==0
        break
      else:
        flag = 1
        payload = json.dumps({
          "fields": {
            "project": {
              "key": input_json['key']
            },
            "parent": {
              "key": each['key']
            },
            "summary": input_json['summary'],
            "description": {
              "type": "doc",
              "version": 1,
              "content": [
                {
                  "type": "paragraph",
                  "content": [
                    {
                      "type": "text",
                      "text": input_json['text']
                    }
                  ]
                }
              ]
            },
            "priority": {
              input_json['priority']
            },
            "issuetype": {
              "name": "Sub-task"
            }
          }
        })
        break

  if flag==0:
    payload = json.dumps({
    "fields": {
      "project": {
        "key":input_json['key']
      },
      "summary": input_json['summary'],
      "description": {
        "type": "doc",
        "version": 1,
        "content": [
          {
            "type": "paragraph",
            "content": [
              {
                "type": "text",
                "text": input_json['text']
              }
            ]
          }
        ]
      },
      # "priority": {
      #   input_json['priority']
      # },
      "issuetype": {
        "name": input_json['issue']
      }
    }
  })



  conn.request("POST", "/rest/api/3/issue", payload, headers)
  res = conn.getresponse()
  data = res.read()
  return jsonify(payload)