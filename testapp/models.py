from django.db import models
from django.utils import timezone
# Create your models here.
#7

class User(models.Model):
    name = models.CharField(max_length=20, default='', null=False)
    username = models.CharField(max_length=20, default='', null=False)
    password = models.CharField(max_length=20, default='', null=False)
    title = models.CharField(max_length=20, default='', null=False) #職稱
    ispro = models.CharField(max_length=20, default='', null=False) #是否是主管職
    Position = models.CharField(max_length=20, default='', null=False) #職位

    class Meta:
        db_table = "User"

class Home(models.Model):
    TYPE = (
        ("簽呈", "簽呈"),
        ("會議記錄表", "會議記錄表"),
        ("內部連絡單", "內部連絡單"),
        ("發包議價表", "發包議價表"),
        ("設計變更通知單", "設計變更通知單")
    )
    DEP = (
        ("總經理室", "總經理室"),
        ("副總經理室", "副總經理室"),
        ("海外事業部", "海外事業部"),
        ("協理室", "協理室"),
        ("文管中心", "文管中心"),
        ("管理部", "管理部"),
        ("業務設計部", "業務設計部"),
        ("廠務部", "廠務部"),
        ("品管課", "品管課"),
        ("設計生技課", "設計生技課"),
        ("業務課", "業務課"),
        ("工程課", "工程課"),
        ("生管課", "生管課"),
        ("採購課", "採購課"),
        ("製造課", "製造課"),
        ("財會課", "財會課"),
        ("人資總務課", "人資總務課"),
    )
    PRO = (
        ("草稿", "草稿"),
        ("流程中", "流程中"),
        ("結案", "結案"),
        ("駁回", "駁回"),
    )
    cNumber = models.CharField(max_length=50, default='', null=False)
    cAuther = models.CharField(max_length=20)#姓名
    cDepartment = models.CharField(max_length=50, choices=DEP)#單位
    cType = models.CharField(max_length=10,default=" ",null=False, choices=TYPE)
    cProgress = models.CharField(max_length=20,default='草稿', choices=PRO)
    cEndDate = models.DateField(blank=True, null=True)
    cReceive  = models.CharField(max_length=20,blank=True,null=True)
    cFile = models.FileField(blank=True, null=True)
    cFile1 = models.FileField(blank=True, null=True)
    cFile2 = models.FileField(blank=True, null=True)
    cFile3 = models.FileField(blank=True, null=True)
    cFile4 = models.FileField(blank=True, null=True)
    cTime = models.DateTimeField(auto_now_add=True)
    cCount = models.IntegerField(default=-1,blank=True)
    cSubject = models.CharField(max_length=255, default='', null=False)#主旨
    cSecret = models.CharField(max_length=10, default='', null=True)
    HomeDate = models.DateField(null=False,default=timezone.now)#日期

    class Meta:
        db_table = "Home"

class Returned(models.Model):
    cNumber = models.CharField(max_length=50, default='',blank=True)
    cName = models.CharField(max_length=20, blank=True)# 誰駁回的(姓名)
    cHow = models.CharField(max_length=20, blank=True)# 同意/駁回
    cIllustrate = models.TextField(blank=True)
    cTransfer = models.CharField(max_length=20, blank=True)# 被駁回的(姓名)
    cReturnedTime = models.DateTimeField(auto_now=True)
    returnTo = models.ForeignKey(Home, on_delete=models.CASCADE, default="" ,related_name='details')

    class Meta:
        db_table = "Returned"

class Transfered(models.Model):
    REC = (("None","無"),("郭文龍","郭文龍"),("侯國興","侯國興"),("郭文河","郭文河"),("高晟琅","高晟琅"),("黃睿堂","黃睿堂"),("鄭任雯","鄭任雯"),("高麗華","高麗華"),("侯宗仁","侯宗仁"),("黃美禎","黃美禎"),("江水木","江水木"),("吳建進","吳建進"),("陳佳欣","陳佳欣"),("蔡孟亭","蔡孟亭"),("馮文明","馮文明"),("陳恆瑞","陳恆瑞"),("郭文欽","郭文欽"),("郭曉穎","郭曉穎"),("黃春北","黃春北"),("許有龍","許有龍"))
    cNumber = models.CharField(max_length=50, default='',blank=True)
    cTransferTo = models.CharField(max_length=20,null=False,choices=REC)
    transferhome = models.ForeignKey(Home, on_delete=models.CASCADE, default="" ,related_name='detailes')
    class Meta:
        db_table = "Transfer"

class Count(models.Model):
    count = models.IntegerField(default=0,blank=True)

    class Meta:
        db_table = "Count"

# 5+1
class Signed (models.Model):
    cNumber = models.CharField(max_length=50, default='', null=False)#編號
    cJob_title = models.CharField(max_length=50,blank=True)#職稱
    cSubject = models.CharField(max_length=255, default='',blank=True)#主旨
    cDiscription = models.TextField(blank=True)#說明
    cProposed=models.TextField(blank=True)#擬辦
    cSecret = models.CharField(max_length=20,default='',blank=True) #是否是保密
    home = models.OneToOneField(Home, on_delete=models.CASCADE,default='')

    class Meta:
        db_table = "Signed"

