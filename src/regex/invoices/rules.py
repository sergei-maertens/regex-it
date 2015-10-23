import rules


def is_invoice_contact(user, invoice):
    import bpdb; bpdb.set_trace()


rules.add_perm('invoices.can_download_pdf', is_invoice_contact)
