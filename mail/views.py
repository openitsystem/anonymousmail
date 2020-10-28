from django.utils.encoding import escape_uri_path
from imap_tools import *
import json
from django.shortcuts import HttpResponse
from django.http import FileResponse
import datetime
from pyDes import des, CBC, PAD_PKCS5
import binascii
from io import BytesIO

mailaccount = ''
mailaccountPassword = ''
mailServerIp = "127.0.0.1"
# 秘钥,需要八位的
KEY = ''


def des_encrypt(s):
    """
    DES 加密
    :param s: 原始字符串
    :return: 加密后字符串，16进制
    """
    secret_key = KEY
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en)


def des_descrypt(s):
    """
    DES 解密
    :param s: 加密后的字符串，16进制
    :return:  解密后的字符串
    """
    secret_key = KEY
    iv = secret_key
    k = des(secret_key, CBC, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de

def getmaillist(request):
    try:
        address = request.GET.get('address', '')
        mailbox = MailBoxUnencrypted(mailServerIp, port=143)
        if not address or "@mfk.app" not in address or not address.replace("@mfk.app",""):
            isSuccessvalue = {"isSuccess":True,"results":[],"count":0}
        else:
            mailbox.login(mailaccount, mailaccountPassword, initial_folder='INBOX')  # or mailbox.folder.set instead 3d arg
            msg = [msg for msg in mailbox.fetch(A(A(all=True,date_gte=(datetime.date.today()-datetime.timedelta(days=1))),OR(to=address,bcc=address,cc=address,)))]
            zzz = list()
            for i in msg:
                zzz.append({"subject":i.subject,"uid":str(des_encrypt(str(i.uid)), encoding = "utf8"),"from":i.from_,"date":(datetime.datetime.fromtimestamp((i.date).timestamp())).strftime('%Y-%m-%d %H:%M:%S'),"attachments":len(i.attachments)})
            zzz.sort(key=lambda x: x['date'], reverse=True)
            isSuccessvalue = {"isSuccess":True,"results":zzz,"count":len(zzz)}
            mailbox.logout()
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(isSuccessvalue))
        return response
    except Exception as e:
        print(e)
        isSuccessvalue = {"isSuccess":False,"message":"系统错误"}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(isSuccessvalue))
        return response

def getmailmessage(request):
    try:
        uid = request.GET.get('uid', '')
        uidValue = str(des_descrypt(uid), encoding = "utf8")
        mailbox = MailBoxUnencrypted(mailServerIp, port=143)
        mailbox.login(mailaccount, mailaccountPassword, initial_folder='INBOX')  # or mailbox.folder.set instead 3d arg
        msg = [msg for msg in mailbox.fetch(A(A(all=True,uid=uidValue)))]
        returnMailMessage = list()
        for i in msg:
            print(i.obj)
            if i.html:
                bodyValue = i.html
                for attachment in i.attachments:
                    srcValue = r'src="cid:'+attachment.content_id+'"'
                    srcValueOld = r'src="data:image/png;base64,'+(attachment.part).get_payload()+'"'
                    if srcValue in bodyValue:
                        bodyValue = bodyValue.replace(srcValue, srcValueOld,100000)
            else:
                bodyValue = i.text
            returnMailMessage.append({"headers":i.headers,"subject":i.subject,"uid":uid,"from":i.from_,"body":bodyValue,"to":i.to,"attachment":[{"name":attachment.filename,"id":attachment.content_id} for attachment in i.attachments]})
        isSuccessvalue = {"isSuccess":True,"results":returnMailMessage[0]}
        mailbox.logout()
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(isSuccessvalue))
        return response
    except Exception as e:
        print(e)
        isSuccessvalue = {"isSuccess":False,"message":"系统错误","results":{}}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(isSuccessvalue))
        return response

def getmailattachment(request):
    try:
        uid = request.GET.get('uid', '')
        attachmentid = request.GET.get('attachmentid', '')
        uidValue = str(des_descrypt(uid), encoding = "utf8")
        mailbox = MailBoxUnencrypted(mailServerIp, port=143)
        mailbox.login(mailaccount, mailaccountPassword, initial_folder='INBOX')  # or mailbox.folder.set instead 3d arg
        msg = [msg for msg in mailbox.fetch(A(A(all=True,uid=uidValue)))]
        for attachment in msg[0].attachments:
            if attachment.content_id == attachmentid:
                mailbox.logout()
                response = FileResponse(BytesIO(attachment.payload),content_type=attachment.content_type)
                response['Content-Disposition'] = 'attachment;filename={}'.format(escape_uri_path(attachment.filename))
                return response
    except Exception as e:
        print(e)
        isSuccessvalue = {"isSuccess":False,"message":"系统错误","results":{}}
        response = HttpResponse()
        response['Content-Type'] = "text/javascript"
        response.write(json.dumps(isSuccessvalue))
        return response
