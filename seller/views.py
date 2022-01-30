import random
import smtplib
from email.mime.text import MIMEText
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from django.conf.urls import url
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from .models import Seller, Message, Store, Staff, Reply
from user.models import User, Expression, Order, Address


def logins(request):
    if request.method == 'GET':
        size = (120, 30)
        chars = ("1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        mode = "RGB"
        font_size = 18
        length = 4
        width, height = size
        img = Image.new(mode, size,(225,225,225))
        draw = ImageDraw.Draw(img)
        c_chars = random.sample(chars, length)
        strs = ' '.join(c_chars)
        font = ImageFont.truetype('arial.ttf', font_size)
        font_width, font_height = font.getsize(strs)
        draw.text(((width - font_width) / 3, (height - font_height) / 3),
                  strs, font=font, fill=(0, 0, 0))
        for i in range(7):
            begin = (random.randint(0, 120), random.randint(0, 30))
            end = (random.randint(0, 120), random.randint(0, 30))
            draw.line([begin, end], fill=(0,0,225))
        chance = 100
        w1 = range(width)
        h1 = range(height)
        while chance > 0:
            w = random.choice(w1)
            h = random.choice(h1)
            chance = chance - 1
            draw.point((w, h), fill=(0, 0, 0))
            str_ = ''.join(c_chars)
            str = str_ + ".png"
            img.save('./static/pins/' + str)
            context = {"pin": str_, "n": str}
        return render(request, 'seller/login.html', context)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        pins = request.POST.get('pins')
        pin = request.POST.get('pin')
        sth = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
               'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '@', 'A', 'B', 'C', 'D', 'E',
               'F',
               'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        if username == '':
            error1 = "用户名不能为空"
            error = {"error": error1}
            return render(request, 'seller/loginerror.html', error)
        if password == '':
            error1 = "密码不能为空"
            error = {"error": error1}
            return render(request, 'seller/loginerror.html', error)
        if pins == '':
            error1 = "验证码不能为空"
            error = {"error": error1}
            return render(request, 'seller/loginerror.html', error)
        for u in username:
            if u not in sth:
                error1 = "输入不合法"
                error = {"error": error1}
                return render(request, 'seller/loginerror.html', error)
        for p in password:
            if p not in sth:
                error1 = "输入不合法"
                error = {"error": error1}
                return render(request, 'seller/loginerror.html', error)
        for pi in pin:
            if pi not in sth:
                error1 = "输入不合法"
                error = {"error": error1}
                return render(request, 'seller/loginerror.html', error)
        ob = Seller.objects.get(username=username)
        if ob.status == 1:
            return HttpResponse("该用户已登录")
        else:
            if Seller.objects.filter(username=username).exists():
                if password == ob.password:
                    if pins == pin:
                        uid = ob.id
                        request.session['uids'] = {'uids': uid}
                        request.session['seller'] = {'seller': 'seller'}
                        ob.status = 1
                        ob.save()
                        return HttpResponseRedirect(reverse('homepages'))
                    else:
                        error1 = "验证码错误"
                        error = {"error": error1}
                        return render(request, 'seller/loginerror.html', error)
                else:
                    error1 = "密码错误"
                    error = {"error": error1}
                    return render(request, 'seller/loginerror.html', error)
            else:
                error1 = "用户名不存在"
                error = {"error": error1}
                return render(request, 'seller/loginerror.html', error)


def registers(request):
    if request.method == 'GET':
        return render(request, 'seller/register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        email = request.POST.get('email')
        type = request.POST.get('type')
        sth = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
               'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '@', 'A', 'B', 'C', 'D', 'E',
               'F',
               'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ']
        for u in username:
            if u not in sth:
                error1 = "输入不合法"
                error = {"error": error1}
                return render(request, 'seller/register.html', error)
        for p in password:
            if p not in sth:
                error1 = "输入不合法"
                error = {"error": error1}
                return render(request, 'seller/register.html', error)
        for r in repassword:
            if r not in sth:
                error1 = "输入不合法"
                error = {"error": error1}
                return render(request, 'seller/register.html', error)
        emails = []
        for e in email:
            emails.append(e)
            if e not in sth:
                error1 = "输入不合法"
                error = {"error": error1}
                return render(request, 'seller/register.html', error)
        a = emails.pop()
        b = emails.pop()
        c = emails.pop()
        d = emails.pop()
        if a != 'm':
            error1 = "输入不合法"
            error = {"error": error1}
            return render(request, 'seller/register.html', error)
        if b != 'o':
            error1 = "输入不合法"
            error = {"error": error1}
            return render(request, 'seller/register.html', error)
        if c != 'c':
            error1 = "输入不合法"
            error = {"error": error1}
            return render(request, 'seller/register.html', error)
        if d != '.':
            error1 = "输入不合法"
            error = {"error": error1}
            return render(request, 'seller/register.html', error)
        if username == '':
            error1 = {"error": "用户名不能为空"}
            return render(request, 'seller/register.html', error1)
        else:
            if User.objects.filter(username=username).exists() or Seller.objects.filter(username=username).exists():
                error2 = {"error": '用户名已存在'}
                return render(request, 'seller/register.html', error2)
            else:
                if password == repassword:
                    if email:
                        a = random.randint(0, 10)
                        b = random.randint(0, 10)
                        c = random.randint(0, 10)
                        d = random.randint(0, 10)
                        pin = f"{a}{b}{c}{d}"
                        server = smtplib.SMTP_SSL('smtp.163.com', 465)
                        server.login("a2660675754@163.com", "ZIVTTRVETIOSWTCN")
                        message = MIMEText(pin, 'plain', 'utf8')
                        message['Subject'] = "验证码"
                        message['From'] = "a2660675754@163.com"
                        message['To'] = email
                        server.sendmail("a2660675754@163.com", email, message.as_string())
                        server.quit()
                        pin_ = make_password(pin, None, 'pbkdf2_sha256')
                        context = {'u': username, 'p': password, 'r': repassword, 'e': email, 't': int(type),
                                   'pin': pin_}
                        return render(request, 'seller/doregister.html', context)
                    else:
                        error5 = {"error": "请输入邮箱"}
                        return render(request, 'seller/register.html', error5)
                else:
                    error4 = {"error": '两次输入的密码不一致'}
                    return render(request, 'seller/register.html', error4)


def error1s(request):
    context = {'error': "请输入全部信息"}
    return render(request, 'info.html', context)


def doregisters(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        email = request.POST.get('email')
        type = request.POST.get('type')
        if username == '':
            error1 = {"error": "用户名不能为空"}
            return render(request, 'seller/register.html', error1)
        else:
            if User.objects.filter(username=username).exists() or Seller.objects.filter(username=username).exists():
                error2 = {"error": '用户名已存在'}
                return render(request, 'seller/register.html', error2)
            else:
                if password == repassword:
                    if email:
                        if request.POST.get('pins'):
                            pins = request.POST.get('pins')
                            if request.POST.get('pin'):
                                pin = request.POST.get('pin')
                                if check_password(pin, pins):
                                    chars = ("1234567890abcdefghijklmnopqrstuvwxyz1234567890")
                                    n = random.sample(chars, 8)
                                    nickname = 'seller-' + ''.join(n)
                                    Seller.objects.create(username=username, password=password, type=type, email=email,
                                                          nickname=nickname, picture='a.bmp')
                                    return HttpResponseRedirect(reverse('logins'))
                                else:
                                    return HttpResponse("验证码错误")
                            else:
                                return HttpResponse("请输入验证码")
                        else:
                            error3 = {"error": "验证码未发送"}
                            return render(request, 'seller/register.html', error3)
                    else:
                        error5 = {"error": "请输入邮箱"}
                        return render(request, 'seller/register.html', error5)
                else:
                    error4 = {"error": '两次输入的密码不一致'}
                    return render(request, 'seller/register.html', error4)


def pleases(request):
    return render(request, 'seller/please.html')


def losts(request):
    if request.method == 'GET':
        return render(request, 'seller/lost1.html')
    else:
        if request.POST.get('username'):
            username = request.POST.get('username')
            if request.POST.get('email'):
                email = request.POST.get('email')
                if Seller.objects.filter(username=username).exists():
                    s = Seller.objects.get(username=username)
                    if s.email == email:
                        context = {"u": username, "e": email}
                        return render(request, 'seller/lost2.html', context)
                    else:
                        return HttpResponse("邮箱与用户名不匹配")
                else:
                    return HttpResponse("用户名不存在")
            else:
                return HttpResponse("请输入邮箱")
        else:
            return HttpResponse("请输入用户名")


def losts2(request):
    if request.method == 'GET':
        return render(request, 'seller/lost1.html')
    else:
        username = request.POST.get('username')
        if request.POST.get('password') and request.POST.get('repassword'):
            password = request.POST.get('password')
            repassword = request.POST.get('repassword')
            email = request.POST.get('email')
            if password == repassword:
                a = random.randint(0, 10)
                b = random.randint(0, 10)
                c = random.randint(0, 10)
                d = random.randint(0, 10)
                pin = f"{a}{b}{c}{d}"
                server = smtplib.SMTP_SSL('smtp.163.com', 465)
                server.login("a2660675754@163.com", "ZIVTTRVETIOSWTCN")
                message = MIMEText(pin, 'plain', 'utf8')
                message['Subject'] = "验证码"
                message['From'] = "a2660675754@163.com"
                message['To'] = email
                server.sendmail("a2660675754@163.com", email, message.as_string())
                server.quit()
                pin_ = make_password(pin, None, 'pbkdf2_sha256')
                context = {'u': username, 'p': password, 'r': repassword, 'e': email, 'pin': pin_}
                return render(request, 'seller/losts3.html', context)
            else:
                return HttpResponse("两次输入密码不一样")
        else:
            return HttpResponse("请输入密码")


def losts3(request):
    if request.method == 'GET':
        return render(request, 'seller/lost1.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        email = request.POST.get('email')
        pins = request.POST.get('pins')
        if password == repassword:
            if email:
                if request.POST.get('pins'):
                    pin = request.POST.get('pin')
                    if check_password(pin, pins):
                        ob = Seller.objects.get(username=username)
                        ob.password = password
                        ob.save()
                        if request.session.get('uids') != '':
                            uids = request.session.get('uids')
                            sid = uids['uids']
                            ob = Seller.objects.get(id=sid)
                            ob.status = 0
                            ob.save()
                            request.session.flush()
                            return HttpResponseRedirect(reverse('logins'))
                        else:
                            return HttpResponseRedirect(reverse('logins'))
                    else:
                        return HttpResponse("验证码错误")
                else:
                    error3 = {"error": "请输入验证码"}
                    return render(request, 'seller/lost2.html', error3)
            else:
                error5 = {"error": "请输入邮箱"}
                return render(request, 'seller/lost2.html', error5)
        else:
            error4 = {"error": '两次输入的密码不一致'}
            return render(request, 'seller/lost2.html', error4)


def homepages(request):
    if request.session.get('seller'):
        uids = request.session.get('uids')
        sid = uids['uids']
        slist = []
        m, n = message(request)
        if Store.objects.filter(sellerid=sid):
            for s in Store.objects.all():
                if int(s.sellerid) == sid:
                    slist.append(s)
            context = {'slist': slist, 'n': n, 'm': m}
            return render(request, 'seller/homepage.html', context)
        else:
            return render(request, 'seller/homepage2.html')
    else:
        return render(request, 'seller/home.html')


def logouts(request):
    uids = request.session.get('uids')
    sid = uids['uids']
    ob = Seller.objects.get(id=sid)
    ob.status = 0
    ob.save()
    request.session.flush()
    return HttpResponseRedirect(reverse('guide'))


def wds(request):
    uids = request.session.get('uids')
    sid = uids['uids']
    s = Seller.objects.get(id=sid)
    context = {"s": s}
    return render(request, 'seller/wd.html', context)


def photo(request):
    if request.FILES.get('photo'):
        file = request.FILES.get('photo')
        uids = request.session.get('uids')
        sid = uids['uids']
        ob = Seller.objects.get(id=sid)
        n = random.randint(1, 100000)
        name = f"{n}{str(file)}"
        file1 = str(file)
        file2 = []
        for word in file1:
            file2.append(word)
        accept = ['bmp', 'jpg', 'png', 'tif', 'gif']
        file2.reverse()
        file3 = []
        for f in file2:
            if f == '.':
                break
            file3.append(f)
        file3.reverse()
        file4 = ''.join(file3)
        if str(file4) in accept:
            ob.photos = name
            ob.save()
            to = open('./static/picture/' + name, "wb+")
            for chunk in file.chunks():
                to.write(chunk)
            to.close()
            return HttpResponseRedirect(reverse('wds'))
        else:
            return HttpResponse('请上传正确文件类型（bmp,jpg,png,tif,gif）')
    else:
        return HttpResponse('请上传文件')


def nicknames(request):
    nickname = request.POST.get('nickname')
    uids = request.session.get('uids')
    sid = uids['uids']
    ob = Seller.objects.get(id=sid)
    ob.nickname = nickname
    ob.save()
    return HttpResponseRedirect(reverse('wds'))


def create(request):
    if request.method == 'GET':
        return render(request, 'seller/create.html')
    else:
        if request.POST.get('name'):
            if request.FILES.get('photo'):
                names = request.POST.get('name')
                file = request.FILES.get('photo')
                uids = request.session.get('uids')
                sid = uids['uids']
                n = random.randint(1, 100000)
                name = f"{n}{str(file)}"
                file1 = str(file)
                file2 = []
                for word in file1:
                    file2.append(word)
                accept = ['bmp', 'jpg', 'png', 'tif', 'gif']
                file2.reverse()
                file3 = []
                for f in file2:
                    if f == '.':
                        break
                    file3.append(f)
                file3.reverse()
                file4 = ''.join(file3)
                if str(file4) in accept:
                    Store.objects.create(sellerid=sid, name=names, picture=name)
                    to = open('./static/store/' + name, "wb+")
                    for chunk in file.chunks():
                        to.write(chunk)
                    to.close()
                    return HttpResponseRedirect(reverse('homepages'))
                else:
                    return HttpResponse('请上传正确文件类型（bmp,jpg,png,tif,gif）')
            else:
                return HttpResponse('请上传文件')
        else:
            return HttpResponse('请输入店铺名')


def manage(request, storeid):
    if request.method == 'GET':
        s = Store.objects.get(id=storeid)
        sellerid = s.sellerid
        uids = request.session.get('uids')
        sid = uids['uids']
        if int(sid) == int(sellerid):
            staff = []
            staffs = []
            n = 0
            m = 0
            if Staff.objects.filter(storeid=storeid).exists():
                for l in Staff.objects.all():
                    if l.storeid != '':
                        if int(l.storeid) == int(storeid):
                            n = n + 1
                            staffs.append(l)
                for s in staffs:
                    if int(s.status) == 3:
                        m = m + 1
                if m == n:
                    context = {'storeid': storeid}
                    return render(request, 'seller/manage2.html', context)
                else:
                    for i in Staff.objects.all():
                        if i.storeid != '':
                            if int(i.storeid) == int(storeid) and int(i.status) != 3:
                                staff.append(i)
                    context = {'list': staff, 'storeid': storeid}
                    return render(request, 'seller/manage.html', context)
            else:
                context = {'storeid': storeid}
                return render(request, 'seller/manage2.html', context)
        else:
            return HttpResponse('你不能管理别人的店')


def dell(request, staffid):
    s = Staff.objects.get(id=staffid)
    s.status = 3
    s.save()
    return HttpResponseRedirect(reverse('manage', args=s.storeid))


def edit(request):
    id = int(request.POST.get('id'))
    s = Staff.objects.get(id=id)
    m = Message.objects.get(id=s.messageid)
    message = m.message
    context = {'s': s, 'message': message}
    return render(request, 'seller/edit.html', context)


def add(request):
    id = request.POST.get('storeid')
    context = {'id': id}
    return render(request, 'seller/add.html', context)


def doadd(request):
    storeid = request.POST.get('storeid')
    if request.POST.get('type'):
        if request.POST.get('name'):
            if request.POST.get('price'):
                if request.POST.get('number'):
                    if request.FILES.get('photo'):
                        if request.POST.get('message'):
                            price = request.POST.get('price')
                            number = request.POST.get('number')
                            names = request.POST.get('name')
                            file = request.FILES.get('photo')
                            type = request.POST.get('type')
                            uids = request.session.get('uids')
                            sid = uids['uids']
                            message = request.POST.get('message')
                            n = random.randint(1, 100000)
                            name = f"{n}{str(file)}"
                            file1 = str(file)
                            file2 = []
                            for word in file1:
                                file2.append(word)
                            accept = ['bmp', 'jpg', 'png', 'tif', 'gif']
                            file2.reverse()
                            file3 = []
                            for f in file2:
                                if f == '.':
                                    break
                                file3.append(f)
                            file3.reverse()
                            file4 = ''.join(file3)
                            if str(file4) in accept:
                                Message.objects.create(message=message, sellerid=sid)
                                list = []
                                ob = Message.objects.all()
                                for m_1 in ob:
                                    list.append(m_1)
                                m = list.pop()
                                Staff.objects.create(storeid=storeid, name=names, pictere=name, status=4, price=price,
                                                     number=number, type=type,
                                                     messageid=m.id)
                                to = open('./static/staff/' + name, "wb+")
                                for chunk in file.chunks():
                                    to.write(chunk)
                                to.close()
                                return HttpResponseRedirect(reverse('manage', args=(storeid,)))
                            else:
                                return HttpResponse('请上传正确文件类型（bmp,jpg,png,tif,gif）')
                        else:
                            return HttpResponse('请输入介绍')
                    else:
                        return HttpResponse('请上传文件')
                else:
                    return HttpResponse('请输入数量')
            else:
                return HttpResponse('请输入价格')
        else:
            return HttpResponse('请输入商品名')
    else:
        return HttpResponse("请选择商品类型")


def doedit(request):
    uids = request.session.get('uids')
    sid = uids['uids']
    s_ = request.POST.get('s')
    s = Staff.objects.get(id=int(s_))
    if request.POST.get('name'):
        names = request.POST.get('name')
    else:
        return HttpResponse('请输入商品名')
    if request.POST.get('price'):
        price = request.POST.get('price')
    else:
        return HttpResponse('请输入价格')
    if request.POST.get('number'):
        number = request.POST.get('number')
    else:
        return HttpResponse('请输入数量')
    if request.POST.get('message'):
        mid = s.messageid
        m = Message.objects.get(id=mid)
        message = request.POST.get('message')
        m.message = message
        m.save()
    if request.FILES.get('photo'):
        names = request.POST.get('name')
        file = request.FILES.get('photo')
        n = random.randint(1, 100000)
        name = f"{n}{str(file)}"
        file1 = str(file)
        file2 = []
        for word in file1:
            file2.append(word)
        accept = ['bmp', 'jpg', 'png', 'tif', 'gif']
        file2.reverse()
        file3 = []
        for f in file2:
            if f == '.':
                break
            file3.append(f)
        file3.reverse()
        file4 = ''.join(file3)
        if str(file4) in accept:
            s.name = names
            s.price = price
            s.number = number
            s.pictere = name
            s.save()
            to = open('./static/staff/' + name, "wb+")
            for chunk in file.chunks():
                to.write(chunk)
            to.close()
            return HttpResponseRedirect(reverse('manage', args=(s.storeid,)))
        else:
            return HttpResponse('请上传正确文件类型（bmp,jpg,png,tif,gif）')
    else:
        s.name = names
        s.price = price
        s.number = number
        s.save()
        return HttpResponseRedirect(reverse('manage', args=(s.storeid,)))


def message(request):
    uids = request.session.get('uids')
    sid = uids['uids']
    n = 0
    for e in Expression.objects.all():
        if e.sellerid:
            if int(e.sellerid) == sid:
                n = n + 1
    s = Seller.objects.get(id=sid)
    m = 0
    for o in Order.objects.all():
        if o.seller == sid:
            m = m + 1
        if o.seller == sid and (o.status == 2 or o.status == 3 or o.status == 4):
            m = m + 1
    m1 = m - int(s.m)
    n1 = n - int(s.n)
    return m1, n1


def sells(request):
    uids = request.session.get('uids')
    sid = uids['uids']
    m = 0
    s = Seller.objects.get(id=sid)
    if s.do_status == 0:
        return HttpResponse("暂无处理订单权限")
    olist = []
    if Order.objects.filter(seller=sid).exists():
        for o in Order.objects.all():
            if o.seller == sid:
                olist.insert(0, o)
                m = m + 1
            if o.seller == sid and (o.status == 2 or o.status == 3 or o.status == 4):
                m = m + 1
        s.m = m
        s.save()
        return render(request, 'seller/sells.html', {'olist': olist})
    else:
        return HttpResponse("暂时没有订单")


def send(request, oid):
    o = Order.objects.get(id=oid)
    o.status = 1
    o.save()
    uids = request.session.get('uids')
    sid = uids['uids']
    m = 0
    s = Seller.objects.get(id=sid)
    olist = []
    if Order.objects.filter(seller=sid).exists():
        for o in Order.objects.all():
            if o.seller == sid:
                olist.append(o)
                m = m + 1
            if o.status == 2 or o.status == 3 or o.status == 4:
                m = m + 1
        s.m = m
        s.save()
        return HttpResponseRedirect(reverse('sells'))


def reply(request):
    if request.method == 'GET':
        uids = request.session.get('uids')
        sid = uids['uids']
        n = 0
        s = Seller.objects.get(id=sid)
        elist = []
        if Expression.objects.filter(sellerid=sid).exists():
            for e in Expression.objects.all():
                if e.sellerid:
                    if int(e.sellerid) == sid:
                        n = n + 1
            s.n = n
            s.save()
            for e in Expression.objects.all():
                if e.sellerid:
                    if int(e.sellerid) == sid and e.dell == 1:
                        elist.append(e)
            return render(request, 'seller/reply.html', {'elist': elist})
        else:
            return HttpResponse("暂时没有留言")
    if request.method == 'POST':
        eid = request.POST.get('eid')
        uids = request.session.get('uids')
        sid = uids['uids']
        return render(request, 'seller/doreply.html', {'eid': eid, 'sid': sid})


def doreply(request):
    eid = request.POST.get('eid')
    uids = request.session.get('uids')
    sid = uids['uids']
    s = Seller.objects.get(id=sid)
    ex = Expression.objects.get(id=eid)
    staff = ex.staffid
    ex.status = 1
    ex.save()
    n = 0
    elist = []
    if request.POST.get('reply'):
        replys = request.POST.get('reply')
        Reply.objects.create(seller=s.nickname, staffid=staff, reply=replys, expressionid=eid, username=ex.username)
        if Expression.objects.filter(sellerid=sid).exists():
            for e in Expression.objects.all():
                if e.sellerid:
                    if int(e.sellerid) == sid:
                        elist.append(e)
                        n = n + 1
            s.n = n
            s.save()
            return HttpResponseRedirect(reverse('reply'))
    else:
        return HttpResponse("请输入回复")


def back(request, oid):
    o = Order.objects.get(id=oid)
    o.status = 4
    o.save()
    uid = o.userid
    staff = Staff.objects.get(id=o.staff)
    staff.number = int(o.buy_number) + int(staff.number)
    staff.save()
    s = Seller.objects.get(id=o.seller)
    s.money = float(s.money) - float(o.price) * float(o.buy_number)
    s.save()
    u = User.objects.get(id=uid)
    u.money = float(u.money) + float(o.price) * int(o.buy_number)
    u.save()
    return HttpResponseRedirect(reverse('sells'))


def changes(request):
    if request.method == 'GET':
        return render(request, 'seller/change.html')
    else:
        if request.method == 'POST':
            names = request.POST.get('names')
            passwords = request.POST.get('passwords')
            if names == '':
                context = {'a': '用户名不能为空'}
                return render(request, 'seller/change.html', context)
            else:
                if Seller.objects.filter(username=names).exists():
                    seller = Seller.objects.get(username=names)
                    if passwords == seller.password:
                        return render(request, 'seller/dochange.html')
                    else:
                        context = {'a': '密码错误'}
                        return render(request, 'seller/change.html', context)
                else:
                    context = {'a': '用户名不存在'}
                    return render(request, 'seller/change.html', context)


def dochanges(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('changes'))
    else:
        uids = request.session.get('uids')
        sid = uids['uids']
        if request.method == 'POST':
            names = request.POST.get('names')
            passwords = request.POST.get('passwords')
            password_ = request.POST.get('password_')
            if names == '':
                return HttpResponse("用户名不能为空")
            else:
                ob = Seller.objects.get(id=sid)
                if names == ob.username:
                    if password_ == passwords:
                        ob.username = names
                        ob.password = passwords
                        ob.save()
                        request.session.flush()
                        return HttpResponseRedirect(reverse('logins'))
                    else:
                        return HttpResponse("两次输入的密码不同")
                else:
                    if Seller.objects.filter(username=names).exists():
                        return HttpResponse("用户名已存在")
                    else:
                        if password_ == passwords:
                            ob.username = names
                            ob.password = passwords
                            ob.save()
                            request.session.flush()
                            return HttpResponseRedirect(reverse('logins'))
                        else:
                            return HttpResponse("两次输入的密码不一样")


def ground(request, sid):
    s = Staff.objects.get(id=sid)
    s.status = 1
    s.save()
    return HttpResponseRedirect(reverse('manage', args=(s.storeid,)))


def down(request, sid):
    s = Staff.objects.get(id=sid)
    s.status = 4
    s.save()
    return HttpResponseRedirect(reverse('manage', args=(s.storeid,)))
