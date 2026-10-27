# CAA demo – Scenario 6 web page

Demo copy of the CAA South Central Ontario page [Insurance: existing customers](https://www.caasco.com/insurance/existing-customers) with the Genesys Cloud web messenger for **Scenario 6 (injury FNOL)** of the CAA RFP technology demonstration. It is not the CAA website: a banner says so, links, styles and images point back to caasco.com, search engines are told not to index it, and CAA's own tracking and chatbot scripts are removed.

## What the chat does
The messenger uses deployment `CAA_demo_S6_Chat_Test` (`a29f9462-75fa-4d32-bfa4-63fd62e3b04d`, US East), which runs the Architect flow `CAA_demo_S6_Website_Chat`:

1. The member says they want to report an accident.
2. Membership number, then a one-time code by text.
3. "Were you or anyone with you injured?" Yes → the chat places a customer-first callback and ends.
4. The callback runs the FNOL voice assistant, then reaches a claims agent on `CAA_demo_FNOL-S6` with the agent script filled in.

Demo member: Alex Morgan, membership number `6202794000044173`.

## Files
- `index.html` – the page (generated; don't edit by hand).
- `tools/build_page.py` – rebuilds `index.html` from the live caasco.com page: `python tools/build_page.py`.
- `.github/workflows/pages.yml` – deploys to GitHub Pages on every push to `main`.

## Deploy
One-time: in the repo, **Settings → Pages → Build and deployment → Source: GitHub Actions**. After that every push to `main` publishes the site at `https://edgardcuadra-cyber.github.io/caademo_scenario6/`.

To change the chat, point the messenger deployment at a different flow in Genesys Cloud, or change `DEPLOYMENT_ID` in `tools/build_page.py` and rebuild.
