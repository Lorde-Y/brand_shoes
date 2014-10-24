#coding: utf-8
import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('order.views',
	# url(r'^Twolink/$','Twolink',{'template_name':'Twolink.html'}),             #二级、三级导航联动
	# url(r'^product_add/$','product_add',{'template_name':'product_add.html'}),     # 商品添加
	url(r'^order_list/$','order_list',{'template_name':'order_list.html'}),  # 商品列表
	# url(r'^product_add_handle/$','product_add_handle'),                        	   # 商品表单处理
	# url(r'^del_product/$','del_product'),                        		           # 删除商品
	# url(r'^product_edit/$','product_edit',{'template_name':'product_edit.html'}),                        		           # 编辑商品
	# url(r'^product_edit_handle/$','product_edit_handle'),                        	   # 商品表单处理
)