from django.shortcuts import render,redirect
from .models import Payment,OrderProduct
from cart.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order
from django.contrib.sites.shortcuts import get_current_site
from instamojo_wrapper import Instamojo
from django.conf import settings
import requests 
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


api = Instamojo(api_key=settings.API_KEY, auth_token=settings.AUTH_TOKEN, endpoint=settings.PAYMENT_PORTAL)


def paymentsuccess(request):
    status=request.GET.get('payment_status')
    payment_request_id=request.GET.get('payment_request_id')
    current_user = request.user
    payment=Payment.objects.get(payment_id=payment_request_id)
    order=Order.objects.get(payment=payment)
    if(status == 'Credit'):
        payment.status = 'Completed'
        order.is_ordered=True
        order.status='Accepted'

        cart_items=CartItem.objects.filter(user=current_user)
        for item in cart_items:
            orderproduct = OrderProduct()
            orderproduct.order_id = order.id
            orderproduct.payment = payment
            orderproduct.user_id = request.user.id
            orderproduct.product_id = item.product_id
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            cart_item = CartItem.objects.get(id=item.id)
            orderproduct = OrderProduct.objects.get(id=orderproduct.id)
            orderproduct.save()

        CartItem.objects.filter(user=request.user).delete()
        message='YOUR ORDER HAS BEEN RECIEVED'

        # Send order recieved email to customer
        mail_subject = 'Thank you for your order!'
        message = render_to_string('order/order_recieved_email.html', {
            'status': status,
            'user': request.user,
            'order': order,
            'message': message,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

    elif(status == 'Failed'):
        payment.status = 'Failed'
        order.status='Cancelled'
        CartItem.objects.filter(user=request.user).delete()
        message='Extremely Sorry for the issue. Kindly Contact our team to inform the issue!'
        # Send order recieved email to customer
        mail_subject = 'Thank you for your order!'
        message = render_to_string('order/order_recieved_email.html', {
            'status': status,
            'user': request.user,
            'order': order,
            'message': message,
        })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

    payment.save()
    order.save()



    return redirect('index')
# Create your views here.
def paynow(request, order_id):
    current_user = request.user
    current_site=get_current_site(request)
    success_site=str(current_site)+"/orders/success"
    failed_site=str(current_site)+"/orders/failed"
    order=Order.objects.get(order_number=order_id, user=current_user)
    if request.method=='POST':
        response = api.payment_request_create(
            amount=order.order_total,
            purpose='Order Process',
            send_email=True,
            email=current_user,
            redirect_url="https://senter.onrender.com/orders/payments_success"
        )
        # print the long URL of the payment request.
        print (response['payment_request']['longurl'])
        # print the unique ID(or payment request ID)
        print (response['payment_request'])
        payment = Payment(
                    user = current_user,
                    payment_id = response['payment_request']['id'],
                    payment_method = 'InstaMojo',
                    amount_paid = order.order_total,
                    status = 'New',
        )
        payment.save()

        order.payment = payment
            # order.is_ordered = True
        order.save()
        return redirect(response['payment_request']['longurl'])

def payments(request):
    if(request=='POST'):
        pay_now(request)
    return render(request,'order/payment.html')

def place_order(request):
    current_user = request.user
    total=0
    quantity=0
    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
            }
            return render(request, 'order/payment.html', context)
        else:
            return redirect('checkout')
    else:
        return redirect('checkout')