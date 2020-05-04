from django.contrib import admin
from .models import PasswordUser, TextInfo, OldPpInfo, NewPpInfo, CreateInfo, ConfirmInfo, SubmitInfo, LoginInfo, SusResult, Image, ClickPoint, ClickPointFail
# Register your models here.
admin.site.register(PasswordUser)
admin.site.register(TextInfo)
admin.site.register(OldPpInfo)
admin.site.register(NewPpInfo)
admin.site.register(CreateInfo)
admin.site.register(ConfirmInfo)
admin.site.register(SubmitInfo)
admin.site.register(LoginInfo)
admin.site.register(SusResult)
admin.site.register(Image)
admin.site.register(ClickPoint)
admin.site.register(ClickPointFail)