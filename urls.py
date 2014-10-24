#coding: utf-8
import settings
from django.conf.urls import patterns, include, url
import os.path

urlpatterns = patterns('',
    url(r'^backend/', include('backend.urls')),		           # 后台
    url(r'^backend/', include('property.urls')),		       # 属性
    url(r'^backend/', include('product.urls')),		       	   # 商品
    url(r'^ueditor/', include('DjangoUeditor.urls' )),                                            # ueditor编辑器
    url(r'^(?P<path>.*)$','django.views.static.serve',{'document_root':settings.PROJECT_PATH}),   #配置media的url
)

# DIRNAME = os.path.dirname(__file__)
# urlpatterns += patterns("",
#     (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(DIRNAME, "media"), 'show_indexes': True }),
# )

# ueditor编辑器显示图片
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT )
