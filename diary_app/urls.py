from django.urls import path
from . import views


urlpatterns =[
    path('', views.index, name = 'index'),
    path('entries/', views.EntryListView.as_view(), name="entries"),
    path('entry/<int:pk>', views.EntryDetailView.as_view(), name="entry-detail")
]