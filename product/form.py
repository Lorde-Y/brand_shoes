# coding:utf8
from django import forms
from DjangoUeditor.forms import UEditorField
	
# ueditor编辑器
class UEditorForm(forms.Form):
	content = UEditorField(u"", 
		initial  = "",
		toolbars = "full", 
		width    = "100%", 
		height   = 350, 
		settings = {"maximumWords" : 10000,
				    "scaleEnabled" : 1,
				    "elementPathEnabled" : 0
				    },
		imagePath= "")