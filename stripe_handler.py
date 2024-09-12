# stripe_handler.py

import stripe
import logging

def initialize_stripe(sk_key):
    """Initialize Stripe API with the provided secret key."""
    stripe.api_key = sk_key
    try:
        stripe.Balance.retrieve()  # Simple API call to verify the key
        logging.info("API key is valid.")
        return True
    except stripe.error.AuthenticationError as e:
        logging.error(f"Authentication failed: {e}")
        return False

def process_verification_charge(card_details):
    """Process a $1 verification charge using Stripe's API."""
    card_number, exp_month, exp_year, cvc = card_details.split('|')
    try:
        # Create a PaymentMethod object using card details
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "number": card_number,
                "exp_month": exp_month,
                "exp_year": exp_year,
                "cvc": cvc
            }
        )

        # Create a PaymentIntent with a $1 charge for verification
        payment_intent = stripe.PaymentIntent.create(
            amount=100,  # $1 in cents
            currency='usd',
            payment_method=payment_method.id,
            confirm=True
        )

        logging.info(f"Charge successful for card ending in {card_number[-4:]}. PaymentIntent ID: {payment_intent.id}")

    except stripe.error.CardError as e:
        logging.error(f"Card declined or other card error: {e}")
    except stripe.error.StripeError as e:
        logging.error(f"Stripe API error: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
