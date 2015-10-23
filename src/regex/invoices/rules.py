import rules


def is_invoice_contact(user, invoice):
    return invoice.client.contacts.filter(user__id=user.id).exists()


rules.add_perm('invoices.can_view_invoice', is_invoice_contact)
