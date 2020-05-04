from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import PasswordUser, TextInfo, OldPpInfo, NewPpInfo, CreateInfo, ConfirmInfo, SubmitInfo, LoginInfo, SusResult, Image, ClickPoint, ClickPointFail
from django.conf import settings
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from .forms import ImageForm
from django.contrib.auth.models import User, Group
from django.template import RequestContext
import random
import datetime
import math as math
from _datetime import timedelta

# json_serializer = serializers.get_serializer("json")()
# Create your views here.
@login_required
def dashboard(request):
    active_user = PasswordUser.objects.get(username = request.user)
    check_user = ConfirmInfo.objects.filter(uid = active_user)
    if active_user.pw_scheme == 'Alphanumeric':
        if check_user:
            return redirect('test_alphanumeric')
        else:
            return redirect('create_alphanumeric')
    elif active_user.pw_scheme == 'Old Passpoints':
        if check_user:
            return redirect('test_passpoints')
        else:
            return redirect('create_passpoints')
    else:
        if check_user:
            return redirect('test_new_passpoints')
        else:
            return redirect('create_new_passpoints')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        pw_user = request.POST.get('pw_user')
        remember_pw = request.POST.get('remember_pw')
        pw_scheme = request.POST.get('pw_scheme')
        if pw_user == 'on':
            pw_user = 'True'
        else:
            pw_user = 'False'
            return render(request, 'gp/register_fail.html', {})
        if remember_pw == 'on':
            remember_pw = 'True'
        else:
            remember_pw = 'False'
            return render(request, 'gp/register_fail.html', {})
        
        user = User.objects.create_user(email.lower(), email, '1')
        if pw_scheme == 'Alphanumeric':
            my_group = Group.objects.get(name='alphanumeric users')
            my_group.user_set.add(user)
        elif pw_scheme == 'Old Passpoints':
            my_group = Group.objects.get(name='passpoints users')
            my_group.user_set.add(user)
        else:
            my_group = Group.objects.get(name='new passpoints users')
            my_group.user_set.add(user)
        
        password_user = PasswordUser(username=user, first_name=first_name.capitalize(), last_name=last_name.capitalize(), email=email.lower(), gender=gender, age=age, pw_user=pw_user, remember_pw=remember_pw, pw_scheme=pw_scheme)
        password_user.save()

        return render(request, 'gp/register_success.html', {})
    else:
        return render(request, 'gp/register.html', {})

@login_required
def success(request):
    return render(request, 'gp/success.html', {})

@login_required
def sus(request):
    active_user = PasswordUser.objects.get(username = request.user)
    if request.method == 'POST':
        q1 = request.POST.get('q1')
        q2 = request.POST.get('q2')
        q3 = request.POST.get('q3')
        q4 = request.POST.get('q4')
        q5 = request.POST.get('q5')
        q6 = request.POST.get('q6')
        q7 = request.POST.get('q7')
        q8 = request.POST.get('q8')
        q9 = request.POST.get('q9')
        q10 = request.POST.get('q10')
        new_survey = SusResult(uid=active_user, q1=q1,q2=q2, q3=q3, q4=q4, q5=q5, q6=q6, q7=q7, q8=q8, q9=q9, q10=q10)
        new_survey.save()
        return render(request, 'gp/success.html', {})        
    else:
        return render(request, 'gp/survey.html', {})

@login_required
def create_alphanumeric(request):
    is_invalid = 'is-invalid'
    active_user = PasswordUser.objects.get(username = request.user)
    if request.method == 'POST':
        email1 = request.POST.get('email1')
        password1 = request.POST.get('password1')
        time_prev = request.POST.get('time_prev')
        if time_prev == '':
            time_prev = 0
        else:
            time_prev = int(time_prev)
        time_create = int(request.POST.get('time'))
        time_create = time_create + time_prev
        m = math.floor(time_create / 60)
        s = time_create % 60
        time = datetime.time(0,m,s)
        check = password_check(password1)
        if check:            
            new_create = CreateInfo(uid=active_user, time_create=time)            
            new_create.save()
            return render(request, 'gp/confirm_alphanumeric.html', {'email1': email1, 'password1': password1})        
        else:
            return render(request, 'gp/create_alphanumeric.html', {'is_invalid': is_invalid, 'time_prev': time_create})
    else:
        return render(request, 'gp/create_alphanumeric.html', {})

