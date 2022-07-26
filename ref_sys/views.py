from django.shortcuts import render,redirect
from profiles.models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate


def signup_view(request):
    profile_id=request.session.get('ref_profile')
    print('profileId',profile_id)
    form=UserCreationForm(request.POST or None)

    if form.is_valid():
        if profile_id is not None:
            recommended_by_profile=Profile.objects.get(id=profile_id)

            instance = form.save()
            registered_user=User.objects.get(id=instance.id)
            registered_profile = Profile.objects.get(user=registered_user)
            registered_profile.recommended_by=recommended_by_profile.user
            registered_profile.save()
        else:
            form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('main-view')

    context={'form':form}
    return render(request,'signup.html',context)

def main_view(request,*args,**kwargs):
    code=str(kwargs.get('ref_code'))
    try:
        profile=Profile.objects.get(code=code)
        request.session['ref_profile']=profile.id
        print('id',profile.id)
    except:
        pass

    print(request.session.get_expiry_date())

    return render(request, 'main.html', {})