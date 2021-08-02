from django.db import models
from django.http import request,JsonResponse
from django.shortcuts import redirect, render,HttpResponseRedirect,HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetView,PasswordResetConfirmView,PasswordResetCompleteView,LoginView,LogoutView,PasswordChangeView
from django.urls import reverse_lazy
from django.views import View
from . models import Cart, Product,Address,OrderPlaced
from . forms import SignUpForm,MyLoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm,AddressForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.views.generic.edit import FormView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.mail import send_mail
import math, random


class HomePageView(TemplateView):
    template_name = "shopapp/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mobiles'] = Product.objects.filter(catagory = 'M')
        context['laptops'] = Product.objects.filter(catagory = 'L')
        context['tops'] = Product.objects.filter(catagory='TW')
        context['bottoms'] = Product.objects.filter(catagory='BW')
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shopapp/product_detail.html'

class SignUp(View):
    def get(self,request):
        form = SignUpForm(initial={'username':self.request.GET.get('email_b',"")})
        return render(request,'myuser/signup.html',{'form':form})
    def post(self,request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['username']
            user = User.objects.get(username=email)
            user.email = email
            user.save()
            messages.success(request,f'Account Created Successfully {email}')
            return HttpResponseRedirect('/signup/')
        else:
            return render(request,'myuser/signup.html',{'form':form})

def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(6) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP

def send_otp(request):
    email=request.GET.get('id',None)
    if email is not None:
        # email=request.GET.get('id')
        print(email)
        o=generateOTP()
        htmlgen = '<p>Your OTP is <strong>'+o+'</strong></p>'
        send_mail('OTP request',o,'camar@gmail.com',[email], fail_silently=False, html_message=htmlgen)
        data = {
            'otp':o
        }
        return JsonResponse(data)
    else:
        return render(request,'shopapp/email_form.html')

def email_form(request):
    pass


def ckeck(request):
    return render(request,'myuser/check_mail.html')
# def active(request):
#     user = User.objects.get(user)
            
class MyLoginview(LoginView):
    template_name = 'myuser/login.html'
    authentication_form = MyLoginForm
    # success_url = reverse_lazy('signup')
    # success_message = 'Login Successfully'
    # redirect_authenticated_user = True

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        messages.success(self.request,'Loding Successfully')
        return HttpResponseRedirect(self.get_success_url())

class MyLogoutView(LogoutView):
    pass

@method_decorator(login_required(login_url='/login'), name='dispatch')
class MyPasswordChangeView(SuccessMessageMixin,PasswordChangeView):
    form_class = MyPasswordChangeForm
    template_name = 'myuser/password_change_form.html'
    # success_url = reverse_lazy('home') 
    success_url = '/'
    success_message = 'Password Changed Successfully'

class MyPasswordResetView(PasswordResetView):
    form_class = MyPasswordResetForm
    template_name = 'myuser/password_reset.html'
    success_url = reverse_lazy('password_reset_done')
    # from_email = settings.EMAIL_HOST_USER
    # html_email_template_name = 'myuser/password_reset_confirm.html'
    # success_url = '/password_reset_done/'
    
class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'myuser/password_reset_done.html'

class MyPasswordResetConfirmView(SuccessMessageMixin,PasswordResetConfirmView):
    form_class = MySetPasswordForm
    template_name = 'myuser/password_reset_confirm.html'
    # success_url = '/password_reset_complete/'
    success_url = reverse_lazy('password_reset_complete')
    success_message = 'Your Password Reset Done Successfully ,Go Ahead To '

class MyPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'myuser/password_reset_confirm_complete.html'

#----------Address Related Work--------
@method_decorator(login_required(login_url='/login'), name='dispatch')
class AddressTemplateView(TemplateView):
    template_name = 'address/show.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user = User.
        context['address'] = Address.objects.filter(user=self.request.user)
        return context

@method_decorator(login_required(login_url='/login'), name='dispatch')
class AddAddress(FormView):
    def get(self,request):
        form = AddressForm()
        return render(request,'address/add.html',{'form':form})

    def post(self,request):
        form = AddressForm(request.POST)
        if form.is_valid():
            usr = request.user
            street = form.cleaned_data['street']
            village = form.cleaned_data['village']
            distic = form.cleaned_data['district']
            state = form.cleaned_data['state']
            pin = form.cleaned_data['pin_code']
            mobile = form.cleaned_data['mobile']
            # usr = User.objects.filter(user=request.user)
            address = Address(user=usr,street=street,village=village,district=distic,state=state,pin_code=pin,mobile=mobile)
            address.save()
            messages.success(request,'Address Added Successfully')
            return HttpResponseRedirect('/address/')
        else:
            return render(request,'address/add.html',{'form':form})

#--------Cart----------------
@method_decorator(login_required(login_url='/login'), name='dispatch')
class AddToCart(View):
    def get(self,request):
        product_id = request.GET['product_id']
        product_instance = Product.objects.get(pk=product_id)
        add_cart = Cart(user=request.user,product=product_instance)
        add_cart.save()
        return redirect('show_cart')

@method_decorator(login_required(login_url='/login'), name='dispatch')
class ShowCartDeatil(View):
    def get(self,request):
        cart_item = Cart.objects.filter(user=request.user)
        cart_product = [p for p in cart_item]
        print(cart_product)
        total_amount = 0
        if cart_product:
            for item in cart_product:
                total_amount += (item.quantity*item.product.selling_price)
        print(total_amount)
        plus_shipping_amount = total_amount + 40
                
        # print(user_all_cart.product.selling_price)
        return render(request,'cart/show_cart.html',{'cart_item':cart_item,'total_amount':total_amount,'plus_shipping_amount':plus_shipping_amount})

@login_required(login_url='/login')
def plus_cart(request):
    if request.method == "GET":
        # user = request.user
        product_id = request.GET['id']
        print(product_id)
        print('start error')
        q = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        print('end error')
        q.quantity +=1
        q.save()
        cart_item = Cart.objects.filter(user=request.user)
        cart_product = [p for p in cart_item]
        total_amount = 0
        if cart_product:
            for item in cart_product:
                total_amount += (item.quantity*item.product.selling_price)
        print(total_amount)
        plus_shipping_amount = total_amount + 40

        data = {
            'quantity':q.quantity,
            'total_amount':total_amount,
            'plus_shipping_amount':plus_shipping_amount
        }

        return JsonResponse(data)

@login_required(login_url='/login')
def minu_cart(request):
    if request.method == "GET":
        product_id = request.GET['id']
        q = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        q.quantity -=1
        q.save()
        cart_item = Cart.objects.filter(user=request.user)
        cart_product = [p for p in cart_item]
        total_amount = 0
        if cart_product:
            for item in cart_product:
                total_amount += (item.quantity*item.product.selling_price)
        print(total_amount)
        plus_shipping_amount = total_amount + 40

        data = {
            'quantity':q.quantity,
            'total_amount':total_amount,
            'plus_shipping_amount':plus_shipping_amount
        }
        return JsonResponse(data)

@login_required(login_url='/login')
def remove_cart(request):
    if request.method == "GET":
        product_id = request.GET['id']
        q = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        q.delete()
        cart_item = Cart.objects.filter(user=request.user)
        cart_product = [p for p in cart_item]
        total_amount = 0
        if cart_product:
            for item in cart_product:
                total_amount += (item.quantity*item.product.selling_price)
        print(total_amount)
        plus_shipping_amount = total_amount + 40

        data = {
            'quantity':q.quantity,
            'total_amount':total_amount,
            'plus_shipping_amount':plus_shipping_amount
        }
        return JsonResponse(data)

@login_required(login_url='/login')
def order_summery(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    address = Address.objects.filter(user=user)
    return render(request,'shopapp/order_summary.html',{'cart':cart,'address':address})

@login_required(login_url='/login')
def payment_done(request):
    user = request.user
    adress_id = request.GET.get('address',default=None)
    if adress_id is not None:
        address = Address.objects.get(id=adress_id)
        cart = Cart.objects.filter(user=user)
        for item in cart:
            OrderPlaced(user=user,address=address,product=item.product,quantity=item.quantity).save()
            cart.delete()
        return redirect("orders")
    else:
        return redirect("order_summery")


@login_required(login_url='/login')
def orders(request):
    order = OrderPlaced.objects.filter(user=request.user)
    return render(request,'shopapp/orders.html',{'order':order})