@login_required
def confirm_alphanumeric(request):
    is_invalid = 'is-invalid'
    active_user = PasswordUser.objects.get(username = request.user)
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        email1 = request.POST.get('email1')
        password1 = request.POST.get('password1')
        time_prev = request.POST.get('time_prev')
        if time_prev == '':
            time_prev = 0
        else:
            time_prev = int(time_prev)
        time_create = int(request.POST.get('time'))
        time_create = time_create + time_prev
        m = math.floor(time_create / 60)
        s = time_create % 60
        time = datetime.time(0,m,s)
        if password == password1:
            new_alpha = TextInfo(uid=active_user, email=email, password=password)
            new_confirm = ConfirmInfo(uid=active_user, time_confirm=time)
            new_confirm.save()
            new_alpha.save()
            return render(request, 'gp/create_alphanumeric_success.html', {'email': email, 'password': password})
        else:
            return render(request, 'gp/confirm_alphanumeric.html', {'email1': email1, 'password1': password1, 'is_invalid': is_invalid, 'time_prev': time_create})
    else:
        return render(request, 'gp/confirm_alphanumeric.html', {'email1': email, 'password1': password1})

@login_required
def test_alphanumeric(request):
    is_invalid = 'is-invalid'
    active_user = PasswordUser.objects.get(username = request.user)
    login_info = LoginInfo.objects.filter(uid=active_user).order_by('login_period')
    confirm_info = ConfirmInfo.objects.get(uid=active_user)
    confirm_date = confirm_info.date_confirmed
    login_period = login_info.count()
    test_period = login_period + 1
    if LoginInfo.objects.filter(uid=active_user).exists():
        last_login = login_info.latest('date_login')
        last_login = last_login.date_login
    today = timezone.now()
    if login_period == 0:
        d = 1
    elif login_period == 1:
        d = 3
    elif login_period == 2:
        d = 7
    else:
        sus_check = SusResult.objects.get(uid=active_user)
        if sus_check:
            return render(request, 'gp/complete.html', {})
        else:
            return render(request, 'gp/login_success.html', {'test_period': test_period})
    test_date = confirm_date + timedelta(days=d)
    if today >= test_date:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            text_info = TextInfo.objects.get(uid=active_user)
            time_prev = request.POST.get('time_prev')
            if time_prev == '':
                time_prev = 0
            else:
                time_prev = int(time_prev)
            time_create = int(request.POST.get('time'))
            time_create = time_create + time_prev
            m = math.floor(time_create / 60)
            s = time_create % 60
            time = datetime.time(0,m,s)
            if email == text_info.email and password == text_info.password:
                new_submit = SubmitInfo(uid=active_user, time_submit=time)
                new_login = LoginInfo(uid=active_user, time_login=time, login_period=test_period)
                new_submit.save()
                new_login.save()
                return render(request, 'gp/login_success.html', {'test_period': test_period, 'test_date': test_date})
            else:
                return render(request, 'gp/test_alphanumeric.html', {'is_invalid': is_invalid, 'test_period': test_period, 'time_prev': time_create})
        return render(request, 'gp/test_alphanumeric.html', {'test_period': test_period})
    else:
        return render(request, 'gp/login_wait.html', {'test_date': test_date})

@login_required
def create_passpoints(request):
    active_user = PasswordUser.objects.get(username = request.user)
    nature_images = Image.objects.filter(category='Nature')
    food_images = Image.objects.filter(category='Food')
    animal_images = Image.objects.filter(category='Animal')
    sports_images = Image.objects.filter(category='Sports')
    cars_images = Image.objects.filter(category='Cars')
    art_images = Image.objects.filter(category='Art')
    if request.method == 'POST':
        time_prev = request.POST.get('time_prev')
        if time_prev == None or time_prev == '':
                time_prev = 0
        else:
            time_prev = int(time_prev)
        time_create = request.POST.get('time')
        if time_create == None or '':
            time_create = request.POST.get('time1')
        time_create = int(time_create) + time_prev
        m = math.floor(time_create / 60)
        s = time_create % 60
        time = datetime.time(0,m,s)
        key = request.POST.get('image')
        image = Image.objects.get(pk=key)
        return render(request, 'gp/create_oldpp2.html', {'image': image, 'time_prev': time_create})
    else:
        return render(request, 'gp/create_oldpp1.html', {'nature_images': nature_images, 'food_images': food_images, 'animal_images': animal_images, 'sports_images': sports_images, 'cars_images': cars_images, 'art_images': art_images})

