from django.urls import path, include
from rest_framework import routers
 
from . import views
 
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'posts', views.BlogPostViewSet)
# router.register(r'posts', views.BlogPostViewSet.as_view())

router.register(r'users', views.UserViewSet)
# router.register(r'login', views.login)
# router.register(r'signup',views.signup)
 
urlpatterns = [
    path(r'api/', include(router.urls)),
    # path(r'api/', include(router.urls)),
    
    path(r'', views.index, name='index'),
    path(r'api/login', views.login),
    path(r'api/signup', views.signup),
     path(r'register', views.register, name='register')

]