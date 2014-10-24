#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
# ---------------------------
# 		品牌类型 : Brands
#           name : 品牌名称
#   	   logo  : 品牌logo 
# ---------------------------
class Brands(models.Model):
	name = models.CharField(max_length=20)
	logo = models.ImageField(upload_to='logo')
	def __unicode__(self):
		return self.name

# ---------------------------
# 	  鞋子类型表 : Shoes_type
#           name : 导航类型名称
#   	    pid  : 存放父导航（外键）
#   	  level  : 导航级数(默认为1,即一级导航)
# ---------------------------
class Shoes_type(models.Model):
	name = models.CharField(max_length=20)
	pid  = models.ForeignKey('self',blank=True,null=True,related_name='child_nav')
	level = models.IntegerField(max_length=1,blank=True,null=True,default=0)
	def __unicode__(self):
		return self.name



# ---------------------------
# 	      商品表 : Product
#           name : 商品名称
#   	   p_id  : 商品的所属父类行
#   	   s_id  : 商品的所属子类型  二级
#   	   t_id  : 商品的所属子类型	 三级
#   	   price : 商品价格
#   	key_words: 商品关键字
#           photo: 封面图片
#     show_photos: 图片轮播切换
#   description  : 商品描述
#   	   is_new: 是否最新
#   	   is_hot: 是否热门
#   	  is_none: 是否下架
#   	  brands : 商品品牌
#   	   color : 商品颜色
#   	   size  : 商品尺寸
# ---------------------------
class Product(models.Model):
	name = models.CharField(max_length=32)
	p_id = models.IntegerField(max_length=11)
	s_id = models.IntegerField(max_length=11)
	t_id = models.IntegerField(max_length=11,blank=True,null=True)
	price = models.DecimalField(max_digits=10,decimal_places=2)
	key_words = models.CharField(max_length=100)
	photo = models.ImageField(upload_to='product')
	show_photos = models.ForeignKey('Photos',blank=True,null=True)
	content = models.TextField()
	is_hot = models.BooleanField(default=False)
	is_new = models.BooleanField(default=False)
	is_none = models.BooleanField(default=False)
	brands = models.CharField(max_length=50)
	color = models.CharField(max_length=50)
	size = models.CharField(max_length=50)
	datetime = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.name

# ---------------------------
# 	  商品图片表 : Photos
#           path : 图片路径
#       goods_id : 商品id
# ---------------------------
class Photos(models.Model):
	goods_id = models.ForeignKey('Product',related_name="photos")
	path = models.CharField(max_length=200)
	def __unicode__(self):
		return self.name

# ---------------------------
# 	      颜色表 : Shoes_color
#           name : 颜色名称
#          color : 颜色RGB
# ---------------------------
class Color(models.Model):
	name = models.CharField(max_length=20)
	color = models.CharField(max_length=20)
	def __unicode__(self):
		return self.name

# ---------------------------
# 	  鞋子尺寸表 : Shoes_size
#           name : 尺寸大小
# ---------------------------
class Size(models.Model):
	name = models.IntegerField(max_length=2)
	def __unicode__(self):
		return self.name


# ---------------------------
# 	      订单表 : Order
#       username : 用户名
#       goods_id : 商品
#         number : 商品数量
#       datetime : 订单时间
#       is_paid  : 是否付款
#       is_cancel: 是否取消。取消就从数据库删除
#     is_delivery: 是否发货。
# ---------------------------
class Order(models.Model):
	user = models.ForeignKey('userInfo', related_name='user_info')
	goods_id = models.ForeignKey('Product')
	number = models.IntegerField(default=1)
	datetime = models.DateTimeField(auto_now_add=True)
	is_paid = models.BooleanField(default=False)
	is_cancel = models.BooleanField(default=False)
	is_delivery = models.BooleanField(default=False)
	def __unicode__(self):
		return self.name

# ---------------------------
# 	  用户信息表 : userInfo(用于其它信息)
#       username : 用户名
#       password : 密码
#          phone : 电话号码
#        address : 联系地址
#         remark : 其它要求
# ---------------------------
class userInfo(models.Model):
	username = models.CharField(max_length=20)
	password = models.CharField(max_length=20)
	phone = models.CharField(max_length=11)
	address = models.CharField(max_length=128)
	remark = models.CharField(max_length=128,blank=True,null=True)
	def __unicode__(self):
		return self.username

# ---------------------------
# 新增用户表字段 : adminInfo  扩展User表字段
#           user : 存放User表字段
#   premissions  : 存放管理员权限
# ---------------------------
class adminInfo(models.Model):
	user = models.OneToOneField(User,related_name='Info')
	premissions = models.CharField(max_length=30,blank=True,null=True)
	def __unicode__(self):
		return self.user.username






