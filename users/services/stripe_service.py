import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_product(name, description=None):
    return stripe.Product.create(name=name, description=description)


def create_price(product_id, amount, currency="usd"):
    amount_in_cents = int(amount * 100)
    return stripe.Price.create(
        product=product_id, unit_amount=amount_in_cents, currency=currency
    )


def create_checkout_session(price_id, success_url, cancel_url):
    return stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
