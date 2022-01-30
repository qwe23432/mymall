import random
import smtplib
from email.mime.text import MIMEText
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from .models import User, Expression, Order, Cart, Address, His
from seller.models import Seller, Message, Store, Staff, Reply


def login(request):
    if request.method == 'GET':
        size = (120, 30)
        chars = ("1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        mode = "RGB"
        font_size = 18
        length = 4
        width, height = size
        img = Image.new(mode, size, (225, 225, 225))
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
            draw.line([begin, end], fill=(0, 0, 225))
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
        return render(request, 'pre/login.html', context)
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
            return render(request, 'pre/loginerror.html', error)
        if password == '':
            error1 = "密码不能为空"
            error = {"error": error1}
            return render(request, 'pre/loginerror.html', error)
        if pin == '':
            error1 = "验证码不能为空"
            error = {"error": error1}
            for u in username:
                if u not in sth:
                    error1 = "输入不合法"
                    error = {"error": error1}
                    return render(request, 'pre/loginerror.html', error)
            for p in password:
                if p not in sth:
                    error1 = "输入不合法"
                    error = {"error": error1}
                    return render(request, 'pre/loginerror.html', error)
            for pi in pin:
                if pi not in sth:
                    error1 = "输入不合法"
                    error = {"error": error1}
                    return render(request, 'pre/loginerror.html', error)
            return render(request, 'pre/loginerror.html', error)
        ob = User.objects.get(username=username)
        if ob.status == 1:
            return HttpResponse("该用户已登录")
        else:
            if User.objects.filter(username=username).exists() or Seller.objects.filter(username=username).exists():
                if password == ob.password:
                    if pins == pin:
                        uid = ob.id
                        request.session['uid'] = {'uid': uid}
                        request.session['user'] = {'user': 'user'}
                        ob.status = 1
                        ob.save()
                        for s in Staff.objects.all():
                            if int(s.number) == 0:
                                s.status = 2
                                s.save()
                        return HttpResponseRedirect(reverse('homepage', args='1'))
                    else:
                        error1 = "验证码错误"
                        error = {"error": error1}
                        return render(request, 'pre/loginerror.html', error)
                else:
                    error1 = "密码错误"
                    error = {"error": error1}
                    return render(request, 'pre/loginerror.html', error)
            else:
                error1 = "用户名不存在"
                error = {"error": error1}
                return render(request, 'pre/loginerror.html', error)


def register(request):
    if request.method == 'GET':
        return render(request, 'pre/register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        email = request.POST.get('email')
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
                return render(request, 'pre/register.html', error)
        for p in password:
            if p not in sth:
                error1 = "输入不合法"
                error = {"error": error1}
                return render(request, 'pre/register.html', error)
        for r in repassword:
            if r not in sth:
                error1 = "输入不合法"
                error = {"error": error1}
                return render(request, 'pre/register.html', error)
        emails = []
        for e in email:
            emails.append(e)
            if e not in sth:
                error1 = "输入不合法"
                error = {"error": error1}
                return render(request, 'pre/register.html', error)
        a = emails.pop()
        b = emails.pop()
        c = emails.pop()
        d = emails.pop()
        if a != 'm':
            error1 = "输入不合法"
            error = {"error": error1}
            return render(request, 'pre/register.html', error)
        if b != 'o':
            error1 = "输入不合法"
            error = {"error": error1}
            return render(request, 'pre/register.html', error)
        if c != 'c':
            error1 = "输入不合法"
            error = {"error": error1}
            return render(request, 'pre/register.html', error)
        if d != '.':
            error1 = "输入不合法"
            error = {"error": error1}
            return render(request, 'pre/register.html', error)
        context = {'u': username, 'p': password, 'r': repassword, 'e': email}
        if username == '':
            error1 = {"error": "用户名不能为空"}
            return render(request, 'pre/register.html', error1)
        else:
            if User.objects.filter(username=username).exists() or Seller.objects.filter(username=username).exists():
                error2 = {"error": '用户名已存在'}
                return render(request, 'pre/register.html', error2)
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
                        context = {'u': username, 'p': password, 'r': repassword, 'e': email, 'pin': pin_}
                        return render(request, 'pre/doregister.html', context)
                    else:
                        error5 = {"error": "请输入邮箱"}
                        return render(request, 'pre/register.html', error5)
                else:
                    error4 = {"error": '两次输入的密码不一致'}
                    return render(request, 'pre/register.html', error4)


def error1(request):
    context = {'error': "请输入全部信息"}
    return render(request, 'info.html', context)


def doregister(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        if username == '':
            error1 = {"error": "用户名不能为空"}
            return render(request, 'pre/register.html', error1)
        else:
            if User.objects.filter(username=username).exists():
                error2 = {"error": '用户名已存在'}
                return render(request, 'pre/register.html', error2)
            else:
                if password == repassword:
                    if request.POST.get('email'):
                        email = request.POST.get('email')
                        if request.POST.get('pins'):
                            pins = request.POST.get('pins')
                            if request.POST.get('pin'):
                                pin = request.POST.get('pin')
                                if check_password(pin, pins):
                                    chars = ("1234567890abcdefghijklmnopqrstuvwxyz1234567890")
                                    n = random.sample(chars, 8)
                                    nickname = 'customer-' + ''.join(n)
                                    User.objects.create(username=username, password=password, email=email,
                                                        nickname=nickname, money='10000000', picture='b.bmp')
                                    return HttpResponseRedirect(reverse('login'))
                                else:
                                    return HttpResponse("验证码错误")
                            else:
                                return HttpResponse("请输入验证码")
                        else:
                            error3 = {"error": "验证码未发送"}
                            return render(request, 'pre/register.html', error3)
                    else:
                        error5 = {"error": "请输入邮箱"}
                        return render(request, 'pre/register.html', error5)
                else:
                    error4 = {"error": '两次输入的密码不一致'}
                    return render(request, 'pre/register.html', error4)


def please(request):
    return render(request, 'pre/please.html')


def lost(request):
    if request.method == 'GET':
        return render(request, 'pre/lost1.html')
    else:
        if request.POST.get('username'):
            username = request.POST.get('username')
            if request.POST.get('email'):
                email = request.POST.get('email')
                if User.objects.filter(username=username).exists():
                    s = User.objects.get(username=username)
                    if s.email == email:
                        context = {"u": username, "e": email}
                        return render(request, 'pre/lost2.html', context)
                    else:
                        return HttpResponse("邮箱与用户名不匹配")
                else:
                    return HttpResponse("用户名不存在")
            else:
                return HttpResponse("请输入邮箱")
        else:
            return HttpResponse("请输入用户名")


def lost2(request):
    if request.method == 'GET':
        return render(request, 'pre/lost1.html')
    else:
        if request.POST.get('password') and request.POST.get('repassword'):
            username = request.POST.get('username')
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
                return render(request, 'pre/lost3.html', context)
            else:
                return HttpResponse("两次输入密码不一样")
        else:
            return HttpResponse("请输入密码")


def lost3(request):
    if request.method == 'GET':
        return render(request, 'pre/lost1.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        email = request.POST.get('email')
        pins = request.POST.get('pins')
        if password == repassword:
            if email:
                if request.POST.get('pins'):
                    if request.POST.get('pin'):
                        pin = request.POST.get('pin')
                        if check_password(pin, pins):
                            ob = User.objects.get(username=username)
                            ob.password = password
                            ob.save()
                            if request.session.get('uid') != '':
                                uid = request.session.get('uid')
                                u_id = uid['uid']
                                ob = User.objects.get(id=u_id)
                                ob.status = 0
                                ob.save()
                                request.session.flush()
                                return HttpResponseRedirect(reverse('login'))
                            else:
                                return HttpResponseRedirect(reverse('login'))
                        else:
                            return HttpResponse("验证码错误")
                    else:
                        error = {"error": "请输入验证码"}
                        return render(request, 'pre/lost2.html', error)
                else:
                    error3 = {"error": "验证码未发送"}
                    return render(request, 'pre/lost2.html', error3)
            else:
                error5 = {"error": "请输入邮箱"}
                return render(request, 'pre/lost2.html', error5)
        else:
            error4 = {"error": '两次输入的密码不一致'}
            return render(request, 'pre/lost2.html', error4)


def guide(request):
    return render(request, 'guide.html')


def homepage(request, home=1):
    slist = []
    for s in Staff.objects.all():
        if s.status == 1:
            slist.append(s)
    p = Paginator(slist, 10)
    if home < 1:
        home = 1
    if home > p.num_pages:
        home = p.num_pages
    list = p.page(home)
    context = {'list': list, "home": home, "pagelist": p.page_range}
    if request.session.get('user'):
        return render(request, 'user/homepage.html', context)
    else:
        return render(request, 'user/home.html', context)


def homepage__(request):
    home = 1
    slist = []
    for s in Staff.objects.all():
        if s.status == 1:
            slist.append(s)
    p = Paginator(slist, 10)
    if home < 1:
        home = 1
    if home > p.num_pages:
        home = p.num_pages
    list = p.page(home)
    context = {'list': list, "home": home, "pagelist": p.page_range}
    if request.session.get('user'):
        return render(request, 'user/homepage.html', context)
    else:
        return render(request, 'user/home.html', context)


def logout(request):
    uid = request.session.get('uid')
    u_id = uid['uid']
    ob = User.objects.get(id=u_id)
    ob.status = 0
    ob.save()
    request.session.flush()
    return HttpResponseRedirect(reverse('homepage', args='1'))


def staff_(request, sid):
    uid = request.session.get('uid')
    u_id = uid['uid']
    list = []
    elist = []
    for e in Expression.objects.all():
        if e.staffid == sid and e.dell == 1:
            elist.append(e)
    for s in Staff.objects.all():
        if s.status == 1:
            list.append(s.id)
    if sid not in list:
        return HttpResponse("找不到该商品")
    rlist = []
    for r in Reply.objects.all():
        if r.staffid:
            if int(r.staffid) == sid:
                rlist.append(r)
    staff = Staff.objects.get(id=sid)
    storeid = staff.storeid
    store = Store.objects.get(id=int(storeid))
    messageid = staff.messageid
    m = Message.objects.get(id=messageid)
    u = User.objects.get(id=u_id)
    His.objects.create(user=u_id, type=staff.type, staff=staff)
    context = {"staff": staff, 'm': m, "elist": elist, "rlist": rlist, "store": store, "uid": str(u_id)}
    return render(request, 'user/staff.html', context)


def wd(request):
    u_id = request.session.get('uid')
    uid = u_id['uid']
    u = User.objects.get(id=uid)
    alist = []
    for a in Address.objects.all():
        if a.user == uid:
            alist.append(a)
    return render(request, 'user/wd.html', {'u': u, 'list': alist})


def photo(request):
    if request.FILES.get('photo'):
        file = request.FILES.get('photo')
        u_id = request.session.get('uid')
        uid = u_id['uid']
        ob = User.objects.get(id=uid)
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
            ob.picture = name
            ob.save()
            to = open('./static/picture/' + name, "wb+")
            for chunk in file.chunks():
                to.write(chunk)
            to.close()
            return HttpResponseRedirect(reverse('wd'))
        else:
            return HttpResponse('请上传正确文件类型（bmp,jpg,png,tif,gif）')
    else:
        return HttpResponse('请上传文件')


def nickname(request):
    nicknames = request.POST.get('nickname')
    u_id = request.session.get('uid')
    uid = u_id['uid']
    ob = User.objects.get(id=uid)
    ob.nickname = nicknames
    ob.save()
    return HttpResponseRedirect(reverse('wd'))


def buy(request, sid):
    list = []
    for s in Staff.objects.all():
        if s.status == 1:
            list.append(s.id)
    if sid not in list:
        return HttpResponse("找不到该商品")
    staff = Staff.objects.get(id=sid)
    u_id = request.session.get('uid')
    uid = u_id['uid']
    u = User.objects.get(id=uid)
    if u.buy_status == 0:
        return HttpResponse("暂无权限")
    store = staff.storeid
    s = Store.objects.get(id=store)
    buy_number_ = 1
    for c in Cart.objects.all():
        if c.status == 0 and c.staff == sid:
            buy_number_ = c.buy_number
    if request.method == 'GET':
        alist = []
        for a in Address.objects.all():
            if a.user == uid:
                alist.append(a)
        return render(request, 'user/address.html', {"list": alist, "sid": sid, "buy_number": buy_number_})
    else:
        for c in Cart.objects.all():
            if c.status == 0 and c.staff == sid:
                c.status = 1
                c.save()
        if request.POST.get('buy_number') and int(request.POST.get('buy_number')) >= 1:
            buy_number = int(request.POST.get('buy_number'))
            bn = buy_number
            if int(staff.number) - bn < 0:
                return HttpResponse("商品数量不足")
            if (float(u.money) - bn * float(staff.price)) < 0:
                return HttpResponse("钱不够")
            while buy_number > 0:
                buy_number = buy_number - 1
                staff.number = int(staff.number) - 1
                staff.save()
                address = request.POST.get('address')
                seller = Seller.objects.get(id=s.sellerid)
                seller.money = float(seller.money) + float(staff.price)
                seller.save()
                u.money = float(u.money) - float(staff.price)
                u.save()
            if int(staff.number) == 0:
                staff.status = 2
                staff.save()
            Order.objects.create(user=u.nickname, staff=staff.id, seller=s.sellerid, address=address, status=0,
                                 number=staff.number, price=staff.price, store=s.name, name=staff.name,
                                 pictere=staff.pictere, userid=uid, buy_number=bn)
        else:
            HttpResponse("购买数量必须大于等于1")
        for s in Staff.objects.all():
            if int(s.number) == 0:
                s.status = 2
                s.save()
        return HttpResponseRedirect(reverse('staff', args=(sid,)))


def incart(request, sid):
    list = []
    for s in Staff.objects.all():
        if s.status == 1:
            list.append(s.id)
    if sid not in list:
        return HttpResponse("找不到该商品")
    staff = Staff.objects.get(id=sid)
    u_id = request.session.get('uid')
    uid = u_id['uid']
    st = staff.storeid
    s = Store.objects.get(id=st)
    n = s.name
    m = 1
    for c in Cart.objects.all():
        if c.status == 0 and c.staff == sid:
            c.status = 2
            c.save()
            m = m + c.buy_number
    Cart.objects.create(staff=int(staff.id), seller=int(s.sellerid), number=staff.number, price=staff.price,
                        store=n, name=staff.name, pictere=staff.pictere, userid=int(uid), status=0, buy_number=m)
    return HttpResponseRedirect(reverse('staff', args=(sid,)))


def address_(request, sid):
    list = []
    for s in Staff.objects.all():
        if s.status == 1:
            list.append(s.id)
    if sid not in list:
        return HttpResponse("找不到该商品")
    u_id = request.session.get('uid')
    uid = u_id['uid']
    if request.method == 'GET':
        alist = []
        for a in Address.objects.all():
            if int(uid) == a.user:
                alist.append(a)
        context = {"list": alist, "sid": sid}
        return render(request, 'user/doaddress.html', context)
    else:
        if request.POST.get('address'):
            address = request.POST.get('address')
            Address.objects.create(user=uid, address=address)
            return HttpResponseRedirect(reverse('buy', args=(sid,)))
        else:
            return HttpResponse("不能为空")


def address__(request):
    u_id = request.session.get('uid')
    uid = u_id['uid']
    if request.method == 'GET':
        alist = []
        for a in Address.objects.all():
            if int(uid) == a.user:
                alist.append(a)
        context = {"list": alist}
        return render(request, 'user/doaddress.html', context)
    else:
        if request.POST.get('address'):
            address = request.POST.get('address')
            Address.objects.create(user=uid, address=address)
            return HttpResponseRedirect(reverse('wd'))
        else:
            return HttpResponse("不能为空")


def myorder(request):
    u_id = request.session.get('uid')
    uid = u_id['uid']
    list = []
    for o in Order.objects.all():
        if uid == int(o.userid) and o.status != 0 and o.status != 1:
            list.insert(0, o)
    return render(request, 'user/myorder.html', {"list": list})


def order(request):
    u_id = request.session.get('uid')
    uid = u_id['uid']
    list = []
    for o in Order.objects.all():
        if uid == int(o.userid) and (o.status == 0 or o.status == 1):
            list.insert(0, o)
    return render(request, 'user/order.html', {"list": list})


def uback(request, oid):
    o = Order.objects.get(id=oid)
    o.status = 3
    o.save()
    return HttpResponseRedirect(reverse('order'))


def receive(request, oid):
    o = Order.objects.get(id=oid)
    o.status = 2
    o.save()
    return HttpResponseRedirect(reverse('order'))


def mycart(request):
    if request.method == "GET":
        u_id = request.session.get('uid')
        uid = u_id['uid']
        clist = []
        for c in Cart.objects.all():
            if int(c.status) == 0 and int(c.userid) == uid:
                clist.append(c)
        return render(request, 'user/cart.html', {"list": clist})


def expression(request, sid):
    u_id = request.session.get('uid')
    uid = u_id['uid']
    if request.POST.get('expression'):
        expressions = request.POST.get('expression')
        staff = Staff.objects.get(id=sid)
        name = staff.name
        storeid = staff.storeid
        store_ = Store.objects.get(id=storeid)
        store = store_.name
        staffid = staff.id
        userid = uid
        user = User.objects.get(id=userid)
        username = user.nickname
        sellerid = store_.sellerid
        Expression.objects.create(expression=expressions, name=name, store=store, staffid=staffid, username=username,
                                  sellerid=sellerid, userid=userid)
        return HttpResponseRedirect(reverse('staff', args=(sid,)))
    else:
        return HttpResponse("请输入")


def store_(request, storeid):
    stores = False
    for s in Store.objects.all():
        if s.id == storeid:
            stores = s
    list = []
    if stores:
        for st in Staff.objects.all():
            if st.storeid:
                if int(st.storeid) == storeid and st.status == 1:
                    list.append(st)
        return render(request, "user/store.html", {"list": list, "store": stores})
    else:
        return HttpResponse("该商店不存在")


def search(request):
    kw = request.GET.get("keyword", None)
    s = Staff.objects.filter(status=1)
    if kw:
        slist = s.filter(name__contains=kw)
    if kw:
        list1 = Store.objects.filter(name__contains=kw)
    p = Paginator(slist, 10)
    home = 1
    if home < 1:
        home = 1
    if home > p.num_pages:
        home = p.num_pages
    list = p.page(home)
    context = {'list': list, "home": home, "pagelist": p.page_range}
    if list1:
        context = {'storelist': list1, 'list': list, "home": home, "pagelist": p.page_range}
    if request.session.get('user'):
        return render(request, 'user/homepage.html', context)
    else:
        return render(request, 'user/home.html', context)


def change(request):
    if request.method == 'GET':
        return render(request, 'user/change.html')
    else:
        if request.method == 'POST':
            names = request.POST.get('names')
            passwords = request.POST.get('passwords')
            if names == '':
                context = {'a': '用户名不能为空'}
                return render(request, 'user/change.html', context)
            else:
                if User.objects.filter(username=names).exists():
                    user = User.objects.get(username=names)
                    if passwords == user.password:
                        return render(request, 'user/dochange.html')
                    else:
                        context = {'a': '密码错误'}
                        return render(request, 'user/change.html', context)
                else:
                    context = {'a': '用户名不存在'}
                    return render(request, 'user/change.html', context)


def dochange(request):
    if request.method == 'GET':
        return HttpResponseRedirect(reverse('change'))
    else:
        u_id = request.session.get('uid')
        uid = u_id['uid']
        if request.method == 'POST':
            names = request.POST.get('names')
            passwords = request.POST.get('passwords')
            password_ = request.POST.get('password_')
            if names == '':
                return HttpResponse("用户名不能为空")
            else:
                ob = User.objects.get(id=uid)
                if names == ob.username:
                    if password_ == passwords:
                        ob.username = names
                        ob.password = passwords
                        ob.save()
                        request.session.flush()
                        return HttpResponseRedirect(reverse('login'))
                    else:
                        return HttpResponse("两次输入的密码不同")
                else:
                    if User.objects.filter(username=names).exists():
                        return HttpResponse("用户名已存在")
                    else:
                        if password_ == passwords:
                            ob.username = names
                            ob.password = passwords
                            ob.save()
                            request.session.flush()
                            return HttpResponseRedirect(reverse('login'))
                        else:
                            return HttpResponse("两次输入的密码不一样")


def dell_(request, eid):
    e = Expression.objects.get(id=eid)
    e.dell = 0
    e.save()
    return HttpResponseRedirect(reverse('staff', args=(e.staffid,)))


def recommend(request):
    u_id = request.session.get('uid')
    uid = u_id['uid']
    list = []
    for p in His.objects.all():
        if p.user == uid:
            list.append(p)
    t = [0, 0, 0, 0, 0]
    for p_ in list:
        if p_.type == 1:
            t[0] = t[0] + 1
        if p_.type == 2:
            t[1] = t[1] + 1
        if p_.type == 3:
            t[2] = t[2] + 1
        if p_.type == 4:
            t[3] = t[3] + 1
        if p_.type == 5:
            t[4] = t[4] + 1
    n1 = 0
    for i in t:
        if i == max(t):
            t[n1] = -1
            m1 = n1
            break
        n1 = n1 + 1
    n2 = 0
    for i in t:
        if i == max(t):
            t[n2] = -1
            m2 = n2
            break
        n2 = n2 + 1
    n3 = 0
    for i in t:
        if i == max(t):
            t[n3] = -1
            m3 = n3
            break
        n3 = n3 + 1
    list1 = []
    list2 = []
    list3 = []
    for s in Staff.objects.all():
        if s.status == 1:
            if s.type == m1 + 1:
                list1.append(s)
            if s.type == m2 + 1:
                list2.append(s)
            if s.type == m3 + 1:
                list3.append(s)
    l1 = random.sample(list1, 3)
    l2 = random.sample(list2, 2)
    l3 = random.sample(list3, 1)
    l = l1 + l2 + l3
    return render(request, "user/recommend.html", {"list": l})


def past(request):
    u_id = request.session.get('uid')
    uid = u_id['uid']
    list = []
    for p in His.objects.all():
        if p.user == uid:
            list.insert(0, p)
    return render(request, "user/past.html", {"list": list})


def rmb(request):
    if request.method == "POST":
        u_id = request.session.get('uid')
        uid = u_id['uid']
        u = User.objects.get(id=uid)
        if request.POST.get("money"):
            money = request.POST.get("money")
            u.money = float(money) + u.money
            u.save()
        else:
            return HttpResponse("不能为空")
        return HttpResponseRedirect(reverse('wd'))
    else:
        return render(request, "user/rmb.html")
