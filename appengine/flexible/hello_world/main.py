# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
import json
from flask import Flask, jsonify, request, redirect, session

import requests

import urllib

import mysql.connector
from mysql.connector.constants import ClientFlag



app = Flask(__name__)
@app.route('/')
def index():
    return jsonify({'name': 'alice',
                    'email': 'alice@outlook.com'})


@app.route('/sql')
def sql():
    config = {
    'user': 'root',
    'password': 'cs411',
    'host': '34.170.81.182',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
    }
    config['database'] = 'testdb'
    cnxn = mysql.connector.connect(**config)

    cursor = cnxn.cursor()  # initialize connection cursor
    cursor.execute('SELECT * FROM test') #sql query
    for row in cursor.fetchall():
        print(row)
    cnxn.close()  # close connection 

    # print('hi')
    return "TEST IMPLMENTATION COMPLETE"
    #sql here

@app.route('/profile')
def profile():
    config = {
    'user': 'root',
    'password': 'cs411',
    'host': '34.170.81.182',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
    }
    
    config['database'] = 'test'
    cnxn = mysql.connector.connect(**config)
    
    cursor = cnxn.cursor()
    cursor.execute('SELECT email FROM Profile where userName = \"' + request.args['userName'] + '\"')
    
    ret = ""
    for row in cursor.fetchall():
        ret += str(row)
    cnxn.close()
    return ret


@app.route('/callback')
def callback():
    code = request.args['code']
    token_url = 'https://accounts.spotify.com/api/token'
    authorization = "Basic ZThjOWEwNzc4N2QyNDIyMWIzM2E4YmRiNzIyZGNmMzQ6NjY2MjU1MTE0MTU5NGE4YmFiNmY1NmU2ZDkzNTBlMTQ="
    redirect_uri = "http://localhost:5000/callback"
    
    headers = {'Authorization': authorization, 
             'Accept': 'application/json', 
             'Content-Type': 'application/x-www-form-urlencoded'}
    body = {'code': code, 
            'redirect_uri': redirect_uri, 
          'grant_type': 'authorization_code'}
    
    post_response = requests.post(token_url,headers=headers,data=body)
    
    session['token'] = post_response.json()['access_token']
    session['refresh_token'] = post_response.json()['refresh_token']
    
    print('idc')
    print(post_response.json())
    
    return redirect('/')

@app.route('/authorize')
def auth():
    client_id = 'e8c9a07787d24221b33a8bdb722dcf34'
    redirect_uri = 'http://localhost:5000/callback'
    
    scope = 'user-read-private user-read-email'
    # see list of scopes: https://developer.spotify.com/documentation/general/guides/authorization/scopes/
    
    try:
        url = 'https://accounts.spotify.com/authorize?'
        params = {
            'response_type': 'code', 
            'client_id': client_id, 
            'redirect_uri': redirect_uri,
            'scope': scope,
            #'state': state_key
        }
        
        query_params = urllib.parse.urlencode(params)
        return redirect(url + query_params)
        
    except:
        print('Spotify login error')
        return 'Spotify login error. oops!'

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host='127.0.0.1', port=8080, debug=True)

# [END gae_flex_quickstart]
