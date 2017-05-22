#!python3
#encoding:utf-8
import requests
import datetime
import time
import json
import web.service.github.api.v3.Response
class SshKeys(object):
    def __init__(self):
        self.__response = web.service.github.api.v3.Response.Response()

    def Create(self, token, mailaddress, public_key):
        url = 'https://api.github.com/user/keys'
        headers=self.__GetHeaders(token)
        data=json.dumps({'title': mailaddress, 'key': public_key})
        print(url)
        print(data)
        r = requests.post(url, headers=headers, data=data)
        return self.__response.Get(r)
        
    def Gets(self, username, token):
        keys = []
        url = 'https://api.github.com/users/{username}/keys'.format(username=username)
        headers=self.__GetHeaders(token)
        while None is not url:
            print(url)
            r = requests.get(url, headers=headers)
            keys += self.__response.Get(r)
            url = self.__response.Headers.Link.Next(r)
        return keys
        
    def Get(self, token, key_id):
        url = 'https://api.github.com/user/keys/{key_id}'.format(key_id=key_id)
        headers=self.__GetHeaders(token)
        print(url)
        r = requests.get(url, headers=headers)
        return self.__response.Get(r)
        
    def __GetHeaders(self, token, otp=None):
        headers = {
            'Time-Zone': 'Asia/Tokyo',
            'Accept': 'application/vnd.github.v3+json',
            'Authorization': 'token ' + token
        }
        if None is not otp:
            headers.update({'X-GitHub-OTP': otp})
        print(headers)
        return headers
