from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('', RedirectView.as_view(url='/login/')),
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.core.urls")),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path('api/v1/rates/', include('apps.rates.urls')),
    path('api/v1/dashboard/', include('apps.dashboard.urls')),
    path('api/v1/assistant/', include('apps.assistant.urls')),
    # SPECTACULAR
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # HTML pages
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('rates/', TemplateView.as_view(template_name='rates.html'), name='rates_page'),
    path('register/', TemplateView.as_view(template_name='register.html'), name='register'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
]
