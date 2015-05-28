#coding=utf-8

import time
from models import ad_info,ad_status
import base64,datetime
from django.http import *
from django.shortcuts import render_to_response
from LongWeiboCreater import *
from django.contrib.sessions.models import Session
import django.contrib.sessions.backends.file
import os
import random
from django.db import transaction
from PIL import Image
import json
from decorators import login_identify


def cpage(request):
    return render_to_response('c.html')

@login_identify
def adAddPage(request):
    return render_to_response('adsubmit.html')

#登录页的展示
def loginpage(request):
    return render_to_response('BSlogin.html')

#系统登录
def login(request):
    u = request.POST.get('username')
    p = request.POST.get('password')
    reference = request.POST.get('reference') or '/index/'

    if u=='ckadol' and p=='ckadol':
        response = HttpResponseRedirect(reference)
        request.session['loginstat']='registed'
        response.set_cookie("sessionid",request.session.session_key)
        return response
    else:
        response = render_to_response('BSlogin.html',{'msg':u"<span style='color:red'>帐号,或者密码错误</span>",'reference':reference})
        return response

#系统退出
def logout(request):
    API(request,apikey='delsession')
    return render_to_response('BSlogin.html')

# 处理函数
@login_identify
def c(request):
    request.session.flush()
    ac = ArticleCreate()
    ac.elem_title = request.POST.get('title')
    ac.elem_coname = request.POST.get('coname')
    ac.elem_cotype = request.POST.get('cotype')
    ac.elem_coindustry = request.POST.get('coindustrydetail')
    ac.elem_location = request.POST.get('location')
    ac.elem_yearcount = request.POST.get('yearcount')
    ac.elem_degree = request.POST.get('degree')
    ac.elem_treatment = request.POST.get('treatment')
    ac.elem_opinfo = request.POST.get('opinfo')
    ac.elem_coinfo = request.POST.get('coinfo')
    ac.elem_cosize = request.POST.get('cosize')
    ac.elem_duty = request.POST.get('duty')
    ac.elem_require = request.POST.get('require')
    ac.elem_custname = request.POST.get('custname')
    ac.elem_phone = request.POST.get('phone')
    ac.elem_email = request.POST.get('email')
    ac.elem_recruiting = request.POST.get('recruiting')
    img = ac.imgprint()

    adinfo = ad_info(
            ad_title = ac.elem_title,
            ad_coname = ac.elem_coname,
            ad_cotype = ac.elem_cotype,
            ad_coindustry = ac.elem_coindustry,
            ad_location = ac.elem_location,
            ad_yearcount = ac.elem_yearcount,
            ad_degree = ac.elem_degree,
            ad_treatment = ac.elem_treatment,
            ad_opinfo = "".join(ac.elem_opinfo),
            ad_coinfo = "".join(ac.elem_coinfo),
            ad_cosize = ac.elem_cosize,
            ad_duty = "".join(ac.elem_duty),
            ad_require = "".join(ac.elem_require),
            ad_custname = ac.elem_custname,
            ad_phone = ac.elem_phone,
            ad_email = ac.elem_email,
            ad_recruiting = ac.elem_recruiting,
            createtime = datetime.datetime.now(),
            updatetime = datetime.datetime.now(),
            ad_type=1
    )
    adinfo.save()

    adstat = ad_status(
            ad_id = adinfo, ad_status=0, ad_vistcount=0,
            createtime = datetime.datetime.now(),
            updatetime = datetime.datetime.now()
            )
    print adstat.save()



    #print request.COOKIES['sessionid']#固化cookie
    request.session['imgbase64']=ac.imgdata #此处为IO流而非字符串
    ssid = request.session.session_key

    msg=(u"【%s】月薪%s，%s"%(ac.elem_title,ac.elem_treatment, ''.join(ac.elem_require))).replace('\r','').replace(' ','').replace('\n','')

    msg = msg[0:110]
    msg = u'%s...'%msg.replace('\r','')

    return render_to_response('d.html', {'img':img,'ssid':ssid,'msg':msg})

def s(request):
    ssid = request.GET.get('ssid') #串化cookie
    print request.COOKIES['sessionid']#固化cookie
    request.session.session_key = ssid
    imgbase64=request.session.get('imgbase64')
    img = Image.open(StringIO(imgbase64))
    response = HttpResponse(mimetype="image/png")
    img.save(response, "png")
    return response

def sendCapture(request):
    from mailSender import send
    request.session.flush()
    result = send.sendCapture()
    request.session['capture'] = result[2]
    print result
    result = "{'stat':%s,'msg':'%s'}"%(result[0],result[1].replace('\n',''))
    print 'sscapture = ',request.session['capture']
    return HttpResponse(result)

def validCapture(request):
    print request.session.get('capture'),request.GET.get('capture')
    if request.session['capture'] == request.GET.get('capture'):
        print request.session['capture'],request.GET.get('capture'),'is right'
    else:
        print request.session['capture'],request.GET.get('capture'),'is wrong'
    return 200

