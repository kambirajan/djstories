from playwright.sync_api import sync_playwright
import time


def scrape_chapter(base_url):
    all_pages = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        try:
            page = browser.new_page()

            # Open first page
            page.goto(
                base_url,
                wait_until="domcontentloaded",
                timeout=200000
            )

            # Find total pages
            links = page.query_selector_all(
                "a.pagination-number"
            )

            pages = [1]

            for link in links:
                txt = link.inner_text().strip()

                if txt.isdigit():
                    pages.append(int(txt))

            max_page = max(pages)

            # Scrape all pages
            for i in range(1, max_page + 1):

                url = (
                    base_url
                    if i == 1
                    else f"{base_url}?page={i}"
                )

                # Retry up to 3 times
                for attempt in range(3):
                    try:
                        page.goto(
                            url,
                            wait_until="domcontentloaded",
                            timeout=200000
                        )
                        break

                    except Exception:
                        if attempt == 2:
                            raise

                        time.sleep(2)

                content = ""

                # Try preferred selector first
                try:
                    page.wait_for_selector(
                        "div.chapter-body.protected-reader-content",
                        timeout=5000
                    )

                    content = page.locator(
                        "div.chapter-body.protected-reader-content"
                    ).inner_text()

                except Exception:
                    # Fallback that works on this site
                    content = page.locator(
                        "body"
                    ).inner_text()

                if not content.strip():
                    raise Exception(
                        f"No content found on page {i}"
                    )

                if "enable JavaScript" in content:
                    raise Exception(
                        f"Blocked on page {i}"
                    )

                all_pages.append(content)

            return "\n\n".join(all_pages)

        finally:
            browser.close()



# from playwright.sync_api import sync_playwright


# def scrape_chapter(base_url):
#     all_pages = []

#     with sync_playwright() as p:
#         browser = p.chromium.launch(
#             headless=True
#             # For debugging:
#             # headless=False,
#             # slow_mo=500
#         )

#         page = browser.new_page()

#         # Open first page
#         page.goto(
#             base_url,
#             wait_until="domcontentloaded",
#             timeout=200000
#         )

#         print("=" * 50)
#         print("Base URL:", page.url)
#         print("Title:", page.title())

#         # Find total pages
#         links = page.query_selector_all(
#             "a.pagination-number"
#         )

#         pages = [1]

#         for link in links:
#             txt = link.inner_text().strip()

#             if txt.isdigit():
#                 pages.append(int(txt))

#         max_page = max(pages)

#         print(f"Total pages found: {max_page}")

#         # Scrape every page
#         for i in range(1, max_page + 1):

#             url = (
#                 base_url
#                 if i == 1
#                 else f"{base_url}?page={i}"
#             )

#             print(f"\nScraping page {i}")
#             print(url)

#             page.goto(
#                 url,
#                 wait_until="domcontentloaded",
#                 timeout=200000
#             )

#             # Save debug files for first page only
#             if i == 1:
#                 page.screenshot(
#                     path="debug.png",
#                     full_page=True
#                 )

#                 with open(
#                     "debug.html",
#                     "w",
#                     encoding="utf-8"
#                 ) as f:
#                     f.write(page.content())

#             # Try the original selector
#             content = ""

#             try:
#                 page.wait_for_selector(
#                     "div.chapter-body.protected-reader-content",
#                     timeout=5000
#                 )

#                 content = page.locator(
#                     "div.chapter-body.protected-reader-content"
#                 ).inner_text()

#                 print("Using protected-reader-content selector")

#             except Exception:
#                 print(
#                     "Selector not found, using body text fallback"
#                 )

#                 content = page.locator(
#                     "body"
#                 ).inner_text()

#             if not content.strip():
#                 raise Exception(
#                     f"No content found on page {i}"
#                 )

#             if "enable JavaScript" in content:
#                 raise Exception(
#                     f"Blocked on page {i}"
#                 )

#             all_pages.append(content)

#             print(
#                 f"Page {i} scraped successfully "
#                 f"({len(content)} characters)"
#             )

#         browser.close()

#     return "\n\n".join(all_pages)