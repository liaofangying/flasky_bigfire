#coding: utf-8

from controller.view import app
from flaskext.mysql import MySQL
from addsalt import *
import forgery_py
from markdown import markdown

mysql = MySQL()
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'FlaskData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

def getindate(userName):
	sqlStatement = "SELECT inDate FROM users WHERE userName = %s;"
	cursor = mysql.connect().cursor()
	cursor.execute(sqlStatement, userName)
	data = cursor.fetchone()
	if data:
		inDate = data[0]
		return inDate
	else:
		return

def login(userName, passWord):
	inDate = getindate(userName)
	passWord = addsalt(passWord, inDate)
	sqlStatement = "SELECT userId FROM users WHERE userName = %s AND passWord = %s;"
	cursor = mysql.connect().cursor()
	cursor.execute(sqlStatement, (userName, passWord))
	data = cursor.fetchone()
	if data:
		return 'ok'
	else:
		return

def checkifexist(userName):
	sqlStatement = "SELECT userId FROM users WHERE userName = %s;"
	cursor = mysql.connect().cursor()
	cursor.execute(sqlStatement, userName)
	data = cursor.fetchone()
	if data:
		return 'ok'
	else:
		return

def adduser(userName, passWord):
	if checkifexist(userName) is None:
		nowTime = getnowtime()
		passWord = addsalt(passWord, nowTime)
		sqlStatement = "INSERT INTO `users` (`userName`, `passWord`, `roleID`, `inDate`) VALUES (%s, %s, 2, %s);"
		connection = mysql.connect()
		cursor = connection.cursor()
		cursor.execute(sqlStatement, (userName, passWord, nowTime))
		connection.commit()
		return "ok"
	else:
		return

def updatepassword(userName, passWord):
	inDate = getindate(userName)
	passWord = addsalt(passWord, inDate)
	sqlStatement = "UPDATE `users` SET passWord = %s WHERE userName = %s;"
	connection = mysql.connect()
	cursor = connection.cursor()
	cursor.execute(sqlStatement, (passWord, userName))
	connection.commit()
	return

def getuserprofile(userName):
	sqlStatement = "SELECT * FROM users WHERE userName = %s;"
	cursor = mysql.connect().cursor()
	cursor.execute(sqlStatement, userName)
	data = cursor.fetchone()
	userName = data[1]
	inDate = data[4]
	location = data[5]
	aboutMe = data[6]
	lastSeen = data[7]
	avatar = data[8]
	return userName, inDate, location, aboutMe, lastSeen, avatar

def getavatar(userName):
	sqlStatement = "SELECT avatar FROM users WHERE userName = %s;"
	cursor = mysql.connect().cursor()
	cursor.execute(sqlStatement, userName)
	data = cursor.fetchone()
	avatar = data[0]
	return avatar

def getuserid(userName):
	sqlStatement = "SELECT userId FROM users WHERE userName = %s;"
	cursor = mysql.connect().cursor()
	cursor.execute(sqlStatement, userName)
	data = cursor.fetchone()
	if data is not None:
		userId = data[0]
		return userId

def getusername(userId):
	sqlStatement = "SELECT userName FROM users WHERE userId = %s;"
	cursor = mysql.connect().cursor()
	cursor.execute(sqlStatement, userId)
	data = cursor.fetchone()
	if data is not None:
		thisUserName = data[0]
		return thisUserName

def edituserprofile(userName, location, aboutMe, oldUserName):
	sqlStatement = "UPDATE users SET userName = %s, location = %s, aboutMe = %s where userName = %s;"
	connection = mysql.connect()
	cursor = connection.cursor()
	cursor.execute(sqlStatement, (userName, location, aboutMe, oldUserName))
	connection.commit()
	return

def writepost(userName, content):
	# htmlcontent = markdown(content)
	userId = getuserid(userName)
	sqlStatement = "INSERT INTO `posts` (`postContent`, `userId`) VALUES (%s, %s);"
	connection = mysql.connect()
	cursor = connection.cursor()
	#cursor.execute(sqlStatement, (htmlcontent, userId))
	cursor.execute(sqlStatement, (content, userId))
	connection.commit()
	return 'ok'

def getallpost():
	sqlStatement = "SELECT b.userName, b.avatar, a.postContent, a.inDate , a.postId FROM posts a INNER JOIN users b ON a.userId = b.userId ORDER BY a.inDate DESC"
	cursor = mysql.connect().cursor()
	cursor.execute(sqlStatement)
	data = cursor.fetchall()
	return data

def getfollowedpost(userName):
	userId = getuserid(userName)
	sqlStatement = "SELECT b.userName, b.avatar, a.postContent, a.inDate , a.postId FROM posts a INNER JOIN users b ON a.userId = b.userId INNER JOIN relations c ON a.userId = c.bloggerId WHERE c.fansId = %s ORDER BY a.inDate DESC;"
	cursor = mysql.connect().cursor()
	cursor.execute(sqlStatement, userId)
	data = cursor.fetchall()
	return data

def getuserpost(userName):
	sqlStatement = "SELECT b.userName, b.avatar, a.postContent, a.inDate , a.postId FROM posts a INNER JOIN users b ON a.userId = b.userId WHERE b.userName = %s ORDER BY a.inDate DESC;"
	cursor = mysql.connect().cursor()
	cursor.execute(sqlStatement, userName)
	data = cursor.fetchall()
	return data

