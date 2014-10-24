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
from backend.models import Shoes_type, Color, Size, Brands        #鞋子类型表

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

@csrf_exempt
def logo(request,template_name):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	premissions = public_premissions(request)    #权限认证
	return render(request,template_name,{
			'premissions':premissions
			}
		)


@csrf_exempt
def logo_add_handle(request):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	if request.method == "POST":
		name = request.POST.get('name','')
		logo = request.FILES.get('logo',None)
		p = Brands(
			name = name,
			logo  = logo,
		)
		p.save()
		return HttpResponseRedirect('/backend/logo/')
	return httpResponse('请求方法错误...')	


@csrf_exempt
def logo_list(request,template_name):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	logoList = Brands.objects.all()
	return render(request,template_name,{'logoList':logoList})

@csrf_exempt
def del_logo(request):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	if request.method == "GET":
		ids = request.GET.get('id','')
		p = Brands.objects.get(id=ids)
		p.delete()
		return HttpResponseRedirect('/backend/logo/')
	return HttpResponse('请求方法错误')


@csrf_exempt
def color(request,template_name):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	premissions = public_premissions(request)    #权限认证
	return render(request,template_name,{
			'premissions':premissions
			}
		)

@csrf_exempt
def color_list(request,template_name):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	colorList = Color.objects.all()
	return render(request,template_name,{'colorList':colorList})

@csrf_exempt
def color_add_handle(request):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	if request.method == "POST":
		name = request.POST.get('name','')
		color = request.POST.get('color','')
		p = Color(
			name = name,
			color  = color,
		)
		p.save()
		return HttpResponseRedirect('/backend/color/')
	return httpResponse('请求方法错误...')	

@csrf_exempt
def del_color(request):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	if request.method == "GET":
		ids = request.GET.get('id','')
		p = Color.objects.get(id=ids)
		p.delete()
		return HttpResponseRedirect('/backend/color/')
	return HttpResponse('请求方法错误')


def size(request,template_name):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	premissions = public_premissions(request)    #权限认证
	return render(request,template_name,{
			'premissions':premissions
			}
		)

@csrf_exempt
def size_list(request,template_name):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	sizeList = Size.objects.all()
	return render(request,template_name,{'sizeList':sizeList})

@csrf_exempt
def size_add_handle(request):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	if request.method == "POST":
		name = request.POST.get('name','')
		p = Size(
			name = name,
		)
		p.save()
		return HttpResponseRedirect('/backend/size/')
	return httpResponse('请求方法错误...')	

@csrf_exempt
def del_size(request):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	if request.method == "GET":
		ids = request.GET.get('id','')
		p = Size.objects.get(id=ids)
		p.delete()
		return HttpResponseRedirect('/backend/size/')
	return HttpResponse('请求方法错误')