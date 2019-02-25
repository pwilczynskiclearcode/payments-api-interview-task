from django.test.client import Client

from pays.models import Payment


def test_patching_payment_organisation_id(client: Client, db_payment: Payment):
    assert str(db_payment.organisation_id) == "743d5b63-8e6f-432e-a8fa-c5d8d2ee5fcb"

    response = client.patch(f"/api/v0/payment/{db_payment.id}/",
                            data={"organisation_id": "143d5b63-8e6f-432e-a8fa-c5d8d2ee5fcd"},
                            content_type="application/json")

    assert response.status_code == 200
    db_payment.refresh_from_db()
    assert str(db_payment.organisation_id) == "143d5b63-8e6f-432e-a8fa-c5d8d2ee5fcd"


def test_patching_payment_amount(client: Client, db_payment: Payment):
    assert db_payment.attributes["amount"] == "100.21"

    response = client.patch(f"/api/v0/payment/{db_payment.id}/",
                            data={"attributes": {"amount": "100.22"}},
                            content_type="application/json")

    assert response.status_code == 200
    db_payment.refresh_from_db()
    assert db_payment.attributes["amount"] == "100.22"


def test_patching_payment_charges_zero(client, db_payment: Payment, payment: dict):
    assert db_payment.attributes["amount"] == "100.21"

    response = client.patch(f"/api/v0/payment/{db_payment.id}/",
                            data={"attributes": {"charges_information": {"sender_charges": []}}},
                            content_type="application/json")

    assert response.status_code == 200
    db_payment.refresh_from_db()
    payment["attributes"]["charges_information"]["sender_charges"] = []
    assert db_payment.attributes == payment["attributes"]


def test_updating_entire_payment(client, db_payment: Payment):
    request_data = {
        "id": "216d4da9-e59a-4cc6-8df3-3da6e7580b77",
        "version": 1,
        "organisation_id": "743d5b63-8e6f-432e-a8fa-c5d8d2ee5fcb",
        "attributes": {
            "amount": "100.21",
            "beneficiary_party": {
                "account_name": "W Owens",
                "account_number": 31926819,
                "account_number_code": "BBAN",
                "account_type": 0,
                "address": "1 The Beneficiary Localtown SE2",
                "bank_id": 403000,
                "bank_id_code": "GBDSC",
                "name": "Wilfred Jeremiah Owens"
            },
            "charges_information": {
                "bearer_code": "SHAR",
                "sender_charges": [
                    {
                        "amount": "5.00",
                        "currency": "GBP"
                    },
                    {
                        "amount": "10.00",
                        "currency": "USD"
                    }
                ],
                "receiver_charges_amount": "1.00",
                "receiver_charges_currency": "USD"
            },
            "currency": "GBP"
        }
    }
    response = client.patch(f"/api/v0/payment/{db_payment.id}/",
                            data=request_data, content_type="application/json")

    assert response.status_code == 200
    db_payment.refresh_from_db()
    assert str(db_payment.id) != request_data["id"], "it is not possible to overwrite payment id"
    assert db_payment.attributes == request_data["attributes"]


def test_patching_payment_failure(client, db_payment: Payment, payment: dict):
    response = client.patch(f"/api/v0/payment/{db_payment.id}/",
                            data={"attributes": {"amount": "-100.22"}},
                            content_type="application/json")

    assert response.status_code == 400
    assert response.json() == {
        "attributes": {"amount": ["Ensure this value is greater than or equal to 0."]}
    }
    db_payment.refresh_from_db()
    assert db_payment.attributes["amount"] == "100.21"
