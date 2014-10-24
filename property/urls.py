#coding: utf-8
import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('property.views',
	url(r'^logo/$','logo',{'template_name':'logo.html'}),              		     # 属性--品牌
	url(r'^logo_add_handle/$','logo_add_handle'),              		             # 属性--添加品牌
	url(r'^logo_list/$','logo_list',{'template_name':'logo_list.html'}),         # 属性--添加颜色
	url(r'^del_logo/$','del_logo'),                        		                 # 属性--删除尺寸
	url(r'^color/$','color',{'template_name':'color.html'}),              		 # 属性--颜色
	url(r'^color_list/$','color_list',{'template_name':'color_list.html'}),      # 属性--添加颜色
	url(r'^color_add_handle/$','color_add_handle'),                        		 # 属性--添加颜色
	url(r'^del_color/$','del_color'),                        		             # 属性--删除颜色
	url(r'^size/$','size',{'template_name':'size.html'}),   			   		 # 属性--大小
	url(r'^size_list/$','size_list',{'template_name':'size_list.html'}),      	 # 属性--添加尺寸
	url(r'^size_add_handle/$','size_add_handle'),                        		 # 属性--添加尺寸
	url(r'^del_size/$','del_size'),                        		                 # 属性--删除尺寸
)