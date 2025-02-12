from django.urls import path

from . import views

# old version views
#app_name = 'polls'
# urlpatterns = [
#     # ex: /polls/
#     path('', views.index, name='index'),

#     path('owner', views.owner, name='owner'),

#     # ex: /polls/5/
#     path('specifics/<int:question_id>/', views.detail, name='detail'),

#     # ex: /polls/5/results/
#     path('<int:question_id>/results/', views.results, name='results'),

#     # ex: /polls/5/vote/
#     path('<int:question_id>/vote/', views.vote, name='vote'),

# ]
# new version generic_views

app_name = 'hello'
urlpatterns = [
    path('', views.sessfun, name='sessfun'),

]