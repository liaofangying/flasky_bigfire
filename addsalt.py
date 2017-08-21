#coding: utf-8

import hashlib
import base64
import time
from datetime import datetime

def getnowtime():
	now = time.time()
	nowTime = datetime.fromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
	return nowTime

def addsalt(password, nowTime):
	sha1First = hashlib.sha1(password).hexdigest()
	sha1First = str(nowTime)[0:19] + sha1First
	sha1Two = hashlib.sha1(sha1First).hexdigest()
	finalPassWord = base64.encodestring(sha1Two)
	return finalPassWord