from django.shortcuts import render
from django.views.generic import TemplateView
from School.models import Class, Session
from django.contrib.auth.mixins import LoginRequiredMixin



class ClassView(LoginRequiredMixin,TemplateView):
    template_name = 'school/class.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation to get a context
        context = super().get_context_data(**kwargs)

        thisclass = Class.objects.get(id=kwargs['pk'])
        students = thisclass.profiles.exclude(status='TR')
        sessions = Session.objects.filter(associated_class=thisclass).order_by('-date')[:10]

        context['class'] = thisclass
        context['students'] = students
        context['sessions'] = sessions

        return context


