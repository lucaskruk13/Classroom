from django.shortcuts import render
from django.views.generic import TemplateView
from School.models import Class
from Account.models import Profile

class ClassView(TemplateView):
    template_name = 'school/class.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation to get a context
        context = super().get_context_data(**kwargs)

        thisclass = Class.objects.get(id=kwargs['pk'])
        students = thisclass.profiles.exclude(status='TR')


        context['class'] = thisclass
        context['students'] = students


        return context


