#!/usr/bin/env python3
"""Publish a draft from _drafts/<slug>/ with today's real date, update listings, commit and push."""
import sys, re, os, subprocess, datetime
slug = sys.argv[1]
no_push = '--no-push' in sys.argv
src = f'_drafts/{slug}/index.html'
if not os.path.exists(src):
    sys.exit(f'No draft at {src}')
today = datetime.date.today()
date = today.strftime('%b ') + str(today.day) + today.strftime(', %Y')
html = open(src).read()
m = re.search(r'<!-- topic: (.*?) \| read: (.*?) -->', html)
topic, read = m.group(1), m.group(2)
title = re.search(r'<h1>(.*?)</h1>', html).group(1)
desc = re.search(r'<meta name="description" content="([^"]*)"', html).group(1)
html = html.replace('{{DATE}}', date).replace(m.group(0) + '\n', '')
os.makedirs(f'blog/{slug}', exist_ok=True)
open(f'blog/{slug}/index.html', 'w').write(html)
card = (f'<li><a class="post" href="/blog/{slug}/"><div class="m">{topic} &middot; {read} read</div>'
        f'<div class="t">{title}</div><div class="d">{desc}</div></a></li>')
for f in ('blog/index.html', 'index.html'):
    s = open(f).read()
    s = s.replace('<ul class="postlist">', '<ul class="postlist">' + card, 1)
    open(f, 'w').write(s)
sm = open('sitemap.xml').read()
sm = sm.replace('</urlset>', f'<url><loc>https://gamefit.gac-labs.com/blog/{slug}/</loc></url>\n</urlset>')
open('sitemap.xml', 'w').write(sm)
os.remove(src); os.rmdir(f'_drafts/{slug}')
subprocess.run(['git', 'add', '-A'], check=True)
subprocess.run(['git', 'commit', '-q', '-m', f'Publish: {title}'], check=True)
if not no_push:
    subprocess.run(['git', 'push', '-q', 'origin', 'main'], check=True)
print(f'{"Created (not pushed)" if no_push else "Published"} {slug} on {date}')
