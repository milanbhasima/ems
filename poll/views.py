from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import QuestionForm, ChoiceForm
# Create your views here.
@login_required(login_url='/login/')
def index(request):
	questions=Question.objects.all()
	context={
	'polls':'Polls',
	'questions':questions,
	}
	return render(request,'poll/index.html', context)

@login_required(login_url='/login/')
def detail(request, id):
	user=request.user
	question=get_object_or_404(Question, id=id)
	context={
	'polls':'Polls',
	'question':question,
	'user':user,
	}
	return render(request,'poll/detail.html', context)

@login_required(login_url='/login/')
def poll(request, id):
	question=get_object_or_404(Question, id=id)
	if request.method=='POST':
		data=request.POST.get('choice')
		answer=Answer.objects.create(user=request.user, choice_id=data)
		if answer:
			return HttpResponse('<h1>You have successsfully voted.')
		else:
			return HttpResponse('<h1>You have not successsfully voted.')
	context={
	'question':question,
	}
	return render(request,'poll/poll.html', context)

@login_required(login_url='/login/')
def addpoll(request):
	if request.user.profile.role_type == 'hr':
		form=QuestionForm(request.POST or None, instance=Question())
		cforms=[ChoiceForm(request.POST or None, prefix=str(x), instance=Choice()) for x in range(0,3)]
		if form.is_valid and all([cf.is_valid() for cf in cforms]):
			new_poll=form.save(commit=False)
			new_poll.created_by=request.user
			new_poll.save()
			for cf in cforms:
				new_choice=cf.save(commit=False)
				new_choice.question=new_poll
				new_choice.save()
			return redirect('index')
		context={
			'form':form,
			'cforms':cforms,
		}
		return render(request,'poll/addpoll.html',context)
	else:
		return redirect('index')

@login_required(login_url='/login/')
def editpoll(request,id):
	if request.user.profile.role_type == 'hr':
		question=get_object_or_404(Question, id=id)
		choices=Choice.objects.filter(question=question)
		# choices=question.choice_set.all()
		qform=QuestionForm(request.POST or None, instance=question)
		cforms=[ChoiceForm(request.POST or None, prefix=str(choice.id), instance=choice) for choice in choices]
		if qform.is_valid() and all([cf.is_valid() for cf in cforms]):
			new_poll=qform.save(commit=False)
			new_poll.created_by=request.user
			new_poll.save()
			for cf in cforms:
				new_choice=cf.save(commit=False)
				new_choice.question=new_poll
				new_choice.save()
			return redirect('index')
		else:
			return render(request,'poll/editpoll.html',{'qform':qform,'cforms':cforms})
		context={
			'qform':qform,
			'cforms':cforms,
		}
		return render(request,'poll/editpoll.html', context)
	else:
		return redirect('index')

@login_required(login_url='/login/')
def deletepoll(request,id):
	if request.user.profile.role_type == 'hr':
		question=get_object_or_404(Question, id=id)
		if request.method=="POST":
			question.delete()
			return redirect('index')
		context={
			'question':question,
		}
		return render(request,'poll/deletepoll.html', context)
	else:
		return redirect('employee-list')