@login_required
def create_passpoints2(request):
    active_user = PasswordUser.objects.get(username = request.user)
    if request.method == 'POST':
        time_prev = request.POST.get('time_prev')
        if time_prev == '':
            time_prev = request.POST.get('time_prev1')
        if time_prev == '':
            time_prev = 0
        else:
            time_prev = int(time_prev)
        time_create = int(request.POST.get('time'))
        if time_create == '':
            time_create = int(request.POST.get('time1'))
        time_create = time_create + time_prev
        m = math.floor(time_create / 60)
        s = time_create % 60
        time = datetime.time(0,m,s)
        pk = request.POST.get('image')
        image = Image.objects.get(pk=pk)
        cpCount = request.POST.get('cpCount')
        cpCount = int(cpCount)
        i = 1
        while i <= cpCount:
            x = request.POST.get("x"+str(i))
            y = request.POST.get("y"+str(i))
            r = request.POST.get("r"+str(i))
            g = request.POST.get("g"+str(i))
            b = request.POST.get("b"+str(i))
            a = request.POST.get("a"+str(i))
            cp = request.POST.get("cp"+str(i))
            new_cp = ClickPoint(iid=image, uid=active_user, x_location=x, y_location=y, color=r+g+b+a, order=cp, img_number=999)
            new_cp.save()
            newc_oldpp = OldPpInfo(uid=active_user, cp_id=new_cp)
            newc_oldpp.save()
            i+=1
        new_create = CreateInfo(uid=active_user, time_create=time)
        new_create.save()
        passpoints = OldPpInfo.objects.filter(uid=active_user).order_by('cp_id')
        clickpoints = ClickPoint.objects.filter(uid=active_user).order_by('order')
        return render(request, 'gp/confirm_oldpp.html', {'image': image, 'cpCount': cpCount, 'clickpoints': clickpoints, 'passpoints': passpoints})
    else:
        return render(request, 'gp/create_oldpp2.html', {'image': image, 'time_prev': time_create})

@login_required
def confirm_passpoints(request):
    active_user = PasswordUser.objects.get(username = request.user)
    if request.method == 'POST':
        time_prev = request.POST.get('time_prev')
        if time_prev == '':
            time_prev = 0
        else:
            time_prev = int(time_prev)
        time_create = int(request.POST.get('time'))
        time_create = time_create + time_prev
        m = math.floor(time_create / 60)
        s = time_create % 60
        time = datetime.time(0,m,s)
        operation = request.POST.get('operation')
        if operation == 'retry':
            ClickPoint.objects.filter(uid=active_user).delete()
            return redirect('create_passpoints')
        else:
            new_confirm = ConfirmInfo(uid=active_user, time_confirm=time)
            new_confirm.save()
            return render(request, 'gp/success.html', {})
    passpoints = OldPpInfo.objects.filter(uid=active_user).order_by('cp_id')
    clickpoints = ClickPoint.objects.filter(uid=active_user).order_by('order')
    one_cp = clickpoints.objects.get()
    image = one_cp.uid
    cpNum = len(passpoints)
    return render(request, 'gp/confirm_oldpp.html', {'passpoints': passpoints, 'clickpoints': clickpoints, 'cpNum': cpNum, 'time_prev': time_create})

@login_required
def test_passpoints(request):
    is_invalid = 'is-invalid'
    active_user = PasswordUser.objects.get(username = request.user)
    login_info = LoginInfo.objects.filter(uid=active_user).order_by('login_period')
    oldpps = OldPpInfo.objects.filter(uid=active_user).order_by('pk')
    oldpp_len = len(oldpps)
    img_key = oldpps.first().cp_id.iid.pk
    img = Image.objects.get(pk=img_key)
    images = Image.objects.all().order_by('?')[:8]
    confirm_info = ConfirmInfo.objects.get(uid=active_user)
    confirm_date = confirm_info.date_confirmed
    login_period = login_info.count()
    test_period = login_period + 1
    if LoginInfo.objects.filter(uid=active_user).exists():
        last_login = login_info.latest('date_login')
        last_login = last_login.date_login
    today = timezone.now()
    if login_period == 0:
        d = 1
    elif login_period == 1:
        d = 3
    elif login_period == 2:
        d = 7
    else:
        try:
            sus_check = SusResult.objects.get(uid=active_user)
        except SusResult.DoesNotExist:
            sus_check = None
        if sus_check:
            return render(request, 'gp/complete.html', {})
        else:
            return render(request, 'gp/login_success.html', {'test_period': test_period})
    test_date = confirm_date + timedelta(days=d)
    if today >= test_date:
        if request.method == 'POST':
            time_prev = request.POST.get('time_prev')
            if time_prev == '':
                time_prev = 0
            else:
                time_prev = int(time_prev)
            time_create = int(request.POST.get('time'))
            time_create = time_create + time_prev
            m = math.floor(time_create / 60)
            s = time_create % 60
            time = datetime.time(0,m,s)
            key = request.POST.get('image')
            image = Image.objects.get(pk=key)
            if image == img:
                img_url = image.image.url
                return render(request, 'gp/test_oldpp2.html', {'img_url': img_url, 'oldpps': oldpps, 'test_period': test_period, 'oldpp_len': oldpp_len, 'image': image, 'time_prev': time_create})
            else:
                return render(request, 'gp/test_oldpp.html', {'img': img, 'images': images, 'test_period': test_period, 'is_invalid': is_invalid, 'time_prev': time_create})
        return render(request, 'gp/test_oldpp.html', {'img': img, 'images': images, 'test_period': test_period})
    else:
        return render(request, 'gp/login_wait.html', {'test_date': test_date})

