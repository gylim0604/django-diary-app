from django.urls import path, include
from . import views


urlpatterns =[

    path('', views.index, name = 'index'),
    path('index',views.index,name="index"),
    path('entries/<slug:date>', views.EntryListView.as_view(), name="entries"),
    path('create_entry', views.EntryCreateView.as_view(), kwargs={'date': None}, name="entry-create"),
    path('entry/<int:pk>', views.EntryDetailView.as_view(), name="entry-detail"),
    path('entry/<int:pk>/update', views.EntryUpdateView.as_view(), name="entry-update"),
    path('user/<int:pk>', views.UserDetailView.as_view(), name="user-detail"),
    path('calendar/',views.CalendarView.as_view(), name='calendar'),
]