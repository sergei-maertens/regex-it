import os
import sys
import tempfile

INVOICES_COMPANY_NAME = os.getenv("COMPANY_NAME")
INVOICES_COMPANY_ADDRESS = (os.getenv("COMPANY_ADDRESS") or "").split(",")
INVOICES_COMPANY_TAX_IDENTIFIER = os.getenv("COMPANY_TAX_IDENTIFIER")
INVOICES_COMPANY_KVK = os.getenv("COMPANY_KVK")
INVOICES_COMPANY_IBAN = os.getenv("COMPANY_IBAN")


if "test" in sys.argv:
    MEDIA_ROOT = tempfile.mkdtemp()
    PRIVATE_MEDIA_ROOT = tempfile.mkdtemp()