@login_required
def test_passpoints2(request):
    is_invalid = 'is-invalid'
    active_user = PasswordUser.objects.get(username = request.user)
    login_info = LoginInfo.objects.filter(uid=active_user).order_by('login_period')
    login_period = login_info.count()
    test_period = login_period + 1
    oldpps = OldPpInfo.objects.filter(uid=active_user).order_by('pk')
    oldpp_len = len(oldpps)
    confirm_info = ConfirmInfo.objects.get(uid=active_user)
    confirm_date = confirm_info.date_confirmed
    if LoginInfo.objects.filter(uid=active_user).exists():
        last_login = login_info.latest('date_login')
        last_login = last_login.date_login
    today = timezone.now()
    if login_period == 0:
        d = 1
    elif login_period == 1:
        d = 3
    else:
        d = 7
    test_date = confirm_date + timedelta(days=d)
    img_id = oldpps.first().cp_id.iid.pk
    img_url = oldpps.first().cp_id.iid.image.url
    image = Image.objects.get(pk=img_id)
    context = {}
    context['oldpps'] = oldpps
    context['test_period'] = test_period
    context['oldpp_len'] = oldpp_len
    context['img_url'] = img_url
    context['image'] = image
    if login_period < 3:
        if request.method == 'POST':
            time_prev = request.POST.get('time_prev')
            if time_prev == '':
                time_prev = 0
            else:
                time_prev = int(time_prev)
            time_create = int(request.POST.get('time'))
            time_create = time_create + time_prev
            m = math.floor(time_create / 60)
            s = time_create % 60
            time = datetime.time(0,m,s)
            operation = request.POST.get('operation')
            cpCount = request.POST.get('cpCount')
            
            if operation == 'retry':
                if cpCount == '':
                    context['time_prev'] = time_create
                    return render(request, 'gp/test_oldpp2.html', context)
                else:
                    cpCount = int(cpCount)
                key = request.POST.get('image')
                image = Image.objects.get(pk=key)
                i = 1
                while i <= cpCount:
                    x = int(request.POST.get("x"+str(i)))
                    y = int(request.POST.get("y"+str(i)))
                    r = int(request.POST.get("r"+str(i)))
                    g = int(request.POST.get("g"+str(i)))
                    b = int(request.POST.get("b"+str(i)))
                    a = int(request.POST.get("a"+str(i)))
                    cp = int(request.POST.get("cp"+str(i)))
                    i+=1
                    new_cpfail = ClickPointFail(iid=image, uid=active_user, x_location=x, y_location=y, color=r+g+b+a, order=cp, img_number=999)
                    new_cpfail.save()
                context['time_prev'] = time_create
                return render(request, 'gp/test_oldpp2.html', context)
            else:
                if cpCount == '':
                    context['is_invalid'] = is_invalid
                    context['time_prev'] = time_create
                    return render(request, 'gp/test_oldpp2.html', context)
                else:
                    cpCount = int(cpCount)
                if cpCount != oldpp_len:
                    i = 1
                    while i <= cpCount:
                        x = int(request.POST.get("x"+str(i)))
                        y = int(request.POST.get("y"+str(i)))
                        r = int(request.POST.get("r"+str(i)))
                        g = int(request.POST.get("g"+str(i)))
                        b = int(request.POST.get("b"+str(i)))
                        a = int(request.POST.get("a"+str(i)))
                        cp = int(request.POST.get("cp"+str(i)))
                        i+=1
                        new_cpfail = ClickPointFail(iid=image, uid=active_user, x_location=x, y_location=y, color=r+g+b+a, order=cp, img_number=999)
                        new_cpfail.save()
                    context['is_invalid'] = is_invalid
                    context['time_prev'] = time_create
                    return render(request, 'gp/test_oldpp2.html', context)
                else:
                    image = request.POST.get('image')
                    image = Image.objects.get(pk=img_id)
                    i = 1
                    while i <= cpCount:
                        x = int(request.POST.get("x"+str(i)))
                        y = int(request.POST.get("y"+str(i)))
                        r = int(request.POST.get("r"+str(i)))
                        g = int(request.POST.get("g"+str(i)))
                        b = int(request.POST.get("b"+str(i)))
                        a = int(request.POST.get("a"+str(i)))
                        cp = int(request.POST.get("cp"+str(i)))
                        i+=1
                        check_pp = ClickPoint.objects.get(uid=active_user, order=cp)
                        x_max = int(check_pp.x_location) + 7
                        x_min = int(check_pp.x_location) -7
                        y_max = int(check_pp.y_location) + 7
                        y_min = int(check_pp.y_location) - 7
                        if x > x_max or x < x_min or y > y_max or y < y_min:
                            new_cpfail = ClickPointFail(iid=image, uid=active_user, x_location=x, y_location=y, color=r+g+b+a, order=cp, img_number=999)
                            new_cpfail.save()
                            context['is_invalid'] = is_invalid
                            context['time_prev'] = time_create
                            return render(request, 'gp/test_oldpp2.html', context)
                    new_submit = SubmitInfo(uid=active_user, time_submit=time)
                    new_submit.save()
                    new_login = LoginInfo(uid=active_user, time_login=time, login_period=test_period)
                    new_login.save()
                    return render(request, 'gp/login_success.html', {'active_user': active_user, 'test_period': test_period, 'test_date': test_date})
        else:
            context['time_prev'] = time_create
            return render(request, 'gp/test_oldpp2.html', context)
    else:
        return redirect('/logout')

