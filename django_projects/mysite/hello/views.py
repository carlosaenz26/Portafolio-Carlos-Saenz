from django.shortcuts import get_object_or_404, render

from django.http import HttpResponse, HttpResponseRedirect



from django.http import Http404

from django.template import loader

from django.urls import reverse

from django.views import generic

def sessfun(request):
    n_v=request.session.get('n_v',0)+1
    request.session['n_v']=n_v
    if n_v>4: del(request.session['n_v'])
    resp=HttpResponse('view count='+str(n_v)+str("9bdd4375"))
    resp.set_cookie('dj4e_cookie', '9bdd4375', max_age=1000)
    return resp
