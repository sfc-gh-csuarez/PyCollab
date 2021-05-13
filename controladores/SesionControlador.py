'''
@ Carlos Suarez 2020
'''

import requests
import datetime
import time 
import json
from cachetools import TTLCache
import ssl
import sys

class SesionControlador():
    def __init__(self,url,token,cert):
        self.url = url
        self.token = token
        self.cert = cert

    def getGrabaciones(self,cursoUUID,tiempo):
        endpoint = 'https://' + self.url + '/recordings' + "?contextExtId=" + cursoUUID + "&startTime=" + str(tiempo)
        bearer = "Bearer " + self.token
        rheaders = {
            "Authorization":bearer,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        r = requests.get(endpoint,headers=rheaders,verify=self.cert)
        if r.status_code == 200:
            res = json.loads(r.text)
            return res
        else:
            print(r)
    



    def getGrabacionUUID(self,recording_id):
        endpoint = 'https://' + self.url + '/recordings/' + recording_id
        bearer = "Bearer " + self.token
        rheaders = {
            "Authorization":bearer,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        r = requests.get(endpoint,headers=rheaders,verify=self.cert)
        if r.status_code == 200:
            res = json.loads(r.text)
            return res
        else:
            print("Error:", str(r))
            return None


    def get_grabacion_UUID_data(self,recording_id):
        authStr = 'Bearer ' + self.token
        url = 'https://' + self.url + '/recordings/' + recording_id + '/data'
        r = requests.get(url,
                         headers={'Authorization': authStr, 'Content-Type': 'application/json',
                                  'Accept': 'application/json'}, verify=self.cert)
        try:
            if r.status_code == 200:
                res = json.loads(r.text)
                return res
            if r.status_code == 403:
                return None
        except requests.exceptions.HTTPError as e: 
            print("Error in recording Id:" + recording_id , str(e))
            return None



    def get_grabacion_UUID_data_secure(self,recording_id):
        authStr = 'Bearer ' + self.token
        url = 'https://' + self.url + '/recordings/' + recording_id + '/data/secure'
        r = requests.get(url,
                         headers={'Authorization': authStr, 'Content-Type': 'application/json',
                                  'Accept': 'application/json'}, verify=self.cert)
        if r.status_code == 200:
            res = json.loads(r.text)
            return res
        if r.status_code == 403:
            return None
        else:
            print("Error", str(r))
            return None



    def get_recording_data(self,recording_id):
        # "Authorization: Bearer $token"
        authStr = 'Bearer ' + self.token
        url = 'https://' + self.url + '/recordings/' + recording_id + '/data'
        r = requests.get(url,
                         headers={'Authorization': authStr, 'Content-Type': 'application/json',
                                  'Accept': 'application/json'}, verify=self.cert)

        if r.status_code == 200:
            res = json.loads(r.text)
            return res
        elif r.status_code == 403:
            return None
        elif r.status_code == 404:
            return None
        else:
            print("Error: " + str(r) + "in recordingId: " + recording_id)
            return None 
    







    def get_recording_data_4url(self,recording_id):
        # "Authorization: Bearer $token"
        authStr = 'Bearer ' + self.token
        url = 'https://' + self.url + '/recordings/' + recording_id 
        r = requests.get(url,
                         headers={'Authorization': authStr, 'Content-Type': 'application/json',
                                  'Accept': 'application/json'}, verify=self.cert)
        if r.status_code == 200:
            res = json.loads(r.text)
            return res
        elif r.status_code == 403:
            return None
        elif r.status_code == 404:
            return None
        else:
            print("Error: " + str(r) + "in recordingId: " + recording_id)
            return None



    def getRecordingURL(self,recording_id):
        authStr = 'Bearer ' + self.token
        url = 'https://' + self.url + '/recordings/' + recording_id + '/url?disposition=download'
        try:
            r = requests.get(url,
                         headers={'Authorization': authStr, 'Content-Type': 'application/json',
                                  'Accept': 'application/json'}, verify=self.cert)
            r.raise_for_status()
            
            if r.status_code == 200:
                data = json.loads(r.text)
                return data['url']
            elif r.status_code == 404:
                return None
            else:
                return None
        except requests.exceptions.HTTPError as e:
            print(e)
            pass



    def delete_recording(self,recording_id):
        authStr = 'Bearer ' + self.token
        url = 'https://' + self.url + '/recordings/' + recording_id
        try:
            r = requests.delete(url,headers={'Authorization': authStr, 'Content-Type': 'application/json','Accept': 'application/json'}, verify=self.cert)
            r.raise_for_status()
            if r.status_code == 200:
                return True
        except requests.exceptions.HTTPError as e:
            return '404'
            pass




    