from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.core.urls")),
    path("api/v1/auth/", include("apps.accounts.urls")),
    path('api/v1/rates/', include('apps.rates.urls')),
    path('api/v1/dashboard/', include('apps.dashboard.urls')),
    path('api/v1/assistant/', include('apps.assistant.urls')),
    # HTML pages
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('rates/', TemplateView.as_view(template_name='rates.html'), name='rates_page'),
]
