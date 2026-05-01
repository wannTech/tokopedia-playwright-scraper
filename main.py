import asyncio
from playwright.async_api import async_playwright
import openpyxl
import time

def extract_sold(item):
    labels = item.get("labelGroups", [])
    for l in labels:
        title = l.get("title", "")
        if "terjual" in title.lower():
            return title
    return None


def save_excel(data):
    filename = f"tokopedia_60_{int(time.time())}.xlsx"

    wb = openpyxl.Workbook()
    ws = wb.active

    ws.append(["Title", "Price", "Rating", "Sold", "Shop", "Location", "URL"])

    for d in data:
        ws.append([
            d["title"],
            d["price"],
            d["rating"],
            d["sold"],
            d["shop"],
            d["location"],
            d["url"],
        ])

    wb.save(filename)
    print(f"✅ Saved: {filename}")


async def scrape_60():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        products = []
        seen = set()

        async def handle_response(response):
            if "SearchProductV5Query" in response.url:
                try:
                    json_data = await response.json()

                    # handle array response
                    if isinstance(json_data, list):
                        json_data = json_data[0]

                    items = json_data.get("data", {}) \
                                     .get("searchProductV5", {}) \
                                     .get("data", {}) \
                                     .get("products", [])

                    print("🔥 items:", len(items))

                    for item in items:
                        title = item.get("name")

                        if not title or title in seen:
                            continue
                        seen.add(title)

                        products.append({
                            "title": title,
                            "price": item.get("price", {}).get("number"),
                            "rating": item.get("rating"),
                            "sold": extract_sold(item),
                            "shop": item.get("shop", {}).get("name"),
                            "location": item.get("shop", {}).get("city"),
                            "url": item.get("url"),
                        })

                except Exception as e:
                    print("❌ ERROR:", e)

        page.on("response", handle_response)

        print("Buka Tokopedia...")
        await page.goto("https://www.tokopedia.com/search?st=product&q=sepatu%20pria")

        # tunggu request pertama
        await page.wait_for_timeout(6000)

        await browser.close()
        return products


async def main():
    data = await scrape_60()

    print("\nTOTAL:", len(data))

    save_excel(data)


if __name__ == "__main__":
    asyncio.run(main())