@login_required
def create_new_passpoints(request):
    active_user = PasswordUser.objects.get(username = request.user)
    nature_images = Image.objects.filter(category='Nature')
    food_images = Image.objects.filter(category='Food')
    animal_images = Image.objects.filter(category='Animal')
    sports_images = Image.objects.filter(category='Sports')
    cars_images = Image.objects.filter(category='Cars')
    art_images = Image.objects.filter(category='Art')
    context = {}
    try:
        newpp_check = NewPpInfo.objects.filter(uid=active_user).exists()
    except NewPpInfo.DoesNotExist:
        newpp_check = None
    if newpp_check:
        new_pp_info = NewPpInfo.objects.filter(uid=active_user).order_by('pk')
        new_pp_row = new_pp_info.latest('img_number')
        img_num = new_pp_row.img_number
        if img_num > 0:
            context['img_num'] = img_num
            # for i in range(1, img_num+1):
            #     img = NewPpInfo.objects.filter(uid=active_user, img_number=i).last()
            #     img_url = img.cp_id.iid.image.url
            #     context["image"+str(i)] = img_url
    if request.method == 'POST':
        time_prev0 = request.POST.get('time_prev')
        time_prev1 = request.POST.get('time_prev1')
        if time_prev0 == None or time_prev0 == '':
            if time_prev1 == None or time_prev1 == '':
                time_prev = 0
            else:
                time_prev = int(time_prev1)
        else:
            time_prev = int(time_prev0)
        time_create = request.POST.get('time')
        if time_create == None or '':
            time_create = request.POST.get('time1')
        time_create = int(time_create) + time_prev
        m = math.floor(time_create / 60)
        s = time_create % 60
        time = datetime.time(0,m,s)
        operation = request.POST.get('operation')
        if operation == 'upload_image':
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                upload = form.save(commit=False)
                upload.category = "User Image"
                upload.save()
                image = Image.objects.latest('date_added')
                context['time_prev'] = time_create
                context['image'] = image
                return render(request, 'gp/create_newpp2.html', context)
        elif operation == 'select_image':
            key = request.POST.get('image')
            image = Image.objects.get(pk=key)
            context['time_prev'] = time_create
            context['image'] = image
            return render(request, 'gp/create_newpp2.html', context)
    else:
        form = ImageForm()
        context['form'] = form
        context['nature_images'] = nature_images
        context['food_images'] = food_images
        context['art_images'] = art_images
        context['sports_images'] = sports_images
        context['cars_images'] = cars_images
        context['animal_images'] = animal_images
        return render(request, 'gp/create_newpp1.html', context)

