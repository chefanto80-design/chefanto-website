"""Renders index.html in headless Chromium at phone, tablet and desktop widths.

Usage: python3 tests/test_render.py index.html   (needs: pip install playwright)
Checks for horizontal scrolling and JavaScript errors, and tests the mobile menu.
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

page_file = pathlib.Path(sys.argv[1]).resolve()
results = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    for w in (375, 768, 1440):
        pg = browser.new_page(viewport={"width": w, "height": 900})
        errors = []
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.goto(page_file.as_uri())
        pg.wait_for_timeout(300)
        sw = pg.evaluate("document.documentElement.scrollWidth")
        results.append((f"{w}px: no horizontal scroll", sw <= w, f"scrollWidth {sw}"))
        results.append((f"{w}px: no JavaScript errors", not errors, "; ".join(errors)))
        if w == 375:
            burger = pg.query_selector("#burger")
            if burger and burger.is_visible():
                burger.click()
                pg.wait_for_timeout(200)
                expanded = burger.get_attribute("aria-expanded")
                results.append(("375px: mobile menu opens (aria-expanded=true)", expanded == "true", f"aria-expanded={expanded}"))
            else:
                results.append(("375px: mobile menu button visible", False, "no visible #burger"))
        pg.close()
    browser.close()
for name, ok, d in results:
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  ({d})" if d else ""))
passed = sum(ok for _, ok, _ in results)
print(f"\n{passed}/{len(results)} checks passed")
sys.exit(0 if passed == len(results) else 1)
