from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import PostForm,LoginForm
from .models import Post,User
from django.db import models
# Create your views here.

#render()调用，render方法接收request作为第一个参数，
# 要渲染的页面为第二个参数，以及需要传递给页面的数据字典作为第三个参数（可以为空）
#用于登录以及获得cookie

def login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        print('hellllllllllllllllllo')
        print(form.is_valid())
        if form.is_valid():
            print('--------in login--------')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            t=User.objects.filter(username=username)
            user=User(username=username) #如果用户名不存在保存用户,否则就使用用户
            if len(t):
                user=User.objects.get(username=username)
            else:
                user.save()
            request.session['is_login']=True
            request.session['user_id']=user.id
            request.session['username']=user.username
            return redirect('/comments/index/')             #保存session后跳转到/comments/index/
    return render(request, 'login.html')

def index(request):  #如果访问localhost:8000/polls/index/
    is_login=request.session.get('is_login',False)
    if is_login: #如果已经登录
        #if forms validate_on_submit,save to db,return redirect(/index/)
        if request.method=='POST':
            #将表单中的数据提取出来,并且存储到数据库中
            return render(request, 'index.html', {'form': request.session.get('username')}) #why use request.session.usernam will raise problem
        return render(request,'index.html')

    else:
        return redirect('/login/') #跳转到登录界面

    # if request.method == 'POST':
    #     form=PostForm()
    #     if form.is_valid(): #and current_user.can(write)
    #         body=form.cleaned_data['body']
    #         author='current user'
    #         post=Post(body=body)
    #         post.save()
    #     # 从post表单里获得请求并提交到数据库中去




def register(request):
    return render(request, 'register.html')


def logout(request):
    pass
    return redirect("/index/")


