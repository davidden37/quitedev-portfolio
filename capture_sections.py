#!/usr/bin/env python3
"""Capture v4 portfolio per section — forces all reveal animations visible."""
import os
from playwright.sync_api import sync_playwright

OUT = "/data/data/com.termux/files/home/portfolio"
URL = "file:///data/data/com.termux/files/home/portfolio/index.html"

sections = [
    ("01_hero", "section.hero"),
    ("02_about", "section#about"),
    ("03_work", "section#work"),
    ("04_stack", "section#stack"),
    ("05_reach_closing", "section#reach"),
    ("06_closing_footer", "section.closing"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        executable_path="/usr/bin/chromium",
        args=["--no-sandbox", "--disable-gpu", "--disable-dev-shm-usage"],
    )
    ctx = browser.new_context(viewport={"width": 1280, "height": 900})
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)  # let fonts load

    # Force all reveal animations to visible (skip IntersectionObserver)
    page.evaluate("document.querySelectorAll('.reveal').forEach(el => el.classList.add('in'))")
    page.wait_for_timeout(500)

    for name, sel in sections:
        el = page.locator(sel).first
        try:
            # Scroll element to top of viewport so it renders fully
            el.scroll_into_view_if_needed()
            page.wait_for_timeout(500)
            path = f"{OUT}/{name}.png"
            el.screenshot(path=path)
            print(f"OK: {name}.png ({os.path.getsize(path)} bytes)")
        except Exception as e:
            print(f"FAIL: {name}: {e}")

    # Bonus: full page from top
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(500)
    path = f"{OUT}/00_full_top.png"
    page.screenshot(path=path, clip={"x": 0, "y": 0, "width": 1280, "height": 900})
    print(f"OK: 00_full_top.png ({os.path.getsize(path)} bytes)")

    browser.close()
