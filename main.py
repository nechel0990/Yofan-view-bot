import yaml
import json
import time
import random
from pathlib import Path
from playwright.sync_api import sync_playwright

# Load settings
with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

link = config["link"]
target_views = config["target_views"]

# Load current view count
views_file = Path("views.json")
if views_file.exists():
    with open(views_file, "r") as f:
        views_data = json.load(f)
else:
    views_data = {"views_sent": 0}

views_sent = views_data["views_sent"]

if views_sent >= target_views:
    print(f"Target reached: {views_sent}/{target_views} views")
    exit()

def send_view():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(link, timeout=60000)
        print(f"Opened: {link}")

        for _ in range(random.randint(2, 4)):
            page.mouse.wheel(0, 1000)
            time.sleep(random.uniform(1, 2))

        wait_time = random.randint(20, 40)
        print(f"Waiting {wait_time}s to simulate view...")
        time.sleep(wait_time)
        browser.close()

send_view()
views_sent += 1
views_data["views_sent"] = views_sent

with open("views.json", "w") as f:
    json.dump(views_data, f)

print(f"Views sent: {views_sent}/{target_views}")