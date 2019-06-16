from django import forms
from django.contrib.auth.models import User
from .models import Question, Choice, Answer

class QuestionForm(forms.ModelForm):
	title=forms.CharField(label='Question')
	class Meta:
		model=Question
		fields=['title','start_date','end_date']
		


class ChoiceForm(forms.ModelForm):
	text=forms.CharField(label='Choice')
	class Meta:
		model=Choice
		exclude=['question']
		

