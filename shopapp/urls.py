
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('',views.HomePageView.as_view(),name='home'),
    path('productdetail/<int:pk>/',views.ProductDetailView.as_view(),name='productdetail'),

    path('registration/',views.SignUp.as_view(),name='registration'),
    path('signup/',views.send_otp,name='signup'),

    path('login/',views.MyLoginview.as_view(),name='login'),
    path('logout/',views.MyLogoutView.as_view(),name='logout'),
    path('passwordchange/',views.MyPasswordChangeView.as_view(),name='passwordchange'),

    path('password_reset/',views.MyPasswordResetView.as_view(),name='password_reset'),
    path('password_reset_done/',views.MyPasswordResetDoneView.as_view(),name='password_reset_done'),
    path('passqord_reset_confirm/<uidb64>/<token>/',views.MyPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('password_reset_complete/',views.MyPasswordResetCompleteView.as_view(),name='password_reset_complete'),

    path('address/',views.AddressTemplateView.as_view(),name='address'),
    path('add_address/',views.AddAddress.as_view(),name='add_address'),

    path('add_to_cart/',views.AddToCart.as_view(),name='add_to_cart'),
    path('show_cart/',views.ShowCartDeatil.as_view(),name='show_cart'),
    path('pluscart/',views.plus_cart),
    path('minus-cart/',views.minu_cart),
    path('remove-cart/',views.remove_cart),

    path('order_summery/',views.order_summery,name='order_summery'),
    path('payment_done/',views.payment_done,name='payment_done'),
    path('orders/',views.orders,name='orders'),

    path('send_otp/',views.send_otp,name='send_otp'),
    # path('send_otps/',views.send_otps,name='send_otps'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
