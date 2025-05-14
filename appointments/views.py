from django.shortcuts import render, redirect
from .forms import AppointmentForm
from .models import AppointmentItem, Appointment
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from main.models import Specialist
from django.conf import settings
import stripe


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
print("STRIPE KEY:", settings.STRIPE_TEST_SECRET_KEY)


@login_required(login_url='/users/login')
def appointment_create(request):
    cart = Cart(request)
    total_price = sum(item['total_price'] for item in cart)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[
                        {
                            'price_data': {
                                'currency': 'usd',
                                'product_data': {
                                    'name': item['item'].name,
                                },
                                'unit_amount': int(item['total_price'] * 100),
                            },
                            'quantity': item['quantity'],
                        } for item in cart 
                    ],
                    mode='payment',
                    success_url='http://localhost:8000/appointments/completed',
                    cancel_url='http://localhost:8000/appointments/create',
                )

                # Now save the appointment only after successful session creation
                appointment = Appointment(
                    user=request.user,
                    first_name=form.cleaned_data.get('first_name'),
                    last_name=form.cleaned_data.get('last_name'),
                    middle_name=form.cleaned_data.get('middle_name'),
                    phone_number=form.cleaned_data.get('phone_number'),
                )
                appointment.save()

                for item in cart:
                    specialist_instance = Specialist.objects.get(name=item['specialist'])
                    AppointmentItem.objects.create(
                        appointment=appointment,
                        procedure=item['item'],
                        specialist=specialist_instance,
                        quantity=item['quantity'],
                        total_price=item['total_price'],
                    )

                return redirect(session.url, code=303)
            except Exception as e:
                return render(request, 'appointments/appointment_failure.html', {
                    'form': form,
                    'cart': cart,
                    'error': str(e),
                })
        else:
            # Handle invalid form
            return render(request, 'appointments/appointment_form.html', {
                'form': form,
                'cart': cart,
                'total_price': total_price,
                'error': 'Invalid form data. Please correct the errors.',
            })

    # Initial GET
    form = AppointmentForm(initial={
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'middle_name': request.user.middle_name,
        'phone_number': request.user.phone_number,
    })

    return render(request, 'appointments/appointment_form.html', {
        'form': form,
        'cart': cart,
        'total_price': total_price,
    })



@login_required(login_url='/users/login')
def appointment_success(request):
    cart = Cart(request)
    cart.clear()
    return render(request, 'appointments/appointment_success.html')

@login_required(login_url='/users/login')
def appointment_failure(request):
    return render(request, 'appointments/appointment_failure.html')
