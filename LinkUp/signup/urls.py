# myapp/urls.py
from django.urls import path
from . import views
from .views import register_user, login_user,LinkViewSet,generate_qr_codes,qr_code_page,user_profile_retrieve,user_profile_update
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'link', views.LinkViewSet, basename='link')

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', login_user, name='login_user'),
    path('links/', LinkViewSet.as_view({'get': 'list','delete': 'destroy'}), name='link-list'),
    path('generate_qr_codes/', generate_qr_codes, name='generate_qr_codes'),#http://127.0.0.1:8000/generate_qr_codes/?user_id=1
    # path('share-link/', qr_code_page, name='share_link'),

    path('profile/retrieve/', user_profile_retrieve, name='user_profile_retrieve'),
    path('profile/update/', user_profile_update, name='user_profile_update'),
]
urlpatterns += router.urls
