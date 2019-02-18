from django.shortcuts import render, get_list_or_404
from django.views.generic import TemplateView
from School.models import Class

class FeedView(TemplateView):
    template_name = 'feed/feed.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation to get a context
        context = super().get_context_data(**kwargs)

        context['class_list'] = Class.objects.filter(profiles__user_id=self.request.user.id)

        return context


