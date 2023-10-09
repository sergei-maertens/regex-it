import os
from contextlib import asynccontextmanager
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Protocol

from dateutil.parser import parse, parserinfo
from playwright.async_api import Page, async_playwright, expect

HEADLESS = "PLAYWRIGHT_NO_HEADLESS" not in os.environ

BASE = "https://mijn.kpn.com/"
INVOICES_URL = f"{BASE}#/facturen"


class OnInvoiceDownload(Protocol):
    async def __call__(
        self,
        filepath: Path,
        invoice_date: date,
        amount: Decimal,
    ) -> None:  # pragma: no cover
        ...


async def main(
    email: str,
    password: str,
    start: date,
    end: date,
    on_invoice_download: OnInvoiceDownload,
):
    async with browser_page() as page:
        await login(page, email, password)
        await download_invoices(page, start, end, on_invoice_download)


@asynccontextmanager
async def browser_page():
    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=HEADLESS)
            context = await browser.new_context(
                locale="nl-NL",
                timezone_id="Europe/Amsterdam",
            )
            page = await context.new_page()
            yield page
        finally:
            await browser.close()


async def login(page: Page, email: str, password: str) -> None:
    await page.goto(BASE)
    await page.wait_for_url("https://inloggen.kpn.com/**")
    decline_cookie_btn = page.get_by_role("button", name="Nee, liever niet")
    await decline_cookie_btn.click()

    # fill out credentials
    email_input = page.get_by_label("E-mailadres", exact=True)
    await email_input.fill(email)
    password_input = page.get_by_label("Wachtwoord", exact=True)
    await password_input.fill(password)

    # hit login button
    await page.get_by_role("button", name="Inloggen", exact=True).click()
    await page.wait_for_url(f"{BASE}#/overzicht")


class nl_parserinfo(parserinfo):
    MONTHS = [
        ("jan", "januari"),
        ("feb", "februari"),
        ("mrt", "maart"),
        ("apr", "april"),
        ("mei", "mei"),
        ("jun", "juni"),
        ("jul", "juli"),
        ("aug", "augustus"),
        ("sep", "sept", "september"),
        ("okt", "oktober"),
        ("nov", "november"),
        ("dec", "december"),
    ]


def parse_date(timestr: str):
    return parse(timestr, parserinfo=nl_parserinfo()).date()


async def download_invoices(
    page: Page,
    start: date,
    end: date,
    on_invoice_download: OnInvoiceDownload,
) -> None:
    # navigate to invoices
    await page.goto(INVOICES_URL)
    await page.get_by_text("Thuis").click()

    await expect(page.get_by_text("Facturen")).to_be_visible()

    for item in await page.get_by_role("listitem").all():
        spans = await item.locator("span").all()
        datestr, _, amount = [await span.text_content() for span in spans]
        assert datestr
        invoice_date = parse_date(datestr)
        if not (start <= invoice_date <= end):
            continue

        assert amount
        invoice_amount = Decimal(amount.replace(",", ".").replace("€", "").strip())

        async with page.expect_download() as download_info:
            await item.click()
        download = await download_info.value
        download_path = await download.path()
        assert download_path
        await on_invoice_download(
            download_path,
            invoice_date=invoice_date,
            amount=invoice_amount,
        )
