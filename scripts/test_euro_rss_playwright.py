from playwright.sync_api import sync_playwright

URL = "https://www.loteriasyapuestas.es/es/euromillones/resultados/.formatoRSS"

def main() -> None:
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        content = page.content()
        browser.close()

    print(content[:5000])

if __name__ == "__main__":
    main()
