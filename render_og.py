#!/usr/bin/env python3
"""Render og_template.html to a 1200x630 PNG using system chromium."""
import os
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(HERE, "og_template.html")
OUT  = os.path.join(HERE, "og.png")

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path="/usr/bin/chromium",
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
    )
    ctx = browser.new_context(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
    page = ctx.new_page()
    page.goto(f"file://{HTML}")
    page.wait_for_load_state("networkidle")
    page.screenshot(path=OUT, clip={"x": 0, "y": 0, "width": 1200, "height": 630}, omit_background=False)
    browser.close()

print(f"OK: {OUT}")