@login_required
def create_new_passpoints2(request):
    active_user = PasswordUser.objects.get(username = request.user)
    context = {}
    img_number = 1
    new_pp_info = NewPpInfo.objects.filter(uid=active_user).order_by('pk')
    if new_pp_info:
        new_pp_row = new_pp_info.latest('img_number')
        img_num = new_pp_row.img_number
        if img_num:
            context['img_num'] = img_num
        img_number = img_num + 1
    if request.method == 'POST':
        time_prev = request.POST.get('time_prev')
        if time_prev == '':
            time_prev = 0
        else:
            time_prev = int(time_prev)
        time_create = int(request.POST.get('time'))
        time_create = time_create + time_prev
        m = math.floor(time_create / 60)
        s = time_create % 60
        time = datetime.time(0,m,s)
        pk = request.POST.get('image')
        image = Image.objects.get(pk=pk)
        cpCount = request.POST.get('cpCount')
        cpCount = int(cpCount)
        i = 1
        while i <= cpCount:
            x = request.POST.get("x"+str(i))
            y = request.POST.get("y"+str(i))
            r = request.POST.get("r"+str(i))
            g = request.POST.get("g"+str(i))
            b = request.POST.get("b"+str(i))
            a = request.POST.get("a"+str(i))
            cp = request.POST.get("cp"+str(i))
            new_cp = ClickPoint(iid=image, uid=active_user, x_location=x, y_location=y, color=r+g+b+a, order=cp, img_number=img_number)
            new_cp.save()
            new_pp = NewPpInfo(uid=active_user, cp_id=new_cp, img_number=img_number)
            new_pp.save()
            i+=1
        new_create = CreateInfo(uid=active_user, time_create=time)
        new_create.save()
        passpoints = NewPpInfo.objects.filter(uid=active_user, img_number=img_number).order_by('cp_id')
        clickpoints = ClickPoint.objects.filter(uid=active_user, img_number=img_number).order_by('order')
        context['image'] = image
        context['cpCount'] = cpCount
        context['clickpoints'] = clickpoints
        context['passpoints'] = passpoints
        return render(request, 'gp/confirm_newpp.html', context)
    else:
        context['image'] = image
        context['time_prev'] = time_create
        return render(request, 'gp/create_newpp2.html', context)

@login_required
def confirm_new_passpoints(request):
    active_user = PasswordUser.objects.get(username = request.user)
    if request.method == 'POST':
        time_prev = request.POST.get('time_prev')
        if time_prev == '':
            time_prev = 0
        else:
            time_prev = int(time_prev)
        time_create = int(request.POST.get('time'))
        time_create = time_create + time_prev
        m = math.floor(time_create / 60)
        s = time_create % 60
        time = datetime.time(0,m,s)
        operation = request.POST.get('operation')
        if operation == 'retry':
            ClickPoint.objects.filter(uid=active_user).delete()
            return redirect('create_passpoints')
        elif operation == 'confirm':
            new_confirm = ConfirmInfo(uid=active_user, time_confirm=time)
            new_confirm.save()
            return render(request, 'gp/create_new_passpoints_success.html', {})
        else:
            new_confirm = ConfirmInfo(uid=active_user, time_confirm=time)
            new_confirm.save()
            return redirect('create_new_passpoints')
    passpoints = NewPpInfo.objects.filter(uid=active_user).order_by('cp_id')
    cp_last = ClickPoint.objects.filter(uid=active_user).latest()
    image = cp_last.iid
    img_number = cp_last.img_number
    clickpoints = ClickPoint.objects.filter(uid=active_user, iid=image, img_number=img_number).order_by('order')
    cpNum = len(passpoints)
    return render(request, 'gp/confirm_newpp.html', {'passpoints': passpoints, 'clickpoints': clickpoints, 'cpNum': cpNum, 'time_prev': time_create})

