from django.shortcuts import render,redirect,reverse
from django.shortcuts import HttpResponse
from .models import Book,Author,Publish,User
from django.db.models import Avg,Count,Max,Min,Sum
from cmdb.models import Emp
from django.db.models import F,Q
import json,datetime

# Create your views here.

def required_login(func):        #编写装饰器，用于用户登录验证
    def inner(*args,**kwargs):
        request = args[0]
        if request.session.get('is_login'):
            return func(*args,**kwargs)
        else:
            return redirect('/login/')
    return inner

def index(request):
    # is_login = request.session.get("is_login")   #如果要用到这个在首页登录验证，就把这几行代码放开
    # if not is_login:
    #     return redirect("/login/")
    # username=request.session.get("username")
    # login_time=request.session.get("login_time")
    return render(request,'index.html')

def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        print(user,pwd)
        user_obj = User.objects.filter(user=user,pwd=pwd).first()
        if user_obj:
            request.session["is_login"] = True
            request.session["username"] = user
            request.session['login_time'] = datetime.datetime.now().strftime("%Y-%m-%d %X")
            return redirect("/books/")
    return render(request,'login.html',locals())

def add(request):
    book = Book.objects.create(title='机械原理',price=80,pub_date='2003-7-8',publish_id = 2)
    zhao = Author.objects.filter(name='zhao').first()
    xie = Author.objects.filter(name='xie').first()
    book.authors.add(zhao,xie)

    return HttpResponse('添加成功！')

@required_login   # 装饰器的作用太强大了，等以后学了中间件以后，也要记住装饰器的作用
def books(request):
    # is_login = request.session.get("is_login")
    # if not is_login:
    #     return redirect("/login/")        #加上装饰器以后就不用这个了
    username = request.session.get("username")
    login_time = request.session.get("login_time")

    list1 = Book.objects.all()
    # return render(request,'books.html',{'list1':list1})
    return render(request,'books.html',{'list1':list1,'username':username,'login_time':login_time})


@required_login
def addbooks(request):
    # is_login = request.session.get("is_login")
    # if not is_login:
    #     return redirect("/login/")
    # username = request.session.get("username")
    # login_time = request.session.get("login_time")

    list2 = Publish.objects.all()
    list3 = Author.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        pub_date = request.POST.get('pub_date')
        publish = request.POST.get('publish')
        author = request.POST.getlist('author')
        book = Book.objects.create(title = title,price = price,pub_date=pub_date,publish_id=publish)
        # book.authors.add(*author)
        book.authors.set(author)
        # return redirect('/books/')
        return redirect(reverse('books'))
    # return render(request,'addbooks.html',{'list2':list2,'list3':list3,'username':username,'login_time':login_time})
    return render(request,'addbooks.html',{'list2':list2,'list3':list3})

@required_login
def edit(request,id):
    # is_login = request.session.get("is_login")
    # if not is_login:
    #     return redirect("/login/")
    # username = request.session.get("username")
    # login_time = request.session.get("login_time")      #加上装饰器以后就不用这个了，可以省略

    publish_list=Publish.objects.all()
    author_list = Author.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        pub_date = request.POST.get('pub_date')
        publish_id = request.POST.get('publish')
        author_list = request.POST.getlist('author')
        Book.objects.filter(id=id).update(title=title,price=price,pub_date=pub_date,publish_id=publish_id)
        book = Book.objects.get(id=id)
        book.authors.set(author_list)
        return redirect('/books/')
    obj = Book.objects.get(id=id)
    # return render(request,'edit.html',{'Publish_list':publish_list,'author_list':author_list,'title':obj.title,'price':obj.price,'pub_date':obj.pub_date,'obj':obj,'username':username,'login_time':login_time})
    return render(request,'edit.html',{'Publish_list':publish_list,'author_list':author_list,'title':obj.title,'price':obj.price,
                                       'pub_date':obj.pub_date,'obj':obj,})

@required_login
def delete(request,id):
    # is_login = request.session.get("is_login")
    # if not is_login:
    #     return redirect("/login/")

    Book.objects.filter(id = id).delete()
    return HttpResponse('ok')

def logout(request):
    request.session.flush()
    return redirect('/login/')





