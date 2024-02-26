from django.contrib import admin
from testapp.models import Signed,Home,Meeting,MeetingInner,Contact,Contract,ContractInner,Count
# Register your models here.
class HomeAdmin(admin.ModelAdmin):
    list_display = ('id','cNumber','cType','cDepartment','cAuther','cProgress','cEndDate','HomeDate')
    # list_fulter = ('cName','cSex')
    search_fields = ('cType','cAuther','cDate',)
    ordering=('id',)
class SignedAdmin(admin.ModelAdmin):
    list_display = ('id','cNumber','cJob_title','cDiscription')
    # list_fulter = ('cName','cSex')
    search_fields = ('cType','cAuther','cDate',)
    ordering=('id',)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ('id','cNumber','cMeetingType','cLeader','cRecoder','cTopic')
    # list_fulter = ('cName','cSex')
    search_fields = ('cType','cRecoder','cDate',)
    ordering=('id',)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id','cNumber','cSubject','cDecisionDep','cImplementDep')
    # list_fulter = ('cName','cSex')
    search_fields = ('cType','cAuther','cDate',)
    ordering=('id',)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id','cNumber','cClient','cConfirm','cLocation','cBudget')
    # list_fulter = ('cName','cSex')
    search_fields = ('cType','cAuther','cDate',)
    ordering=('id',)
class CountAdmin(admin.ModelAdmin):
    list_display = ('id','count')
    search_fields = ('id','count')
    ordering=('id',)
admin.site.register(Signed,SignedAdmin)
admin.site.register(Meeting,MeetingAdmin)
admin.site.register(Home,HomeAdmin)
admin.site.register(MeetingInner)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Contract)
admin.site.register(ContractInner)
admin.site.register(Count,CountAdmin)