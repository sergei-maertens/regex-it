import asyncio
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Callable, Protocol

from playwright.async_api import Page, async_playwright, expect

HEADLESS = "PLAYWRIGHT_NO_HEADLESS" not in os.environ

BASE = "https://www.odido.nl"
LOGIN_URL = f"{BASE}/login"
INVOICES_URL = f"{BASE}/my/facturen"
OVERVIEW_URL = f"{BASE}/my/abonnement-overzicht"


class OnInvoiceDownload(Protocol):
    async def __call__(self, filepath: Path, comments: str) -> None:  # pragma: no cover
        ...


async def main(
    email: str,
    password: str,
    on_mfa_prompt: Callable[[], str],
    on_invoice_download: OnInvoiceDownload,
):
    async with browser_page() as page:
        await login(page, email, password, on_mfa_prompt)
        await download_invoices(page, on_invoice_download)


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


async def login(
    page: Page, email: str, password: str, on_mfa_prompt: Callable[[], str]
):
    await page.goto(LOGIN_URL)
    decline_cookie_btn = page.get_by_role(
        "button", name="Nee, ik wil geen optimale ervaring"
    )
    await decline_cookie_btn.click()

    # fill out credentials
    email_input = page.get_by_label("E-mailadres")
    await email_input.fill(email)
    password_input = page.get_by_label("Wachtwoord", exact=True)
    await password_input.fill(password)

    # hit login button and prompt for 2FA code
    await page.get_by_role("button", name="Inloggen", exact=True).click()

    await asyncio.sleep(1)
    await expect(page.get_by_text("Tweestapsverificatie")).to_be_visible()

    mfa_textboxes = page.locator('input[name="verification-code"]')
    await expect(mfa_textboxes).to_have_count(4)
    mfa_code = on_mfa_prompt().strip()
    for textbox, number in zip(await mfa_textboxes.all(), mfa_code):
        await textbox.fill(number)

    await page.wait_for_url(OVERVIEW_URL)


def clean_text(text: str) -> str:
    parts = text.strip().split("\n")
    cleaned_parts = [cleaned for x in parts if (cleaned := x.strip())]
    return "\n".join(cleaned_parts)


async def download_invoices(page: Page, on_invoice_download: OnInvoiceDownload) -> None:
    await page.goto(INVOICES_URL)
    await expect(page.get_by_text("Betaalde facturen")).to_be_visible(timeout=30_000)

    invoice_entries = page.get_by_role("listitem").filter(
        has=page.get_by_role("link", name="Factuur", exact=True)
    )
    for item in await invoice_entries.all():
        texts = await item.all_text_contents()
        download_link = item.get_by_role("link", name="Factuur", exact=True)
        invoice_comments = "".join([clean_text(text) for text in texts])
        async with page.expect_download() as download_info:
            await download_link.click()
        download = await download_info.value
        download_path = await download.path()
        assert download_path
        await on_invoice_download(download_path, invoice_comments)
