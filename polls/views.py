from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import LoginForm
from django.template import loader
import json

from .models import Question


def login(request):
    print(request.method)
    return render(request, 'polls/login.html')


def result(requst):  #如果访问localhost:8000/polls/result/
    print('---------------now in result------------------')
    if requst.method == 'POST':
        form = LoginForm(requst.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            return render(requst, 'polls/result.html', {'form': username})
    else:
        return HttpResponse('It is not a post resquest')


# Create your views here.
def index(request):
    # context='hello,world'
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # context={'lastest_question_list':latest_question_list}
    List = ['A', 'B']
    Dict = {'A': 'a', 'B': 'b'}
    context = {
        # 'List':json.dumps(List),
        # 'Dict':json.dumps(Dict)
        'List': List,
        'Dict': Dict,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
    # question=get_object_or_404(Question,pk=question_id)
    # return render(request,'polls/detail.html',{'question':question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)
    # return HttpResponse("You'are looking on question %s." % (question_id))


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
