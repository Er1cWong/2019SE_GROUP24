from django.shortcuts import render
import json

# Create your views here.
from django.shortcuts import HttpResponse #导入HttpResponse模块
from .models import DataSet, UserProfile
from time import sleep
def index(request):
    data = DataSet.objects.all()#全选
    from_date = time_to_date('2018/10/30')
    to_date = time_to_date('2018/10/30')
    a_data = DateFilter(data,from_date,to_date)
    result = {}
    for a in data:
        if a.dispose_unit_name != '-':
            result[a.dispose_unit_name] = int(a.dispose_unit_id)
    for k in sorted(result,key=result.__getitem__):
        print("<option value=\"%s\" />" % (k))
    #data = DataSet.objects.filter(event_src_name='12345').order_by('field_id')#筛选-升序
    #data = DataSet.objects.exclude(event_property_name='投诉').order_by('-field_id')#过滤-降序
    return render(request,'index.html',{'data':a_data})#通过render模块把index.html这个文件返回到前端，并且返回给了前端一个变量data，在写html时可以调用这个data

def study(request):
    if not request.is_ajax():
        return render(request,'study.html')

    is_change = request.GET.get('change')
    is_back = request.GET.get('back')
    if is_back == 'true':
        # 回滚到10000
        DataSet.objects.filter(occur_place='newadd').delete()
        return JsonResponse({'recall':"back end"})
    elif is_change == 'true':
        data = DataSet.objects.all()#全选
        from_date = time_to_date('2018/11/1')
        to_date = time_to_date(request.GET.get('to_date'))
        a_data = DateFilter(data,from_date,to_date)
        id = 0
        for a in data:
            if a.field_id > id:
                id = a.field_id
        for a in a_data:
            id+=1
            DataSet.objects.create(
                field_id = id,
                report_num = a.report_num,
                create_time = '2018/10/30  12:00',
                district_name = a.district_name,
                district_id = a.district_id,
                street_name = a.street_name,
                street_id = a.street_id,
                community_name = a.community_name,
                community_id = a.community_id,
                event_type_name = a.event_type_name,
                event_type_id = a.event_type_id,
                main_type_name = a.main_type_name,
                main_type_id = a.main_type_id,
                sub_type_name = a.sub_type_name,
                sub_type_id = a.sub_type_id,
                dispose_unit_name = a.dispose_unit_name,
                dispose_unit_id = a.dispose_unit_id,
                event_src_name = a.event_src_name,
                event_src_id = a.event_src_id,
                operate_num = a.operate_num ,
                overtime_archive_num = a.overtime_archive_num,
                intime_to_archive_num = a.intime_to_archive_num,
                intime_archive_num = a.intime_to_archive_num,
                event_property_id = a.event_property_id,
                event_property_name = a.event_property_name,
                occur_place = 'newadd'
                )
            sleep(1)
        return JsonResponse({'recall':"change end, add%d" % (len(a_data))})
    else:
        return JsonResponse({'recall':"error"})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .forms import RegistrationForm, LoginForm#, ProfileForm, PwdChangeForm
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction


def register(request):
    if request.method == 'POST':

        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            #email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            unit_name = form.cleaned_data['unit_name']

            # 使用内置User自带create_user方法创建用户，不需要使用save()
            user = User.objects.create_user(username=username, password=password)

            # 如果直接使用objects.create()方法后不需要使用save()
            user_profile = UserProfile(user=user,username=username,unit_name=unit_name)
            user_profile.save()

            return HttpResponseRedirect("/accounts/login/")

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def login(request):
    nexturl = '/HomePage/'
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)
                return redirect(nexturl)

            else:
                # 登陆失败
                 return render(request, 'login.html', {'form': form,
                               'message': '密码错误，请重试'})
        else:
            return render(request, "login.html", {'form': form,
                               'message': '用户不存在'})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
