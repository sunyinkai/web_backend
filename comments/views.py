from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import PostForm, LoginForm
from .models import Post, User
from django.db import models


# Create your views here.

# 访问localhost:8000/comments/login
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        # print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            t = User.objects.filter(username=username)
            user = User(username=username)  # 如果用户名不存在,注册保存用户,否则就使用用户
            if len(t):
                user = User.objects.get(username=username)
            else:
                user.save()
            request.session['is_login'] = True
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return redirect('/comments/index/')  # 保存session后跳转到/comments/index/
    return render(request, 'login.html')


# 访问localhost:8000/comments/index/由这个视图函数处理
# 　主界面，发布post,查看其他人的post
def index(request):
    is_login = request.session.get('is_login', False)
    if is_login is False:  # 如果没有登录,跳转到登录界面
        return redirect('/comments/login/')
    if is_login:  # 如果已经登录
        # 如果表单提交合法,那么保存到数据库中，然后重定向到当前页面
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                body = form.cleaned_data['body']
                user_id = request.session.get('user_id')
                username = request.session.get('username')
                user = User(username=username, id=user_id)
                post = Post(body=body, author=user)
                post.save()  # 将表单中的数据提取出来,并且存储到数据库中
                return redirect('/comments/index/')
        posts = Post.objects.all()  # 注意:这里是显示所有的动态页面:
        return render(request, 'index.html', {'form': request.session.get('username'), 'posts': posts, })


# 访问 localhost:8000/comments/post/1
# 为每一个post分配一个固定链接,也就是唯一的url引用
def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'post.html', {'post': post})


# 访问 localhost:8000/comments/edit/1
# 编辑编号为post_id的post
def edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.session.get('user_id') == post.author.id:  # 如果文章是当前用户的
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post.body = form.cleaned_data['body']
                post.save()
        return render(request, 'edit_post.html', {'post': post})
    else:  # 文章不属于当前用户,显示没有权限修改
        return HttpResponse('Sorry,You have no the access to modify it!')


def register(request):
    return render(request, 'register.html')


def logout(request):
    session_keys=list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect("/comments/login/")
