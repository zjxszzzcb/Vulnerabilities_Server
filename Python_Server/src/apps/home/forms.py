from django import forms
 
# 更新用户信息form
class UpUserForm(forms.Form):
    ID = forms.IntegerField(label='id')
    Username = forms.CharField(label='username')
    Sex = forms.CharField(label='sex')
    Avatar = forms.CharField(label='avatar')

# 文件上传表单
class UpFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()