from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("hospital/", include("hospital.urls")),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', include('hospital.urls'))
]