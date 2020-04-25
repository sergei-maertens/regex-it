from appconf import AppConf


class InvoicesConf(AppConf):
    COMPANY_NAME = "Company Name"
    COMPANY_ADDRESS = ["address", "city", "country"]
    COMPANY_TAX_IDENTIFIER = "NL123456789B01"
    COMPANY_KVK = "12345678"
    COMPANY_IBAN = "NL48 INGB 1234 5678 91"
