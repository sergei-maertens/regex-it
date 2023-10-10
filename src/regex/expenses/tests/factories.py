import factory


class CreditorFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("bs")

    class Meta:
        model = "expenses.Creditor"


class InvoiceFactory(factory.django.DjangoModelFactory):
    identifier = factory.Faker("word")
    date = factory.Faker("date_this_decade", after_today=False)
    amount = factory.Faker("pydecimal", left_digits=3, right_digits=2, min_value=1)

    class Meta:
        model = "expenses.Invoice"

    class Params:
        with_pdf = factory.Trait(
            pdf=factory.django.FileField(
                data=b"dummy", name=factory.Sequence(lambda n: f"invoice-{n}.pdf")
            ),
        )
