#coding: utf-8
import settings
from django.conf.urls import patterns, include, url

urlpatterns = patterns('backend.views',
	url(r'^login/$','login_in',{'template_name':'login.html'}),            # 登陆界面
	url(r'^check_login/$','check_login',{'template_name':'login.html'}),   # 登陆检查
	url(r'^login_out/$','login_out'),                                      # 登出
	url(r'^$', 'index',{"template_name":"home.html"}),		             # 后台

)

urlpatterns += patterns('backend.views',
	url(r'^navigation_list/$', 'navigation_list',{'template_name':'navigation_list.html'}),  # 导航列表 
	url(r'^navigation_add/$', 'navigation_add',{'template_name':'navigation_add.html'}),     # 导航添加
	url(r'^navigation_add_handle/$','navigation_add_handle'),                                # 导航添加表单处理
	url(r'^del_navigation/$','del_navigation'),                                              # 导航删除处理
	# url(r'^Twolink/$','Twolink',{'template_name':'Twolink.html'}),                           # 二级、三级导航联动
	# url(r'^Twolink2/$','Twolink2',{'template_name':'Twolink2.html'}),                           # 二级、三级导航联动
	url(r'^navigation_edit/$', 'navigation_edit', {'template_name':'navigation_edit.html'}), # 导航修改
	url(r'^navigation_edit_handle/$', 'navigation_edit_handle'),                             # 导航修改表单处理
)

urlpatterns += patterns('backend.views',
	url(r'^user_add_handle','user_add_handle',{'template_name' : "admin_add.html"}),          # 添加管理员表单处理 避免 admin_add_handle
	url(r'^admin_list/$','admin_list',{'template_name' : "admin_list.html"}),                 # 管理员列表 
	url(r'^admin_add/$' , 'admin_add',{'template_name':'admin_add.html'}),                    # 添加管理员
	url(r'^admin_delete/$', 'admin_delete'),			                                      # 删除管理员
	url(r'^admin_edit/$', 'admin_edit', {'template_name' : "admin_edit.html"}),	              # 管理员编辑
	url(r'^admin_edit_handle/$', 'admin_edit_handle'),                                        # 修改管理员表单处理
	url(r'^admin_changePwd/$', 'admin_changePwd', {'template_name':"admin_changePwd.html"}),  # 更改密码
	url(r'^admin_changePwd_handle$', 'admin_changePwd_handle'),                               # 更改密码表单处理
)