# chefanto.com 🌿

**Source of [chefanto.com](https://chefanto.com), Chef Anto's main brand hub: "Born in Romania. Rebuilt in Miami."**
Built by Chef Anto (Antoanela Alexander), Miami. *I am the heart. AI is the brain.*

## What's on the page
| Section | Content |
|---|---|
| Hero | "Born in Romania. Rebuilt in Miami." |
| Story | "The flavor of resilience": Chef Anto's journey |
| Experiences | "Come hungry. Leave inspired.": cards for the app, Baba by Chef Anto and Dream House |
| Watch | "The journey, in public": YouTube @livewithchefanto |
| Join | Free guide signup: "5 Meals From What's Already In Your Fridge" |
| Footer | Links to the app, Instagram, pets.chefanto.com |

One self-contained `index.html` (HTML, about 11 KB of inline CSS, a small menu script, one inline image). No build step.

## Files
| Path | What it is |
|---|---|
| [`index.html`](index.html) | The live home page, downloaded from chefanto.com on 2026-10-01 |
| [`tests/audit_site.py`](tests/audit_site.py) | 19-point audit: SEO basics, accessibility, brand rules, signup form |
| [`tests/test_render.py`](tests/test_render.py) | Renders the page at 375 / 768 / 1440 px in Chromium |

The only change from the live file: the GoDaddy hosting monitoring script, which the server adds automatically, was removed.

## Deploy
Hosted on GoDaddy (cPanel). To update, upload `index.html` to `public_html` in cPanel File Manager. It also works by drag-and-drop on Netlify.

## Test results (only tests actually run, 2026-10-01)
| # | Test | Result |
|---|---|---|
| 1 | `python3 tests/audit_site.py index.html` | **13 passed · 4 warnings · 2 failed** (of 19) |
| 2 | `python3 tests/test_render.py index.html` | ✅ **7/7 passed**: no horizontal scroll and no JS errors at 375, 768 and 1440 px; mobile menu opens |
| 3 | Signup form submitted on the live site in Chrome | ❌ Shows an alert: "Connect this form to MailerLite (form ID: LpK5ms) before publishing." |

### ❌ Failed: fix these first
1. **Signup form isn't connected.** The form posts to `#` and shows a placeholder alert, so **no emails are being collected**. Fix: paste the MailerLite embedded form for group "Website Signups" (form LpK5ms) in place of the current form.
2. **Instagram link points to `instagram.com/antoanelalexander`**, but the brand kit's handle is **@antoanelaalexander**. Check which one is right and update the 3 links.

### ⚠️ Warnings: worth fixing
3. **Old app names on the page:** "FridgeChef AI" and "Larder" appear. The brand kit's app name is now **Chef Anto**.
4. **No Open Graph tags**, so links shared on LinkedIn, WhatsApp or iMessage show no preview image or title.
5. **No skip-to-content link** for keyboard and screen-reader users.
6. **No "Chef Anto 🌿🤓❤️" sign-off** on the page.

### ✅ Passed
Language set, mobile viewport, title, meta description (147 characters), one `<h1>`, image alt text, all in-page links work, tagline present, no hype words, email field labeled, page weight 168 KB (147 KB of it is one inline image).

**Not tested yet:** Lighthouse/PageSpeed score, real-phone testing, the other domains attached to chefanto.com.

## Run the tests
```bash
python3 tests/audit_site.py index.html                          # Python 3 only
pip install playwright && playwright install chromium
python3 tests/test_render.py index.html
```

---
Chef Anto 🌿🤓❤️
