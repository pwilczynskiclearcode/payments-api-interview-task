from uuid import UUID

from django.test.client import Client

from pays.models import Payment


def test_fetching_single_payment(client: Client, payment: dict, db_payment: Payment):
    response = client.get(f"/api/v0/payment/{db_payment.id}/")

    assert response.status_code == 200

    assert UUID(response.json()["id"]) == db_payment.id
    assert response.json()["version"] == db_payment.version
    assert response.json()["organisation_id"] == "743d5b63-8e6f-432e-a8fa-c5d8d2ee5fcb"
    assert response.json()["attributes"] == db_payment.attributes


def test_fetching_single_payment_404(client: Client):
    response = client.get(f"/api/v0/payment/999d5b63-8e6f-432e-a8fa-c5d8d2ee5fop/")

    assert response.status_code == 404
