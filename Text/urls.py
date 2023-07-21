from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from .views import *

from summerize import settings

urlpatterns = [
path('admin/', admin.site.urls),
path('', Home2, name='Home2'),
path('Home', Home, name='Home'),
path('Login', Login, name='Login'),
path('Logout', Logout, name='Logout'),
path('Register', Registration, name='Registration'),
path('collect', Text_to_summerize, name='Text_to_summerize'),
path('collectlink', Link_to_summerize, name='Link_to_summerize'),
path('collectimg', Img_to_summerize, name='Img_to_summerize'),
path('contact', Contact, name='Contact'),
path('about', About, name='About'),
path('services', Services, name='Services'),





    ]