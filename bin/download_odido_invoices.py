#!/usr/bin/env python
import asyncio
import os
from contextlib import asynccontextmanager

from playwright.async_api import Page, async_playwright, expect

HEADLESS = "PLAYWRIGHT_NO_HEADLESS" not in os.environ
EMAIL = os.getenv("EMAIL", "")
PASSWORD = os.getenv("PASSWORD", "")

BASE = "https://www.odido.nl"
LOGIN_URL = f"{BASE}/login"
INVOICES_URL = f"{BASE}/my/facturen"
OVERVIEW_URL = f"{BASE}/my/abonnement-overzicht"


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


async def login(page: Page):
    await page.goto(LOGIN_URL)
    decline_cookie_btn = page.get_by_role(
        "button", name="Nee, ik wil geen optimale ervaring"
    )
    await decline_cookie_btn.click()
    await page.get_by_role("button", name="Inloggen bij Odido").click()

    # fill out credentials
    email_input = page.get_by_label("E-mailadres")
    await email_input.fill(EMAIL)
    password_input = page.get_by_label("Wachtwoord", exact=True)
    await password_input.fill(PASSWORD)

    # hit login button and prompt for 2FA code
    await page.get_by_role("button", name="Inloggen", exact=True).click()

    await asyncio.sleep(1)
    await expect(page.get_by_text("Tweestapsverificatie")).to_be_visible()

    mfa_textboxes = page.locator('input[name="verification-code"]')
    await expect(mfa_textboxes).to_have_count(4)
    mfa_code = input("Enter MFA code: ").strip()
    for textbox, number in zip(await mfa_textboxes.all(), mfa_code):
        await textbox.fill(number)

    await page.wait_for_url(OVERVIEW_URL)


def clean_text(text: str) -> str:
    parts = text.strip().split("\n")
    cleaned_parts = [cleaned for x in parts if (cleaned := x.strip())]
    return "\n".join(cleaned_parts)


async def go_to_invoices(page: Page):
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
        print(invoice_comments)
        await download.save_as("/tmp/" + download.suggested_filename)


async def main():
    async with browser_page() as page:
        await login(page)
        await go_to_invoices(page)


if __name__ == "__main__":
    asyncio.run(main())
