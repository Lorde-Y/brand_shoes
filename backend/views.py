#coding: utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.template import Context,Template,RequestContext
from django.shortcuts import render_to_response, RequestContext

from django.shortcuts import render,redirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import settings
import json
# #导入数据model
from django.contrib.auth.models import User  #用户表
from backend.models import adminInfo         #继承User表
from backend.models import Shoes_type        #鞋子类型表

#导入form表单
from backend.form import loginForm,adminForm

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password, check_password

# #导入分页
# from django.core.paginator import Paginator,InvalidPage,EmptyPage
# from datetime import *

# ======================================
# 	名字：判断权限公共函数
#   功能：根据权限显示左侧栏目
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
def public_premissions(request):
	username = request.user                       # 获取 当前 登陆的 管理员名称
	user = User.objects.get(username=username)    # User表中找到 当前管理员
	Info = adminInfo.objects.get(user=user)        # 查询adminInfo
	premissions = Info.premissions
	if premissions:
		list_premissions = premissions.split(',')
		length = len(list_premissions)    
		del(list_premissions[length-1])           #移除最后一个 ',' 元素
	return list_premissions

# ======================================
# 	名字：后台首页
#   功能：展示后台首页
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
def index(request,template_name):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	username = request.user                       # 获取 当前 登陆的 管理员名称
	user = User.objects.get(username=username)    # User表中找到 当前管理员
	Info = adminInfo.objects.get(user=user)         # 查询userInfo
	premissions = Info.premissions
	if premissions:
		list_premissions = premissions.split(',')
		length = len(list_premissions)    
		del(list_premissions[length-1])               #移除最后一个 ',' 元素
		# print list_premissions
		# data = []
		# for lists in list_premissions:
		# 	print '*'*20
		# 	print lists
		# # print '*'*20
		# # print list_premissions[0]
	return render(request,template_name,{'premissions':list_premissions})
	
# ======================================
# 	名字：登陆界面
#   功能：管理员登陆
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
def login_in(request,template_name):
	return render(request,template_name)

# ======================================
# 	名字：登出
#   功能：管理员登出
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
@csrf_exempt
def login_out(request):
	logout(request)
	return HttpResponseRedirect('/backend/login/')

# ======================================
# 	名字：登陆验证
#   功能：管理员登陆
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
@csrf_exempt
def check_login(request,template_name):
	if request.method == "POST":
		form = loginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username,password=password)
			if user is not None:
				login(request,user)
				return HttpResponseRedirect('/backend/')
			else:
				form.errors['username'] = u'用户名或密码错误'
				return render(request,template_name,{'form':form})
		else:
			return render(request,template_name,{'form':form})			
	else:
		form = loginForm()
		return render(request,template_name,{'form': form})

# ======================================
# 	名字：导航列表
#   功能：罗列导航信息
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
def navigation_list(request,template_name):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	navlist = Shoes_type.objects.filter(level=1)
	premissions = public_premissions(request)    #权限认证
	return render(request,template_name,{
			'navlist':navlist,
			'premissions':premissions
			}
		)

# ======================================
# 	名字：导航添加
#   功能：添加子导航(二级、三级导航)
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
@csrf_exempt
def navigation_add(request,template_name):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	if request.method == "GET":
		navId = request.GET.get('id','')
		premissions = public_premissions(request)   #权限认证
		return render(request,template_name,{'id':navId,'premissions':premissions})
	return HttpResponse('请求方法错误...')

# ======================================
# 	名字：导航添加表单处理
#   功能：添加子导航(二级、三级导航)
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
@csrf_exempt
def navigation_add_handle(request):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	if request.method =="POST":
		navId = request.POST.get('id','')
		nav_name = request.POST.get('name','')
		p_nav = Shoes_type.objects.get(id=navId)   #找到父ID
		p = Shoes_type(
			name = nav_name,
			pid  = p_nav,
		)
		p.save()
		return HttpResponseRedirect('/backend/navigation_list/')
	return httpResponse('请求方法错误...')

# ======================================
# 	名字：导航修改页面
#   功能：导航显示
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
@csrf_exempt
def navigation_edit(request, template_name):
	if request.method == "GET":
		ids = request.GET['id']
		navs = Shoes_type.objects.get(id = ids)
		premissions = public_premissions(request)
		return render(request, template_name, {'nav': navs,'premissions':premissions})

# ======================================
# 	名字：导航修改表单处理
#   功能：导航修改
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
@csrf_exempt
def navigation_edit_handle(request):
	if request.method == "POST":
		ids = request.POST['id']
		name = request.POST['name']
		navs = Shoes_type.objects.get(id = ids)
		navs.name = name
		navs.save()
		return render(request, "backend_href.html", {'title':'修改成功 :)', 'href':'navigation'})
	else:
		return render(request, "backend_href.html", {'title':'修改失败，请重试 :(', 'href':'navigation'})

# ======================================
# 	名字：导航删除
#   功能：从数据库中将导航删除
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
def del_navigation(request):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	if request.method == "GET":
		navId = request.GET.get('id','')
		try:
			# 若删除的导航时父级导航 就要把他的子导航全部删除
			p = Shoes_type.objects.filter(pid=navId)     
		except Exception:
			p = None
		if p:
			for lists in p:
				delNav = Shoes_type.objects.get(id=lists.id)
				delNav.delete()
		delNav = Shoes_type.objects.get(id=navId)
		delNav.delete()
		return HttpResponseRedirect('/backend/navigation_list/')
	return httpResponse('请求方法错误...')

