


from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from api.views import dashboard_router
from django.shortcuts import redirect

# def home_redirect(request):
#     return redirect("/admin/login/")

# urlpatterns = [
#     path("", include("api.urls")),   # <-- THIS LINE IS REQUIRED
#     path("admin/", admin.site.urls),
# ]

# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#       # load your app URLs
#     # path("admin/", admin.site.urls), # only ONE admin registration
#     path("admin/", admin.site.urls),
#     path("", include("api.urls")), # only ONE admin registration

# ]


from django.contrib import admin

from django.urls import path, include


from django.contrib.auth import views as auth_views
from api.views import dashboard_router

from django.shortcuts import redirect
from api.admin import admin_site

def home_redirect(request):
    return redirect("/admin/login/")


urlpatterns = [
    # path("", root_redirect),  # <--- FIX
    path("dashboard/", include("api.urls")),
    # path("admin/", admin_site.urls),
    path("", home_redirect),
    path("login/", auth_views.LoginView.as_view(
        template_name="registration/login.html"
    ), name="login"),
    #path("dashboard/", dashboard_router, name="dashboard"),
    path("admin/", admin.site.urls),
   
   path("api/", include("api.urls"))
]
