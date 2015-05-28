#-*- coding: UTF-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response


def login_identify(fn):
    def wrapper(*request,**kwargs):
        reference = request[0].path
        print reference
        if reference==None:
            reference = u'/'
        if request[0].session.get('loginstat')=='registed':
            return fn(request[0],**kwargs)
        else:
            response=render_to_response('BSlogin.html',{'msg':'请先登录','reference':reference})
            response.set_cookie("username",'admin')
            #response.set_cookie("sessionid",request[0].session.session_key)
            return response
    return wrapper
