#coding: utf-8

import sys

sys.path.append("..")
reload(sys)
sys.setdefaultencoding("utf-8")

from flask import Flask, render_template, redirect, url_for, session, flash, request, make_response
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_pagedown import PageDown
from datetime import datetime
import sys
from model import *
from forms import *
from paging import *

app = Flask(__name__)

pagedown = PageDown()
pagedown.init_app(app)

app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/page=<page>', methods = ['GET', 'POST'])
def index(page=1):
	form = PostForm()
	if form.validate_on_submit():
		if writepost(session.get('name'), form.content.data):
			#addtestdata(session.get('name'))
			flash('wirte successfully!')
		else:
			flash('wrong')
		return redirect(url_for('index'))
	show_followed = False
	if session.get('name'):
		show_followed = bool(request.cookies.get('show_followed', ''))
	if show_followed:
		posts = getfollowedpost(session.get('name'))
	else:
		posts = getallpost()
	displayRangeList = startend(len(posts), 10)
	if len(posts) != 0:
		pagenum = range(len(displayRangeList))
		start = displayRangeList[int(page)-1][0]
		end = displayRangeList[int(page)-1][1]
		posts = posts[start:end]
	else:
		pagenum = []
		posts = []
	return render_template('index.html',
		form = form,
		name = session.get('name'),
		avatar = session.get('avatar'),
		pagenum = pagenum,
		posts = posts,
		nowpage = int(page),
		show_followed = show_followed)

@app.route('/all')
def show_all():
	resp = make_response(redirect(url_for('index')))
	resp.set_cookie('show_followed', '', max_age = 5*24*60*60)
	return resp

@app.route('/followed')
def show_followed():
	resp = make_response(redirect(url_for('index')))
	resp.set_cookie('show_followed', '1', max_age = 5*24*60*60)
	return resp


