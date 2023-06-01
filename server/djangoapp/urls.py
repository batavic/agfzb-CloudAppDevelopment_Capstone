from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from djangoapp.views import about
from djangoapp.views import contact
from djangoapp.views import login_request
from djangoapp.views import logout_request
from djangoapp.views import registration_request
from djangoapp.views import get_dealerships
from djangoapp.views import get_dealer_details
from djangoapp.views import add_review
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
    path('registration/', registration_request, name='registration'),

    # path for login
    path('login/', login_request, name='login'),

    # path for logout
    path('logout/', logout_request, name='logout'),

    #index path
    path('', get_dealerships, name='index'),

    # path for dealer reviews view
    path('dealer/<int:dealer_id>/', get_dealer_details, name='dealer_details'),

    # path for add a review view
    path('dealer/<int:dealer_id>/add_review/', add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
