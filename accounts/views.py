from django.shortcuts import redirect, render
from . forms import SignupForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from shop.utils.collab_filtering import  *
from shop.models import Post
from shop.utils.produce_dataset import produce_dataset


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(settings.LOGIN_URL) # 회원가입에 성공하면, LOGIN 페이지로 이동
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html',
                  {'form': form,})


@login_required
def profile(request):
    #produce_dataset()
    recommendation = user_recommendations(str(request.user))
    recommend_restaurant_list = []
    for name in recommendation:
        object = Post.objects.get(title = name)
        recommend_restaurant_list.append(object)

    return render(request, 'accounts/profile.html',
                  {'recommendation': recommend_restaurant_list,})
