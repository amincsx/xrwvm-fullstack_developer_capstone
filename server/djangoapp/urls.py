from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from . import views

app_name = 'djangoapp'

urlpatterns = [
    # API endpoint for login (POST request)
    path(route='login', view=views.login_user, name='login'),

    # API endpoint for logout (POST request)
    path('api/logout/', views.logout_request, name='logout_api'),

    # Render the login page template (GET request)
    path('login/', TemplateView.as_view(template_name="index.html"), name='login_page'),
    # Registration endpoint
    path('register/', views.registration, name='register'),
    # Placeholder for future endpoints
    # path('register/', views.registration, name='register'),
    # path('dealers/', views.get_dealerships, name='dealers'),
    # path('dealer/<int:dealer_id>/reviews/', views.get_dealer_reviews, name='dealer_reviews'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
