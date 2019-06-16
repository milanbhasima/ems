from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from .forms import UserForm,UserUpdateForm,UserLoginForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.generic import(DetailView, UpdateView)
from poll.models import *
from .models import Profile
# Create your views here.
@login_required(login_url='/login/')
def add_user(request):
	if request.user.profile.role_type == 'admin':
		form=UserForm(request.POST or None)
		pform=ProfileForm(request.POST or None)
		if form.is_valid() and pform.is_valid():
			user=form.save(commit=False)
			user.set_password(request.POST.get('password'))
			user.save()
			profile=pform.save(commit=False)
			profile.user=user
			profile.save()
			return redirect('employee-list')
		else:
			return render(request,'employee/user_form.html',{'form':form,'pform':pform})
		context={
			'form':form,
			'pform':pform,
		}
		return render(request,'employee/user_form.html',context)
	else:
		return redirect('employee-list')


@login_required(login_url='/login')
def employee_list(request):
	users=User.objects.all()
	questions=Question.objects.all().order_by('-created_at')[0:3]
	context={
		'users':users,
		'questions':questions,
		'polls':'Polls',
	}
	return render(request,'employee/index.html', context)

@login_required(login_url='/login/')
def employee_detail(request,id):
	user=get_object_or_404(User, id=id)

	context={
		'user':user,
	}
	return render(request,'employee/detail.html', context)

@login_required(login_url='/login/')
def employee_edit(request,id):
	if request.user.profile.role_type == 'admin':
		user=get_object_or_404(User, id=id)
		profile=Profile.objects.get(user=user)
		form=UserUpdateForm(request.POST or None, instance=user)
		pform=ProfileForm(request.POST or None, instance=profile)
		if form.is_valid() and pform.is_valid():
			user=form.save(commit=False)
			user.save()
			pform.save()
			return redirect('employee-list')
		else:
			return render(request,'employee/user_form.html',{'form':form,'pform':pform})
		context={
			'user':user,
			'form':form,
		}
		return render(request,'employee/edit.html', context)
	else:
		return redirect('employee-list')

@login_required(login_url='/login/')
def employee_delete(request,id):
	if request.user.profile.role_type == 'admin':
		user=get_object_or_404(User, id=id)
		if request.method=="POST":
			user.delete()
			return redirect('employee-delete')
		context={
			'user':user,
		}
		return render(request,'employee/delete.html', context)
	else:
		return redirect('employee-list')

def user_login(request):
	form=UserLoginForm(request.POST or None)	
	cform=UserForm()
	pform=ProfileForm(request.POST or None)
	if form.is_valid():
		username=form.cleaned_data.get('username')
		password=form.cleaned_data.get('password')
		user=authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				if request.GET.get('next', None):
					return redirect(request.GET['next'])
				return redirect('success')
			else:
				return HttpResponse('user is not active')		
		else:
			context={
				'error':'invalid credentials',
				'form':form,
				'cform':cform,
				'pform':pform,
				}
			return render(request,'auth/login.html', context)
	return render(request, 'auth/login.html', {'form':form,'cform':cform,'pform':pform})

@login_required(login_url='/login')
def success(request):
	context={
		'user':request.user,
	}
	
	return render(request,'auth/success.html',context)


def user_logout(request):
	logout(request)
	return redirect('user-login')


class MyProfile(DetailView):

	template_name='auth/detail.html'

	def get_object(self):
		return self.request.user

class MyProfileUpdate(UpdateView):
	fields=['designation','salary']
	template_name='auth/update.html'
	success_url=reverse_lazy('profile')

	def get_object(self):
		return self.request.user.profile