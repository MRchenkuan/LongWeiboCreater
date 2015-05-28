#-*- coding: UTF-8 -*-

import sendMail
import captureCreate
import StringIO
import base64



def sendCapture():
    code_img = captureCreate.create_validate_code()
    fileIO=StringIO.StringIO()
    code_img[0].save(fileIO, "png")
    fileIO = base64.encodestring(fileIO.getvalue())#base64

    if sendMail.send_mail(['393667111@qq.com'],"长沙好工作提交验证",u"<html><body><a>验证码为%s</a></body></html>"%(code_img[1])):
        print u"发送成功"
        return ['200',fileIO,code_img[1]]
    else:
        print u"发送失败"
        return ['503',fileIO,code_img[1]]
    # return ['200',fileIO]