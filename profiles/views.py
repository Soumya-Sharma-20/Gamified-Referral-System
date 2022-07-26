from cProfile import Profile
from django.shortcuts import redirect, render
from .models import Profile

# Create your views here.
def my_recommendations_view(request):
    profile=Profile.objects.get(user=request.user)
    my_recs=profile.get_recommend_profiles()
    rewards=len(my_recs)*20
    context={'my_recs':my_recs,'rewards':rewards}
    return render(request,'profiles/main.html',context)