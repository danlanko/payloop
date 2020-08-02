from django.urls import path
from .views import *
from django.contrib.auth import views


urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('pricing', Pricing.as_view(), name='pricing'),
    path('education/package', EducationView.as_view(), name='education'),
    path('register/<package_id>/<modules>', RegisterProduct.as_view(), name='register_product'),
    path('module_detail/<product_id>', ProductDetail.as_view(), name='product_detail'),
    path('process/<package_id>', process_modular, name='process_modular'),
    path('demo_form/<package_id>', demo_view, name='demo_view'),

    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('login_redirect/', login_redirect, name='login_redirect'),

    # path('account/forgot-password', Login.as_view(), name='login'),

]
