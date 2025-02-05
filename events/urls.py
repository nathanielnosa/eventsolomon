from django.urls import path
from .views import (RegisterView,EventView, EventGroupView,LoginView,UserDetailView,UserLookupView,UserListView,GroupDetailView,EventDetailView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user/', UserDetailView.as_view(), name='user-detail'),
    path('events/', EventView.as_view(), name='events'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('groups/', EventGroupView.as_view(), name='groups'),
    path('groups/<int:pk>/', GroupDetailView.as_view(), name='group-detail'),
    path('user/', UserLookupView.as_view(), name='user-lookup'),
    path('users/', UserListView.as_view(), name='user-list'),
]
