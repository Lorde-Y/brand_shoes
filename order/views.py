#coding: utf-8
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.template import Context,Template,RequestContext
from django.shortcuts import render_to_response, RequestContext

from django.shortcuts import render,redirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import settings
import os
import json
import sys
import string
reload(sys) 
sys.setdefaultencoding("utf8")
# #导入数据model
from django.contrib.auth.models import User  #用户表
from backend.models import adminInfo         #继承User表
from backend.models import Shoes_type, Color, Size, Brands, Product        #鞋子类型表

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password, check_password

#导入form表单
from product.form import UEditorForm
#导入分页
from django.core.paginator import Paginator,InvalidPage,EmptyPage
import datetime

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

def order_list(request,template_name):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	# lists = Product.objects.all()
	premissions = public_premissions(request)    #权限认证
	# public_pages = public_page(request,lists,8)  #分页
	return render(request,template_name,{'premissions':premissions})

