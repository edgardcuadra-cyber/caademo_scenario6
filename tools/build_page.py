"""Build index.html: a demo copy of https://www.caasco.com/insurance/existing-customers with the S6 web messenger.

Usage: python tools/build_page.py            (fetches the live page)
       python tools/build_page.py page.html  (uses a saved copy)

What it changes:
- site-relative links, styles, scripts and images point back to https://www.caasco.com, so the copy looks like
  the live page without mirroring its assets;
- tracking, A/B, bot-protection, social and map scripts are removed (GTM, ABTasty, reCAPTCHA, Zenedge, AddThis,
  Facebook, Piwik, Google Maps with CAA's key), and so is CAA's own Curatu chatbot, which would compete with the
  Genesys Messenger;
- adds noindex, a "demo" banner, and the Genesys Messenger snippet for deployment CAA_demo_S6_Chat_Test.
"""
import re, sys, urllib.request, os

SOURCE = "https://www.caasco.com/insurance/existing-customers"
ORIGIN = "https://www.caasco.com"
DEPLOYMENT_ID = "a29f9462-75fa-4d32-bfa4-63fd62e3b04d"   # CAA_demo_S6_Chat_Test -> CAA_demo_S6_Website_Chat
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "index.html")

DROP_SRC = re.compile(r"recaptcha|ABTasty|GoogleTagManager|__zenedge|addthis|maps\.google|curatu|chatbot|"
                      r"footer-store-locator|piwik", re.I)
DROP_INLINE = re.compile(r"gtm\.start|strUserGTMID|abtiming|___zen|__zjc|FB\.init|fbAsyncInit|curatu|Hotjar|"
                         r"piwik|ppms\.js|dataLayer\.push", re.I)

SNIPPET = f"""<script type="text/javascript" charset="utf-8">
  (function (g, e, n, es, ys) {{
    g['_genesysJs'] = e;
    g[e] = g[e] || function () {{
      (g[e].q = g[e].q || []).push(arguments)
    }};
    g[e].t = 1 * new Date();
    g[e].c = es;
    ys = document.createElement('script'); ys.async = 1; ys.src = n; ys.charset = 'utf-8'; document.head.appendChild(ys);
  }})(window, 'Genesys', 'https://apps.mypurecloud.com/genesys-bootstrap/genesys.min.js', {{
    environment: 'use1',
    deploymentId: '{DEPLOYMENT_ID}'
  }});
</script>"""

BANNER = ('<div id="caa-demo-banner" style="position:relative;z-index:99999;background:#003087;color:#fff;'
          'font:600 13px/1.4 Arial,sans-serif;text-align:center;padding:6px 12px">'
          'Demo copy for the CAA RFP technology demonstration (Scenario 6). Not the CAA website: '
          'links go to caasco.com, and the chat is a Genesys Cloud demo.</div>')


def main():
    if len(sys.argv) > 1:
        html = open(sys.argv[1], encoding="utf-8").read()
    else:
        req = urllib.request.Request(SOURCE, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        html = urllib.request.urlopen(req).read().decode("utf-8")

    def script(m):
        attrs, body = m.group(1), m.group(2)
        src = re.search(r'src="([^"]+)"', attrs)
        if src and DROP_SRC.search(src.group(1)):
            return ""
        if not src and DROP_INLINE.search(body):
            return ""
        return m.group(0)

    html = re.sub(r"<script\b([^>]*)>(.*?)</script>", script, html, flags=re.S)
    html = re.sub(r"<noscript>.*?</noscript>", "", html, flags=re.S)           # GTM iframe
    html = re.sub(r'((?:href|src|action|data-src|poster)=")~?/(?!/)', rf"\1{ORIGIN}/", html)
    html = re.sub(r'(srcset=")([^"]+)"',
                  lambda m: m.group(1) + re.sub(r"(^|,\s*)/(?!/)", rf"\1{ORIGIN}/", m.group(2)) + '"', html)
    html = re.sub(r"url\((['\"]?)/(?!/)", rf"url(\1{ORIGIN}/", html)
    html = re.sub(r'(=")//', r'\1https://', html)
    html = html.replace("<head>", '<head>\n<meta name="robots" content="noindex,nofollow">', 1)
    html = html.replace("</head>", SNIPPET + "\n</head>", 1)
    html = re.sub(r"(<body\b[^>]*>)", r"\1" + BANNER, html, count=1)
    assert DEPLOYMENT_ID in html and "caa-demo-banner" in html
    open(OUT, "w", encoding="utf-8").write(html)
    left = re.findall(r'<script\b[^>]*src="([^"]+)"', html)
    print("wrote", OUT, len(html), "bytes; scripts kept:", left)


if __name__ == "__main__":
    main()
