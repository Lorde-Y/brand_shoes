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
from datetime import *

#---------------------------------------------------
#      名字 ： 分页公共函数
#      功能 :  实现分页
#      人员 ： 杨凯
#      日期 ： 2014.08.27
#  all_list :  传递需要分页的 数据
#       num :  传递每页显示的
#---------------------------------------------------
def public_page(request,all_list,num):
    #确保传进来的page参数为整数，如果不是，则设置为1
    try:
        page = int(request.GET.get('page','1'))
        # page =1
    except ValueError:
        page = 1
        currentpage = 1
    #分页实现
    #实例化中文分页器
    paginator = Paginator(all_list,num)
    
    #中文页码列表初始化
    if(paginator.num_pages>10):
        page_list = range(0,10)
    else:
        page_list = range(0,paginator.num_pages)
    
    #判断最大页数是否超过最大显示页数
    #判断最大显示页数是否超过实际页码范围
    if(paginator.num_pages > 10 and paginator.num_pages -page > 9):
        # page_list[0] = 1
        # page_list[1] = 2
        # page_list[2] = 3
        for x in range(0,3):
            page_list[x] = x + 1
        for x in range(3,8):
            # if(paginator.num_pages - page <= 9 ):
            #     page_list[x] = x + 9
            if page < 3:
                if page == 1:
                    page_list[x] = page + x
                else:
                    page_list[x] = page + x - 1
            else:
                page_list[x] = x + page - 2
        page_list[7] = '...'
        for x in range(8,10):
            page_list[x] = paginator.num_pages - 9 + x
    
    #如果最大页数超过最大显示页数，并且是最后几页，则只显示最后几页
    elif(paginator.num_pages > 10 and paginator.num_pages -page <= 9):
        for x in range(0,10):
            page_list[x] = paginator.num_pages - 9 + x
    
    #如果最大页码数不超过显示页码数，则将全部页数在前台输出
    else:     
        for x in range(0,paginator.num_pages):
            page_list[x] = x+1
  
    #确保传进来的当前page为整数，如果不是，则设置为1
    try:
        currentpage = int(request.GET.get('currentpage','1'))
    except ValueError:
        currentpage = 1
    
    #确保页面没有超出范围，否则输出最后一页的值
    try:
        info_list = paginator.page(page)
        currentpage = page
        # return HttpResponse(currentpage)
    except ValueError (EmptyPage, InvalidPage):
        info_list = paginator.page(paginator.num_pages)
        currentpagepage =paginator.num_pages
    
    #获取上一页和下一页的值
    prevpage = currentpage - 1
    nextpage = currentpage + 1

    #确保上一页没有超出页面范围，否则分别赋值为1和最大页码数
    if(prevpage < 1):
        prevpage = 1
    if(nextpage > paginator.num_pages):
        nextpage = paginator.num_pages
    pages = {}
    pages['info_list'] = info_list
    pages['page']      = page
    pages['currentpage'] = currentpage
    pages['prevpage'] = prevpage
    pages['nextpage'] = nextpage
    pages['page_list'] = page_list
    return pages

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
# 	名字：导航联动
#   功能：根据父导航实现 实现二级、三级导航的 联动效果
#   人员：杨凯
#   日期：2014.10.19
# --------------------------------------
@csrf_exempt
def Twolink(request,template_name):
	if request.is_ajax():
		nav_id = int(request.POST.get('id',''))
		product_nav = Shoes_type.objects.filter(level=1)  
		if nav_id <= 3:          #一级导航id <= 3
			p_id = nav_id        #父导航 id
			s_id = ''  		     #二级导航 id
			product_nav1 = Shoes_type.objects.filter(id=nav_id)   #获取当前导航  
			try:
				product_second_nav = Shoes_type.objects.filter(pid=product_nav1[0])
			except Exception:
				product_second_nav = None
			try:
				product_third_nav = Shoes_type.objects.filter(pid=product_second_nav[0])
			except Exception:
				product_third_nav = None
		else:					 #二级导航以上id >3
			pid = int(request.POST.get('pid',''))                   
			#product_nav = nav.objects.filter(id=p_id)
			p_id = pid     #父导航   id
			# print '*'*20
			s_id = nav_id  #二级导航 id
			try:
				product_second_nav = Shoes_type.objects.filter(pid=p_id)     #获取所有二级导航
				product_second_nav1 = Shoes_type.objects.filter(id=nav_id)   #获取当前导航 
				product_third_nav = Shoes_type.objects.filter(pid=nav_id)
			except Exception:
				product_third_nav = None
		# print p_id
		# print s_id
		return render(request,template_name,{
				'product_nav':product_nav,
				'Pid':p_id,
				'Sid':s_id,
				'product_second_nav':product_second_nav,
				'product_third_nav':product_third_nav,
			}
			)
	return HttpResponse('请求方法错误...')

