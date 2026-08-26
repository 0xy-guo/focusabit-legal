# Focusabit Official Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current root legal landing page with the approved one-page Focusabit product website while preserving every existing legal URL and legal body text.

**Architecture:** Keep the GitHub Pages repository dependency-free. `index.html` and `site.css` own the product website, `legal.html` and `legal.css` own the support/legal presentation, and a Python standard-library verification script checks required content, assets, and internal links.

**Tech Stack:** Semantic HTML5, CSS3, inline SVG, Python 3 `unittest`, GitHub Pages static hosting.

**Spec:** `docs/superpowers/specs/2026-08-26-focusabit-official-website-design.md`

## Global Constraints

- Preserve `privacy.html`, `support.html`, `terms.html`, `data-deletion.html`, `membership.html`, `automatic-renewal.html`, and `open-source.html` paths and body copy.
- Use no JavaScript, framework, build tool, CMS, analytics, form, or external runtime dependency.
- Use `#6D927F`, `#475253`, `#B5C3BC`, white, and warm gray as the visual palette.
- Keep the App Store status non-interactive until a real download URL exists.
- Support 1440px, 768px, 390px, and 320px widths without horizontal overflow.
- Keep all work local; do not push, publish, change DNS, or add `CNAME`.

---

### Task 1: Add Static Site Acceptance Checks

**Files:**
- Create: `tests/verify_site.py`

**Interfaces:**
- Consumes: HTML files and local asset paths in the repository root.
- Produces: `python3 -m unittest tests/verify_site.py -v`, which returns non-zero when the site contract is broken.

- [ ] **Step 1: Write the failing acceptance checks**

Create a `unittest.TestCase` that:

```python
SITE_ROOT = Path(__file__).resolve().parents[1]
LEGAL_PAGES = (
    "privacy.html", "support.html", "terms.html", "data-deletion.html",
    "membership.html", "automatic-renewal.html", "open-source.html",
)

def local_hrefs(path: Path) -> list[str]:
    parser = LinkParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return [href for href in parser.hrefs if not urlsplit(href).scheme and not href.startswith(("#", "mailto:"))]
```

Assert that the new homepage contains the approved title, all four feature headings, `id="features"`, `id="product"`, and no clickable App Store element; that `legal.html` exists and links to all seven legal pages; that all local `href` targets exist; that the homepage references `site.css` and `assets/focusabit-logo.svg`; and that every concrete legal page links back to `legal.html` while its brand links to `index.html`.

- [ ] **Step 2: Run the checks and verify the new-site contract fails**

Run: `cd focusabit-legal && python3 -m unittest tests/verify_site.py -v`

Expected: failures for missing `legal.html`, `site.css`, homepage sections, or website assets.

- [ ] **Step 3: Commit the acceptance checks with the implementation batch**

Do not create an intermediate remote commit. Keep the new check local until the complete site passes it.

---

### Task 2: Add Approved Brand Assets and Homepage Styling

**Files:**
- Create: `assets/focusabit-logo.svg`
- Create: `assets/apple-touch-icon.png`
- Create: `site.css`

**Interfaces:**
- Consumes: the existing App assets `onboarding-logo.svg` and `AppIcon-1024.png`.
- Produces: local asset URLs used by `index.html` and a responsive class system for the homepage.

- [ ] **Step 1: Copy only existing approved brand artwork**

Copy the existing onboarding SVG unchanged to `assets/focusabit-logo.svg`. Create the 180×180 Apple touch icon from the existing 1024×1024 App icon using the bundled macOS image tool:

```bash
sips -z 180 180 ../focusabit_client/FocusApp/Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png --out assets/apple-touch-icon.png
```

- [ ] **Step 2: Implement the shared homepage design tokens and layout**

Create `site.css` with variables for the approved palette, a 1120px content container, visible keyboard focus styles, a sticky translucent header, spacious hero grid, four-feature grid, green product showcase, three CSS phone frames, launch panel, and complete legal footer.

Use these responsive boundaries:

```css
@media (max-width: 900px) { /* hero and showcase become stacked */ }
@media (max-width: 640px) { /* hide center nav; features become one column */ }
@media (max-width: 360px) { /* reduce phone scale and edge padding */ }
@media (prefers-reduced-motion: reduce) { /* remove decorative motion */ }
```

The stylesheet must set `overflow-x: hidden` only as a final guard; all positioned artwork and phone compositions must still fit their containing blocks by construction.

- [ ] **Step 3: Run the asset-related checks**

Run: `cd focusabit-legal && python3 -m unittest tests.verify_site.SiteContractTests.test_required_assets_exist -v`

Expected: PASS.

---

### Task 3: Build the One-Page Product Homepage