@login_required
def HomePage(request):
    return render(request,'HomePage.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse(login))

def getdaterange(request):
    fd = request.GET.get('from_date')
    td = request.GET.get('to_date')
    if fd is None or fd == '':
        fd = "2018-10-30"
    if td is None or td == '':
        td = "2018-10-30"
    return fd,td
@login_required
def show1(request):#展示特定时间范围内的“问题性质”的数目
    if not request.is_ajax():
        return render(request,'show1.html')
    data = DataSet.objects.all()#全选
    fd,td = getdaterange(request)
    from_date = time_to_date(fd)
    to_date = time_to_date(td)
    a_data = DateFilter(data,from_date,to_date)
    result = {}
    count = 0
    for a in a_data:
        if a.event_property_name != '-':
            result[a.event_property_name] = 0
            count+=1
    if count == 0:
        return JsonResponse({'isnone':True,'result':[]})
    for a in a_data:
        if a.event_property_name != '-':
            result[a.event_property_name] += 100/count
    show_result = [{'name':r[0],'y':r[1]} for r in result.items()]
    return JsonResponse({'isnone':False,'result':show_result})

@login_required
def show2(request):#展示今日和特定月份下的各街道民生事件情况
    if not request.is_ajax():
        return render(request,'show2.html')
    data = DataSet.objects.all()#全选
    istoday = request.GET.get('istoday')
    month = request.GET.get('month')
    if istoday is None or istoday == 'true':
        fd = "2018-10-30"
        td = "2018-10-30"
        from_date = time_to_date(fd)
        to_date = time_to_date(td)
        a_data = DateFilter(data,from_date,to_date)
    else:
        a_data = MonthFilter(data,month)
    result_a = {}
    result_b = {}
    count = 0
    for a in a_data:
        if a.street_name != '-':
            result_a[a.street_name] = {}
            result_b[a.event_type_name] = {}
            count+=1
    if count == 0:
        return JsonResponse({'isnone':True,'streets':[],'result':[]})
    streets = [r[0] for r in result_a.items()]
    main_types=[r[0] for r in result_b.items()]
    for x in main_types:
        for y in streets:
            result_b[x][y] = 0
    for a in a_data:
        if a.street_name != '-':
            result_b[a.event_type_name][a.street_name] += 1
    show_result = [{'name':r[0],'data':[rr[1] for rr in r[1].items()]} for r in result_b.items()]
    return JsonResponse({'isnone':False,'streets':streets,'result':show_result})

@login_required
def show3(request):#展示今日/特定月份“热点社区”情况community_name
    if not request.is_ajax():
        return render(request,'show3.html')
    if request.GET.get('isinit') == 'true':
        site = [
        {'lng':114.372841,'lat':22.753346,'community_name':'龙田社区'}, 
        {'lng':114.338203,'lat':22.644538,'community_name':'马峦社区'}, 
        {'lng':114.406461,'lat':22.663744,'community_name':'金龟社区'}, 
        {'lng':114.408079,'lat':22.743131,'community_name':'金沙社区'}, 
        {'lng':114.369312,'lat':22.734866,'community_name':'老坑社区'},
        {'lng':114.395074,'lat':22.715733,'community_name':'竹坑社区'},  
        {'lng':114.381223,'lat':22.746873,'community_name':'秀新社区'}, 
        {'lng':114.295663,'lat':22.67342,'community_name':'碧岭社区'},  
        {'lng':114.390978,'lat':22.697625,'community_name':'石井社区'}, 
        {'lng':114.421943,'lat':22.700351,'community_name':'田心社区'},  
        {'lng':114.410837,'lat':22.697197,'community_name':'田头社区'}, 
        {'lng':114.404444,'lat':22.761764,'community_name':'沙田社区'},  
        {'lng':114.326552,'lat':22.67909,'community_name':'沙湖社区'},  
        {'lng':114.377888,'lat':22.690889,'community_name':'沙坣社区'}, 
        {'lng':114.331079,'lat':22.678805,'community_name':'汤坑社区'}, 
        {'lng':114.362596,'lat':22.69202,'community_name':'江岭社区'},   
        {'lng':114.35474,'lat':22.688096,'community_name':'坪环社区'},  
        {'lng':114.353907,'lat':22.69667,'community_name':'坪山社区'},  
        {'lng':114.390013,'lat':22.753031,'community_name':'坑梓社区'}, 
        {'lng':114.355104,'lat':22.697106,'community_name':'和平社区'},  
        {'lng':114.375607,'lat':22.70534,'community_name':'南布社区'},  
        {'lng':114.336721,'lat':22.69849,'community_name':'六联社区'},   
        {'lng':114.349914,'lat':22.707919,'community_name':'六和社区'}, 
        ]
        return JsonResponse({'points':site})
    data = DataSet.objects.all()#全选
    istoday = request.GET.get('istoday')
    month = request.GET.get('month')
    if istoday is None or istoday == 'true':
        fd = "2018-10-30"
        td = "2018-10-30"
        from_date = time_to_date(fd)
        to_date = time_to_date(td)
        a_data = DateFilter(data,from_date,to_date)
    else:
        a_data = MonthFilter(data,month)
    result = {}
    count = 0
    for a in a_data:
        result[a.community_name] = 0
        count+=1
    if count == 0:
        return JsonResponse({'isnone':True,'viewpoint':[]})
    for a in a_data:
        result[a.community_name] += 1
    viewpoint = getcommunitysite(result)
    return JsonResponse({'isnone':False,'viewpoint':viewpoint})
#社区坐标
def getcommunitysite(result):
    site = [
        {'lng':114.372841,'lat':22.753346,'community_name':'龙田社区'}, 
        {'lng':114.338203,'lat':22.644538,'community_name':'马峦社区'}, 
        {'lng':114.406461,'lat':22.663744,'community_name':'金龟社区'}, 
        {'lng':114.408079,'lat':22.743131,'community_name':'金沙社区'}, 
        {'lng':114.369312,'lat':22.734866,'community_name':'老坑社区'},
        {'lng':114.395074,'lat':22.715733,'community_name':'竹坑社区'},  
        {'lng':114.381223,'lat':22.746873,'community_name':'秀新社区'}, 
        {'lng':114.295663,'lat':22.67342,'community_name':'碧岭社区'},  
        {'lng':114.390978,'lat':22.697625,'community_name':'石井社区'}, 
        {'lng':114.421943,'lat':22.700351,'community_name':'田心社区'},  
        {'lng':114.410837,'lat':22.697197,'community_name':'田头社区'}, 
        {'lng':114.404444,'lat':22.761764,'community_name':'沙田社区'},  
        {'lng':114.326552,'lat':22.67909,'community_name':'沙湖社区'},  
        {'lng':114.377888,'lat':22.690889,'community_name':'沙坣社区'}, 
        {'lng':114.331079,'lat':22.678805,'community_name':'汤坑社区'}, 
        {'lng':114.362596,'lat':22.69202,'community_name':'江岭社区'},   
        {'lng':114.35474,'lat':22.688096,'community_name':'坪环社区'},  
        {'lng':114.353907,'lat':22.69667,'community_name':'坪山社区'},  
        {'lng':114.390013,'lat':22.753031,'community_name':'坑梓社区'}, 
        {'lng':114.355104,'lat':22.697106,'community_name':'和平社区'},  
        {'lng':114.375607,'lat':22.70534,'community_name':'南布社区'},  
        {'lng':114.336721,'lat':22.69849,'community_name':'六联社区'},   
        {'lng':114.349914,'lat':22.707919,'community_name':'六和社区'}, 
    ]
    maxcount = max([r[1] for r in result.items()])
    result_name = [r[0] for r in result.items()]
    for a in site:
        if a['community_name'] not in result_name:
            a['count'] = 0
        else:
            a['count'] = result[a['community_name']]*100/maxcount
    return site

@login_required
def show4(request):#展示特定月份/特定季度/当前所有时间范围内“处置中”,“超期结办”，“按期结办”情况,同时还能显示在每个结办情况下“问题类型的情况”。
    #overtime_archive_num 超期办结
    #intime_to_archive_num 处置中
    #intime_archive_num 按期办结
    if not request.is_ajax():
        return render(request,'show4.html')
    data = DataSet.objects.all()#全选
    istoday = request.GET.get('istoday')
    month = request.GET.get('month')
    isseason = request.GET.get('isseason')
    year = request.GET.get('year')
    season = request.GET.get('season')
    if istoday is None or istoday == 'true':
        fd = "2018-10-30"
        td = "2018-10-30"
        from_date = time_to_date(fd)
        to_date = time_to_date(td)
        a_data = DateFilter(data,from_date,to_date)
    else:
        if isseason == 'true':
            if season == '1':
                fd = year+"-1-1"
                td = year+"-3-31"
            elif season == '2':
                fd = year+"-4-1"
                td = year+"-6-30"
            elif season == '3':
                fd = year+"-7-1"
                td = year+"-9-30"
            elif season == '4':
                fd = year+"-10-1"
                td = year+"-12-31"
            from_date = time_to_date(fd)
            to_date = time_to_date(td)
            a_data = DateFilter(data,from_date,to_date)
        else:
            a_data = MonthFilter(data,month)
    result = {'超期办结':{'total':0},'处置中':{'total':0},'按期办结':{'total':0}}
    count = 0
    for a in a_data:##
        if a.overtime_archive_num == 1:
            result['超期办结'][a.event_type_name] = 0
        elif a.intime_to_archive_num == 1:
            result['处置中'][a.event_type_name] = 0
        elif a.intime_archive_num == 1:
            result['按期办结'][a.event_type_name] = 0
        count+=1
    for a in a_data:
        if a.overtime_archive_num == 1:
            result['超期办结'][a.event_type_name] += 100/count
            result['超期办结']['total'] += 100/count
        elif a.intime_to_archive_num == 1:
            result['处置中'][a.event_type_name] += 100/count
            result['处置中']['total'] += 100/count
        elif a.intime_archive_num == 1:
            result['按期办结'][a.event_type_name] += 100/count
            result['按期办结']['total'] += 100/count
    viewcategories = [r[0] for r in result.items()]
    viewy = [r[1]['total'] for r in result.items()]
    dcategorie = [[rr[0] for rr in r[1].items()] for r in result.items()]
    for k in dcategorie:
        del k[0]
    viewdcategorie = dcategorie
    ddata = [[rr[1] for rr in r[1].items()] for r in result.items()]
    for k in ddata:
        del k[0]
    viewddata = ddata
    if count == 0:
        isnone = True
    else:
        isnone = False
    return JsonResponse({'isnone':isnone,'viewcategories':viewcategories,'viewy':viewy,'viewdcategorie':viewdcategorie,'viewddata':viewddata})


#日期筛选
def time_to_date(time_string):
    date = {}
    for i in range(len(time_string)):
        if time_string[i]=='/' or time_string[i]=='-':
            break
    date['year'] = int(time_string[:i])
    st = i+1
    for i in range(st,len(time_string)):
        if time_string[i]=='/' or time_string[i]=='-':
            break
    date['month']= int(time_string[st:i])
    st = i+1
    for i in range(st,len(time_string)):
        if time_string[i]==' ':
            i-=1
            break
    date['day']  = int(time_string[st:i+1])
    return date
def is_dateinrange(date,from_date,to_date):
    if date['year'] < from_date['year']:
        return False
    elif date['year'] == from_date['year']:
        if date['month'] < from_date['month']:
            return False
        elif date['month'] == from_date['month']:
            if date['day'] < from_date['day']:
                return False
    if date['year'] > to_date['year']:
        return False
    elif date['year'] == to_date['year']:
        if date['month'] > to_date['month']:
            return False
        elif date['month'] == to_date['month']:
            if date['day'] > to_date['day']:
                return False
    return True
def DateFilter(data,from_date,to_date):
    filterdata = []
    for a in data:
        createdate = time_to_date(a.create_time)
        if is_dateinrange(createdate,from_date,to_date):
            filterdata.append(a)
    return filterdata
def time_to_month(month_string):
    date = {}
    for i in range(len(month_string)):
        if month_string[i]=='-':
            break
    date['year'] = int(month_string[:i])
    st = i+1
    date['month']= int(month_string[st:len(month_string)])
    return date
def is_monthinrange(date,month):
    if date['year'] != month['year']:
        return False
    elif date['month'] != month['month']:
        return False
    return True
def MonthFilter(data,month_string):
    filterdata = []
    month = time_to_month(month_string)
    for a in data:
        createdate = time_to_date(a.create_time)
        if is_monthinrange(createdate,month):
            filterdata.append(a)
    return filterdata

@login_required
#2018年10月30日street_name的community_name从event_src_name接到sub_type_name event_property_name，请dispose_unit_name尽快前往处理。
def AbnormalEvents(request):
    data = DataSet.objects.all()#全选
    from_date = time_to_date('2018/10/30')
    to_date = time_to_date('2018/10/30')
    #user_unit = UserProfile.objects.get(user_id = request.user.id).unit_name
    a_data = DateFilter(data,from_date,to_date)
    result = []
    for a in a_data:
        #if user_unit is None or a.dispose_unit_name == user_unit:
            a_result = {}
            a_result['street_name']         = a.street_name
            a_result['community_name']      = a.community_name
            a_result['event_src_name']      = a.event_src_name
            a_result['sub_type_name']       = a.sub_type_name
            a_result['event_property_name'] = a.event_property_name
            a_result['dispose_unit_name']   = a.dispose_unit_name
            result.append(a_result)
    return render(request,'AbnormalEvents.html',{'result':result})

def alarm(request,maxid = [0]):
    if request.is_ajax():
        if request.GET.get('intime') == 'true':
            data = DataSet.objects.filter(field_id__gt = maxid[-1])
        else:
            data = DataSet.objects.all()#全选
        id = 0
        for a in data:
            if a.field_id > id:
                id = a.field_id
        if id != 0:
            maxid.append(id)
            from_date = time_to_date('2018/10/30')
            to_date = time_to_date('2018/10/30')
            a_data = DateFilter(data,from_date,to_date)
            #user_unit = UserProfile.objects.get(user_id = request.user.id).unit_name
            result = []
            for a in a_data:
                #if user_unit is None or a.dispose_unit_name == user_unit:
                if alarm_sub_type(a.sub_type_name):
                    a_result = {}
                    a_result['street_name']         = a.street_name
                    a_result['community_name']      = a.community_name
                    a_result['event_src_name']      = a.event_src_name
                    a_result['sub_type_name']       = a.sub_type_name
                    a_result['event_property_name'] = a.event_property_name
                    a_result['dispose_unit_name']   = a.dispose_unit_name
                    #result.append([a_result,1])
                    result.append(a_result)
            
            return JsonResponse({'result':result})
        else:
            return JsonResponse({'result':[]})
def alarm_sub_type(sub_type):
    those_sub_type = [
    "临时线路隐患",
    "交通事故",
    "供水故障",
    "劳动安全",
    "劳动关系纠纷",
    "医疗事故纠纷",
    "医疗救助",
    "危险用电",
    "危险安全隐患",
    "危险山塘、水库",
    "城镇危房改造",
    "墙体安全隐患",
    "宣传栏存在倾斜、倒塌、严重破损等安全隐患",
    "小区内摆放、堆放物品存在安全隐患或影响卫生、通行",
    "居住场所内存放危险性物品",
    "居住人员隐患",
    "工程建设地质灾害",
    "市政公园设施隐患",
    "建筑工地存在安全隐患",
    "患者权益",
    "房屋质量安全隐患",
    "招生违法行为",
    "擅自变动或者损坏房屋",
    "擅自开工建设",
    "施工安全隐患",
    "易燃易爆危险品",
    "无证掘路",
    "暗渠化河道和地下排水管渠",
    "有证药店非法行医",
    "未经批准燃放烟花爆竹",
    "未经批准的营业性演出活动",
    "机动车和驾驶员管理",
    "校园内安全隐患",
    "机动车非法营运",
    "校园周边安全隐患",
    "核安全",
    "消防设施无法正常使用",
    "消防设备配备不全",
    "涉嫌从事色情活动",
    "消防通道堵塞",
    "涉嫌聚众赌博",
    "燃气管道破裂",
    "环卫设施隐患",
    "生活污水集污沟渠裸露黑臭",
    "电力设施故障",
    "电动车存消防安全隐患",
    "社区公园设施隐患",
    "私搭乱建",
    "私自砍伐、迁移城市树木",
    "粉尘涉爆隐患",
    "经济违法行为举报",
    "自来水水质发黄等水质问题",
    "股份合作公司纠纷",
    "蚊蝇孳生",
    "自来水管破裂",
    "规划和土地违法行为",
    "跨河桥、河堤、河道破损",
    "违法在建建筑",
    "路肩墙、路堤墙、路垫墙、山坡墙隐患",
    "违法建设",
    "违规使用直排式热水器、强排式热水器",
    "道路塌陷、盖板坍塌",
    "道路桥梁设施隐患",
    "道路破损",
    "道路路面塌陷、凹陷",
    "野生动、植物病虫害",
    "邻里纠纷"
    ]
    if sub_type in those_sub_type:
        return True
    else:
        return False