#11+1
class Meeting (models.Model):
    cNumber = models.CharField(max_length=50, default='', null=False)
    cMeetingType = models.CharField(max_length=10,null=False)#會議型態
    cLocation = models.CharField(max_length=30, blank=True) #開會地點
    cTime = models.CharField(max_length=20, null=False,default="")#時間
    cLeader = models.CharField(max_length=10, null=False)#主席
    cRecoder = models.CharField(max_length=10, null=False)#紀錄者
    cTopic = models.CharField(max_length=50, null=False)#主題
    cAttendees1 = models.TextField(blank=True)#列席人員
    cAttendees2 = models.TextField(blank=True)#出席人員
    home = models.OneToOneField(Home, on_delete=models.CASCADE,default='')

    class Meta:
        db_table = "Meeting"

#4+1   
class MeetingInner(models.Model):
    cNumber = models.CharField(max_length=50, default='',blank=True)
    cContent = models.TextField(blank=True)
    cDoPerson = models.CharField(max_length=30, default='', blank=True)
    cStartDate = models.CharField(max_length=20, default='', blank=True)
    cExpectDate = models.CharField(max_length=20, default='', blank=True)
    cFile = models.FileField(blank=True, null=True)
    innermeeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, default="" ,related_name='details')

    class Meta:
        db_table = "MeetingInner"

class MeetingPurpose(models.Model):
    cNumber = models.CharField(max_length=50, default='',blank=True)
    cPurpose = models.TextField(blank=True)
    cPerson = models.CharField(max_length=30, default='', blank=True)
    cDate = models.DateField(blank=True, null=True)
    cFile = models.FileField(blank=True, null=True)
    purposemeeting = models.ForeignKey(MeetingInner, on_delete=models.CASCADE, default="" ,related_name='details')

    class Meta:
        db_table = "MeetingPurpose"

#7+1
class Contact (models.Model):
    cNumber = models.CharField(max_length=50, default='', null=False)#編號
    cAutherManager = models.CharField(max_length=20,blank=True)#發文主管
    cDecisionDep = models.CharField(max_length=50,null=False)#決策單位
    cImplementDep = models.CharField(max_length=50)#執行單位
    cSubject = models.TextField(null=False)#主旨
    cDiscription = models.TextField(blank=True)#說明
    home = models.OneToOneField(Home, on_delete=models.CASCADE,default='')

    class Meta:
        db_table = "Contact"

#12+1
class Contract(models.Model):
    cNumber = models.CharField(max_length=50, default='', null=False) #編號
    cClient = models.CharField(max_length=20, null=False) #客戶名稱
    cLocation = models.CharField(max_length=20, null=False)#工作地點
    cContent = models.TextField()#發包內容
    cPayMode = models.CharField(max_length=20, null=False)#付款方式
    cBudget = models.CharField(max_length=20, null=False)#預算
    cOther = models.TextField() #備註
    cConfirm = models.TextField(blank=True,default="_年_月_日決定以___元整交由__承攬本工程") #是否承攬工程
    home = models.OneToOneField(Home, on_delete=models.CASCADE,default='')

    class Meta:
        db_table = "Contract"

#5+1
class ContractInner(models.Model):
    cNumber = models.CharField(max_length=50, default='')
    cContractor = models.CharField(max_length=20, null=False) #承包商
    cQuotation = models.CharField(max_length=20, null=False) #報價
    cBargain1 = models.CharField(max_length=20, null=False) # 議價1
    cBargain2 = models.CharField(max_length=20, null=False) # 議價2
    cRemark = models.TextField()
    innercontract = models.ForeignKey(Contract, on_delete=models.CASCADE, default="" ,related_name='details')

    class Meta:
        db_table = "ContractInner"

class Change(models.Model):
    cNumber = models.CharField(max_length=50, default='', null=False) #編號
    cProjectName = models.CharField(max_length=50, default='', null=False) #專案名稱
    cChangeitem = models.CharField(max_length=20, null=False) #變更項目
    cChangereason = models.CharField(max_length=20, null=False) #變更原因
    cHowChange = models.CharField(max_length=10, null=False)#如何變更(設計變更、規格變更)
    cAffectitem = models.TextField()#影響項目
    cEarn = models.CharField(max_length=10,null=False,default='')#有償無償
    cRisk = models.TextField()#變更風險說明
    cKeypoint = models.TextField()#變更要點說明
    cOption_FS = models.TextField()#廠務部建議
    cOption_Design = models.TextField()#設計部建議
    cOption_Quality = models.TextField()#品管部建議
    cOption_Purchase = models.TextField()#採購建議
    cCC = models.CharField(max_length=10, blank=True) #副本印製
    cTech_bulletin = models.CharField(max_length=5, null=False)#是否技術通報
    cUndertaker = models.CharField(max_length=20,blank=True)#承辦人
    cFs_Sign = models.CharField(max_length=5,blank=True) #廠務部是否有簽名
    cDesign_Sign = models.CharField(max_length=5,blank=True) #設計部是否有簽名
    cQuality_Sign = models.CharField(max_length=5,blank=True)  #品管部是否有簽名
    cPurchase_Sign = models.CharField(max_length=5,blank=True) #採購是否有簽名
    home = models.OneToOneField(Home, on_delete=models.CASCADE,default='')

    class Meta:
        db_table = "Changes"