@login_required
def test_new_passpoints(request):
    is_invalid = 'is-invalid'
    active_user = PasswordUser.objects.get(username = request.user)
    login_info = LoginInfo.objects.filter(uid=active_user).order_by('login_period')
    test_period = login_info.count() + 1
    oldpps = NewPpInfo.objects.filter(uid=active_user).order_by('pk')
    oldpp_len = len(oldpps)
    newpps = oldpps.last()
    img_count = newpps.img_number
    img_fin = request.POST.get('img_fin')
    if img_fin == None:
        img_fin = 1
    else:
        img_fin = int(img_fin)
    if img_fin <= img_count:
        img_key = NewPpInfo.objects.filter(uid=active_user, img_number=img_fin).first()
        img_key = img_key.cp_id.iid.pk
    img = Image.objects.get(pk=img_key)
    images = Image.objects.all().order_by('?')[:8]
    confirm_info = ConfirmInfo.objects.filter(uid=active_user).last()
    confirm_date = confirm_info.date_confirmed
    login_period = login_info.count()
    test_period = login_period + 1
    if LoginInfo.objects.filter(uid=active_user).exists():
        last_login = login_info.latest('date_login')
        last_login = last_login.date_login
    today = timezone.now()
    if login_period == 0:
        d = 1
    elif login_period == 1:
        d = 3
    elif login_period == 2:
        d = 7
    else:
        try:
            sus_check = SusResult.objects.get(uid=active_user)
        except SusResult.DoesNotExist:
            sus_check = None
        if sus_check:
            return render(request, 'gp/complete.html', {})
        else:
            return render(request, 'gp/login_success.html', {'test_period': test_period})
    test_date = confirm_date + timedelta(days=d)
    if today >= test_date:
        if request.method == 'POST':
            time_prev = request.POST.get('time_prev')
            if time_prev == '':
                time_prev = 0
            else:
                time_prev = int(time_prev)
            time_create = int(request.POST.get('time'))
            time_create = time_create + time_prev
            m = math.floor(time_create / 60)
            s = time_create % 60
            time = datetime.time(0,m,s)
            key = request.POST.get('image')
            image = Image.objects.get(pk=key)
            if image == img:
                img_url = image.image.url
                return render(request, 'gp/test_newpp2.html', {'img_url': img_url, 'oldpps': oldpps, 'test_period': test_period, 'oldpp_len': oldpp_len, 'image': image, 'time_prev': time_create, 'img_fin': img_fin})
            else:
                return render(request, 'gp/test_newpp.html', {'img': img, 'images': images, 'test_period': test_period, 'is_invalid': is_invalid, 'time_prev': time_create, 'img_fin': img_fin, 'image': image})
        return render(request, 'gp/test_newpp.html', {'img': img, 'images': images, 'test_period': test_period, 'img_fin': img_fin})
    else:
        return render(request, 'gp/login_wait.html', {'test_date': test_date})

