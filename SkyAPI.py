#!/usr/bin/env python3
"""
Skycoin API python interface
"""
import requests
from functools import wraps

HEADERS = {'Content-Type' : 'application/x-www-form-urlencoded; charset=utf-8'}

@wraps(requests.post)
def post(*args, **kwargs):
    #Handle all relevant error from requests.posts
    try:
        resp = requests.post(*args, **kwargs)
    except requests.ConnectionError:
        print("failed to connect")
    if not (200 <= resp.status_code < 300):
        raise Exception('status code: {} outside of 2xx range'.format(resp.status_code))
    return resp

@wraps(requests.get)
def get(*args, **kwargs):
    try:
        resp = requests.get(*args, **kwargs)
    except requests.ConnectionError:
        print("failed to connect")
    if not (200 <= resp.status_code < 300):
        raise Exception('status code: {} outside of 2xx range'.format(resp.status_code))
    return resp


class SkyAPI(object):
    #API that should create a session and update over time the status of nodes
    def __init__(self, secret=None):
        self._secret = secret
        self.token = None
        self.nodesKeys = None
        self.cookies = None
        self.headers = HEADERS
        self.keysAddr = None
        self.nodesInfo = None
        self.nodesConnected = None

    def login(self):
        if self._secret is None:
            raise Exception("Skycoin secret pass is undefined")
        data = {'pass': self._secret}
        self.res = post('http://127.0.0.1:8000/login', headers=self.headers, data=data)
        self.token = self.res.cookies.values()[0]
        self.cookies = self.res.cookies

    def checkLogin(self):
        post('http://127.0.0.1:8000/checkLogin', headers=self.headers)

    def getNodesKeys(self):
        #get Nodes key list
        response = get('http://127.0.0.1:8000/conn/getAll')
        self.nodesKeys = [node['key'] for node in response.json()]

    def getNodesAddr(self, cookies=None):
        #get Node IP:PORT list
        if cookies == None:
            if self.cookies == None:
                raise Exception("bug: no cookies defined")
        if self.nodesKeys == None:
                raise Exception("No node keys : should call getNodesKeys before get NodesAddr")
        #get Node IP/port
        headers = 'http://127.0.0.1:8000/conn/getNode?key='
        self.keysAddr = {key : post(headers+key, cookies=self.cookies).json()['addr']\
                for key in self.nodesKeys}

    def getNodesInfo(self):
        #get dictionary of node IPs and Status
        if self.cookies == None:
            if self.cookies == None:
                raise Exception("bug: no cookies defined")
        if self.keysAddr == None:
            raise Exception("No node addr: ...")
        def params(addrNport):
            return { 'addr' : 'http://' + addrNport + '/node/getInfo', 'method' : 'post'}

        self.nodesInfo = {}
        for key, addr in self.keysAddr.items():
            res = post('http://127.0.0.1:8000/req', headers=self.headers,\
                    cookies=self.cookies, data=params(addr)).json()['discoveries']
            self.nodesInfo.update({key : [addr, bool(res.values())]})

    def update(self):
        self.login()
        self.getNodesKeys()
        self.getNodesAddr()
        self.getNodesInfo()
