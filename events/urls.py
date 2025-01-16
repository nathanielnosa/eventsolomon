from django.urls import path
from .views import RegisterView, EventView, EventGroupView,LoginView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('events/', EventView.as_view(), name='events'),
    path('events/<int:event_id>/', EventView.as_view(), name='event-detail'),
    path('groups/', EventGroupView.as_view(), name='groups'),
]