@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		if adduser(form.name.data, form.password.data):
			addself = addfans(form.name.data, form.name.data)
			flash('注册成功，请登录')
			return redirect(url_for('login_view'))
		else:
			flash('账号已存在，请换个账号注册吧!')
	return render_template('register.html',
		form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_view():
	form = NameForm()
	if form.validate_on_submit():
		if login(form.name.data, form.password.data):
			session['name'] = form.name.data
			session['password'] = form.password.data
			session['avatar'] = getavatar(session.get('name'))
			flash('Logged in successfully')
			return redirect(url_for('index',
				name = session.get('name'),
				avatar = session.get('avatar')))
		else:
			flash('Username or Password is wrong')
	return render_template('login.html',
		form = form,
		current_time = datetime.utcnow())

@app.route('/logout')
def logout_view():
	session['name'] = ''
	session['password'] = ''
	flash('You have been logged out.')
	return redirect(url_for('login_view'))

@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		session['old_password'] = form.old_password.data
		session['password'] = form.password.data
		if login(session.get('name'), session.get('old_password')):
			updatepassword(session.get('name'), session.get('password'))
			flash('Your password has been updated.please login again')
			session['name'] = ''
			session['password'] = ''
			return redirect(url_for('login_view'))
		else:
			flash('faild')
	return render_template('changepassword.html',
		form = form,
		name = session.get('name'),
		avatar = session.get('avatar'))

@app.route('/user/<username>')
@app.route('/user/<username>/page=<page>')
def user(username, page=1):
	userName, inDate, location, aboutMe, lastSeen, avatar = getuserprofile(username)
	session['location'] = location
	session['aboutMe'] = aboutMe
	followers, following = getrelations(username)
	fansNameList = []
	for eachitem in followers:
		eachName = getusername(eachitem[2])
		fansNameList.append(eachName)
	if inDate is None:
		abort(404)
	posts = getuserpost(userName)
	displayRangeList = startend(len(posts), 10)
	if len(posts) != 0:
		pagenum = range(len(displayRangeList))
		start = displayRangeList[int(page)-1][0]
		end = displayRangeList[int(page)-1][1]
		posts = posts[start:end]
	else:
		pagenum = []
		posts = []
	return render_template('user.html',
		username = userName,
		location = location,
		aboutMe = aboutMe,
		inDate = inDate,
		lastSeen = lastSeen,
		thisavatar = avatar,
		name = session.get('name'),
		avatar = session.get('avatar'),
		pagenum = pagenum,
		nowpage = int(page),
		followers = len(followers),
		following = len(following),
		fansNameList = fansNameList,
		posts = posts
		)

@app.route('/editprofile', methods = ['GET', 'POST'])
def editprofile():
	form = EditProfileForm()
	if form.validate_on_submit():
		userName = form.name.data
		location = form.location.data
		aboutMe = form.aboutMe.data
		oldUserName = session.get('name')
		edituserprofile(userName, location, aboutMe, oldUserName)
		session['name'] = userName
		flash('modify successfully!')
		return redirect(url_for('user',
			username = session.get('name')))
	form.name.data = session.get('name')
	form.location.data = session.get('location')
	form.aboutMe.data = session.get('aboutMe')
	return render_template('editprofile.html',
		form = form,
		name = session.get('name'),
		avatar = session.get('avatar'))

@app.route('/post/<int:postId>', methods = ['GET', 'POST'])
@app.route('/post/<int:postId>/page=<page>', methods = ['GET', 'POST'])
def post(postId, page = 1):
	posts = getonepost(postId)
	username = posts[0][0]
	form = CommentForm()
	if form.validate_on_submit():
		addcommentresp = addcomment(postId, session.get('name'), form.body.data)
		flash(addcommentresp)
		return redirect(url_for('post', postId = postId))
	comments = getcomment(postId)
	displayRangeList = startend(len(comments), 10)
	if len(comments) != 0:
		pagenum = range(len(displayRangeList))
		start = displayRangeList[int(page)-1][0]
		end = displayRangeList[int(page)-1][1]
		comments = comments[start:end]
	else:
		pagenum = []
		comments = []
	return render_template('post.html',
		posts = posts,
		name = session.get('name'),
		username = username,
		avatar = session.get('avatar'),
		form = form,
		pagenum = pagenum,
		nowpage = int(page),
		postId = postId,
		comments = comments)

@app.route('/delectonecomment/<commentId>', methods = ['GET'])
def delectonecomment(commentId):
	response = delectcomment(commentId)
	return response

@app.route('/editpost/<int:postId>', methods = ['GET', 'POST'])
def editpost(postId):
	form = PostForm()
	if form.validate_on_submit():
		edituserpost(postId, form.content.data)
		flash('wirte successfully!')
		return redirect(url_for('post', postId = postId))
	posts = getonepost(postId)
	form.content.data = posts[0][2]
	return render_template('editpost.html',
		form = form,
		name = session.get('name'),
		avatar = session.get('avatar'))

@app.route('/unfollow/<bloggerUserName>/<fansUserName>', methods = ['GET'])
def unfollow(bloggerUserName, fansUserName):
	response = delectfans(bloggerUserName, fansUserName)
	return response

@app.route('/follow/<bloggerUserName>/<fansUserName>', methods = ['GET'])
def follow(bloggerUserName, fansUserName):
	response = addfans(bloggerUserName, fansUserName)
	return response

@app.route('/fanslist/<username>', methods = ['GET'])
def fanslist(username):
	userList = getfanslist(username)
	return render_template('userlist.html',
		username = username,
		userList = userList,
		name = session.get('name'),
		avatar = session.get('avatar'),
		isfans = 1)

@app.route('/followinglist/<username>', methods = ['GET'])
def followinglist(username):
	userList = getfollowinglist(username)
	return render_template('userlist.html',
		username = username,
		userList = userList,
		name = session.get('name'),
		avatar = session.get('avatar'),
		isfans = 0)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def interal_server_error(e):
	return interal_server_error('505.html'), 500

if __name__ == '__main__':
	app.run(debug = True)