def getonepost(postId):
	sqlStatement = "SELECT b.userName, b.avatar, a.postContent, a.inDate , a.postId FROM posts a INNER JOIN users b ON a.userId = b.userId WHERE a.postId = %s;"
	cursor = mysql.connect().cursor()
	cursor.execute(sqlStatement, postId)
	data = cursor.fetchall()
	return data

def addtestdata(userName):
	for i in range(10):
		content = forgery_py.lorem_ipsum.paragraphs()
		userId = getuserid(userName)
		sqlStatement = "INSERT INTO `posts` (`postContent`, `userId`) VALUES (%s, %s);"
		connection = mysql.connect()
		cursor = connection.cursor()
		cursor.execute(sqlStatement, (content, userId))
		connection.commit()
	return 'ok'

def edituserpost(postId, content):
	sqlStatement = "UPDATE `posts` SET postContent = %s where postId = %s;"
	connection = mysql.connect()
	cursor = connection.cursor()
	cursor.execute(sqlStatement, (content, postId))
	connection.commit()
	return

def getrelations(userName):
	data = []
	userId = getuserid(userName)
	sqlStatement_followers = "SELECT * FROM relations WHERE bloggerId = %s;"
	sqlStatement_following = "SELECT * FROM relations WHERE fansId = %s;"
	cursor = mysql.connect().cursor()
	cursor.execute(sqlStatement_followers, userId)
	followers = cursor.fetchall()
	cursor.execute(sqlStatement_following, userId)
	following = cursor.fetchall()
	return followers, following

def queryiffansexist(bloggerUserName, fansUserName):
	bloggerUserId = getuserid(bloggerUserName)
	fansUserId = getuserid(fansUserName)
	sqlStatement = "SELECT * FROM relations WHERE bloggerId = %s AND fansId = %s;"
	cursor = mysql.connect().cursor()
	cursor.execute(sqlStatement, (bloggerUserId, fansUserId))
	data = cursor.fetchall()
	return data

def delectfans(bloggerUserName, fansUserName):
	if queryiffansexist(bloggerUserName, fansUserName):
		bloggerUserId = getuserid(bloggerUserName)
		fansUserId = getuserid(fansUserName)
		sqlStatement = "DELETE FROM relations WHERE bloggerId = %s AND fansId = %s;"
		connection = mysql.connect()
		cursor = connection.cursor()
		cursor.execute(sqlStatement, (bloggerUserId, fansUserId))
		connection.commit()
		return '成功取消关注'
	else:
		return '已经取消过了'

def addfans(bloggerUserName, fansUserName):
	if queryiffansexist(bloggerUserName, fansUserName):
		return '已经关注过了'
	else:
		bloggerUserId = getuserid(bloggerUserName)
		fansUserId = getuserid(fansUserName)
		sqlStatement = "INSERT INTO `relations` (`bloggerId`, `fansId`) VALUES (%s, %s);"
		connection = mysql.connect()
		cursor = connection.cursor()
		cursor.execute(sqlStatement, (bloggerUserId, fansUserId))
		connection.commit()
		return '成功关注'

def getfanslist(userName):
	bloggerUserId = getuserid(userName)
	sqlStatement = "SELECT a.avatar, a.userId, a.userName FROM users a LEFT JOIN relations b ON a.userId = b.fansId WHERE b.bloggerId = %s AND b.fansId != %s;"
	cursor = mysql.connect().cursor()
	cursor.execute(sqlStatement, (bloggerUserId, bloggerUserId))
	data = cursor.fetchall()
	return data

def getfollowinglist(userName):
	fansUserId = getuserid(userName)
	sqlStatement = "SELECT a.avatar, a.userId, a.userName FROM users a LEFT JOIN relations b ON a.userId = b.bloggerId WHERE b.fansId = %s AND b.bloggerId != %s;"
	cursor = mysql.connect().cursor()
	cursor.execute(sqlStatement, (fansUserId, fansUserId))
	data = cursor.fetchall()
	return data

def addcomment(postId, userName, commentContent):
	userId = getuserid(userName)
	sqlStatement = "INSERT INTO `comments` (`commentContent`, `userId`, `postId`) VALUES (%s, %s, %s);"
	connection = mysql.connect()
	cursor = connection.cursor()
	cursor.execute(sqlStatement, (commentContent, userId, postId))
	connection.commit()
	return '评论成功'

def getcomment(postId):
	sqlStatement = "SELECT b.avatar, b.userName, a.commentContent, a.inDate, a.commentId FROM comments a LEFT JOIN users b ON a.userId = b.userId WHERE postId = %s ORDER BY a.inDate DESC"
	cursor = mysql.connect().cursor()
	cursor.execute(sqlStatement, postId)
	data = cursor.fetchall()
	return data

def delectcomment(commentId):
	sqlStatement = "DELETE FROM comments WHERE commentId = %s;"
	connection = mysql.connect()
	cursor = connection.cursor()
	cursor.execute(sqlStatement, commentId)
	connection.commit()
	return '删除成功'