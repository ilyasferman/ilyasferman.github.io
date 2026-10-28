# İlyas Ferman Academic Website — Current Known-Good State

> This file is the canonical handoff/reference for future edits to this website. Before changing the site, read this file and inspect the current `main` branch. Never reconstruct the site from memory or from an older chat/draft.

## Repository and live site

- Repository: `ilyasferman/ilyasferman.github.io`
- Live domain: `https://ilyasferman.com/`
- Hosting: GitHub Pages
- Branch: `main`
- Known-good functional baseline before this documentation commit: `9524082ba3a9adc2307f07fb0d91d9dfd9147731`
- That baseline was deployed successfully via GitHub Pages on 2026-10-28.

## Critical rule for all future edits

When İlyas asks to add/change something on the website, **modify the current latest working `main` version surgically**. Do not rebuild the site from an old draft, do not replace `index.html` wholesale with an older version, and do not roll back unrelated features.

Before any edit:
1. Read this file.
2. Fetch the latest `main` versions of the file(s) being changed.
3. Compare against the current working behavior if the change touches CV, certificates, navigation, modal code, or academic-profile links.
4. Change only the requested feature.
5. Verify GitHub Pages deployment completes successfully.

## Homepage ↔ CV parallel-content rule

The homepage and the academic CV are intended to stay substantially in sync for academic/profile content.

Default rule: when İlyas asks to add an academic profile, publication, education item, professional/academic credential, contact/profile link, research-related item, or similar substantive profile information to the homepage, add the corresponding item to the CV as well unless he explicitly says not to.

Likewise, if a substantive academic/profile item is added to the CV and it has a natural place on the homepage, keep the homepage synchronized.

Exceptions are presentation-only website elements that do not belong in a CV, such as navigation controls, button styling, responsive layout, modal UI, visual decoration, animation, or other interface-only changes.

When making a parallel homepage + CV update:
- Start from the current latest working `main` state.
- Preserve the existing layout and wording conventions of each surface.
- Do not treat the CV as a separate stale artifact.
- If the CV must be regenerated, preserve certificate links/annotations and the `from=cv` return behavior.
- After regeneration, verify both the homepage and the CV-specific behavior before considering the task complete.

## Current website structure

Main file:
- `index.html`

Main navigation:
- Hakkımda
- Araştırma Alanları
- Çalışmalar
- Eğitim
- Sertifikalar
- CV
- İletişim

The CV opens inside the existing site document modal. Do **not** replace this with a PDF.js/canvas viewer unless İlyas explicitly requests that and accepts the risk.

## Academic profile buttons / links

Current academic profile set includes:
- ORCID: `https://orcid.org/0000-0003-4844-3508`
- Google Scholar: `https://scholar.google.com/citations?user=lYZXEKEAAAAJ&hl=tr`
- ResearchGate: `https://www.researchgate.net/profile/Ilyas-Ferman-2`
- Zenodo all-works exact creator search: `https://zenodo.org/search?q=metadata.creators.person_or_org.name%3A%22Ferman%2C%20%C4%B0lyas%22&l=list&p=1&s=10&sort=newest`
- OSF: `https://osf.io/3gntq/`

OSF is present on the homepage academic-profile buttons and footer/profile links, and is intended to remain part of the academic-profile set.

## Academic works currently represented

### Thesis
- Title: `112 Acil Servis Çalışanlarının İş Güçlüğü ve İş Riski Sorunları; Ordu İli 112 Acil Servis Çalışanları Üzerinde Bir Araştırma`
- Year: 2022
- Zenodo DOI/record: `10.5281/zenodo.23146579`

### Book chapter
- Title: `Endüstri 3.0 ve Endüstri 4.0`
- Book: `Sosyal Bilimlerde Güncel Gelişmeler ve Tematik İncelemeler`
- Platanus Publishing
- Chapter 34, pp. 756–767, 2026
- DOI: `10.5281/zenodo.23544985`

## CV files and generation

Current CV file:
- `cv/ilyas-ferman-akademik-cv.pdf`

Generator files:
- `scripts/build_academic_cv.py`
- `scripts/build_academic_cv_fixed.py`

Workflow:
- `.github/workflows/rebuild-academic-cv.yml`

Important: changes to the generator/wrapper can trigger automatic CV regeneration and can also patch `index.html`. Therefore generator changes are high-risk and must be tested against the certificate/modal behavior before considering the task complete.

## Certificate behavior — DO NOT BREAK

This is a required working feature.

### Homepage certificates
- Clicking a certificate card opens the certificate in the site's large document modal.
- The certificate is rendered from its corresponding `<template>` in `index.html`.
- Clicking the modal X closes the certificate normally.

### Certificates opened from CV
- Certificate thumbnails/links in the PDF point back to the site using a URL like:
  `https://ilyasferman.com/?cert=<certificate-key>&from=cv`
- The requested certificate opens large in the site's modal.
- Clicking X must restore the CV in the modal at **page 2**.
- The restoration target is:
  `cv/ilyas-ferman-akademik-cv.pdf#page=2&view=FitH`

### Critical JavaScript invariant
There must be only **one** declaration of:
- `const requestedCertificate`

A previous regression duplicated `const requestedCertificate`, causing a JavaScript syntax error that disabled certificate behavior on both the homepage and CV flow.

The known-good logic uses:
- `const queryParams = new URLSearchParams(window.location.search);`
- `const requestedCertificate = queryParams.get('cert');`
- `let restoreCvOnClose = Boolean(requestedCertificate);`
- `restoreCv()`
- `handleDocumentClose()`

Do not add a second legacy `requestedCertificate` block before this logic.

## Known regression history / things not to repeat

1. PDF.js/canvas viewer experiments broke clickable link hitboxes and caused certificate/link routing errors. Do not reintroduce them casually.
2. Opening CV/internal certificate links in new tabs was explicitly rejected.
3. Direct PDF/browser-history workarounds caused Back-navigation problems.
4. A duplicate `const requestedCertificate` declaration disabled the whole certificate JavaScript path.
5. Rebuilding the CV unnecessarily can change PDF annotations/link targets. For unrelated website edits, do not regenerate the PDF.
6. Do not change certificate behavior, CV navigation, or unrelated buttons while adding a simple profile/link/content item.

## Safe-edit policy

For a normal request such as “add this account/link/text to my site”:
- Fetch current `main`.
- Patch only the exact requested location(s).
- For substantive academic/profile content, apply the homepage ↔ CV parallel-content rule above.
- Do not touch CV generator unless the requested change must also appear inside the PDF CV.
- If CV must change, preserve certificate URL annotations and the `from=cv` return behavior.
- After any CV-related change, inspect final `index.html` for duplicate JS declarations and confirm Pages deployment success.
- Never say the site is fixed merely because a workflow build succeeded; verify the final source state relevant to the requested feature.

## User instruction for future chats

İlyas expects website work to continue from the **current latest working version**, even in a new conversation. Do not say the site is forgotten or unavailable before checking the connected GitHub repository. Use this `SITE_STATE.md` as the first reference, then inspect current `main` and make the requested incremental change.
