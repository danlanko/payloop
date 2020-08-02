from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from .forms import NewProductForm, PackageForm, BannerTextForm, EducationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product, Packages, ClientProfile, BannerText, UserType, ClientModule, DemoList, Education
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
import random
import requests
import datetime
# Create your views here.


def user_is_staff(request):
    try:
        user_type = UserType.objects.get(user=request.user)
        if user_type.is_staff:
            return True
        else:
            return False
    except UserType.DoesNotExist:
        raise SystemError('User type not found')


class Dashboard(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'backend/dashboard.html'
    raise_exception = True

    def test_func(self):
        return user_is_staff(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['total_product'] = Product.objects.count()
        context['total_client'] = ClientProfile.objects.count()
        context['total_erp'] = Product.objects.filter(category=1).count()
        context['total_ems'] = Product.objects.filter(category=2).count()
        context['products'] = Product.objects.order_by("-pk")[:10]
        context['demos'] = DemoList.objects.order_by("-pk")[:10]
        return context


class CustomProfile(LoginRequiredMixin, generic.DetailView):
    model = ClientProfile
    template_name = 'backend/customer_profile.html'
    pk_url_kwarg = 'customer_id'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        modules = ClientModule.objects.filter(user_id=self.object.user_id)
        context['modules'] = modules
        payable = 0
        for item in modules.filter(suspend=False):
            payable += item.module.amount
        context['payable'] = payable
        context['product'] = Product.objects.all()
        return context


def delete_customer(request, user_id):
    try:
        modules = ClientModule.objects.filter(user_id=user_id)
        active_modules = 0
        for item in modules:
            if item.is_active:
                active_modules += 1
        if active_modules == 0:
            user = User.objects.get(id=user_id)
            user.delete()
            messages.success(request, 'Action successful, user deleted')
        else:
            print(active_modules)
            messages.error(request, 'System error... User has an active module')
    except ClientModule.DoesNotExist:
        user = User.objects.get(id=user_id)
        user.delete()
        messages.success(request, 'Action successful, user deleted')
    return redirect('customer_list')


@login_required()
def generate_ref_id(request, customer_id):
    ref_id = str(random.randrange(0, 9876543210, 4))
    ref_id += customer_id
    customer_user = ClientProfile.objects.get(id=customer_id)
    modules = ClientModule.objects.filter(user_id=customer_user.user_id)
    payable = 0
    for item in modules.filter(suspend=False):
        payable += item.module.amount
    payable = payable
    product = Product.objects.all()
    return render(request, 'backend/customer_profile.html', {'customer_id': customer_id, 'ref_id': ref_id,
                                                             'modules': modules, 'payable': payable, 'product': product,
                                                             'object': customer_user})


@login_required()
def verify_payment(request, customer_id, ref_id):
    customer_user = ClientProfile.objects.get(id=customer_id)
    modules = ClientModule.objects.filter(user_id=customer_user.user_id)
    payable = 0
    for item in modules.filter(suspend=False):
        payable += item.module.amount
    payable = payable
    product = Product.objects.all()
    headers = {
        "Content-Type": 'application/json',
        "Authorization": "Bearer " + 'sk_live_8e7fff67b47a13c21578b0d227f5d34c165cb374'
    }
    response = requests.get('https://api.paystack.co/transaction/verify/' + ref_id, headers=headers)
    pay_stack = response.json()
    if pay_stack['status'] is True and float(pay_stack['data']['amount'] / 100) == float(payable):
        for item in modules:
            today = datetime.date.today()
            item.last_pay_date = today
            item.next_pay_date = today + datetime.timedelta(days=30)
            item.is_active = True
            item.save()
        messages.success(request, 'Payment successful')
    else:
        messages.error(request, pay_stack['message'])

    return render(request, 'backend/customer_profile.html', {'customer_id': customer_id,
                                                             'modules': modules, 'payable': payable, 'product': product,
                                                             'object': customer_user})


class CreateProduct(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    template_name = 'backend/new_product.html'
    form_class = NewProductForm
    success_url = reverse_lazy('new_product')
    raise_exception = True

    def test_func(self):
        return user_is_staff(self.request)

    def form_valid(self, form):

        messages.success(self.request, 'New Product Created Successfully')
        return super().form_valid(form)


class EditProduct(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    template_name = 'backend/new_product.html'
    model = Product
    form_class = NewProductForm
    success_url = reverse_lazy('product_list')
    pk_url_kwarg = 'product_id'
    raise_exception = True

    def test_func(self):
        return user_is_staff(self.request)

    def form_valid(self, form):

        messages.success(self.request, 'Product Was Edited Successfully')
        return super().form_valid(form)


class CreateEducation(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    template_name = 'backend/new_edu_product.html'
    form_class = EducationForm
    success_url = reverse_lazy('new_edu_product')
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

    def test_func(self):
        return user_is_staff(self.request)

    def form_valid(self, form):
        messages.success(self.request, 'Education Created Successfully')
        return super().form_valid(form)


class EditEducation(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    template_name = 'backend/new_edu_product.html'
    model = Education
    form_class = EducationForm
    success_url = reverse_lazy('edit_edu_product')
    pk_url_kwarg = 'product_id'
    raise_exception = True

    def get_object(self, queryset=None):
        return Education.objects.first()

    def test_func(self):
        return user_is_staff(self.request)

    def form_valid(self, form):
        messages.success(self.request, 'Education Was Edited Successfully')
        return super().form_valid(form)


class EducationList(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Education
    template_name = 'backend/edu_product_list.html'
    raise_exception = True

    def test_func(self):
        return user_is_staff(self.request)


class ProductList(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Product
    template_name = 'backend/product_list.html'
    raise_exception = True

    def test_func(self):
        return user_is_staff(self.request)


@login_required()
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()

    messages.success(request, 'Product Was Deleted Successfully')

    return redirect('product_list')


class ProductPackage(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Packages
    form_class = PackageForm
    success_url = reverse_lazy('new_package')
    template_name = 'backend/new_package.html'
    raise_exception = True

    def test_func(self):
        return user_is_staff(self.request)

    def form_invalid(self, form):
        messages.error(self.request, 'Form Error.. You cannot have more than 3 packages')
        return super().form_invalid(form)

    def form_valid(self, form):
        packages = Packages.objects.all()
        if packages.count() == 3:
            return self.form_invalid(form)
        else:
            messages.success(self.request, 'New Package Created Successfully')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Packages.objects.all().order_by('-id')
        return context


class UpdateProductPackage(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Packages
    form_class = PackageForm
    success_url = reverse_lazy('new_package')
    template_name = 'backend/new_package.html'
    pk_url_kwarg = 'package_id'
    raise_exception = True

    def test_func(self):
        return user_is_staff(self.request)

    def form_valid(self, form):
        messages.success(self.request, 'Package Updated Successfully')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Packages.objects.all().order_by('-id')
        return context


@login_required()
def delete_package(request, package_id):
    package = Packages.objects.get(id=package_id)
    package.delete()

    messages.success(request, 'Package Deleted Successfully')
    return redirect('new_package')


class CustomerList(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    template_name = 'backend/customer_list.html'
    model = ClientProfile
    raise_exception = True

    def test_func(self):
        return user_is_staff(self.request)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['modules'] = ClientModule.objects.all()
        return context


class BannerTextView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    template_name = 'backend/banner_text.html'
    model = BannerText
    form_class = BannerTextForm
    success_url = reverse_lazy('banner_text')
    raise_exception = True

    def test_func(self):
        return user_is_staff(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = BannerText.objects.all().order_by('-id')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Banner text added successfully')
        return super().form_valid(form)


class BannerTextUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    template_name = 'backend/banner_text.html'
    model = BannerText
    form_class = BannerTextForm
    success_url = reverse_lazy('banner_text')
    pk_url_kwarg = 'banner_id'
    raise_exception = True

    def test_func(self):
        return user_is_staff(self.request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = BannerText.objects.all().order_by('-id')
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Banner text added successfully')
        return super().form_valid(form)


@login_required()
def banner_delete(request, banner_id):
    banner = BannerText.objects.get(id=banner_id)
    banner.delete()
    messages.success(request, 'Banner text deleted successfully')

    return redirect('banner_text')


@login_required()
def add_module(request, customer_id):
    customer = ClientProfile.objects.get(id=customer_id)
    try:
        ClientModule.objects.get(module_id=request.POST['module'], user_id=customer.user_id)
        messages.error(request, 'User already registered for this module')
    except ClientModule.DoesNotExist:
        module = ClientModule.objects.create(
            user_id=customer.user_id,
            module_id=request.POST['module']
        )
        module.save()
        messages.success(request, 'Action successful')
    return redirect('customer_profile', customer_id)


@login_required()
def delete_module(request, module_id, customer_id):
    customer = ClientProfile.objects.get(id=customer_id)
    module = ClientModule.objects.get(id=module_id, user_id=customer.user_id)
    module.delete()
    messages.success(request, 'Action successful')
    return redirect('customer_profile', customer_id)


@login_required()
def suspend_module(request, module_id, customer_id, action):
    customer = ClientProfile.objects.get(id=customer_id)
    module = ClientModule.objects.get(id=module_id, user_id=customer.user_id)
    if action == 'suspend':
        module.suspend = True
    else:
        module.suspend = False
    module.save()
    messages.success(request, 'Action Successful')
    return redirect('customer_profile', customer_id)


class DemoListView(generic.ListView):
    model = DemoList
    template_name = 'backend/demo_list.html'
