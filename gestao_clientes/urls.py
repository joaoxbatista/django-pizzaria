
from django.contrib import admin
from django.urls import path, include
from pizzas import urls as pizzas_urls
from .views import dashboard_home
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView,LogoutView

urlpatterns = [

    path('', dashboard_home, name="dashboard.home"),
    path('pizza/', include(pizzas_urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
