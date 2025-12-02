"""Generate a simple HTML report from Semgrep JSON results.

This script is intentionally small and dependency-free so it can run
inside the GitHub Actions runner without extra installs.
"""
import json
import sys
from html import escape

INPUT = 'semgrep-results.json'
OUTPUT = 'semgrep-results.html'

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return None

def row_for(result):
    check = result.get('check_id') or result.get('rule_id') or result.get('check') or result.get('meta', {}).get('id') or ''
    message = result.get('extra', {}).get('message') or result.get('message') or ''
    path = result.get('path') or result.get('file') or result.get('start', {}).get('file') or ''
    line = result.get('start', {}).get('line') or result.get('line') or ''
    severity = result.get('extra', {}).get('severity') or result.get('severity') or ''
    return check, message, path, line, severity

def make_html(data):
    results = data.get('results') if isinstance(data, dict) else None
    if not results:
        body = '<p>No results from Semgrep.</p>'
    else:
        rows = []
        for r in results:
            check, message, path, line, severity = row_for(r)
            rows.append((escape(str(check)), escape(str(message)), escape(str(path)), escape(str(line)), escape(str(severity))))

        table_rows = '\n'.join(
            f"<tr><td>{c}</td><td>{m}</td><td>{p}</td><td>{l}</td><td>{s}</td></tr>" for c, m, p, l, s in rows
        )
        body = f"<table border=1 cellpadding=6><thead><tr><th>Rule</th><th>Message</th><th>File</th><th>Line</th><th>Severity</th></tr></thead><tbody>{table_rows}</tbody></table>"

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Semgrep Results</title>
  <style>body{{font-family: Arial, sans-serif; padding:20px}} table{{border-collapse:collapse}} th{{background:#eee}}</style>
</head>
<body>
  <h1>Semgrep Scan Results</h1>
  {body}
</body>
</html>
"""
    return html

def main():
    data = load_json(INPUT)
    if data is None:
        print(f"Warning: could not read {INPUT}")
        # create a minimal html to keep the workflow happy
        with open(OUTPUT, 'w', encoding='utf-8') as f:
            f.write('<html><body><p>No semgrep JSON found.</p></body></html>')
        return

    html = make_html(data)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Wrote {OUTPUT}")

if __name__ == '__main__':
    main()
