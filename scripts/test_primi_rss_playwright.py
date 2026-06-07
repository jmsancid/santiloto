from playwright.sync_api import sync_playwright

URL = "https://www.loteriasyapuestas.es/es/la-primitiva/resultados/.formatoRSS"

with sync_playwright() as p:
    browser = p.firefox.launch(headless=True)
    page = browser.new_page()
    page.goto(URL, wait_until="domcontentloaded", timeout=30000)
    print(page.content()[:4000])
    browser.close()
