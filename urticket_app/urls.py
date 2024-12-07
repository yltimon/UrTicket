from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LogoutView

from django.http import HttpResponse

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('login', views.user_login, name="login"),
    path('dash', views.dash, name="orgdash"),
    path('myticket/<str:pk_test>', views.ticket, name="myticket"),
    path('ticketsbought/<str:pk_org>', views.ticketsbought, name="ticketsbought"),
    path('addevent', views.createvent, name="addevent"),
    path('buyticket/<int:event_id>/', views.buy_ticket, name="buyticket"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('edit_event/<int:event_id>/', views.edit_event, name="edit_event"),
    path('edit_ticket/<int:event_id>/', views.edit_tickets, name='edit_ticket'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
