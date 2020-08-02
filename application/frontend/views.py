from django.views import generic
from ..backend.models import Packages, BannerText, Product, ClientProfile, UserType, ClientModule, Education
from .forms import RegisterProductForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db import transaction
from .forms import LoginForm, DemoForm, DemoList
from ..base import send_welcome_email, send_notification


# Create your views here.


def login_redirect(request):
    user_id = request.user.id
    try:
        is_staff = UserType.objects.get(user_id=user_id).is_staff
        if is_staff is True:
            return redirect('dashboard')
        else:
            customer_pk = ClientProfile.objects.get(user_id=request.user.id).pk
            return redirect('customer_profile', customer_pk)
            pass
    except UserType.DoesNotExist:
        messages.error(request, 'System Error!...UserType does not exist')
        return redirect('login')


class Login(generic.FormView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('login')


class HomePage(generic.TemplateView):
    template_name = 'frontend/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['packages'] = Packages.objects.all()
        try:
            context['banner_text'] = BannerText.objects.get(activate=True)
        except BannerText.DoesNotExist:
            pass
        context['erp'] = Product.objects.filter(category=1)
        context['edu'] = Product.objects.filter(category=2)
        context['products'] = Product.objects.all()
        context['form'] = DemoForm
        return context


class Pricing(generic.TemplateView):
    template_name = 'frontend/pricing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['packages'] = Packages.objects.all()
        return context


class ProductDetail(generic.DetailView):
    template_name = 'frontend/inventory.html'
    model = Product
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DemoForm
        return context


class RegisterProduct(generic.FormView):
    template_name = 'frontend/register_product.html'
    form_class = RegisterProductForm

    def get_success_url(self):
        return reverse_lazy('register_product', kwargs={'package_id': self.kwargs['package_id'],
                                                        'modules': self.kwargs['modules']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        package = Packages.objects.get(id=self.kwargs['package_id'])

        s_modules = self.kwargs['modules']
        if s_modules == 'custom':
            context['s_modules'] = None
        elif s_modules == 'no-module':
            context['s_modules'] = 'None Selected'
        elif s_modules == 'all_package':
            all_module = []
            payable = 0
            modules = Product.objects.all()
            for item in modules:
                all_module.append(item.id)
                amount = Product.objects.get(id=item.id).amount
                payable += amount
            context['s_modules'] = list(map(int, all_module))
            context['product'] = Product.objects.all()
            context['payable'] = payable
        elif s_modules == 'education':
            package.name = 'Educational Module'
            payable = 0
            all_module = []
            modules = Product.objects.filter(category=2)
            for item in modules:
                all_module.append(item.id)
                amount = Product.objects.get(id=item.id).amount
                payable += amount
            context['payable'] = payable
            context['product'] = modules
            all_module = []
            modules = Product.objects.all()
            for item in modules:
                all_module.append(item.id)
            context['s_modules'] = list(map(int, all_module))

        else:
            s_modules = list(self.request.session.get('s_module', ''))
            payable = 0
            for element in s_modules:
                if element == ',':
                    s_modules.remove(element)
            for element in s_modules:
                amount = Product.objects.get(id=int(element)).amount
                payable += amount

            results = list(map(int, s_modules))
            context['payable'] = payable
            context['s_modules'] = results
            context['product'] = Product.objects.all()
        context['package'] = package
        return context

    @staticmethod
    def generate_username(first_name, last_name):
        val = "{0}{1}".format(first_name[0], last_name).lower()
        x = 0
        while True:
            if x == 0 and User.objects.filter(username=val).count() == 0:
                return val
            else:
                new_val = "{0}{1}".format(val, x)
                if User.objects.filter(username=new_val).count() == 0:
                    return new_val
            x += 1
            if x > 1000000:
                raise Exception("Name is super popular!")

    def form_valid(self, form):
        if self.request.method == 'POST':
            f_name = self.request.POST['first_name']
            l_name = self.request.POST['last_name']
            email = self.request.POST['email']
            company_name = self.request.POST['company_name']
            phone = self.request.POST['phone']
            address = self.request.POST['address']

            username = self.generate_username(f_name, l_name)
            password = User.objects.make_random_password()
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    first_name=f_name,
                    last_name=l_name,
                    email=email,
                    password=password
                )
                user.save()
                user_type = UserType.objects.create(
                    user=user,
                    is_staff=False
                )
                user_type.save()

                s_modules = self.kwargs['modules']
                package = Packages.objects.get(id=self.kwargs['package_id'])
                if s_modules == 'custom':
                    new_profile = ClientProfile.objects.create(
                        user=user,
                        phone=phone,
                        address=address,
                        package_id=package.id,
                        company_name=company_name
                    )
                elif s_modules == 'no-module':
                    new_profile = ClientProfile.objects.create(
                        user=user,
                        phone=phone,
                        address=address,
                        package_id=package.id,
                        company_name=company_name
                    )
                elif s_modules == 'all_package':
                    product = Product.objects.all()
                    for item in product:
                        client_modules = ClientModule.objects.create(
                            user=user,
                            module_id=item.id,

                        )
                        client_modules.save()
                    new_profile = ClientProfile.objects.create(
                        user=user,
                        phone=phone,
                        address=address,
                        package_id=package.id,
                        company_name=company_name,
                    )
                elif s_modules == 'education':
                    product = Product.objects.filter(category=2)
                    for item in product:
                        client_modules = ClientModule.objects.create(
                            user=user,
                            module_id=item.id,
                        )
                        client_modules.save()
                    new_profile = ClientProfile.objects.create(
                        user=user,
                        phone=phone,
                        address=address,
                        package_id=package.id,
                        company_name=company_name,
                    )

                else:
                    s_modules = list(self.request.session.get('s_module', ''))
                    s_modules = list(s_modules)
                    for element in s_modules:
                        if element == ',':
                            s_modules.remove(element)
                    for element in s_modules:
                        try:
                            Product.objects.get(id=int(element))
                            client_modules = ClientModule.objects.create(
                                user=user,
                                module_id=element,
                            )
                            client_modules.save()
                        except KeyError:
                            pass

                    new_profile = ClientProfile.objects.create(
                        user=user,
                        phone=phone,
                        address=address,
                        package_id=package.id,
                        company_name=company_name,
                    )
                new_profile.save()

            send_welcome_email(user.id, password)
            send_notification(user.id)
            messages.success(self.request, 'Your registration was successful.. Please check your email for more '
                                           'instructions')
        return super().form_valid(form)


def process_modular(request, package_id):
    form_post = request.POST
    module = []
    for item in form_post:
        module.append(item)

    module.pop(0)

    modular_string = ''
    for ele in module:
        modular_string += ele + ','
        request.session['s_module'] = modular_string

    if len(modular_string) is 0:
        modular_string = 'no-module'

    return redirect('register_product', package_id, 'single')


def demo_view(request, package_id=None):
    form = DemoList.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        phone=request.POST['phone'],
        email=request.POST['email'],
        company_name=request.POST['company_name'],
        company_address=request.POST['company_address'],
        demo_type=request.POST['demo_type']
    )
    form.save()
    messages.success(request, 'Your request for Demo has been received. We will contact you shortly')
    if request.POST['demo_type'] == "education":
        return redirect('education',)

    return redirect('product_detail', package_id)


class EducationView(generic.TemplateView):
    template_name = 'frontend/education.html'
    form_class = RegisterProductForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['product'] = Product.objects.filter(category=2)
        context['form'] = DemoForm
        return context