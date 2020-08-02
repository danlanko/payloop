from django.urls import path
from .views import *


urlpatterns = [
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('new_product', CreateProduct.as_view(), name='new_product'),
    path('product_list', ProductList.as_view(), name='product_list'),
    # path('new_edu_product', CreateEducation.as_view(), name='new_edu_product'),
    # path('edu_product_list', EducationList.as_view(), name='edu_product_list'),

    path('edit_product/<product_id>', EditProduct.as_view(), name='edit_product'),
    path('edit_edu_product', EditEducation.as_view(), name='edit_edu_product'),
    path('delete_product/<product_id>', delete_product, name='delete_product'),
    path('new_package', ProductPackage.as_view(), name='new_package'),
    path('update_package/<package_id>', UpdateProductPackage.as_view(), name='update_package'),
    path('delete_package/<package_id>', delete_package, name='delete_package'),
    path('customer_list', CustomerList.as_view(), name='customer_list'),
    path('banner_text', BannerTextView.as_view(), name='banner_text'),
    path('banner_text_update/<banner_id>', BannerTextUpdateView.as_view(), name='banner_text_update'),
    path('banner_text_delete/<banner_id>', banner_delete, name='banner_delete'),

    path('demo_list', DemoListView.as_view(), name='demo_list_view'),

    path('delete_customer/<user_id>', delete_customer, name='delete_customer'),
    path('customer_profile/<customer_id>', CustomProfile.as_view(), name='customer_profile'),
    path('add_new_module/<customer_id>', add_module, name='add_module'),
    path('delete_module/<module_id>/<customer_id>', delete_module, name='delete_module'),
    path('suspend_module/<module_id>/<customer_id>/<action>', suspend_module, name='suspend_module'),

    path('preparing_payment/<customer_id>', generate_ref_id, name='generate_ref'),
    path('verify_payment/<customer_id>/<ref_id>', verify_payment, name='verify_payment'),

]
