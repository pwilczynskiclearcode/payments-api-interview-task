from django.test.client import Client

from pays.models import Payment


def test_deleting_payment(client: Client, db_payment: Payment):
    response = client.delete(f"/api/v0/payment/{db_payment.id}/")

    assert response.status_code == 204
    assert Payment.objects.count() == 0


def test_deleting_non_existing_payment_404(client: Client):
    response = client.delete(f"/api/v0/payment/z43d5b6x-8e6f-432e-a8fa-c5d8d2ee5fcb/")
    assert response.status_code == 404
