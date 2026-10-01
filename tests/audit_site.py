"""Audit of the chefanto.com home page (index.html) against the Chef Anto brand kit and web basics.

Usage: python3 tests/audit_site.py index.html
Python 3 only, no installs. Reports PASS / FAIL / WARN; it does not change the page.
"""
import re
import sys
from html.parser import HTMLParser


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags, self.links, self.imgs, self.forms, self.inputs = [], [], [], [], []
        self.meta, self.ids, self.text = {}, set(), []
        self._skip = 0
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags.append(tag)
        if "id" in a:
            self.ids.add(a["id"])
        if tag in ("script", "style"):
            self._skip += 1
        if tag == "title":
            self._in_title = True
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag == "img":
            self.imgs.append(a)
        if tag == "form":
            self.forms.append(a)
        if tag == "input":
            self.inputs.append(a)
        if tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = a.get("content", "")

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if not self._skip:
            self.text.append(data)


html = open(sys.argv[1], encoding="utf-8").read()
p = Page()
p.feed(html)
text = " ".join(p.text)
lower = text.lower()
results = []


def res(status, name, detail=""):
    results.append((status, name, detail))


def check(name, ok, detail="", warn=False):
    res("PASS" if ok else ("WARN" if warn else "FAIL"), name, detail)


check("lang attribute on <html>", re.search(r"<html[^>]+lang=", html) is not None)
check("Viewport meta (mobile)", "viewport" in p.meta)
check("Page title", bool(p.title.strip()), p.title.strip())
check("Meta description (50–160 chars)", 50 <= len(p.meta.get("description", "")) <= 160,
      f"{len(p.meta.get('description', ''))} chars")
check("Exactly one <h1>", p.tags.count("h1") == 1, str(p.tags.count("h1")))
check("All images have alt text", all("alt" in i for i in p.imgs), f"{len(p.imgs)} images")
check("Open Graph tags for link previews", any(k.startswith("og:") for k in p.meta), warn=True)
check("Skip-to-content link", bool(re.search(r'<a[^>]+href="#(main|content)"', html)), warn=True)
anchors = [h[1:] for h in p.links if h.startswith("#") and len(h) > 1]
missing = [a for a in anchors if a not in p.ids]
check("In-page links all have a target", not missing, ", ".join(missing))
check("Sign-off 'Chef Anto 🌿🤓❤️'", "Chef Anto 🌿🤓❤️" in text, warn=True)
check("Tagline 'Born in Romania. Rebuilt in Miami.'", "born in romania" in lower and "rebuilt in miami" in lower)
for w in ["revolutionary", "game-changer", "hurry"]:
    check(f"No hype word '{w}'", w not in lower)
legacy = sorted(set(re.findall(r"fridgechef ai|larder", lower)))
check("Uses current app name 'Chef Anto' (no FridgeChef AI / Larder)", not legacy,
      "found: " + ", ".join(legacy), warn=True)
ig = [h for h in p.links if "instagram.com" in h]
check("Instagram link matches @antoanelaalexander", all("antoanelaalexander" in h for h in ig),
      ", ".join(ig))
form_ok = bool(p.forms) and all(f.get("action", "#") not in ("", "#") for f in p.forms)
onsubmit_alert = bool(re.search(r"onsubmit=\"[^\"]*alert\(", html))
check("Signup form is connected (posts somewhere real)", form_ok and not onsubmit_alert,
      "form action '#' with an alert placeholder" if onsubmit_alert else "")
check("Email field has a label or aria-label",
      all(i.get("aria-label") or i.get("id") for i in p.inputs if i.get("type") == "email"))
kb = len(html.encode("utf-8")) / 1024
b64 = sum(len(m) for m in re.findall(r"data:image/[^\"')]+", html)) / 1024
check("Page weight under 200 KB", kb < 200, f"{kb:.0f} KB, of which {b64:.0f} KB is an inline base64 image", warn=True)

order = {"FAIL": 0, "WARN": 1, "PASS": 2}
for s, n, d in sorted(results, key=lambda r: order[r[0]]):
    print(f"{s}  {n}" + (f"  ({d})" if d else ""))
c = {k: sum(r[0] == k for r in results) for k in order}
print(f"\n{c['PASS']} passed · {c['WARN']} warnings · {c['FAIL']} failed (of {len(results)})")
sys.exit(1 if c["FAIL"] else 0)
