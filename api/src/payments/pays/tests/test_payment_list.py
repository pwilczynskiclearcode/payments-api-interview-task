from uuid import UUID

from django.test.client import Client

from pays.models import Payment


def test_listing_payments_empty(db, client: Client):
    response = client.get("/api/v0/payments/")

    assert response.status_code == 200
    assert response.json() == []


def test_listing_payments(client: Client, payment: dict, db_payment: Payment):
    response = client.get("/api/v0/payments/")

    assert response.status_code == 200
    assert len(response.json()) == 1

    assert UUID(response.json()[0].pop("id")) == db_payment.id
    assert response.json()[0] == payment
