import pytest

from pays.models import Payment


@pytest.fixture
def payment() -> dict:
    return {
        "version": 0,
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
            "currency": "GBP",
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
        }
    }


@pytest.fixture
def db_payment(db, payment) -> Payment:
    return Payment.objects.create(**payment)
