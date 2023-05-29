from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from djangoapp.views import about
from djangoapp.views import contact
from djangoapp.views import login_request
from djangoapp.views import logout_request
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path('about/', about, name='about'),

    # path for contact us view
    path('contact/', contact, name='contact'),

    # path for registration

    # path for login
    path('login/', login_request, name='login'),

    # path for logout
    path('logout/', logout_request, name='logout'),


    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
