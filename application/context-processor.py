from .backend.models import Product, UserType, ClientProfile


def get_products(request):
    category_1 = Product.objects.filter(category=1)
    category_2 = Product.objects.filter(category=2)
    return {'base_products': category_1, 'base_products2': category_2}


def user_is_staff(request):
    try:
        user_type = UserType.objects.get(user_id=request.user.id)
        if user_type.is_staff is True:
            return {'is_staff': True}
        else:
            customer_pk = ClientProfile.objects.get(user_id=request.user.id).pk
            return {'is_staff': False, 'customer_id': customer_pk}
    except UserType.DoesNotExist:
        return {}