# ======================================
# 	名字：商品添加
#   功能：显示商品添加页面
#   人员：杨凯
#   日期：2014.10.19
# --------------------------------------
def product_add(request,template_name):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	# ueditor编辑器初始化
	form = UEditorForm()
	#获取 商品 一级导航
	product_nav = Shoes_type.objects.filter(level=1)
	#获取 所有二级导航
	try:
		product_second_nav = Shoes_type.objects.filter(pid = product_nav[0])
	except Exception:
		product_second_nav = None
	#获取属于当前二级导航的 三级导航
	try:
		product_third_nav = Shoes_type.objects.filter(pid = product_second_nav[0])
	except Exception:
		product_third_nav = None 
	brands = Brands.objects.all()
	color = Color.objects.all()
	size = Size.objects.all()
	premissions = public_premissions(request)    #权限认证
	return render(request,template_name,{"form": form,
			'brands':brands,
			'size':size,
			'color':color,
			'premissions':premissions,
			"product_nav":product_nav,
			"product_second_nav":product_second_nav,
			"product_third_nav":product_third_nav,
			}
		)

# ======================================
# 	名字：商品添加表单处理
#   功能：商品添加表单处理
#   人员：杨凯
#   日期：2014.10.21
# --------------------------------------
@csrf_exempt
def product_add_handle(request):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	if request.method == "POST":
		p_id  = request.POST.get('p_id','')
		s_id  = request.POST.get('s_id','')
		t_id  = request.POST.get('t_id','0')
		name  = request.POST.get('name','')
		photo = request.FILES.get('photo',None)
		price = request.POST.get('price','')
		key_words = request.POST.get('key_words', '')
		is_hot = request.POST.get('is_hot','')
		is_new = request.POST.get('is_new','')
		brands = request.POST.get('brands','')
		color  = request.POST.getlist('color','')
		size   = request.POST.getlist('size','')
		content = request.POST.get('content','')
		if not is_hot:
			is_hot = False
		if not is_new:
			is_new = False
		is_size = ''
		#是否选择尺寸  有		
		if size:
			for i in size:
				is_size += i + ','    #以 ',' 分割,组合成字符串
		is_color = ''
		#是否选择颜色  有		
		if color:
			for i in color:
				is_color += i + ','    #以 ',' 分割,组合成字符串
		p = Product(
			p_id = p_id,
			s_id = s_id,
			t_id = t_id,
			name = name,
			photo = photo,
			price = price,
			key_words = key_words,
			is_hot = is_hot,
			is_new = is_new,
			brands = brands,
			color  = is_color,
			size   = is_size,
			content = content,
			)
		p.save()
		return HttpResponseRedirect('/backend/product_add/')
	return HttpResponse('请求方法错误...')

# ======================================
# 	名字：商品列表
#   功能：分页罗列商品
#   人员：杨凯
#   日期：2014.10.21
# --------------------------------------
def product_list(request,template_name):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	lists = Product.objects.all()
	premissions = public_premissions(request)    #权限认证
	public_pages = public_page(request,lists,8)  #分页
	return render(request,template_name,{'public_pages':public_pages,'premissions':premissions})

