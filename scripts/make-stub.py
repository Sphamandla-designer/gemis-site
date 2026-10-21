#!/usr/bin/env python3
"""
Write a redirect stub for a retired page.

GitHub Pages has no server redirects, so a retired URL becomes a small page that
carries a canonical link, noindex, a meta-refresh, a visible fallback link for
anyone the refresh does not move, and a location.replace that preserves the hash
so deep links to anchors survive.

    python3 scripts/make-stub.py case-studies.html work/ "Case Studies" "Our Work"

Anchor mapping is handled by the caller passing a target that already includes
the new anchor where one is needed.
"""
import sys

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{old_name} has moved — GEMIS®</title>
  <meta name="robots" content="noindex" />
  <link rel="canonical" href="{target}" />
  <meta http-equiv="refresh" content="0; url={target}" />
  <link rel="icon" type="image/svg+xml" href="{base}assets/img/favicon.svg" />
  <style>
    body{{margin:0;min-height:100vh;display:grid;place-items:center;padding:24px;
      background:#f2f2f1;color:#16181b;font:15px/1.6 system-ui,-apple-system,"Segoe UI",sans-serif}}
    .b{{max-width:46ch;text-align:center}}
    h1{{margin:0 0 12px;font-size:22px;font-weight:500;letter-spacing:-.02em}}
    p{{margin:0 0 20px;color:#55565a}}
    a{{display:inline-block;padding:12px 26px;border-radius:999px;background:#161b40;color:#fff;text-decoration:none}}
    a:focus-visible{{outline:2px solid #1f2557;outline-offset:3px}}
  </style>
</head>
<body>
  <!-- Redirect stub. {old_name} moved to {new_name} in the GEMIS Stories update.
       The stub keeps older inbound links, bookmarks and search results working
       instead of 404ing. The script below carries the hash across, so a deep
       link to an anchor lands on the matching anchor at the new address. -->
  <div class="b">
    <h1>{old_name} is now {new_name}</h1>
    <p>This page moved to <strong>{target}</strong>. You should be redirected automatically.</p>
    <a href="{target}">Go to {new_name}</a>
  </div>
  <script>
    (function () {{
      var target = {target_js};
      // keep the anchor: services.html#process lands on .../#process
      location.replace(target + location.hash);
    }})();
  </script>
</body>
</html>
'''


def write_stub(path, target, old_name, new_name):
    base = '../' * path.count('/')
    html = TEMPLATE.format(target=target, old_name=old_name, new_name=new_name,
                           base=base, target_js='"' + target + '"')
    open(path, 'w', encoding='utf-8').write(html)
    return path


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(2)
    print('wrote', write_stub(*sys.argv[1:]))
