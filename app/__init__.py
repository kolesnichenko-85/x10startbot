from pathlib import Path

# Inject the latest reveal layer after the page's inline app script so it can
# reliably override showReveal inside Telegram's iOS WebView.
try:
    p = Path(__file__).resolve().parent / "static" / "index.html"
    html = p.read_text(encoding="utf-8")
    tag = '<script src="/static/hatch_v2.js?v=20260917_3"></script>'
    if tag not in html:
        html = html.replace("</body>", tag + "</body>")
        p.write_text(html, encoding="utf-8")
except Exception as exc:
    print(f"DROP1 hatch script injection skipped: {exc}")
