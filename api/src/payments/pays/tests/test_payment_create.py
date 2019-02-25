from uuid import UUID

import pytest
from django.test.client import Client

from pays.models import Payment


pytestmark = [pytest.mark.django_db]


def test_creating_payment(client: Client, payment: dict):
    response = client.post("/api/v0/payments/", data=payment, content_type="application/json")

    assert response.status_code == 201
    uuid = UUID(response.json().pop("id"))
    assert response.json() == payment

    db_payment = Payment.objects.get()
    assert db_payment.id == uuid
    assert db_payment.version == 0
    assert db_payment.organisation_id == UUID("743d5b63-8e6f-432e-a8fa-c5d8d2ee5fcb")
    assert db_payment.attributes == payment["attributes"]


def test_creating_payment_validation(client: Client, payment: dict):
    # rebuild payment request so it contains many errors:
    payment["organisation_id"] = "743d5b63-8e6f-432e-a8fa-c5d8d2ee5fc"
    attributes = payment["attributes"]
    attributes["amount"] = "this_is_not_a_number"
    del attributes["beneficiary_party"]
    attributes["charges_information"]["sender_charges"][0]["amount"] = "this_is_not_a_decimal_value"
    del attributes["charges_information"]["sender_charges"][0]["currency"]

    response = client.post("/api/v0/payments/", data=payment, content_type="application/json")

    assert response.status_code == 400
    assert response.json() == {
        "organisation_id": ["Must be a valid UUID."],
        "attributes": {
            "amount": ["A valid number is required."],
            'beneficiary_party': ['This field is required.'],
            'charges_information': {
                'sender_charges': [{
                    'amount': ["A valid number is required."],
                    'currency': ['This field is required.'],
                }, {}]
            }
        }
    }

    assert Payment.objects.count() == 0
