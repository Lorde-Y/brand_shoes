# coding:utf8
from django import forms

#登陆验证
class loginForm(forms.Form):
	username = forms.CharField(max_length=20,required=True,error_messages={'required':u'账号不能为空'})
	password = forms.CharField(max_length=20,required=True,error_messages={'required':u'密码不能为空'})

#添加管理员
class adminForm(forms.Form):
	username = forms.CharField(max_length=20,required=True,error_messages={'required':u'账号不能为空'})
	password = forms.CharField(max_length=20,required=True,error_messages={'required':u'密码不能为空'})
	password2 = forms.CharField(max_length=20,required=True,error_messages={'required':u'两次密码输入不一致'})

#编辑管理员
class edit_user_Form(forms.Form):
	username = forms.CharField(max_length=20,required=True,error_messages={'required':u'账号不能为空'})