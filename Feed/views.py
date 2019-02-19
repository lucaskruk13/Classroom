from django.shortcuts import render, get_list_or_404, redirect
from django.views.generic import TemplateView
from School.models import Class
from django.contrib.auth.mixins import LoginRequiredMixin


class FeedView(LoginRequiredMixin,TemplateView):
    template_name = 'feed/feed.html'

    def render_to_response(self, context, **response_kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')

        return super(FeedView, self).render_to_response(context)


    def get_context_data(self, **kwargs):
        # Call the base implementation to get a context
        context = super().get_context_data(**kwargs)

        context['class_list'] = Class.objects.filter(profiles__user_id=self.request.user.id)

        return context




