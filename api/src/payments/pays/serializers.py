from rest_framework.serializers import (
    CharField, IntegerField, DecimalField, UUIDField, Serializer, ModelSerializer)

from pays.models import Payment


class MoneyField(DecimalField):

    def __init__(self, *args, **kwags):
        super().__init__(allow_null=False, max_digits=None, decimal_places=2, min_value=0,
                         coerce_to_string=True)

    def run_validation(self, data):
        return str(super().run_validation(data))


class BeneficiaryPartySerializer(Serializer):

    account_name = CharField(allow_blank=False)
    account_number = IntegerField(allow_null=False, min_value=0)
    account_number_code = CharField(allow_blank=False)
    account_type = IntegerField(min_value=0)
    address = CharField(allow_blank=False)
    bank_id = IntegerField(allow_null=False, min_value=0)
    bank_id_code = CharField(allow_blank=False)
    name = CharField(allow_blank=False)


class SenderChargesSerializer(Serializer):

    amount = MoneyField()
    currency = CharField(allow_null=False)


class ChargesInformationSerializer(Serializer):

    bearer_code = CharField(allow_blank=False)
    sender_charges = SenderChargesSerializer(many=True, allow_null=True)
    receiver_charges_amount = MoneyField()
    receiver_charges_currency = CharField(allow_null=False)


class PaymentAttributesSerializer(Serializer):

    amount = MoneyField()
    beneficiary_party = BeneficiaryPartySerializer(allow_null=False)
    charges_information = ChargesInformationSerializer(allow_null=False)
    currency = CharField(allow_blank=False)


class PaymentSerializer(ModelSerializer):

    id = UUIDField(read_only=True)
    attributes = PaymentAttributesSerializer(allow_null=False)
    organisation_id = UUIDField(allow_null=False)
    version = IntegerField(min_value=0)

    class Meta:
        model = Payment
        fields = ('id', 'attributes', 'organisation_id', 'version')

    def create(self, validated_payment: dict):
        return Payment.objects.create(**validated_payment)

    def update(self, db_payment: Payment, validated_payment: dict):
        if "attributes" in validated_payment:
            attributes = validated_payment.pop("attributes")

            if "charges_information" in attributes:
                charges_information = attributes.pop("charges_information")
                db_payment.attributes['charges_information'].update(**charges_information)
            db_payment.attributes.update(**attributes)

        for key, value in validated_payment.items():
            setattr(db_payment, key, value)

        db_payment.save()
        return db_payment