@login_required
def test_new_passpoints2(request):
    is_invalid = 'is-invalid'
    active_user = PasswordUser.objects.get(username = request.user)
    login_info = LoginInfo.objects.filter(uid=active_user).order_by('login_period')
    login_period = login_info.count()
    test_period = login_period + 1
    img_fin = request.POST.get('img_fin')
    oldpps = NewPpInfo.objects.filter(uid=active_user, img_number=img_fin)
    oldpp_len = len(oldpps)
    confirm_info = ConfirmInfo.objects.filter(uid=active_user).last()
    confirm_date = confirm_info.date_confirmed
    if LoginInfo.objects.filter(uid=active_user).exists():
        last_login = login_info.latest('date_login')
        last_login = last_login.date_login
    today = timezone.now()
    if login_period == 0:
        d = 1
    elif login_period == 1:
        d = 3
    else:
        d = 7
    test_date = confirm_date + timedelta(days=d)
    newpps = NewPpInfo.objects.filter(uid=active_user).order_by('pk').last()
    img_count = newpps.img_number
    img_id = oldpps.first().cp_id.iid.pk
    img_url = oldpps.first().cp_id.iid.image.url
    image = Image.objects.get(pk=img_id)
    context = {}
    context['img_fin'] = img_fin
    context['oldpps'] = oldpps
    context['test_period'] = test_period
    context['oldpp_len'] = oldpp_len
    context['img_url'] = img_url
    context['image'] = image
    if login_period < 3:
        if request.method == 'POST':
            time_prev = request.POST.get('time_prev')
            if time_prev == '':
                time_prev = 0
            else:
                time_prev = int(time_prev)
            time_create = int(request.POST.get('time'))
            time_create = time_create + time_prev
            m = math.floor(time_create / 60)
            s = time_create % 60
            time = datetime.time(0,m,s)
            operation = request.POST.get('operation')
            cpCount = request.POST.get('cpCount')
            
            if operation == 'retry':
                if cpCount == '':
                    context['time_prev'] = time_create
                    return render(request, 'gp/test_newpp2.html', context)
                else:
                    cpCount = int(cpCount)
                key = request.POST.get('image')
                image = Image.objects.get(pk=key)
                i = 1
                while i <= cpCount:
                    x = int(request.POST.get("x"+str(i)))
                    y = int(request.POST.get("y"+str(i)))
                    r = int(request.POST.get("r"+str(i)))
                    g = int(request.POST.get("g"+str(i)))
                    b = int(request.POST.get("b"+str(i)))
                    a = int(request.POST.get("a"+str(i)))
                    cp = int(request.POST.get("cp"+str(i)))
                    i+=1
                    new_cpfail = ClickPointFail(iid=image, uid=active_user, x_location=x, y_location=y, color=r+g+b+a, order=cp, img_number=img_fin)
                    new_cpfail.save()
                context['time_prev'] = time_create
                return render(request, 'gp/test_newpp2.html', context)
            else:
                if cpCount == '':
                    context['is_invalid'] = is_invalid
                    context['time_prev'] = time_create
                    return render(request, 'gp/test_newpp2.html', context)
                else:
                    cpCount = int(cpCount)
                if cpCount != oldpp_len:
                    i = 1
                    while i <= cpCount:
                        x = int(request.POST.get("x"+str(i)))
                        y = int(request.POST.get("y"+str(i)))
                        r = int(request.POST.get("r"+str(i)))
                        g = int(request.POST.get("g"+str(i)))
                        b = int(request.POST.get("b"+str(i)))
                        a = int(request.POST.get("a"+str(i)))
                        cp = int(request.POST.get("cp"+str(i)))
                        i+=1
                        new_cpfail = ClickPointFail(iid=image, uid=active_user, x_location=x, y_location=y, color=r+g+b+a, order=cp, img_number=img_fin)
                        new_cpfail.save()
                    context['is_invalid'] = is_invalid
                    context['time_prev'] = time_create
                    return render(request, 'gp/test_newpp2.html', context)
                else:
                    image = request.POST.get('image')
                    image = Image.objects.get(pk=img_id)
                    i = 1
                    while i <= cpCount:
                        x = int(request.POST.get("x"+str(i)))
                        y = int(request.POST.get("y"+str(i)))
                        r = int(request.POST.get("r"+str(i)))
                        g = int(request.POST.get("g"+str(i)))
                        b = int(request.POST.get("b"+str(i)))
                        a = int(request.POST.get("a"+str(i)))
                        cp = int(request.POST.get("cp"+str(i)))
                        i+=1
                        check_pp = ClickPoint.objects.get(uid=active_user, order=cp, iid=image, img_number=img_fin)
                        x_max = int(check_pp.x_location) + 7
                        x_min = int(check_pp.x_location) -7
                        y_max = int(check_pp.y_location) + 7
                        y_min = int(check_pp.y_location) - 7
                        if x > x_max or x < x_min or y > y_max or y < y_min:
                            new_cpfail = ClickPointFail(iid=image, uid=active_user, x_location=x, y_location=y, color=r+g+b+a, order=cp, img_number=img_fin)
                            new_cpfail.save()
                            context['is_invalid'] = is_invalid
                            context['time_prev'] = time_create
                            return render(request, 'gp/test_newpp2.html', context)
                    if int(img_fin) == int(img_count):
                        new_submit = SubmitInfo(uid=active_user, time_submit=time)
                        new_submit.save()
                        new_login = LoginInfo(uid=active_user, time_login=time, login_period=test_period)
                        new_login.save()
                        return render(request, 'gp/login_success.html', {'active_user': active_user, 'test_period': test_period, 'test_date': test_date})
                    else:
                        img_fin = int(img_fin) + 1
                        img_key = NewPpInfo.objects.filter(uid= active_user, img_number=img_fin).first()
                        img_key = img_key.cp_id.iid.pk
                        img = Image.objects.get(pk=img_key)
                        images = Image.objects.all().order_by('?')[:8]
                        return render(request, 'gp/test_newpp.html', {'img': img, 'images': images, 'test_period': test_period, 'img_fin': img_fin})
        else:
            context['time_prev'] = time_create
            return render(request, 'gp/test_newpp2.html', context)
    else:
        return redirect('/logout')

def password_check(passwd):
    SpecialSym =['!', '"', '#', '$', '%', '&','(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\', "]', '^', '_', '`', '{', '|', '}', '~']
    val = True
    
    if len(passwd) < 8:
        # print('length should be at least 8')
        val = False
    
    if not any(char.isdigit() for char in passwd):
        # print('Password should have at least one numeral')
        val = False
    
    if not any(char.isupper() for char in passwd):
        # print('Password should have at least one uppercase letter')
        val = False
    
    if not any(char.islower() for char in passwd):
        # print('Password should have at least one lowercase letter')
        val = False
    
    if not any(char in SpecialSym for char in passwd):
        # print('Password should have at least one symbol')
        val = False
    
    return val