# ======================================
# 	名字：管理员列表
#   功能：超级管理员查看操作普通管理员
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
def admin_list(request,template_name):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	adminlist = User.objects.all()
	premissions = public_premissions(request)
	return render(request,template_name,{'adminlist':adminlist,'premissions':premissions})

# ======================================
# 	名字：添加管理员
#   功能：超级管理员添加普通管理员
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
def admin_add(request,template_name):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	premissions = public_premissions(request)   #权限认证
	return render(request,template_name,{'premissions':premissions})

# ======================================
# 	名字：添加管理员以及权限表单处理
#   功能：超级管理员添加普通管理员以及添加权限
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
@csrf_exempt
def user_add_handle(request,template_name):
	print '*'*100
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	if request.method == "POST":
		premissions = request.POST.getlist('premissions','')
		is_premissions = ''
		#是否有权限  有		
		if premissions:
			for i in premissions:
				is_premissions += i + ','    #以 ',' 分割,组合成字符串

		form = adminForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			password2 = form.cleaned_data['password2']			
			# list1 = premissions[0]
			# print premissions
			checkUser = User.objects.filter(username=username)
			pwdMatch = password == password2
			if checkUser:
				form.errors['username'] = u'管理员已存在'
				return render(request,template_name,{'form':form})
			if not pwdMatch:
				form.errors['password'] = u'两次密码输入不一致'
				return render(request,template_name,{'form':form})
			new_user = User.objects.create_user(
						username = username,
						password = password,
					)
			UInfo = adminInfo.objects.create(
						user = new_user,
						premissions = is_premissions,
				)

			return HttpResponseRedirect('/backend/admin_list/')
		else:
			return render(request,template_name,{'form':form})
	else:
		form = adminForm()
		return render(request,template_name,{'form': form})

# ======================================
# 	名字：管理员修改跳转
#   功能：修改跳转页面
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
@csrf_exempt
def admin_edit(request, template_name):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')

	if request.method == "GET":							   		# 确保是get提交
		ids = request.GET.get('id','')	                   		# 要修改的管理员id
		info = User.objects.get(id=ids)					   		    # 获取管理员信息
		premissions = public_premissions(request)
		return render(request, template_name, {'info' : info,'premissions':premissions}) # 跳转到修改页面
	return HttpResponse('请求方法错误...')

# ======================================
# 	名字：管理员修改表单处理
#   功能：修改管理员
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
@csrf_exempt
def admin_edit_handle(request):
	if request.method == "POST":
		# 获取表单
		ids = request.POST.get('id', '')
		username = request.POST['username']
		premissions = request.POST.getlist('premissions','')
		is_premissions = ''
		# 以 ',' 分割,组合成字符串
		if premissions:
			for i in premissions:
				is_premissions += i + ','   	

		# 修改基本资料
		user1 = User.objects.get(id = ids)
		user1.username = username
		user1.save()

		# 修改权限
		usrInfo1 = adminInfo.objects.get(user = user1)
		usrInfo1.premissions = is_premissions
		usrInfo1.save()

		return render(request, "backend_href.html", {'title':"修改成功 :)", 'href':"admin"})
	else:
		return render(request, "backend_href.html", {'title':"修改失败，请重试 :(", 'href':"admin"})

# ======================================
# 	名字：管理员修改密码
#   功能：修改密码页面显示
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
def admin_changePwd(request, template_name):
	premissions = public_premissions(request)
	return render(request, template_name, {'premissions':premissions})

# ======================================
# 	名字：管理员修改密码表单处理
#   功能：修改密码
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
@csrf_exempt
def admin_changePwd_handle(request):
	if request.method == "POST":
		oldPwd = request.POST['oldPwd']            # 旧密码
		newPwd = request.POST['newPwd']            # 新密码

		# 旧密码如果一致，则修改密码
		if check_password(oldPwd, request.user.password): 
			users = User.objects.get(username = request.user.username)
			users.password = make_password(newPwd, None, 'pbkdf2_sha256')
			users.save()
			return render(request, "backend_href.html", {'title':"修改密码成功 :)", 'href':"index"})
		else:
			return render(request, "backend_href.html", {'title':"旧密码输入不一致 :(", 'href':"index"})

	return render(request, "backend_href.html", {'title':"请求失误 :(", 'href':"home"})

# ======================================
# 	名字：管理员删除用户
#   功能：删除普通管理员
#   人员：杨凯
#   日期：2014.10.18
# --------------------------------------
@csrf_exempt
def admin_delete(request):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')

	if request.method == "POST":                                        # 确保表单提交是post
		ids = request.POST.get('id_attr', '')                           # 要删除的管理员id
		password = request.POST.get('delete_attr', '')                  # 确认密码

	userInfos = User.objects.get(is_superuser=1)                         # 获取超级管理员
	userPassword = userInfos.password                                    # 获取超级管理员密码

	if check_password(password, userPassword):                        
		deleteUser = User.objects.get(id = ids)            		        # 获取要删除的用户
		deletePremissions = adminInfo.objects.get(user=deleteUser)       # 删除Info表中的权限	
		deletePremissions.delete()                                      # 删除权限
		deleteUser.delete()                                		        # 删除用户

		return render(request, "backend_href.html", {'title':"用户删除成功 :)", 'href':"admin"})  # 删除成功跳转
	else:                                                             
		return render(request, "backend_href.html", {'title':"密码错误，删除失败 :(", 'href':"admin"})  # 删除失败跳转
