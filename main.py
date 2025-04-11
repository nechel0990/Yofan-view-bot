import yaml
import json
import asyncio
from playwright.async_api import async_playwright

# Load config
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

url = config["link"]
target_views = int(config["target_views"])

# Load or initialize views.json
try:
    with open("views.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {"views_sent": 0}

views_sent = data.get("views_sent", 0)

async def send_view():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_timeout(5000)  # Wait 5 seconds to simulate view
        await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")  # Scroll
        await page.wait_for_timeout(2000)  # Wait again
        await browser.close()

# Run until target views are sent
async def run_views():
    global views_sent
    while views_sent < target_views:
        await send_view()
        views_sent += 1
        print(f"Views sent: {views_sent}")
        with open("views.json", "w") as f:
            json.dump({"views_sent": views_sent}, f)

asyncio.run(run_views())