**Files:**
- Replace: `index.html`

**Interfaces:**
- Consumes: `site.css`, `assets/focusabit-logo.svg`, and the fixed Chinese copy from the design spec.
- Produces: the root website at `/` with product anchors and direct legal links.

- [ ] **Step 1: Add the complete metadata and navigation shell**

Use the exact title `微专注 Focusabit｜开启一次专注，如此简单`, a concise product description, Open Graph title/description/site name, canonical `https://focusabit.github.io/focusabit-legal/`, touch icon, and the approved Logo. Navigation links are `#product`, `#features`, and `support.html`; the launch state is a `<span>`, not an anchor.

- [ ] **Step 2: Build the hero and feature sections**

The hero includes `FOCUS · BREATHE · REPEAT`, the exact approved heading and paragraph, the non-clickable App Store status, `了解微专注` linking to `#features`, and `比闹钟温柔，比任务管理简单`. Build the four approved feature items with semantic headings and decorative inline SVG for focus, sound, meditation, and rhythm.

- [ ] **Step 3: Build the product showcase and launch sections**

Under `id="product"`, create three clearly labeled non-interactive phone mockups: quick focus, weekly rhythm, and guided meditation. The meditation phone includes a meditation title, duration, breathing illustration, waveform/play state, and breathing guidance. End with the approved launch copy and a non-interactive `Focusabit for iPhone · 敬请期待` status.

- [ ] **Step 4: Add the complete footer**

Link directly to `privacy.html`, `terms.html`, `support.html`, `data-deletion.html`, `membership.html`, `automatic-renewal.html`, `open-source.html`, and `legal.html`, plus the support email. Do not hide links behind scripting or menus.

- [ ] **Step 5: Run the homepage checks**

Run: `cd focusabit-legal && python3 -m unittest tests.verify_site.SiteContractTests.test_homepage_contract -v`

Expected: PASS.

---

### Task 4: Migrate the Legal Landing Page and Update Page Shells

**Files:**
- Create: `legal.html`
- Modify: `legal.css`
- Modify: `privacy.html`
- Modify: `support.html`
- Modify: `terms.html`
- Modify: `data-deletion.html`
- Modify: `membership.html`
- Modify: `automatic-renewal.html`
- Modify: `open-source.html`

**Interfaces:**
- Consumes: the original `index.html` legal landing body, current legal body copy, and `assets/focusabit-logo.svg`.
- Produces: a dedicated legal overview and consistent legal-page navigation without changing substantive legal text.

- [ ] **Step 1: Preserve the old legal landing at `legal.html`**

Move the prior legal landing content into `legal.html`, change the brand target to `index.html`, add the shared Logo treatment, and ensure all seven concrete legal pages remain directly reachable.

- [ ] **Step 2: Update only the page shells of the seven concrete pages**

For each page, preserve the existing `<main>` body verbatim. Update the header brand to use the Logo and link to `index.html`; add a `官网首页` link to `index.html` and a `法律与支持` link to `legal.html`; and ensure the footer provides a route back to `legal.html`.

- [ ] **Step 3: Refine `legal.css` without altering content semantics**

Match the homepage palette and typography, add the Logo lockup, improve the legal content card and footer link wrapping, retain visible focus states, and keep the current dark-mode support for the legal documents.

- [ ] **Step 4: Run legal-content and link checks**

Run: `cd focusabit-legal && python3 -m unittest tests/verify_site.py -v`

Expected: all tests PASS.

---

### Task 5: Verify Local Rendering and Present the Preview

**Files:**
- Modify only if visual verification identifies an in-scope layout defect.

**Interfaces:**
- Consumes: the complete static site.
- Produces: a verified local preview URL shown in the Codex browser.

- [ ] **Step 1: Run automated repository checks**

Run:

```bash
cd focusabit-legal
python3 -m unittest tests/verify_site.py -v
rg -n 'href="#"|\.example|【请替换' --glob '*.html' .
git diff --check
```

Expected: unit tests PASS; the content scan and `git diff --check` produce no findings.

- [ ] **Step 2: Start a local static server**

Run: `cd focusabit-legal && python3 -m http.server 4173 --bind 127.0.0.1`

Expected: `http://127.0.0.1:4173/` returns HTTP 200.

- [ ] **Step 3: Inspect the page at four viewport widths**

Check approximately 1440×900, 768×1024, 390×844, and 320×568. Confirm no horizontal scrolling, no overlap, readable text, visible focus states, meaningful meditation visuals, and non-clickable launch statuses.

- [ ] **Step 4: Open the final local homepage for user review**

Show `http://127.0.0.1:4173/` in the in-app browser. Do not push or publish until the user explicitly approves the preview.
