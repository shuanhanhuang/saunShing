from django import forms
from datetime import datetime
from testapp.models import Home
class HomeForm(forms.Form):
    REC = (("None","無"),("郭文龍","郭文龍"),("侯國興","侯國興"),("郭文河","郭文河"),("高晟琅","高晟琅"),("黃睿堂","黃睿堂"),("鄭任雯","鄭任雯"),("高麗華","高麗華"),("侯宗仁","侯宗仁"),("黃美禎","黃美禎"),("江水木","江水木"),("吳建進","吳建進"),("王韋盛","王韋盛"),("陳佳欣","陳佳欣"),("蔡孟亭","蔡孟亭"),("馮文明","馮文明"),("陳恆瑞","陳恆瑞"),("郭文欽","郭文欽"),("陳春能","陳春能"),("黃春北","黃春北"))
    cNumber = forms.CharField(max_length=50,initial="免填",disabled=True)
    cAuther = forms.CharField(max_length=20,initial="免填",disabled=True)#姓名
    cDepartment = forms.CharField(max_length=50)#單位
    cType = forms.CharField(max_length=10)
    cProgress = forms.CharField(max_length=20)
    cDate = forms.DateField(initial=datetime.now())#日期
    cEndDate = forms.DateField(initial=datetime.now(),required=False)
    cLock = forms.CharField(max_length=5,initial="否")
    cReceive = forms.CharField(max_length=20,required=False,widget=forms.Select(choices=REC))
    cFile = forms.FileField(required=False)
    
class CountForm(forms.Form):
	count = forms.IntegerField(initial=0,required=False)
    
class ReturnedForm(forms.Form):
	REC = (("None","無"),("郭文龍","郭文龍"),("侯國興","侯國興"),("郭文河","郭文河"),("高晟琅","高晟琅"),("黃睿堂","黃睿堂"),("鄭任雯","鄭任雯"),("高麗華","高麗華"),("侯宗仁","侯宗仁"),("黃美禎","黃美禎"),("江水木","江水木"),("吳建進","吳建進"),("王韋盛","王韋盛"),("陳佳欣","陳佳欣"),("蔡孟亭","蔡孟亭"),("馮文明","馮文明"),("陳恆瑞","陳恆瑞"),("郭文欽","郭文欽"),("陳春能","陳春能"),("黃春北","黃春北"))
	cName = forms.CharField(max_length=20,initial="免填",disabled=True)#誰駁回的(姓名)
	cTransfer = forms.CharField(max_length=20,initial="免填",required=False)#被駁回的(姓名)
	cIllustrate = forms.CharField(widget=forms.Textarea, required=False)

class SignedForm (forms.Form):
	cNumber = forms.CharField(max_length=50,initial='免填',disabled=True)
	cJob_title = forms.CharField(max_length=50,initial='',required=False)
	cSubject = forms.CharField(max_length=255, initial='') # ,required=False
	cProposed=forms.CharField(widget=forms.Textarea,required=False)#擬辦
	cCheck=forms.CharField(widget=forms.Textarea,required=False)#批示
	cDiscription = forms.CharField(widget=forms.Textarea,required=False)

class MeetingInnerForm(forms.Form):
	cContent = forms.CharField(widget=forms.Textarea, required=False)
	cDoPerson = forms.CharField(max_length=30, initial='', required=False)
	cExpectDate = forms.CharField(max_length=20, initial='', required=False)
	cOther = forms.CharField(widget=forms.Textarea, required=False)

#17
class MeetingForm (forms.Form):
	cNumber = forms.CharField(max_length=50, initial='免填',disabled=True)
	cMeetingType = forms.CharField(max_length=10)#會議型態
	cLocation = forms.CharField(max_length=30,required=False)
	cTime = forms.CharField(max_length=20)#時間
	cLeader = forms.CharField(max_length=10)#主席
	cRecoder = forms.CharField(max_length=10 )#紀錄者
	cTopic = forms.CharField(max_length=50)#主題
	cAttendees1 = forms.CharField(widget=forms.Textarea,required=False)#列席人員
	cAttendees2 = forms.CharField(widget=forms.Textarea,required=False)#出席人員
	cViceGeneral_Sign = forms.CharField(max_length=20,required=False) #副總簽名
	cManger_Sign = forms.CharField(max_length=20,required=False)#主管簽名
	