# ======================================
# 	名字：删除商品
#   功能：从数据库中将商品(包括图片处理)删除,
#   人员：杨凯
#   日期：2014.10.21
# --------------------------------------
def del_product(request):
	if not request.user.is_authenticated():
		return redirect('/backend/login/')
	if request.method == "GET":
		Id = request.GET.get('id','')
		delProduct = Product.objects.get(id=Id)
		# if delProduct.photo:       # 信息 中有 图片
		# 	print '*'*100
		# 	aa = settings.PROJECT_PATH.replace('\\','/')
		# 	print aa
		# 	file_directory = delProduct.photo;
		# 	file_directory = aa + file_directory;
		# 	print file_directory
		# 	if os.path.exists(file_directory):
		# 		os.remove(file_directory)
		# 		delProduct.delete()
		# 		return HttpResponseRedirect('/backend/product_list/')
		# else:
		delProduct.delete()
		return HttpResponseRedirect('/backend/product_list/')
	return HttpResponse('请求方法错误...')


# ======================================
# 	名字：资讯修改页面
#   功能：修改页面显示资讯
#   人员：黄晓佳
#   日期：2014.08.25
# --------------------------------------
def product_edit(request, template_name):
	if request.method == "GET":
		ids = request.GET.get('id','')
	new = Product.objects.get(id = ids)
	p_id = new.p_id
	s_id = new.s_id
	t_id = new.t_id

	p_id_name = Shoes_type.objects.get(id = p_id).name
	s_id_name = Shoes_type.objects.get(id = s_id).name
	# t_id_name = Shoes_type.objects.get(id = t_id).name
	
	premissions = public_premissions(request)
	brands = Brands.objects.all()
	color = Color.objects.all()
	size = Size.objects.all()
	# ueditor编辑器初始化
	form = UEditorForm()

	param = {
		'new':new, 
		'form':form,
		'brands':brands,
		'color':color,
		'size':size,
		'p_id_name':p_id_name,
		's_id_name':s_id_name,
		# 't_id_name':t_id_name,
		'premissions':premissions,
	}

	if t_id != 0:
		t_id_name = Shoes_type.objects.get(id = t_id).name
		param['t_id_name'] = t_id_name

	return render(request, template_name, param)


# ======================================
# 	名字：资讯修改表单处理
#   功能：修改表单
#   人员：黄晓佳
#   日期：2014.08.25
# --------------------------------------
@csrf_exempt
def product_edit_handle(request):
	if request.method == "POST":
		ids = request.POST.get('id','')
		print '*'*100
		print ids
		p_id  = request.POST.get('p_id','')
		s_id  = request.POST.get('s_id','')
		t_id  = request.POST.get('t_id','0')
		name  = request.POST.get('name','')
		photo = request.FILES.get('photo',None)
		hiddenImg = request.POST.get('hiddenImg','')
		price = request.POST.get('price','')
		key_words = request.POST.get('key_words', '')
		is_hot = request.POST.get('is_hot','')
		is_new = request.POST.get('is_new','')
		is_none = request.POST.get('is_none','')
		brands = request.POST.get('brands','')
		color  = request.POST.getlist('color','')
		size   = request.POST.getlist('size','')
		content = request.POST.get('content','')
		if not is_hot:
			is_hot = False
		if not is_new:
			is_new = False
		is_size = ''
		#是否选择尺寸  有		
		if size:
			for i in size:
				is_size += i + ','    #以 ',' 分割,组合成字符串
		is_color = ''
		#是否选择颜色  有		
		if color:
			for i in color:
				is_color += i + ','    #以 ',' 分割,组合成字符串

		# 如果没有上传图片
		if not photo:
			photo = hiddenImg

		# 保存修改
		p = Product.objects.get(id = ids)
		p.p_id = p_id,
		p.s_id = s_id,
		p.t_id = t_id,
		p.name = name,
		p.photo = photo,
		p.price = price,
		p.key_words = key_words,
		p.is_hot = is_hot,
		p.is_new = is_new,
		p.is_none = is_none,
		p.brands = brands,
		p.color  = is_color,
		p.size   = is_size,
		p.content = content,
		p.save()

		return render(request, "backend_href.html", {'title':"修改成功 :)", 'href':'product'})
	else:
		return render(request, "backend_href.html", {'title':"修改失败，请重试 :(", 'href':'product'})