from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
#from django.contrib.auth.models import User
from .models import Choice, Question
#from .forms import NewQuestion
#from django import forms
#from django.utils import timezone
from datetime import datetime
from django.db import connection
from django.shortcuts import redirect

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def secrets(request):
    #if request.user.username == 'admin':
        if request.method == 'POST':
            title = request.POST.get('title')
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #sql = ''

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO polls_question (pub_date, question_text) VALUES (%s," '%s ' ")", (date, title))
            #connection.commit()
                return render(request, "polls/secrets.html")
        return render(request, "polls/secrets.html")
    #return redirect("https://www.youtube.com/watch?v=gvGyS5j9aFY")

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# Create your views here.
