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

## Test results (only tests actually run)
| # | Test | Result |
|---|---|---|
| 1 | `python3 tests/audit_site.py index.html`, 2026-10-01 | **13 passed · 4 warnings · 2 failed** (of 19) |
| 2 | `python3 tests/test_render.py index.html`, 2026-10-01 | ✅ **7/7 passed**: no horizontal scroll and no JS errors at 375, 768 and 1440 px; mobile menu opens |
| 3 | Signup form submitted on the live site in Chrome, 2026-10-01 | ❌ Showed an alert: "Connect this form to MailerLite (form ID: LpK5ms) before publishing." |
| 4 | Re-run of both tests, 2026-10-12, after the MailerLite fix and the Instagram check update | ✅ Audit **15 passed · 4 warnings · 0 failed**; render **7/7 passed** |

### ✅ Fixed since the first audit
1. **Signup form:** `index.html` now posts to MailerLite (synced from the live site in commit `1b651e9`). Checked in the source only; a live test signup was not submitted in the re-run.
2. **Instagram link:** Chef Anto confirmed her main Instagram is **@antoanelalexander** (one "a" in the middle), so the site's 3 links were already right. The audit check was wrong and now expects this handle.

### 🔜 Next update for the live site
- The YouTube links still point to **@livewithchefanto**. The current channel is **@chefantoai** ("Chef Anto AI"). Update the 3 YouTube links and the handle label, then upload `index.html` to GoDaddy.

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
