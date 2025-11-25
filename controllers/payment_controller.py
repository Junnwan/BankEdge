import stripe
import os
from flask import Blueprint, redirect, url_for, request, flash

payment_bp = Blueprint('payment', __name__)

# Use your actual keys
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', '')

@payment_bp.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        # Get amount from the modal form
        amount_str = request.form.get('amount', '20')
        amount_in_cents = int(float(amount_str) * 100)

        session = stripe.checkout.Session.create(
            payment_method_types=['card', 'fpx', 'grabpay'],
            line_items=[{
                'price_data': {
                    'currency': 'myr',
                    'product_data': {'name': 'BankEdge Service'},
                    'unit_amount': amount_in_cents,
                },
                'quantity': 1,
            }],
            mode='payment',
            # Redirect back to the endpoint that renders your dashboard (e.g., 'dashboard')
            success_url=url_for('dashboard', _external=True) + '?payment_status=success',
            cancel_url=url_for('dashboard', _external=True) + '?payment_status=cancel',
        )
        return redirect(session.url, code=303)

    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('dashboard'))