#內部連絡單
class ContactForm (forms.Form):
	cNumber = forms.CharField(max_length=50, initial='免填',disabled=True)
	cAutherManager = forms.CharField(max_length=20,required=False)
	cDecisionDep = forms.CharField(max_length=50)
	cImplementDep = forms.CharField(max_length=50)
	cSubject = forms.CharField(max_length=255, initial='')
	cDiscription = forms.CharField(widget=forms.Textarea,required=False)
	cOption = forms.CharField(widget=forms.Textarea,required=False)
#發包單
class ContractInnerForm(forms.Form):
	cContractor = forms.CharField(max_length=50,required=False) #承包商
	cQuotation = forms.CharField(max_length=50,required=False) #報價
	cBargain1 = forms.CharField(max_length=50,required=False) # 議價1
	cBargain2 = forms.CharField(max_length=50,required=False) # 議價2
	cRemark = forms.CharField(widget=forms.Textarea,required=False)

class ContractForm(forms.Form):
	cNumber = forms.CharField(max_length=50, initial='免填',disabled=True) #編號
	cClient = forms.CharField(max_length=20) #客戶名稱
	cLocation = forms.CharField(max_length=20)#工作地點
	cContent = forms.CharField(widget=forms.Textarea,required=False)#發包內容
	cPayMode = forms.CharField(max_length=20)#付款方式
	cBudget = forms.CharField(max_length=20,required=False)#預算
	cOther = forms.CharField(widget=forms.Textarea,required=False) #備註
	cConfirm = forms.CharField(widget=forms.Textarea,required=False,initial="_年_月_日決定以___元整交由__承攬本工程") #是否承攬工程
	cGeneral_Sign = forms.CharField(max_length=20,required=False) #總座簽名
	cViceGeneral_Sign = forms.CharField(max_length=20,required=False) # 副總簽名
	cManager_Sign = forms.CharField(max_length=20,required=False) #部門主管簽名
	cDepartmentManager_Sign = forms.CharField(max_length=20,required=False) #單位主管簽名
	cUndertaker = forms.CharField(max_length=20,required=False)#承辦人
	
class ChangeForm(forms.Form):
    cNumber = forms.CharField(max_length=50, initial='免填',disabled=True) #編號
    cProjectName = forms.CharField(max_length=50, initial='') #專案名稱
    cChangeitem = forms.CharField(max_length=20) #變更項目
    cChangereason = forms.CharField(max_length=20) #變更原因
    cHowChange = forms.CharField(max_length=10)#如何變更(設計變更、規格變更)
    cAffectitem = forms.CharField(widget=forms.Textarea,required=False)#影響項目
    cEarn = forms.CharField(max_length=10,required=False)
    cRisk = forms.CharField(widget=forms.Textarea,required=False)#變更風險說明
    cKeypoint = forms.CharField(widget=forms.Textarea,required=False)#變更要點說明
    cOption_FS = forms.CharField(widget=forms.Textarea,required=False)#廠務部建議
    cOption_Design = forms.CharField(widget=forms.Textarea,required=False)#設計部建議
    cOption_Quality = forms.CharField(widget=forms.Textarea,required=False)#品管部建議
    cOption_Purchase = forms.CharField(widget=forms.Textarea,required=False)#採購建議
    cCC = forms.CharField(max_length=10) #副本印製
    cTech_bulletin = forms.CharField(max_length=5)#是否技術通報
    cApproved = forms.CharField(max_length=20,required=False)#核准人
    cReview = forms.CharField(max_length=20,required=False)#審查人
    cUndertaker = forms.CharField(max_length=20,required=False)#承辦人
    cFs_Sign = forms.CharField(max_length=5,required=False) #廠務部是否有簽名
    cDesign_Sign = forms.CharField(max_length=5,required=False) #設計部是否有簽名
    cQuality_Sign = forms.CharField(max_length=5,required=False)  #品管部是否有簽名
    cPurchase_Sign = forms.CharField(max_length=5,required=False) #採購是否有簽名
