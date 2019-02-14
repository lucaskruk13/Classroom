from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect, get_object_or_404, reverse

# Create your views here.
def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request, 'accounts/auth/signup.html', {'form': form})