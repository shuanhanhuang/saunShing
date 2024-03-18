from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
# import datetime
from datetime import datetime
from django.contrib import auth
from testapp.form import HomeForm,SignedForm,MeetingInnerForm,MeetingForm,ContactForm,ContractForm,ContractInnerForm,ChangeForm,ReturnedForm,CountForm,TransferedForm,UserForm,MeetingPurposeForm
from testapp.models import Home,Signed,MeetingInner,Meeting,Contact,Contract,ContractInner,Change,Returned,Count,Transfered,User,MeetingPurpose
from django.db.models import Q
from testapp.filter import HomeFilter
from openpyxl import Workbook
import requests
import json
from datetime import timedelta


# from python_function import encrypt, write_data_to_contract, read_data_from_sqlite, read_data_from_contract, decrypt
# excel_filter = []
excel_filter = Home.objects.all()
def download_workbook(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="homeform.xlsx"'

    wb = Workbook()
    ws = wb.active

    # columns = ['cNumber', 'cAuther', 'cDepartment', 'cType', 'cProgress', 'HomeDate', 'cEndDate','cReceive']
    columns = ['編號', '發文者', '部門別', '種類', '主旨','文件進度', '建立日期', '完成日期','簽核進度']
    ws.append(columns)

    data = excel_filter
    for row in data:
        row_data = [row.cNumber, row.cAuther, row.cDepartment, row.cType,row.cSubject,row.cProgress
                    , row.HomeDate, row.cEndDate, row.cReceive]  # Adjust fields as needed
        ws.append(row_data)

    wb.save(response)
    return response

# Create your views here.
def HomePost(request):
    current_time = str(datetime.now().strftime("%Y-%m-%d %H:%M")).replace("月","-").replace("年","-").replace("年","")
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    if request.method == "POST":  #如果是以POST方式才處理
        homeform = HomeForm(request.POST,request.FILES)  #建立forms物件
        if homeform.is_valid():
            C = Count.objects.get(id=1)
            Acount = C.count
            if (Acount>=1000):
                Acount=Acount%100

            if(Acount//100 == 0):
                    if((Acount%100)//10 ==0):
                        count = "00"
                    else:
                        count = "0"
            else:
                count = ""
            C.count = Acount+1
            C.save()
            cType = homeform.cleaned_data['cType']
            cDepartment = position
            cTime = homeform.cleaned_data['cTime']
            
            HomeDate = datetime.now()
            if(HomeDate.day //10 == 0):
                date = "0" + str(HomeDate.day)
            else:
                date = str(HomeDate.day)

            if(HomeDate.month //10 == 0):
                month = "0" + str(HomeDate.month)
            else:
                month = str(HomeDate.month)
            if(homeform.cleaned_data['cType'] == "簽呈"):
                cNumber = "R18"+str(HomeDate.year)+month+date+count+str(Acount)
            elif(homeform.cleaned_data['cType'] == "會議記錄表"):
                cNumber = "R07"+str(HomeDate.year)+month+date+count+str(Acount)
            elif(homeform.cleaned_data['cType'] == "內部連絡單"):
                cNumber = "R14"+str(HomeDate.year)+month+date+count+str(Acount)
            elif(homeform.cleaned_data['cType'] == "發包議價表"):
                cNumber = "P16"+str(HomeDate.year)+month+date+count+str(Acount)
            elif(homeform.cleaned_data['cType'] == "設計變更通知單"):
                cNumber = "D08"+str(HomeDate.year)+month+date+count+str(Acount)
            cAuther = firstname
            cEndDate =  homeform.cleaned_data['cEndDate'] #取得表單輸入資料
            cProgress =  "草稿"
            cSubject = homeform.cleaned_data['cSubject']
            cReceive = firstname
            cFile = homeform.cleaned_data['cFile']
            cFile1 = homeform.cleaned_data['cFile1']
            cFile2 = homeform.cleaned_data['cFile2']
            cFile3 = homeform.cleaned_data['cFile3']
            cFile4 = homeform.cleaned_data['cFile4']

            unit = Home.objects.create(cType=cType,cNumber=cNumber,cAuther=cAuther, HomeDate=HomeDate, cDepartment=cDepartment, cEndDate=cEndDate, cProgress=cProgress,cReceive=cReceive,cFile=cFile,cFile1=cFile1,cFile2=cFile2,cFile3=cFile3,cFile4=cFile4,cTime=cTime,cSubject=cSubject)
            home = unit.save()  #寫入資料庫
            message = '已儲存...'
            
            if cType == "簽呈":
                return redirect('/signPost/'+str(cNumber)+'/')
            elif cType == '會議記錄表':
                return redirect('/meetingPost/'+str(cNumber)+'/')
            elif cType == '內部連絡單':
                return redirect('/contactPost/'+str(cNumber)+'/')
            elif cType == '發包議價表':
                return redirect('/contractPost/'+str(cNumber)+'/')
            elif cType == '設計變更通知單':
                return redirect('/changePost/'+str(cNumber)+'/')
        else:
            message = '驗證碼錯誤！'
    else:
        message = '請選擇表單種類和主旨！'
    homeform = HomeForm({'cAuther':firstname,'cDepartment':position,'cProgress':"草稿",'cTime':current_time})
    return render(request, "homePost.html", locals())

def homeIndex(request):
    global excel_filter
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
    allPerson = Home.objects.filter(cReceive = firstname)
    transferall = Transfered.objects.all().order_by("id")
    transferallCount = len(transferall)
    allpersonCount = len(allPerson)
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(cNumber__icontains=q) | Q(cSubject__icontains=q) | Q(cDepartment__icontains=q) | Q(cType__icontains=q) | Q(cAuther__icontains=q) | Q(cProgress__icontains=q) | Q(HomeDate__icontains=q) | Q(cEndDate__icontains=q))
        all = Home.objects.filter(multiple_q)
        excel_filter = all
    else:
        all = Home.objects.all().order_by("id")
        homeFilter = HomeFilter(request.GET, queryset=all)
        all = homeFilter.qs
        excel_filter = all
    allHomeCount = len(all)
    return render(request, "homeIndex.html",locals())


open = False
def open1(request,id=None,mode=None):
    global open
    open = True
    return redirect('/homeEdit/'+str(id)+"/"+str(mode))

def homeEdit(request,id=None,mode=None):
    global open
    Open = open
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = Home.objects.get(id=id)  #取得要修改的資料記  
        return render(request, "homeEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = Home.objects.get(id=id)  #取得要修改的資料記錄
        if request.FILES.get('cFile', '') != "":
            try:
                unit.cFile = request.FILES['cFile']
            except:
                unit.cFile = request.POST["cFile"]
        else:
            unit.cFile = unit.cFile
        if request.FILES.get('cFile1', '') != "":
            try:
                unit.cFile1 = request.FILES['cFile1']
            except:
                unit.cFile1 = request.POST["cFile1"]
        else:
            unit.cFile1 = unit.cFile1
        if request.FILES.get('cFile2', '') != "":
            try:
                unit.cFile2 = request.FILES['cFile2']
            except:
                unit.cFile2 = request.POST["cFile2"]
        else:
            unit.cFile2 = unit.cFile2
        if request.FILES.get('cFile3', '') != "":
            try:
                unit.cFile3 = request.FILES['cFile3']
            except:
                unit.cFile3 = request.POST["cFile3"]
        else:
            unit.cFile3 = unit.cFile3
        if request.FILES.get('cFile4', '') != "":
            try:
                unit.cFile4 = request.FILES['cFile4']
            except:
                unit.cFile4 = request.POST["cFile4"]
        else:
            unit.cFile4 = unit.cFile4
        
        unit.save()  #寫入資料庫

        message = '已修改...'
        return redirect('/homeIndex/')
    
def homeDelete(request,id=None):
    if id!=None:
        if request.method == "POST":  #如果是以POST方式才處理
            print("BBB")
            id=request.POST['cId'] #取得表單輸入的編號
            print("this is id !!!!",id)
        try:
            unit = Home.objects.get(id=id)
            print(unit)
            unit.delete()
            return redirect('/homeIndex/')
        except:
            unit.delete()
            message = "讀取錯誤!"
    unit.delete()
    return render(request, "homeDelete.html", locals())

def transferPost(request,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    transferHome = Home.objects.get(cNumber=cNumber)
    unitinner = Transfered.objects.filter(transferhome=transferHome).order_by("id")
    unitinnercount = len(unitinner)
    if request.method == 'POST':
        transferform = TransferedForm(request .POST)
        if transferform.is_valid():
            cTransferTo = transferform.cleaned_data['cTransferTo']
            cNumber = cNumber
            transferedunit = Transfered.objects.create(transferhome=transferHome, cTransferTo=cTransferTo,cNumber=cNumber)
            transferedunit.save()
            return redirect('/transferPost/'+ str(transferHome.cNumber) +'/')
        else:
             message="驗證錯誤"
    else:
         message='收件人為必選'
    transferform = TransferedForm()
    return render(request, "transferPost.html", locals())

def transferDelete(request,cNumber=None,id=None):
	if id!=None:
		if request.method == "POST":  #如果是以POST方式才處理
			id=request.POST['cId'] #取得表單輸入的編號
		try:
			unit = Transfered.objects.get(id=id)
			unit.delete()
			return redirect('/transferPost/'+str(cNumber)+'/')
		except:
			message = "讀取錯誤!"
	return render(request, "transferDelete.html", locals())

def transferIndex(request,id=None):
    home = Home.objects.get(id = id)
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    allPerson = Home.objects.filter(cReceive = firstname)
    allpersonCount = len(allPerson)
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(cTransferTo__icontains=q))
        transfered = Transfered.objects.filter(multiple_q)
    else:
        transfered = Transfered.objects.filter(transferhome=home).order_by('id')
    allunittransferCount = len(transfered)
    return render(request, "transferIndex.html",locals())

def returnedDelete(request,id2=None,id=None):
	if id!=None:
		if request.method == "POST":  #如果是以POST方式才處理
			id=request.POST['cId'] #取得表單輸入的編號
		try:
			unit = Returned.objects.get(id=id)
			unit.delete()
			return redirect('/returnedIndex/'+str(id2)+'/')
		except:
			message = "讀取錯誤!"
	return render(request, "returnedDelete.html", locals())

def returnedPost(request,id=None,cNumber=None):
    re_id=id
    current_time = str(datetime.now().strftime("%Y-%m-%d %H:%M")).replace("月","-").replace("年","-").replace("年","")
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    returnedHome = Home.objects.get(id=id)
    tempCount = returnedHome.cCount
    if(returnedHome.cType == "簽呈"):
        returnedSign = Signed.objects.get(cNumber = cNumber)
    elif(returnedHome.cType == "會議記錄表"):
        returnedMeeting = Meeting.objects.get(cNumber = cNumber)
        returnedMeetinginner = MeetingInner.objects.filter(innermeeting=returnedMeeting).order_by("id")
        meetingpurpose = MeetingPurpose.objects.all().order_by("id")
    elif (returnedHome.cType == "內部連絡單"):
        returnedContact = Contact.objects.get(cNumber = cNumber)
    elif (returnedHome.cType == "發包議價表"):
        returnedContract = Contract.objects.get(cNumber = cNumber)
        returnedContractinner = ContractInner.objects.filter(innercontract=returnedContract).order_by("id")
    else:
        returnedChange = Change.objects.get(cNumber = cNumber)
    unitinner = Returned.objects.filter(returnTo=returnedHome).order_by("id")
    transfered = Transfered.objects.filter(transferhome=returnedHome).order_by('id')
    lentransfer = len(transfered)
    if request.method == 'POST':
        returnedform = ReturnedForm(request.POST)
        if returnedform.is_valid():
            if returnedHome.cAuther == firstname:
                cNumber = cNumber
                cName = firstname
                cHow = "同意"
                cIllustrate = ""
            else:
                cNumber = cNumber
                cName = firstname
                cHow = returnedform.cleaned_data['cHow']
                cIllustrate =  returnedform.cleaned_data['cIllustrate']
            tempcHow = cHow
            if tempcHow == "同意":
                if returnedHome.cCount == lentransfer-1:
                    returnedHome.cReceive = "無"
                    returnedHome.cEndDate = datetime.now()
                    returnedHome.cCount = -1
                    returnedHome.save()
                else:
                    tempCount = returnedHome.cCount+1
                    returnedHome.cReceive = transfered[tempCount].cTransferTo
                    # tempCount = tempCount+1
                    returnedHome.cCount = tempCount
                    returnedHome.save()
            elif tempcHow == "駁回":
                returnedHome.cReceive = "無"
                returnedHome.cEndDate = datetime.now()
                returnedHome.cCount = -1
                returnedHome.save()
            elif tempcHow == "修正再呈":
                if returnedHome.cCount == 0:
                    returnedHome.cReceive = returnedHome.cAuther
                    returnedHome.cCount = -1
                else:
                    tempCount = returnedHome.cCount-1
                    returnedHome.cReceive = transfered[tempCount].cTransferTo
                    returnedHome.cCount = tempCount
                returnedHome.save()
            cReturnedTime = datetime.now().time()
            cTransfer = returnedHome.cReceive
            returnedunit = Returned.objects.create(returnTo=returnedHome, cNumber = cNumber,cName=cName, cIllustrate=cIllustrate, cTransfer=cTransfer, cHow=cHow, cReturnedTime=cReturnedTime)
            returnedunit.save()
            returned = Returned.objects.filter(returnTo=returnedHome).order_by("id")
            allunitreturnCount = len(returned)
            if allunitreturnCount != 0:
                if returnedHome.cCount == -1:
                    if returned[allunitreturnCount-1].cHow == "同意":
                        returnedHome.cProgress = "結案"
                        returnedHome.save()
                    elif returned[allunitreturnCount-1].cHow == "駁回":
                        returnedHome.cProgress = "駁回"
                        returnedHome.save()
                else:
                    returnedHome.cProgress = "流程中"
                    returnedHome.save()
            if(returnedHome.cType == "簽呈"):
                return redirect('/signView/'+str(cNumber)+'/')
            elif(returnedHome.cType == "會議記錄表"):
                return redirect('/meetingView/'+str(cNumber)+'/')
            elif (returnedHome.cType == "內部連絡單"):
                return redirect('/contactView/'+str(cNumber)+'/')
            elif (returnedHome.cType == "發包議價表"):
                return redirect('/contractView/'+str(cNumber)+'/')
            else:
                return redirect('/changeView/'+str(cNumber)+'/')
        else:
             message="驗證錯誤"
    else:
         message=''
    returned = Returned.objects.filter(returnTo=returnedHome).order_by("id")
    allunitreturnCount = len(returned)
    returnedform = ReturnedForm({'cName':firstname,'cReturnedTime':current_time,'cHow':'同意'})
    return render(request, "returnedPost.html", locals())

def returnedIndex(request,id=None):
    home = Home.objects.get(id = id)
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    allPerson = Home.objects.filter(cReceive = firstname)
    allpersonCount = len(allPerson)
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(cName__icontains=q) | Q(cIllustrate__icontains=q) | Q(cTransfer__icontains=q))
        returned = Returned.objects.filter(multiple_q)
    else:
        returned = Returned.objects.filter(returnTo=home).order_by("id")
    allunitreturnCount = len(returned)
    print("allunitreturnCount",allunitreturnCount)
    print("home.cCount",home.cCount)
    if allunitreturnCount != 0:
        if home.cCount == -1:
            if returned[allunitreturnCount-1].cHow == "同意" or returned[allunitreturnCount-1].cHow == "駁回":
                home.cProgress = "結案"
                home.save()
        else:
            home.cProgress = "流程中"
            home.save()
    return render(request, "returnedIndex.html",locals())


def Detail(request,cNumber=None):
    index = Home.objects.get(cNumber = cNumber)
    if index.cType == "簽呈":
        sign_detail = Signed.objects.get(cNumber=cNumber)
        return redirect('/signEdit/'+str(cNumber)+'/'+str(sign_detail.id)+'/load')
    elif index.cType == "會議記錄表":
        meeting_detail = Meeting.objects.get(cNumber=cNumber)
        return redirect('/meetingEdit/'+str(cNumber)+'/'+str(meeting_detail.id)+'/load')
    elif index.cType == '內部連絡單':
        contact_detail = Contact.objects.get(cNumber=cNumber)
        return redirect('/contactEdit/'+str(cNumber)+'/'+str(contact_detail.id)+'/load')
    elif index.cType == '發包議價表':
        contract_detail = Contract.objects.get(cNumber=cNumber)
        return redirect('/contractEdit/'+str(cNumber)+'/'+str(contract_detail.id)+'/load')
    else:
        change_detail = Change.objects.get(cNumber=cNumber)
        return redirect('/changeEdit/'+str(cNumber)+'/'+str(change_detail.id)+'/load')

def perosonIndex(request,cUsername = None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    all = Home.objects.filter(cReceive = cUsername)
    allHomeCount = len(all)
    return render(request, "perosonIndex.html",locals())

def signCopyPost(request,cNumber=None,thisNumber=None):# cNumber複製的;thisNumber被複製
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    home = Home.objects.get(cNumber=cNumber)
    unitinner = Signed.objects.get(cNumber=thisNumber)
    if request.method == 'POST':
        signedform = SignedForm(request.POST)
        if signedform.is_valid():
            cNumber =  cNumber
            cJob_title = unitinner.cJob_title
            cDiscription = unitinner.cDiscription
            cSubject = unitinner.cSubject
            cProposed = unitinner.cProposed
            cSecret = unitinner.cSecret
            home.cSecret = unitinner.cSecret
            home.save()
            signunit = Signed.objects.create(home=home, cNumber=cNumber,cJob_title= cJob_title, cDiscription=cDiscription,cProposed=cProposed,cSubject=cSubject,cSecret=cSecret)
            signunit.save()

            return redirect('/signallIndex/')
        else:
            message="驗證錯誤"
    signedform = SignedForm({'cDiscription':unitinner.cDiscription,'cProposed':unitinner.cProposed,'cSubject':unitinner.cSubject}) #有必填欄位要寫進去
    return render(request, "signCopyPost.html", locals())

#簽呈
def signPost(request,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    home = Home.objects.get(cNumber=cNumber)
    unitinner = Signed.objects.filter(home=home).order_by("id")
    if request.method == 'POST':
        signedform = SignedForm(request.POST)
        if signedform.is_valid():
            cNumber =  home.cNumber
            cJob_title = title
            cSubject = home.cSubject
            cDiscription =  signedform.cleaned_data['cDiscription']
            cProposed = signedform.cleaned_data['cProposed']
            cSecret = signedform.cleaned_data['cSecret']
            home.cSecret = request.POST['cSecret']
            try:
                home.cFile = request.FILES['cFile']
            except:
                home.cFile = request.POST["cFile"]
            try:
                home.cFile1 = request.FILES['cFile1']
            except:
                home.cFile1 = request.POST["cFile1"]
            try:
                home.cFile2 = request.FILES['cFile2']
            except:
                home.cFile2 = request.POST["cFile2"]
            try:
                home.cFile3 = request.FILES['cFile3']
            except:
                home.cFile3 = request.POST["cFile3"]
            try:
                home.cFile4 = request.FILES['cFile4']
            except:
                home.cFile4 = request.POST["cFile4"]
            home.save()
            signunit = Signed.objects.create(home=home, cNumber=cNumber,cJob_title= cJob_title, cDiscription=cDiscription,cProposed=cProposed,cSubject=cSubject,cSecret=cSecret)
            signunit.save()
            return redirect('/transferPost/'+ str(cNumber)+'/')
        else:
             message="驗證錯誤"
    else:
         message='說明、擬辦 為必填欄位'
    signedform = SignedForm({'cSubject':home.cSubject,'cJob_title':title,'cNumber':cNumber})
    return render(request, "signPost.html", locals())


def signView(request,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    allPerson = Home.objects.filter(cReceive = firstname)
    allpersonCount = len(allPerson)
    home = Home.objects.get(cNumber=cNumber)
    returned = Returned.objects.filter(returnTo=home).order_by("id")
    sign = Signed.objects.get(cNumber=cNumber)
    return render(request, "signView.html",locals())

def homeCopyPost(request,cNumber1=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    home = Home.objects.get(cNumber=cNumber1)
    if request.method == 'POST':
        homeform = HomeForm(request.POST,request.FILES)  #建立forms物件
        if homeform.is_valid():
            C = Count.objects.get(id=1)
            Acount = C.count
            if(Acount//100 == 0):
                if((Acount%100)//10 ==0):
                    count = "00"
                else:
                    count = "0"
            else:
                count = ""
            C.count = Acount+1
            C.save()
            cType = home.cType
            cDepartment =home.cDepartment
            cTime = homeform.cleaned_data['cTime']
            HomeDate = datetime.now()
            if(HomeDate.day //10 == 0):
                date = "0" + str(HomeDate.day)
            else:
                date = str(HomeDate.day)

            if(HomeDate.month //10 == 0):
                month = "0" + str(HomeDate.month)
            else:
                month = str(HomeDate.month)
            if(home.cType == "簽呈"):
                cNumber = "R18"+str(HomeDate.year)+month+date+count+str(Acount)
            elif(home.cType == "會議記錄表"):
                cNumber = "R07"+str(HomeDate.year)+month+date+count+str(Acount)
            elif(home.cType == "內部連絡單"):
                cNumber = "R14"+str(HomeDate.year)+month+date+count+str(Acount)
            elif(home.cType == "發包議價表"):
                cNumber = "P16"+str(HomeDate.year)+month+date+count+str(Acount)
            elif(home.cType == "設計變更通知單"):
                cNumber = "D08"+str(HomeDate.year)+month+date+count+str(Acount)
            cAuther = firstname
            cSubject = home.cSubject 
            cEndDate =  homeform.cleaned_data['cEndDate'] #取得表單輸入資料
            cProgress =  "草稿"
            cReceive = firstname
            cFile = home.cFile
            cFile1 = home.cFile1
            cFile2 = home.cFile2
            cFile3 = home.cFile3
            cFile4 = home.cFile4
            unit = Home.objects.create(cType=cType,cNumber=cNumber,cAuther=cAuther, HomeDate=HomeDate, cTime=cTime, cDepartment=cDepartment, cEndDate=cEndDate, cProgress=cProgress,cReceive=cReceive,cFile=cFile,cFile1=cFile1,cFile2=cFile2,cFile3=cFile3,cFile4=cFile4,cSubject=cSubject)
            ome = unit.save()

            if cType == "簽呈":
                return redirect('/signCopyPost/'+str(cNumber)+'/'+str(home.cNumber)+'/')
            elif cType == '會議記錄表':
                return redirect('/meetingCopyPost/'+str(cNumber)+'/'+str(home.cNumber)+'/')
            elif cType == '內部連絡單':
                return redirect('/contactCopyPost/'+str(cNumber)+'/'+str(home.cNumber)+'/')
            elif cType == '發包議價表':
                return redirect('/contractCopyPost/'+str(cNumber)+'/'+str(home.cNumber)+'/')
            elif cType == '設計變更通知單':
                return redirect('/changeCopyPost/'+str(cNumber)+'/'+str(home.cNumber)+'/')
        else:
            message = '驗證碼錯誤！'
    else:
        message = ''
    homeform = HomeForm({'cAuther':firstname,'cDepartment':position,'cSubject':home.cSubject})
    return render(request, "homeCopyPost.html", locals())


def signPdf(request,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    home = Home.objects.get(cNumber=cNumber)
    sign = Signed.objects.get(cNumber=cNumber)
    return render(request, "signPdf.html",locals())

def signallIndex(request):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    allPerson = Home.objects.filter(cReceive = firstname)
    homeall = Home.objects.all().order_by("id")
    transferall = Transfered.objects.all().order_by("id")
    allpersonCount = len(allPerson)
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(cNumber__icontains=q) | Q(cSubject__icontains=q))
        signall = Signed.objects.filter(multiple_q)       
    else:
        signall = Signed.objects.all().order_by("id")
    signallCount = len(signall)
    return render(request, "signall_Index.html",locals())

def signEdit(request,id=None,mode=None,cNumber=None):
    homeform = HomeForm(request.POST,request.FILES)
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    unithome = Home.objects.get(cNumber = cNumber)
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = Signed.objects.get(id = id)  #取得要修改的資料記
        strdate=str(unithome.HomeDate)
        strdate2=strdate.replace("年","-")
        strdate2=strdate.replace("月","-")
        strdate2=strdate.replace("日","-")
        unithome.HomeDate = strdate2

        strdate1=str(unithome.cEndDate)
        strdate3=strdate1.replace("年","-")
        strdate3=strdate1.replace("月","-")
        strdate3=strdate1.replace("日","-")
        unithome.cEndDate = strdate3
        return render(request, "signEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        # unithome = Home.objects.get(cNumber = cNumber)
        if unithome.cProgress == "結案":
            unithome.cReceive = request.POST['cReceive']
        else:
            unithome.cAuther = request.POST['cAuther']
            # unithome.cDepartment = request.POST['cDepartment']
            if request.POST['cEndDate'] != "":
                unithome.cEndDate = request.POST['cEndDate']
            else:
                unithome.cEndDate = None
            # unithome.cProgress = request.POST['cProgress']
            unithome.cSubject = request.POST['cSubject']
            unithome.cSecret = request.POST['cSecret']
            unit = Signed.objects.get(id = id)  #取得要修改的資料記錄
            unit.cJob_title = request.POST['cJob_title']
            unit.cSubject = unithome.cSubject
            unit.cDiscription=request.POST['cDiscription']
            unit.cProposed=request.POST['cProposed']
            unit.cSecret = request.POST['cSecret']
            unit.save()
        unithome.save()  #寫入資料庫

          #寫入資料庫
        message = '已修改...'
        return redirect('/signallIndex/')


def meetingCopyPost(request,cNumber=None,thisNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    home = Home.objects.get(cNumber=cNumber)
    unitinner = Meeting.objects.get(cNumber=thisNumber)
    if request.method == 'POST':
        meetingform = MeetingForm(request.POST)
        if meetingform.is_valid():
            cNumber =  cNumber
            cMeetingType = unitinner.cMeetingType
            cRecoder = unitinner.cRecoder
            cLocation = unitinner.cLocation
            cTime = unitinner.cTime
            cLeader = unitinner.cLeader
            cTopic =  unitinner.cTopic
            cAttendees1 =  unitinner.cAttendees1
            cAttendees2 =  unitinner.cAttendees2
            # Save the signature data with the associated document
            unit = Meeting.objects.create(home=home,cNumber=cNumber, cRecoder=cRecoder, cMeetingType=cMeetingType, cLocation=cLocation, cTime=cTime, cLeader=cLeader, cTopic=cTopic, cAttendees1=cAttendees1, cAttendees2=cAttendees2)
            unit.save()  #寫入資料庫
            return redirect('/meetingallIndex/')
        else:
             message="驗證錯誤"
    meetingform = MeetingForm({'cMeetingType':unitinner.cMeetingType,'cLocation':unitinner.cLocation,'cTime':unitinner.cTime,
                               'cLeader':unitinner.cLeader,'cRecoder':unitinner.cRecoder,'cTopic':unitinner.cTopic})
    return render(request, "meetingCopyPost.html", locals())

#會議記錄表 
def meetingPost(request,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    home = Home.objects.get(cNumber=cNumber)
    unitinner = Meeting.objects.filter(home=home).order_by("id")
    if request.method == 'POST':
        meetingform = MeetingForm(request.POST)
        if meetingform.is_valid():
            cNumber =  home.cNumber
            cMeetingType = meetingform.cleaned_data['cMeetingType']
            cRecoder = firstname
            cLocation = meetingform.cleaned_data['cLocation']
            cTime = meetingform.cleaned_data['cTime']
            cLeader = meetingform.cleaned_data['cLeader']
            cTopic =  meetingform.cleaned_data['cTopic']
            cAttendees1 =  meetingform.cleaned_data['cAttendees1']
            cAttendees2 =  meetingform.cleaned_data['cAttendees2']
            # try:
            #     home.cFile = request.FILES['cFile']
            #     home.save()
            # except:
            #     home.cFile = request.POST["cFile"]
            #     home.save()
            try:
                home.cFile = request.FILES['cFile']
            except:
                home.cFile = request.POST["cFile"]
            try:
                home.cFile1 = request.FILES['cFile1']
            except:
                home.cFile1 = request.POST["cFile1"]
            try:
                home.cFile2 = request.FILES['cFile2']
            except:
                home.cFile2 = request.POST["cFile2"]
            try:
                home.cFile3 = request.FILES['cFile3']
            except:
                home.cFile3 = request.POST["cFile3"]
            try:
                home.cFile4 = request.FILES['cFile4']
            except:
                home.cFile4 = request.POST["cFile4"]
            home.save()
            # Save the signature data with the associated document
            unit = Meeting.objects.create(home=home,cNumber=cNumber, cRecoder=cRecoder, cMeetingType=cMeetingType, cLocation=cLocation, cTime=cTime, cLeader=cLeader, cTopic=cTopic, cAttendees1=cAttendees1, cAttendees2=cAttendees2)
            unit.save()  #寫入資料庫

            # return redirect('/transferPost/'+ str(cNumber)+'/')
            return redirect('/meetinginnerIndex/'+ str(cNumber)+'/')
        else:
             message="驗證錯誤"
    else:
         message='會議型態、開會日期、地點、主席、主題、出席人員必須輸入或點選'
    meetingform = MeetingForm({'cNumber':home.cNumber,'cRecoder':firstname})
    return render(request, "meetingPost.html", locals())

def meetingEdit(request,id=None,mode=None,cNumber=None):
    homeform = HomeForm(request.POST)
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    unithome = Home.objects.get(cNumber = cNumber)
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = Meeting.objects.get(id = id)  #取得要修改的資料記
        strdate=str(unithome.HomeDate)
        strdate2=strdate.replace("年","-")
        strdate2=strdate.replace("月","-")
        strdate2=strdate.replace("日","-")
        unithome.HomeDate = strdate2

        strdate1=str(unithome.cEndDate)
        strdate3=strdate1.replace("年","-")
        strdate3=strdate1.replace("月","-")
        strdate3=strdate1.replace("日","-")
        unithome.cEndDate = strdate3
        return render(request, "meetingEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = Meeting.objects.get(id = id)  #取得要修改的資料記錄
        if unithome.cProgress == "結案":
            unithome.cReceive = request.POST['cReceive']
        else:
            unithome.cAuther = request.POST['cAuther']
            unithome.cSubject = request.POST['cSubject']
            # unithome.cDepartment = request.POST['cDepartment']
            if request.POST['cEndDate'] != "":
                unithome.cEndDate = request.POST['cEndDate']
            else:
                unithome.cEndDate = None
            # unithome.cProgress = request.POST['cProgress']
            unit.cMeetingType = request.POST['cMeetingType']
            unit.cLocation=request.POST['cLocation']
            unit.cTopic=request.POST['cTopic']
            unit.cAttendees1=request.POST['cAttendees1']
            unit.cAttendees2=request.POST['cAttendees2']
            unit.cLeader = request.POST['cLeader']
            unit.save()  #寫入資料庫
        unithome.save()

        message = '已修改...'
        return redirect('/meetinginnerIndex/'+ str(unithome.cNumber)+'/')

def meetingpurposePost(request,cNumber=None,id=None,id2=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    home = Home.objects.get(cNumber=cNumber)
    meeting = Meeting.objects.get(cNumber=cNumber)
    unitinner = MeetingInner.objects.filter(innermeeting=meeting).order_by("id")
    meetingunit = MeetingInner.objects.get(id=id)
    if request.method == 'POST':
        meetingpurposeform = MeetingPurposeForm(request.POST,request.FILES)
        if meetingpurposeform.is_valid():
            cNumber =  home.cNumber
            cPerson = firstname
            cPurpose = meetingpurposeform.cleaned_data['cPurpose']
            cDate = datetime.now()
            cFile = meetingpurposeform.cleaned_data['cFile']
            
            # Save the signature data with the associated document
            unit = MeetingPurpose.objects.create(purposemeeting=meetingunit,cNumber=cNumber, cPerson=cPerson, cPurpose=cPurpose, cDate=cDate, cFile=cFile)
            unit.save()  #寫入資料庫

            # return redirect('/transferPost/'+ str(cNumber)+'/')
            return redirect('/returnedPost/'+ str(id2)+ "/"+ str(cNumber)+'/')
        else:
             message="驗證錯誤"
    meetingpurposeform = MeetingPurposeForm({'cNumber':home.cNumber,'cPerson':firstname,'cDate':datetime.now()})
    return render(request, "meetingpurposePost.html", locals())    

def meetingpurposeEdit(request,cNumber=None,id=None,id2=None,mode=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    unithome = Home.objects.get(cNumber = cNumber)
    unit = MeetingPurpose.objects.get(id=id2)
    cNumber = cNumber
    tempid = id
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = MeetingPurpose.objects.get(id=id2)  #取得要修改的資料記
        return render(request, "meetingpurposeEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = MeetingPurpose.objects.get(id=id2)  #取得要修改的資料記錄
        unit.cPurpose = request.POST['cPurpose']
        unit.cDate=datetime.now()
        unit.save()  #寫入資料庫

        message = '已修改...'
        return redirect('/returnedPost/'+ str(unithome.id)+ "/"+ str(cNumber)+'/')
    
def meetingpurposefileEdit(request,cNumber=None,id=None,id2=None,mode=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    tempid = id
    unithome = Home.objects.get(cNumber=cNumber)
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = MeetingPurpose.objects.get(id=id2)  #取得要修改的資料記  
        return render(request, "meetingpurposefileEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = MeetingPurpose.objects.get(id=id2)  #取得要修改的資料記錄
        try:
            unit.cFile = request.FILES['cFile']
        except:
            unit.cFile = request.POST["cFile"]
        unit.save()  #寫入資料庫

        message = '已修改...'
        return redirect('/returnedPost/'+ str(unithome.id)+ "/"+ str(cNumber)+'/')

def meetingView(request,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    allPerson = Home.objects.filter(cReceive = firstname)
    allpersonCount = len(allPerson)
    home = Home.objects.get(cNumber=cNumber)
    returned = Returned.objects.filter(returnTo=home).order_by("id")
    meeting = Meeting.objects.get(cNumber=cNumber)
    unitinner = MeetingInner.objects.filter(innermeeting=meeting).order_by("id")
    return render(request, "meetingView.html",locals())

def meetingallIndex(request):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    allPerson = Home.objects.filter(cReceive = firstname)
    allpersonCount = len(allPerson)
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(cNumber__icontains=q) | Q(cTopic__icontains=q) | Q(cMeetingType__icontains=q))
        meetingall = Meeting.objects.filter(multiple_q)
    else:
        meetingall = Meeting.objects.all().order_by("id")   
    meetingallCount = len(meetingall)
    return render(request, "meetingall_Index.html",locals())

#會議記錄表-會議內容
def meetinginnerPost(request,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    innermeeting = Meeting.objects.get(cNumber = cNumber)
    unitinner = MeetingInner.objects.filter(innermeeting=innermeeting).order_by("id")
    if request.method == "POST":  #如果是以POST方式才處理
        meetinginnerform = MeetingInnerForm(request.POST,request.FILES)  #建立forms物件
        if meetinginnerform.is_valid():
            cNumber = cNumber
            cContent = meetinginnerform.cleaned_data['cContent']
            cDoPerson = meetinginnerform.cleaned_data['cDoPerson']
            cStartDate = meetinginnerform.cleaned_data['cStartDate']
            cExpectDate = meetinginnerform.cleaned_data['cExpectDate']
            cFile = meetinginnerform.cleaned_data['cFile']
            innerunit = MeetingInner.objects.create(innermeeting=innermeeting,cNumber = cNumber,cContent=cContent, cDoPerson=cDoPerson, cExpectDate=cExpectDate, cStartDate=cStartDate,cFile=cFile)
            innerunit.save()

            return redirect('/meetinginnerIndex/'+str(innermeeting.cNumber)+'/')
        else:
             message="驗證錯誤"
    else:
         message='無一定要新增的選項'
    meetinginnerform = MeetingInnerForm()
    return render(request, "meetinginnerPost.html", locals())

def meetinginnerEdit(request,id=None,mode=None,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    index = Meeting.objects.get(cNumber = cNumber)
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = MeetingInner.objects.get(id=id)  #取得要修改的資料記
        return render(request, "meetinginnerEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = MeetingInner.objects.get(id=id)  #取得要修改的資料記錄
        unit.cContent = request.POST['cContent']
        unit.cDoPerson=request.POST['cDoPerson']
        unit.cExpectDate=request.POST['cExpectDate']
        unit.cStartDate=request.POST['cStartDate']
        unit.save()  #寫入資料庫

        message = '已修改...'
        return redirect('/meetinginnerIndex/'+str(index.cNumber)+'/')

def meetingfileEdit(request,id=None,mode=None,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = MeetingInner.objects.get(id=id)  #取得要修改的資料記  
        return render(request, "meetingfileEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = MeetingInner.objects.get(id=id)  #取得要修改的資料記錄
        try:
            unit.cFile = request.FILES['cFile']
        except:
            unit.cFile = request.POST["cFile"]
        unit.save()  #寫入資料庫

        message = '已修改...'
        return redirect('/meetinginnerIndex/'+str(cNumber)+'/')

def meetinginnerIndex(request,cNumber=None):
    home = Home.objects.get(cNumber = cNumber)
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    allPerson = Home.objects.filter(cReceive = firstname)
    allpersonCount = len(allPerson)
    id = Meeting.objects.get(cNumber = cNumber)
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(cContent__icontains=q) | Q(cDoPerson__icontains=q) | Q(cExpectDate__icontains=q) | Q(cStartDate__icontains=q))
        unitinner = MeetingInner.objects.filter(multiple_q)
    else:
        unitinner = MeetingInner.objects.filter(innermeeting=id).order_by("id")
    allinnerMeetingCount = len(unitinner)
    return render(request, "meetinginnerIndex.html",locals())

def meetinginnerView(request,cNumber=None,id=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    allPerson = Home.objects.filter(cReceive = firstname)
    allpersonCount = len(allPerson)
    home = Meeting.objects.get(cNumber=cNumber)
    meetinginner = MeetingInner.objects.get(id=id)
    return render(request, "meetinginnerView.html",locals())

def meetinginnerDelete(request,id=None,cNumber=None):
    index = Meeting.objects.get(cNumber = cNumber)
    if id!=None:
        if request.method == "POST":  #如果是以POST方式才處理
            id=request.POST['cId'] #取得表單輸入的編號
        try:
            unit = MeetingInner.objects.get(id=id)
            unit.delete()
            return redirect('/meetinginnerIndex/'+str(index.cNumber)+'/')
        except:
            message = "讀取錯誤!"
    return render(request, "meetinginnerDelete.html", locals())

def contactCopyPost(request,cNumber=None,thisNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    home = Home.objects.get(cNumber=cNumber)
    unitinner = Contact.objects.get(cNumber=thisNumber)
    if request.method == 'POST':
        contactform = ContactForm(request.POST)
        if contactform.is_valid():
            cNumber =  home.cNumber
            cAutherManager = unitinner.cAutherManager
            cDecisionDep = unitinner.cDecisionDep
            cImplementDep = unitinner.cImplementDep
            cSubject =  home.cSubject
            cDiscription =  unitinner.cDiscription
            unit = Contact.objects.create(home=home, cNumber=cNumber, cAutherManager=cAutherManager, cDecisionDep=cDecisionDep, cSubject=cSubject, cImplementDep=cImplementDep, cDiscription=cDiscription)
            unit.save()  #寫入資料庫

            return redirect('/contactallIndex/')
        else:
             message="執行單位未選填"
    contactform = ContactForm({'cNumber':home.cNumber,'cAutherManager':unitinner.cAutherManager,'cSubject':unitinner.cSubject,'cImplementDep':unitinner.cImplementDep,'cDiscription':unitinner.cDiscription})
    return render(request, "contactCopyPost.html", locals())

# 內部連絡單
def contactPost(request,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    home = Home.objects.get(cNumber=cNumber)
    unitinner = Contact.objects.filter(home=home).order_by("id")
    if request.method == 'POST':
        contactform = ContactForm(request.POST)
        if contactform.is_valid():
            cNumber =  home.cNumber
            cAutherManager = firstname
            cDecisionDep = contactform.cleaned_data['cDecisionDep']
            cImplementDep = contactform.cleaned_data['cImplementDep']
            cSubject =  home.cSubject
            cDiscription =  contactform.cleaned_data['cDiscription']
            try:
                home.cFile = request.FILES['cFile']
            except:
                home.cFile = request.POST["cFile"]
            try:
                home.cFile1 = request.FILES['cFile1']
            except:
                home.cFile1 = request.POST["cFile1"]
            try:
                home.cFile2 = request.FILES['cFile2']
            except:
                home.cFile2 = request.POST["cFile2"]
            try:
                home.cFile3 = request.FILES['cFile3']
            except:
                home.cFile3 = request.POST["cFile3"]
            try:
                home.cFile4 = request.FILES['cFile4']
            except:
                home.cFile4 = request.POST["cFile4"]
            home.save()
            unit = Contact.objects.create(home=home, cNumber=cNumber, cAutherManager=cAutherManager, cDecisionDep=cDecisionDep, cSubject=cSubject, cImplementDep=cImplementDep, cDiscription=cDiscription)
            unit.save()  #寫入資料庫

            return redirect('/transferPost/'+ str(cNumber)+'/')
        else:
             message="決策單位或執行單位未選填"
    else:
         message='所有欄位必須輸入或勾選!'
    contactform = ContactForm({'cNumber':cNumber,"cAutherManager":firstname})
    return render(request, "contactPost.html", locals())


def contactView(request,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    allPerson = Home.objects.filter(cReceive = firstname)
    allpersonCount = len(allPerson)
    home = Home.objects.get(cNumber=cNumber)
    returned = Returned.objects.filter(returnTo=home).order_by("id")
    contact = Contact.objects.get(cNumber=cNumber)
    return render(request, "contactView.html",locals())

def contactallIndex(request):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    allPerson = Home.objects.filter(cReceive = firstname)
    allpersonCount = len(allPerson)
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(cNumber__icontains=q) | Q(cSubject__icontains=q) | Q(cDecisionDep__icontains=q))
        contactall = Contact.objects.filter(multiple_q)
    else:
        contactall = Contact.objects.all().order_by("id")
    contactallCount = len(contactall)
    return render(request, "contactall_Index.html",locals())

def contactEdit(request,id=None,mode=None,cNumber=None):
    homeform = HomeForm(request.POST)
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    unithome = Home.objects.get(cNumber = cNumber)
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = Contact.objects.get(id = id)  #取得要修改的資料記
        strdate=str(unithome.HomeDate)
        strdate2=strdate.replace("年","-")
        strdate2=strdate.replace("月","-")
        strdate2=strdate.replace("日","-")
        unithome.HomeDate = strdate2

        strdate1=str(unithome.cEndDate)
        strdate3=strdate1.replace("年","-")
        strdate3=strdate1.replace("月","-")
        strdate3=strdate1.replace("日","-")
        unithome.cEndDate = strdate3
        return render(request, "contactEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = Contact.objects.get(id = id)#取得要修改的資料記錄
        if unithome.cProgress == "結案":
            unithome.cReceive = request.POST['cReceive']
        else:
            unithome.cAuther = request.POST['cAuther']
            unithome.cSubject = request.POST['cSubject']
            if request.POST['cEndDate'] != "":
                unithome.cEndDate = request.POST['cEndDate']
            else:
                unithome.cEndDate = None
            unit.cDecisionDep=request.POST['cDecisionDep']
            unit.cImplementDep=request.POST['cImplementDep']
            unit.cSubject=unithome.cSubject
            unit.cDiscription=request.POST['cDiscription']
            unit.cAutherManager = unithome.cAuther
            unithome.save()
        unit.save()  #寫入資料庫
        message = '已修改...'
        return redirect('/contactallIndex/')

def contractCopyPost(request,cNumber=None,thisNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    home = Home.objects.get(cNumber=cNumber)
    unitinner = Contract.objects.get(cNumber=thisNumber)
    if request.method == 'POST':
        contractform = ContractForm(request.POST)
        if contractform.is_valid():
            cNumber =  home.cNumber
            cClient = unitinner.cClient
            cLocation = unitinner.cLocation
            cContent = unitinner.cContent
            cPayMode = unitinner.cPayMode
            cBudget =  unitinner.cBudget
            cOther =  unitinner.cOther
            cConfirm =  unitinner.cConfirm
            unit = Contract.objects.create(home=home, cNumber=cNumber, cClient=cClient, cLocation=cLocation, cContent=cContent, cPayMode=cPayMode, cOther=cOther, cBudget=cBudget, cConfirm=cConfirm)
            unit.save()  #寫入資料庫
            return redirect('/contractallIndex/')
        else:
            message="驗證錯誤"
    contractform = ContractForm({'cNumber':home.cNumber,'cClient':unitinner.cClient,'cContent':unitinner.cContent,'cLocation':unitinner.cLocation,'cPayMode':unitinner.cPayMode,'cBudget':unitinner.cBudget,'cOther':unitinner.cOther,'cConfirm':unitinner.cConfirm})
    return render(request, "contractCopyPost.html", locals())

#發包議價表
def contractPost(request,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    home = Home.objects.get(cNumber=cNumber)
    unitinner = Contract.objects.filter(home=home).order_by("id")
    if request.method == 'POST':
        contractform = ContractForm(request.POST)
        if contractform.is_valid():
            cNumber =  home.cNumber
            cClient = contractform.cleaned_data['cClient']
            cLocation = contractform.cleaned_data['cLocation']
            cContent = contractform.cleaned_data['cContent']
            cPayMode = contractform.cleaned_data['cPayMode']
            cBudget =  contractform.cleaned_data['cBudget']
            cOther =  contractform.cleaned_data['cOther']
            cConfirm =  contractform.cleaned_data['cConfirm']
            try:
                home.cFile = request.FILES['cFile']
            except:
                home.cFile = request.POST["cFile"]
            try:
                home.cFile1 = request.FILES['cFile1']
            except:
                home.cFile1 = request.POST["cFile1"]
            try:
                home.cFile2 = request.FILES['cFile2']
            except:
                home.cFile2 = request.POST["cFile2"]
            try:
                home.cFile3 = request.FILES['cFile3']
            except:
                home.cFile3 = request.POST["cFile3"]
            try:
                home.cFile4 = request.FILES['cFile4']
            except:
                home.cFile4 = request.POST["cFile4"]
            home.save()
            unit = Contract.objects.create(home=home, cNumber=cNumber, cClient=cClient, cLocation=cLocation, cContent=cContent, cPayMode=cPayMode, cOther=cOther, cBudget=cBudget, cConfirm=cConfirm)
            unit.save()  #寫入資料庫
            return redirect('/transferPost/'+ str(cNumber)+'/')
            # return redirect('/contractinnerPost/'+cNumber)
        else:
             message="驗證錯誤"
    else:
         message='客戶名稱、工作地點必須輸入或勾選!'
    contractform = ContractForm({'cNumber':cNumber,'cConfirm':"_年_月_日決定以___元整交由__承攬本工程"})
    return render(request, "contractPost.html", locals())


def contractView(request,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    allPerson = Home.objects.filter(cReceive = firstname)
    allpersonCount = len(allPerson)
    home = Home.objects.get(cNumber=cNumber)
    returned = Returned.objects.filter(returnTo=home).order_by("id")
    contract = Contract.objects.get(cNumber=cNumber)
    unitinner = ContractInner.objects.filter(innercontract=contract).order_by("id")
    return render(request, "contractView.html",locals())

def contractallIndex(request):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    allPerson = Home.objects.filter(cReceive = firstname)
    allpersonCount = len(allPerson)
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(cNumber__icontains=q) | Q(cClient__icontains=q) | Q(cLocation__icontains=q) | Q(cContent__icontains=q))
        contractall = Contract.objects.filter(multiple_q)
    else:
        contractall = Contract.objects.all().order_by("id")
    contractallCount = len(contractall)
    return render(request, "contractall_Index.html",locals())

def contractEdit(request,id=None,mode=None,cNumber=None):
    homeform = HomeForm(request.POST)
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    unithome = Home.objects.get(cNumber = cNumber)
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = Contract.objects.get(id = id)  #取得要修改的資料記
        # unit.cConfirm = unit.cConfirm.replace("支票，當月結","").replace("天票","")
        strdate=str(unithome.HomeDate)
        strdate2=strdate.replace("年","-")
        strdate2=strdate.replace("月","-")
        strdate2=strdate.replace("日","-")
        unithome.HomeDate = strdate2

        strdate1=str(unithome.cEndDate)
        strdate3=strdate1.replace("年","-")
        strdate3=strdate1.replace("月","-")
        strdate3=strdate1.replace("日","-")
        unithome.cEndDate = strdate3
        return render(request, "contractEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = Contract.objects.get(id = id)  #取得要修改的資料記錄
        if unithome.cProgress == "結案":
            unithome.cReceive = request.POST['cReceive']
        else:
            unithome.cAuther = request.POST['cAuther']
            unithome.cSubject = request.POST['cSubject']
            if request.POST['cEndDate'] != "":
                unithome.cEndDate = request.POST['cEndDate']
            else:
                unithome.cEndDate = None
            unit.cClient=request.POST['cClient']         
            unit.cLocation=request.POST['cLocation']
            unit.cContent=request.POST['cContent']
            unit.cPayMode=request.POST['cPayMode']
            unit.cBudget = request.POST['cBudget']
            unit.cOther = request.POST['cOther']
            unit.cConfirm=request.POST['cConfirm']
            unithome.save()
        unit.save()  #寫入資料庫

        message = '已修改...'
        return redirect('/contractinnerIndex/'+ str(unithome.cNumber)+'/')
    
#發包議價表-議價記錄
def contractinnerPost(request,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    innercontract = Contract.objects.get(cNumber = cNumber)
    unitinner = ContractInner.objects.filter(innercontract=innercontract).order_by("id")
    if request.method == "POST":  #如果是以POST方式才處理
        contractinnerform = ContractInnerForm(request.POST)  #建立forms物件
        if contractinnerform.is_valid():
            cNumber = cNumber
            cContractor = contractinnerform.cleaned_data['cContractor']
            cQuotation = contractinnerform.cleaned_data['cQuotation']
            cBargain1 = contractinnerform.cleaned_data['cBargain1']
            cBargain2 = contractinnerform.cleaned_data['cBargain2']
            cRemark = contractinnerform.cleaned_data['cRemark']
            innerunit = ContractInner.objects.create(innercontract=innercontract,cNumber = cNumber, cContractor=cContractor, cQuotation=cQuotation, cBargain1=cBargain1, cBargain2=cBargain2, cRemark=cRemark)
            innerunit.save()
            return redirect('/contractinnerIndex/'+str(innercontract.cNumber)+'/')
        else:
             message="驗證錯誤"
    contractinnerform = ContractInnerForm()
    return render(request, "contractinnerPost.html", locals())

def contractinnerEdit(request,id=None,mode=None,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    index = Contract.objects.get(cNumber = cNumber)
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = ContractInner.objects.get(id=id)  #取得要修改的資料記
        return render(request, "contractinnerEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = ContractInner.objects.get(id=id)  #取得要修改的資料記錄
        unit.cContractor = request.POST['cContractor']
        unit.cQuotation=request.POST['cQuotation']
        unit.cBargain1=request.POST['cBargain1']
        unit.cBargain2=request.POST['cBargain2']
        unit.cRemark=request.POST['cRemark']
        unit.save()  #寫入資料庫

        message = '已修改...'
        return redirect('/contractinnerIndex/'+str(index.cNumber)+'/')

def contractinnerIndex(request,cNumber=None):
    home = Home.objects.get(cNumber = cNumber)
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    allPerson = Home.objects.filter(cReceive = firstname)
    allpersonCount = len(allPerson)
    id = Contract.objects.get(cNumber = cNumber)
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(cContractor__icontains=q) | Q(cRemark__icontains=q))
        unitinner = ContractInner.objects.filter(multiple_q)
    else:
        unitinner = ContractInner.objects.filter(innercontract=id).order_by("id")
    allinnerContractCount = len(unitinner)
    return render(request, "contractinnerIndex.html",locals())

def contractinnerView(request,cNumber=None,id=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    allPerson = Home.objects.filter(cReceive = firstname)
    allpersonCount = len(allPerson)
    home = Contract.objects.get(cNumber=cNumber)
    contractinner = ContractInner.objects.get(id=id)
    return render(request, "contractinnerView.html",locals())

def contractinnerDelete(request,id=None,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    index = Contract.objects.get(cNumber = cNumber)
    if id!=None:
        if request.method == "POST":  #如果是以POST方式才處理
            id=request.POST['cId'] #取得表單輸入的編號
        try:
            unit = ContractInner.objects.get(id=id)
            unit.delete()
            return redirect('/contractinnerIndex/'+str(index.cNumber)+'/')
        except:
            message = "讀取錯誤!"
    return render(request, "contractinnerDelete.html", locals())

def changeCopyPost(request,cNumber=None,thisNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    home = Home.objects.get(cNumber=cNumber)
    unitinner = Change.objects.get(cNumber=thisNumber)
    if request.method == 'POST':
        changeform = ChangeForm(request.POST)
        if changeform.is_valid():
            cNumber =  home.cNumber
            cProjectName = unitinner.cProjectName
            cChangeitem = unitinner.cChangeitem
            cChangereason = unitinner.cChangereason
            cHowChange = unitinner.cHowChange
            cAffectitem = unitinner.cAffectitem
            cRisk =  unitinner.cRisk
            cKeypoint = unitinner.cKeypoint
            cCC =  unitinner.cCC
            cEarn = unitinner.cEarn
            cTech_bulletin = unitinner.cTech_bulletin
            cUndertaker =  unitinner.cUndertaker
            cOption_FS =  changeform.cleaned_data['cOption_FS']
            cFs_Sign =  changeform.cleaned_data['cFs_Sign']
            cOption_Design =  changeform.cleaned_data['cOption_Design']
            cDesign_Sign =  changeform.cleaned_data['cDesign_Sign']
            cOption_Quality =  changeform.cleaned_data['cOption_Quality']
            cQuality_Sign =  changeform.cleaned_data['cQuality_Sign']
            cOption_Purchase =  changeform.cleaned_data['cOption_Purchase']
            cPurchase_Sign = changeform.cleaned_data['cPurchase_Sign']
            unit = Change.objects.create(home=home, cNumber=cNumber, cProjectName=cProjectName, cChangeitem=cChangeitem, cChangereason=cChangereason, cAffectitem=cAffectitem,
                                          cRisk=cRisk,cKeypoint=cKeypoint, cOption_FS=cOption_FS,cOption_Design=cOption_Design,
                                          cOption_Quality=cOption_Quality,cOption_Purchase=cOption_Purchase,cCC=cCC,cEarn=cEarn,
                                          cTech_bulletin=cTech_bulletin,cUndertaker=cUndertaker,cFs_Sign=cFs_Sign,cDesign_Sign=cDesign_Sign,cQuality_Sign=cQuality_Sign,
                                          cPurchase_Sign=cPurchase_Sign,cHowChange=cHowChange)
            unit.save()  #寫入資料庫

            return redirect('/changeallIndex/')
        else:
             message="副本未選填"
    else:
         message='專案名稱和副本必須輸入或勾選'
    changeform = ChangeForm({'cProjectName':unitinner.cProjectName,'cCC':unitinner.cCC})
    return render(request, "changeCopyPost.html", locals())

#設計變更通知單
def changePost(request,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    home = Home.objects.get(cNumber=cNumber)
    unitinner = Change.objects.filter(home=home).order_by("id")
    if request.method == 'POST':
        changeform = ChangeForm(request.POST)
        if changeform.is_valid():
            cNumber =  home.cNumber
            cProjectName = changeform.cleaned_data['cProjectName']
            cChangeitem = changeform.cleaned_data['cChangeitem']
            cChangereason = changeform.cleaned_data['cChangereason']
            cHowChange = changeform.cleaned_data['cHowChange']
            cAffectitem = changeform.cleaned_data['cAffectitem']
            cRisk =  changeform.cleaned_data['cRisk']
            cKeypoint =  changeform.cleaned_data['cKeypoint']
            cCC =  changeform.cleaned_data['cCC']
            cEarn = changeform.cleaned_data['cEarn']
            cTech_bulletin = changeform.cleaned_data['cTech_bulletin']
            cUndertaker =  changeform.cleaned_data['cUndertaker']
            cOption_FS =  changeform.cleaned_data['cOption_FS']
            cFs_Sign =  changeform.cleaned_data['cFs_Sign']
            cOption_Design =  changeform.cleaned_data['cOption_Design']
            cDesign_Sign =  changeform.cleaned_data['cDesign_Sign']
            cOption_Quality =  changeform.cleaned_data['cOption_Quality']
            cQuality_Sign =  changeform.cleaned_data['cQuality_Sign']
            cOption_Purchase =  changeform.cleaned_data['cOption_Purchase']
            cPurchase_Sign = changeform.cleaned_data['cPurchase_Sign']
            try:
                home.cFile = request.FILES['cFile']
            except:
                home.cFile = request.POST["cFile"]
            try:
                home.cFile1 = request.FILES['cFile1']
            except:
                home.cFile1 = request.POST["cFile1"]
            try:
                home.cFile2 = request.FILES['cFile2']
            except:
                home.cFile2 = request.POST["cFile2"]
            try:
                home.cFile3 = request.FILES['cFile3']
            except:
                home.cFile3 = request.POST["cFile3"]
            try:
                home.cFile4 = request.FILES['cFile4']
            except:
                home.cFile4 = request.POST["cFile4"]
            home.save()
            unit = Change.objects.create(home=home, cNumber=cNumber, cProjectName=cProjectName, cChangeitem=cChangeitem, cChangereason=cChangereason, cAffectitem=cAffectitem,
                                          cRisk=cRisk,cKeypoint=cKeypoint, cOption_FS=cOption_FS,cOption_Design=cOption_Design,
                                          cOption_Quality=cOption_Quality,cOption_Purchase=cOption_Purchase,cCC=cCC,cEarn=cEarn,
                                          cTech_bulletin=cTech_bulletin,cUndertaker=cUndertaker,cFs_Sign=cFs_Sign,cDesign_Sign=cDesign_Sign,cQuality_Sign=cQuality_Sign,
                                          cPurchase_Sign=cPurchase_Sign,cHowChange=cHowChange)
            unit.save()  #寫入資料庫

            return redirect('/transferPost/'+ str(cNumber)+'/')
            # return redirect('/changeallIndex/')
        else:
             message="副本未選填"
    else:
         message='專案名稱和副本必須輸入或勾選'
    changeform = ChangeForm()
    return render(request, "changePost.html", locals())

def changeView(request,cNumber=None):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    allPerson = Home.objects.filter(cReceive = firstname)
    allpersonCount = len(allPerson)
    home = Home.objects.get(cNumber=cNumber)
    returned = Returned.objects.filter(returnTo=home).order_by("id")
    change = Change.objects.get(cNumber=cNumber)
    return render(request, "changeView.html",locals())

def changeallIndex(request):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    allPerson = Home.objects.filter(cReceive = firstname)
    allpersonCount = len(allPerson)
    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(cNumber__icontains=q) | Q(cProjectName__icontains=q) | Q(cChangeitem__icontains=q) | Q(cChangereason__icontains=q) | Q(cHowChange__icontains=q))
        changeall = Change.objects.filter(multiple_q)
    else:
        changeall = Change.objects.all().order_by("id")
    changeallCount = len(changeall)
    return render(request, "changeall_Index.html",locals())

def changeEdit(request,id=None,mode=None,cNumber=None):
    homeform = HomeForm(request.POST)
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title
    unithome = Home.objects.get(cNumber = cNumber)
    if mode == "load":  # 由 index.html 按 編輯二 鈕
        unit = Change.objects.get(id = id)  #取得要修改的資料記
        strdate=str(unithome.HomeDate)
        strdate2=strdate.replace("年","-")
        strdate2=strdate.replace("月","-")
        strdate2=strdate.replace("日","-")
        unithome.HomeDate = strdate2

        strdate1=str(unithome.cEndDate)
        strdate3=strdate1.replace("年","-")
        strdate3=strdate1.replace("月","-")
        strdate3=strdate1.replace("日","-")
        unithome.cEndDate = strdate3
        return render(request, "changeEdit.html", locals())
    elif mode == "save": # 由 edit2.html 按 submit
        unit = Change.objects.get(id = id)  #取得要修改的資料記錄
        if unithome.cProgress == "結案":
            unithome.cReceive = request.POST['cReceive']
        else:
            unithome.cAuther = request.POST['cAuther']
            unithome.cSubject = request.POST['cSubject']
            if request.POST['cEndDate'] != "":
                unithome.cEndDate = request.POST['cEndDate']
            else:
                unithome.cEndDate = None
            unit.cProjectName=request.POST['cProjectName']
            unit.cChangeitem=request.POST['cChangeitem']
            unit.cChangereason=request.POST['cChangereason']
            unit.cHowChange=request.POST['cHowChange']
            unit.cAffectitem = request.POST['cAffectitem']
            unit.cRisk = request.POST['cRisk']
            unit.cEarn = request.POST['cEarn']
            unit.cKeypoint=request.POST['cKeypoint']
            unit.cCC = request.POST['cCC']
            unit.cTech_bulletin=request.POST['cTech_bulletin']
            unit.cUndertaker = request.POST['cUndertaker']
            if position == "廠務部":
                unit.cOption_FS=request.POST['cOption_FS']
                unit.cFs_Sign = request.POST['cFs_Sign']
            elif position == '業務設計部':
                unit.cOption_Design=request.POST['cOption_Design']
                unit.cDesign_Sign = request.POST['cDesign_Sign'] 
            elif position == '品管課':
                unit.cOption_Quality=request.POST['cOption_Quality']
                unit.cQuality_Sign = request.POST['cQuality_Sign']
            elif position == '採購':
                unit.cOption_Purchase = request.POST['cOption_Purchase']
                unit.cPurchase_Sign = request.POST['cPurchase_Sign']
            unithome.save()

        unit.save()  #寫入資料庫

        message = '已修改...'
        return redirect('/changeallIndex/')
    
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username,password=password)
            # user = User.objects.all()
            # 如果找到匹配的用户，将其存储在 session 中，表示已登录
            request.session['user_id'] = user.id
            return redirect('/homeIndex/')  # 登录成功后重定向到仪表板或其他页面
        except User.DoesNotExist:
            print("abbb")
            # 如果未找到用户，可以返回登录页面或显示错误消息
            message = "登入失敗"
            return render(request, 'login.html', {'message': message})
            
    return render(request, 'login.html')

def logout(request):
	auth.logout(request)
	return redirect('/login/')

def HomePage(request):
	if request.user.is_authenticated:
		name=request.user.username
		firstname = request.user.first_name
	return render(request, "HomePage.html", locals())

def message(request):
    if 'user_id' in request.session:  # 假设你的用户 ID 存在于 session 中
        user_id = request.session['user_id']
        user = User.objects.get(pk=user_id)  # 获取当前登录用户信息
        firstname = user.name  # 传递用户名到模板中
        position = user.Position
        title = user.title 
    today = datetime.now().date()
    thirty_days_ago = (datetime.now() - timedelta(days=30)).date()
    homes = Home.objects.filter(cEndDate__gte=thirty_days_ago).order_by('-id')
    allPerson = Home.objects.filter(cReceive = firstname)
    allpersonCount = len(allPerson)
    temp=[]
    for home in homes:
        if (home.cProgress == "駁回" or home.cProgress == "結案"):
            homes = Home.objects.get(cNumber=home.cNumber)
            returned = Returned.objects.filter(returnTo=homes)
            if(len(returned)>0):
                last_returned = returned.last()
                temp.append({"cNumber":home.cNumber,'cEndDate':home.cEndDate,'subject':home.cSubject,'type':home.cProgress,'how':last_returned.cIllustrate,"people":home.cAuther})
            else:
                temp.append({"cNumber":"",'type':"",'how':""})
            
    Transfer = Transfered.objects.all()
    time = datetime.now()
    return render(request, "message.html",locals())
    