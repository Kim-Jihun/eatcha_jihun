from django.shortcuts import redirect, render
from . forms import SignupForm, LoginForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from shop.utils.collab_filtering import  *
from shop.models import Post
from shop.utils.produce_dataset import produce_dataset
from django.contrib.auth.views import login as auth_login
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers

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


def login(request):
    providers = []
    for provider in get_providers():
    # social_app속성은 provider에는 없는 속성입니다.
        try:
            provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)
    return auth_login(request,
        authentication_form=LoginForm,
        template_name='accounts/login_form.html',
        extra_context={'providers': providers},

        )


