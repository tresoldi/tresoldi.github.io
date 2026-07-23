# Silvæ — deferred tasks

Things intentionally left for later. Delete items as they're done.

## IndieWeb wiring
- [ ] **Add Mastodon `rel="me"`** — add an entry to `me:` in `site.yaml`, and add the
      matching `rel="me"` link back from the Mastodon profile so verification is mutual.
- [ ] **Webmentions** — register `www.tresoldi.org` at [webmention.io](https://webmention.io)
      (the `<link rel="webmention">` endpoint is already in `templates/base.html`), set up
      [Brid.gy](https://brid.gy) for social backfeed, and add a section to `templates/post.html`
      that fetches and displays received mentions (likes / replies) under each essay.

## Seeded content to make my own
These pages were seeded from my profile and are placeholders — rewrite them.
- [ ] **`content/pages/now.md`** — keep it honestly dated; update whenever life changes.
- [ ] **`content/pages/uses.md`** — the tools list is inferred; correct it to my real setup.
- [ ] **`content/pages/blogroll.md`** + **`data/blogroll.yaml`** — expand with the sites and
      people I actually read.
- [ ] **`content/notes/`** — replace the single starter note with real notes as they come.

## Hosting
- [ ] **Move to a host that allows a private source repo** while keeping the site public.
      GitHub Free only serves Pages from public repos; options that deploy a public site
      from a private repo include **GitHub Pro** (private repo + Pages) or a static host
      such as **Cloudflare Pages / Netlify / Vercel** (free tiers deploy from private repos).
      Since the build is a plain `python build.py`, any of these can run it; keep the
      `CNAME`/custom domain and update DNS if the host changes.

## Showcase follow-ups (verify / refine)
- [ ] **Sync the full publication list from ORCID** (0000-0002-2863-1467) — I seeded the
      major recent papers (Tupí-Guaraní PLOS ONE, GLED, CLDF feature-vectors); confirm
      author orders and add the rest. A one-time BibTeX export from ORCID/Zotero into
      `data/publications.bib` keeps it complete and correct.
- [ ] **Review the software descriptions** in `data/software.yaml` — a few are curated
      guesses from repo names (e.g. maniphono, alteruphono, multitiers, panphylo); tweak to
      taste.
- [ ] **Add a CV PDF** — drop `cv.pdf` into `static/assets/` and link it from `/cv/`.
- [ ] **Confirm the docent year** and any missing positions on `/cv/` and About.
- [ ] Consider **embedding the runestaves visualisation** on `/curiosities/` rather than
      just linking it.

## Nice-to-have later
- [ ] A CV: drop a `cv.pdf` into `static/assets/` and link it from About (the old broken
      link was removed).
- [ ] Old `/blog/:year/:month/:day/:title` permalinks changed to `/writing/<slug>/`;
      add redirects if any old URLs are indexed or linked externally.