# 广告新增函数
@login_identify
def addAd(request):
    cname = request.GET.get("cname")
    contact = request.GET.get("contact")
    user = request.GET.get("user")
    imgurl = request.GET.get("imgurl")
    imglink = request.GET.get("imglink")
    adtype=request.GET.get("adtype")

    print 'ok'

    adinfo = ad_info(
            ad_coname = cname,
            ad_custname = user,
            ad_phone = contact,
            ad_imurl = imgurl,
            ad_links = imglink,
            createtime = datetime.datetime.now(),
            updatetime = datetime.datetime.now(),
            ad_type = adtype
    )
    adinfo.save()
    print 'ok'
    adstat = ad_status(
        ad_id = adinfo,ad_status=0,
        ad_vistcount=0,
        createtime = datetime.datetime.now(),
        updatetime = datetime.datetime.now(),
        ad_effective = datetime.datetime.strptime('2014-02-03','%Y-%m-%d'),
        ad_expiry = datetime.datetime.strptime('2020-12-31','%Y-%m-%d')
    )
    adstat.save()
    print 'ok'
    return HttpResponse('提交成功！')


# 审核页面
@login_identify
def adReveiw(request):
    info = API(request,apikey='getAdReveiw',type=1)
    return render_to_response('adreview.html',{'info':info})

@login_identify
def adReveiwAd(request):
    ad = API(request,apikey='getAdReveiw',type=2)
    return render_to_response('adreview-ad.html',{'ad':ad})

# 审核操作
@login_identify
def review(request):
    reveiwid = request.GET.get('reveiwid')
    reveiwrst = request.GET.get('reveiwrst')
    startdate = request.GET.get('startdate')
    enddate = request.GET.get('enddate')

    print(datetime.datetime.strptime(startdate,'%Y-%m-%d'))
    adobj = ad_status.objects.get(id=reveiwid)
    adobj.ad_status = (1 and reveiwrst=='pass') or (( -1 and reveiwrst=='reject') and -1 ) or (0)
    adobj.updatetime = datetime.datetime.now()
    adobj.ad_effective = startdate #not surpport as : datetime.datetime.strptime('2014-02-03','%Y-%m-%d'),
    adobj.ad_expiry = enddate #not surpport as :datetime.datetime.strptime('2020-12-31','%Y-%m-%d')

    print reveiwid,reveiwrst,adobj
    adobj.save()
    print reveiwid,reveiwrst,adobj
    return HttpResponse('审核成功')

# 统一api入口
@login_identify
def API(request,**kwargs):
    apiKey = request.GET.get('apikey') or kwargs['apikey']
    responses = []
    # type = kwargs.get('type') or 'newest'
    # limit = kwargs.get('limit') or 20

    # 获取招聘岗位
    def getHireAd(kwargs):
        count = 0
        result = []
        if kwargs['type'] == 'newest':
            result = ad_status.objects.filter(ad_status=1).order_by('-updatetime')
        if kwargs['type'] == 'hotest':
            result = ad_status.objects.filter(ad_status=1).order_by('-ad_vistcount')
        if(len(result)==0):return HttpResponse('no result!')
        for obj in result:
            objinfo = obj.ad_id
            if objinfo.ad_type==1:
                if count >= kwargs['limit']:
                    break
                responses.append({
                    'title':objinfo.ad_title,
                    'coname':objinfo.ad_coname,
                    'vistcount':obj.ad_vistcount,
                    'id':objinfo.id})
                count+=1
        return responses

    # 获取广告数据
    def getFlashAd(**kwargs):
        pass

    # 获得广告审核信息
    def getAdReveiw(kwargs):
        type = kwargs.get('type')
        adstat = ad_status.objects.all().order_by('-createtime') or []
        infomation = []
        for eachitem in adstat:
            if eachitem.ad_id.ad_type == type:
                adobj = {
                    'id':eachitem.ad_id.id,
                    'coindustry':eachitem.ad_id.ad_cotype,
                    'title':eachitem.ad_id.ad_title,
                    'statid':eachitem.id,
                    'coname':eachitem.ad_id.ad_coname,
                    'adtype':u'广告页面',
                    'imgurl':eachitem.ad_id.ad_imurl,
                    'imglink':eachitem.ad_id.ad_links,
                    'contact':eachitem.ad_id.ad_phone,
                    'creattime':eachitem.ad_id.createtime,
                    'efftime':eachitem.ad_effective or '0000-00-00',
                    'exptime':eachitem.ad_expiry or '0000-00-00',
                    'stat':(eachitem.ad_status==0 and u'待审核' ) or (eachitem.ad_status==1 and u'已经生效') or (u'已失效')
                }
                infomation.append(adobj)
        return infomation

    def getPhotoAd(kwargs):
        limit=kwargs.get('limit') or None

        now = datetime.datetime.now()
        results = ad_status.objects.filter(ad_status=1,ad_effective__lte=now,ad_expiry__gte=now)[0:limit]
        responses = []
        for items in results:
            iteminfo = items.ad_id
            responses.append({'imgurl':iteminfo.ad_imurl,'imglink':iteminfo.ad_links,'id':iteminfo.id,'veiwcount':items.ad_vistcount,})
        return HttpResponse(responses)

    def delsession(kwargs):
        del request.session['loginstat']
        return HttpResponse('退出成功')

    apilib = {
        'getHireAd':getHireAd,
        'getFlashAd':getFlashAd,
        'getAdReveiw':getAdReveiw,
        'getPhotoAd':getPhotoAd,
        'delsession':delsession
        }
    return apilib[apiKey](kwargs)

@login_identify
def displayhome(request):
    info = API(request,apikey='getHireAd',limit=20,type='newest')
    return render_to_response('homepage.html',{'info':info})

def test(request):
    time.sleep(1)
    return HttpResponse('yes')
def testpage(request):
    time.sleep(1)
    try:
        return render_to_response('test.html')
    except:
        print('respons fail')






