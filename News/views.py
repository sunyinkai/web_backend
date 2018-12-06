from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from .forms import PostForm, LoginForm, CommentForm
from .models import Post, User, Comment
from django.db import models
import json
import datetime


def timeconvert(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


# Create your views here.
# get request
def get_friend_news(request):
    posts = Post.objects.order_by("-date").all()
    all_message = {}
    obj = []
    for post in posts:
        # -union-
        union = {}
        # --user--
        user = {}
        user["userID"] = post.author.id
        user["Nick"] = post.author.username
        # --news--
        news = {}
        news["content"] = post.body
        news["newsID"] = post.id
        news["date"] = post.date
        news["cntlike"] = 0
        news["liked"] = False
        news_comment = []
        comments = Comment.objects.filter(post__id=post.id).select_related()  # 找到所有当前post下的评论

        for comment in comments:
            d = {}
            d["userID"] = comment.author.id
            d["Nick"] = comment.author.username
            d["commentID"] = comment.id
            d["content"] = comment.body
            news_comment.append(d)
        news["comment"] = news_comment

        union["News"] = news
        union["user"] = user
        obj.append(union)
    all_message['data'] = obj
    all_message['error'] = False
    return HttpResponse(json.dumps(all_message, default=timeconvert), content_type='application/json')


# post request
def news_operate(request):
    if request.session.get('is_login') is not True:  # not login,redirect to the index
        user = User.objects.get(username='ubunt')
        request.session['is_login'] = True
        request.session['user_id'] = user.id
        request.session['username'] = user.username
        # return redirect('/News/login/')

    result = json.loads(request.body.decode())
    content = result.get('content')
    op = result.get('op')
    news_id = result.get('newsID')
    current_user = request.session.get('user_id')
    if op == 'add':
        body = content
        user_id = current_user
        username = request.session.get('username')
        user = User(username=username, id=user_id)
        post = Post(body=body, author=user)
        post.save()

        # dump the data
        obj = {}
        data = {'newsID': post.id}
        obj['data'] = data
        obj['error'] = False
        return HttpResponse(json.dumps(obj), content_type='application/json')
    elif op == 'delete':
        post = Post.objects.get(id=news_id)
        if current_user is post.author.id:
            post.delete()
            obj = {}
            data = {'newsID': news_id}
            obj['data'] = data
            obj['error'] = False
            return HttpResponse(json.dumps(obj), content_type='application/json')
        else:
            obj = {}
            return HttpResponse('You have no access to delete news')
    elif op == 'update':
        pass
        # post = get_object_or_404(Post, id=news_id)
        # if current_user is post.author.id:  # 如果文章是当前用户的,可以对其修改
        #     post.body = content
        #     post.save()
        #     return HttpResponse('update ok!')
        # else:  # 文章不属于当前用户,显示没有权限修改
        #     return HttpResponse('Sorry,You have no the access to modify it!')
    else:
        return HttpResponse('System Error!')


# post request
def comment_operate(request):
    # if request.session.get('is_login') is False:  # judge the user whether login
    user = User.objects.get(username='ubunt')
    request.session['is_login'] = True
    request.session['user_id'] = user.id
    request.session['username'] = user.username
    # return redirect('/News/login')

    # load the data from post form
    result = json.loads(request.body.decode())
    op = result.get('op')
    content = result.get('content')
    news_id = result.get('newsID')
    comment_id = result.get('commentID')

    current_user = request.session.get('user_id')
    if op == 'add':
        body = content
        author = User.objects.get(id=current_user)
        post = Post.objects.get(id=news_id)
        comment = Comment(body=body, author=author, post=post)
        comment.save()
        obj = {"error": False}
        data = {"commentID": comment.id}
        obj["data"] = data
        return HttpResponse(json.dumps(obj), content_type="application/json")
    elif op == 'delete':
        comment = Comment.objects.get(id=comment_id)
        if comment.author.id == current_user:
            comment.delete()
            obj = {"error": False}
            data = {"commentID": comment.id}
            obj["data"] = data
            return HttpResponse(json.dumps(obj), content_type="application/json")
        else:
            return HttpResponse('You have no access to delete!')
    elif op == 'update':
        pass
        # comments = Comment.objects.filter(post__id=news_id).select_related()  # 将指定id号下的所有comment都找出来
        # for comment in comments:
        #     if comment.id is comment_id:
        #         if comment.author.id == current_user:
        #             comment.body = content
        #             comment.save()
        #             return HttpResponse('comment update ok!')
        #         else:
        #             return HttpResponse('You have no access to update!')
    else:
        return HttpResponse('System Error!')


def like_operate(request):
    pass


def follow(request, user_id):
    if not request.session.get("is_login"):
        return redirect("/News/index/")
    return HttpResponse('you are now in follow')


def register(request):
    return render(request, 'register.html')


def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect("/News/login/")


def to_json(obj):
    return serializers.serialize('json', obj)


# 访问localhost:8000/comments/login
def login(request):
    if request.method == 'POST':
        print("post", request.POST)
        form = LoginForm(request.POST)
        # print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            action = form
            t = User.objects.filter(username=username)
            user = User(username=username)  # 如果用户名不存在,注册保存用户,否则就使用用户
            if len(t):
                user = User.objects.get(username=username)
            else:
                user.save()
                return redirect('/News/login/')  # 如果不加这一步，直接进行session的相关东西会出问题，user.id is None
            request.session['is_login'] = True
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return redirect('/News/index/')  # 保存session后跳转到/comments/index/
    return render(request, 'login.html')


# 访问localhost:8000/comments/index/由这个视图函数处理
# 　主界面，发布post,查看其他人的post
def index(request):
    is_login = request.session.get('is_login', False)
    if is_login is False:  # 如果没有登录,跳转到登录界面
        return redirect('/News/login/')
    if is_login:  # 如果已经登录
        # 如果表单提交合法,那么保存到数据库中，然后重定向到当前页面
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                body = form.cleaned_data['body']
                user_id = request.session.get('user_id')
                username = request.session.get('username')
                user = User.objects.get(id=user_id)
                post = Post(body=body, author=user)
                post.save()  # 将表单中的数据提取出来,并且存储到数据库中
                return redirect('/News/index/')
        posts = Post.objects.all()  # 注意:这里是显示所有的动态页面:
        # return HttpResponse(to_json(posts),content_type='application/json')
        return render(request, 'index.html', {'form': request.session.get('username'), 'posts': posts, })


# 访问 localhost:8000/comments/post/1
# 为每一个post分配一个固定链接,也就是唯一的url引用
# 评论这个post
def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            body = form.cleaned_data['body']
            author = User.objects.get(id=request.session.get('user_id'))
            post = Post.objects.get(id=post_id)
            Comment.objects.create(body=body, author=author, post=post)  # 创建并保存
            return redirect('/News/post/' + str(post_id))  # 重定向到当前页面，防止刷新
    comments = Comment.objects.filter(post__id=post_id).select_related()  # 找到所有当前post下的评论
    return render(request, 'post.html', {'post': post, 'comments': comments, 'post_id': post_id})


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
