from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    # def signup(request):
    # #if user is signed in
    # if request.user.is_authenticated:
    #     return redirect("/")
    # # if is a post request
    # if request.method == 'POST':
    #     form = UserCreationForm(request.POST)
    #     # if valid form is provided
    #     if form.is_valid():
    #         form.save()
    #         username= form.cleaned_data.get('username')
    #         password = form.cleaned_data.get('password1')
    #         #log user in and redirect to index
    #         user = authenticate(username=username, password=password)
    #         login(request, user)
    #         return redirect('/')
    #     else:
    #         return render(request, 'auth/signup.html', {'form': form})
    # else:
    #     form = UserCreationForm()
    #     return render(request, 'auth/signup.html', {'form':form})
