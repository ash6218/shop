from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/<int:product_id>/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('pay/<int:order_id>/', views.OrderPayView.as_view(), name='order_pay'),
    path('verify/', views.OrderVerifyView.as_view(), name='order_verify'),
    path('unpaid/', views.UnpaidOrderView.as_view(), name='unpaid_orders'),
    path('paid/', views.paidOrderView.as_view(), name='paid_orders'),
    path('unpaid_detail/<int:order_id>/', views.UnpaidDetailView.as_view(), name='unpaid_detail'),
    path('paid_detail/<int:order_id>/', views.PaidDetailView.as_view(), name='paid_detail'),
    path('delete_unpaid/<int:order_id>/', views.DeleteUnpaidOrderView.as_view(), name='delete_unpaid'),
]