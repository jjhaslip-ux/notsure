#!/usr/bin/env python3
"""Convert the OSINT markdown dossiers into NS-FLUID dossier pages."""
import html, re, pathlib

SITE = pathlib.Path('/home/hatch/workspace/ns-fluid-site')

HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — NS-FLUID Florida News</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="assets/simple-mark.png">
<link rel="apple-touch-icon" href="assets/badge.png">
<meta property="og:title" content="{title} — NS-FLUID">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{photo}">
<meta property="og:type" content="article">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>

<header class="site-header">
  <div class="wrap bar">
    <img class="badge" src="assets/badge.png" alt="" width="44" height="44">
    <a class="wordmark" href="index.html">NS-FLUID<small>Florida News</small></a>
    <nav class="main-nav" aria-label="Main">
      <ul>
        <li><a href="index.html">Today</a></li>
        <li><a href="index.html#desks">Regions</a></li>
        <li><a href="index.html#weather">Weather</a></li>
        <li><a href="index.html#government">Government</a></li>
        <li><a href="dossiers.html">Dossiers</a></li>
        <li><a href="corrections.html">Corrections</a></li>
      </ul>
    </nav>
  </div>
</header>

<main id="main">
  <section class="dossier-hero">
    <div class="wrap">
      <p class="file-no">{fileno} · OSINT Dossier · Open Sources Only</p>
      <h1>{h1}</h1>
      <p class="sub">{sub}</p>
    </div>
  </section>

  <figure class="dossier-photo">
    <img src="{photo}" alt="{photoalt}">
    <figcaption>{caption}</figcaption>
  </figure>

  <article class="dossier-body">
{body}
    <hr>
    <p><a class="backlink" href="dossiers.html">← All dossiers</a></p>
  </article>
</main>

<footer class="site-footer">
  <div class="wrap">
    <img class="badge" src="assets/badge.png" alt="" width="52" height="52">
    <div>
      <p><strong>NS-FLUID</strong> — Florida News</p>
      <p class="fine">ns-fluid.com</p>
      <p class="agape">The 4 stands for Agape — selfless, community-first love. It is the desk’s north star, and the filter for every story: does this serve the people here?</p>
    </div>
    <nav aria-label="Footer">
      <a href="about.html">About</a>
      <a href="corrections.html">Corrections</a>
      <a href="about.html#sources">Sources policy</a>
    </nav>
  </div>
</footer>
</body>
</html>
"""

def inline(text):
    text = html.escape(text)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)

def convert(md_text):
    lines = md_text.splitlines()
    out = []
    facts = []
    para = []
    in_list = False
    seen_content = False

    def flush_para():
        if para:
            out.append('<p>' + inline(' '.join(para)) + '</p>')
            para.clear()

    def close_list():
        nonlocal in_list
        if in_list:
            out.append('</ul>')
            in_list = False

    def flush_facts():
        if facts:
            items = ''.join(f'<p><strong>{html.escape(k)}</strong> {inline(v)}</p>' for k, v in facts)
            out.append(f'<div class="facts">{items}</div>')
            facts.clear()

    for raw in lines:
        line = raw.rstrip()
        if set(line.strip()) <= set('═') and line.strip():
            continue
        if line.startswith('**SECRET') or line.startswith('**OSINT DOSSIER'):
            continue
        if line.strip() == '---':
            flush_para(); close_list(); flush_facts()
            out.append('<hr>')
            continue
        m = re.match(r'^\*\*([A-Z][A-Z /]+):\*\*\s*(.*)$', line)
        if m and not seen_content:
            flush_para()
            facts.append((m.group(1), m.group(2)))
            continue
        if line.startswith('**END OF FILE'):
            flush_para(); close_list(); flush_facts()
            seen_content = True
            out.append('<p class="endfile">' + inline(line.strip().strip('*')) + '</p>')
            continue
        m = re.match(r'^\*\*([^*]+)\*\*$', line.strip())
        if m:
            flush_para(); close_list(); flush_facts()
            seen_content = True
            out.append(f'<h2>{inline(m.group(1))}</h2>')
            continue
        if line.startswith('- '):
            flush_para(); flush_facts()
            seen_content = True
            if not in_list:
                out.append('<ul>'); in_list = True
            out.append('<li>' + inline(line[2:]) + '</li>')
            continue
        if not line.strip():
            flush_para(); close_list()
            continue
        # continuation of a list item or paragraph
        if in_list and out and out[-1].startswith('<li>'):
            out[-1] = out[-1].replace('</li>', '') + ' ' + inline(line.strip()) + '</li>'
            continue
        close_list()
        para.append(line.strip())
        if re.match(r'^\*\*[A-Z]', line):
            seen_content = True
    flush_para(); close_list(); flush_facts()
    return '\n'.join(out)

PAGES = [
    dict(
        src='/home/hatch/workspace/your_files/claire-liu-osint-cv.md',
        out='dossier-liu.html',
        title='Claire Liu — File 593-Liu',
        desc='Open-source dossier on WTA tennis player Claire Liu: junior world number one, the 2024 reset, and the 2026 Hong Kong run.',
        fileno='File 593-Liu',
        h1='Claire Liu',
        sub='The Thousand Oaks Asset. Professional tennis player, WTA Tour — a former junior world number one rebuilding toward the top fifty. Compiled from open sources only.',
        photo='assets/liu.jpg',
        photoalt='Claire Liu playing a two-handed backhand',
        caption='Claire Liu — photograph: USTA',
    ),
    dict(
        src='/home/hatch/workspace/your_files/abdul-el-sayed-osint-cv.md',
        out='dossier-elsayed.html',
        title='Abdul El-Sayed — File 462-ElSayed',
        desc='Open-source dossier on Abdul El-Sayed: Rhodes scholar, epidemiologist, Detroit health director, and the first Muslim American elected to the U.S. Senate.',
        fileno='File 462-ElSayed',
        h1='Abdul El-Sayed',
        sub='The Doctor of Detroit. Epidemiologist, former Detroit and Wayne County health director, and United States Senator-elect from Michigan. Compiled from open sources only.',
        photo='assets/elsayed.jpg',
        photoalt='Abdul El-Sayed speaking at a Senate campaign podium in Michigan',
        caption='Abdul El-Sayed, primary night, August 2026 — photograph: Reuters',
    ),
    dict(
        src='/home/hatch/workspace/your_files/james-uthmeier-osint-cv.md',
        out='dossier-uthmeier.html',
        title='James Uthmeier — File 377-Uthmeier',
        desc='Open-source dossier on James Uthmeier: the Destin native who rose from DeSantis general counsel to chief of staff to Florida attorney general — appointed in 2025, held in contempt, cleared by an appeals court, and elected to a full term in November 2026.',
        fileno='File 377-Uthmeier',
        h1='James Uthmeier',
        sub='The Governor’s Shield. Destin native, former DeSantis chief of staff, Florida’s 39th attorney general — appointed in 2025 and elected to a full term in November 2026. Compiled from open sources only.',
        photo='assets/uthmeier.jpg',
        photoalt='Official portrait of Florida Attorney General James Uthmeier, 2025',
        caption='James Uthmeier, official portrait, 2025 — Office of the Attorney General, via Wikimedia Commons',
    ),
    dict(
        src='/home/hatch/workspace/your_files/ward-mcdaniel-osint-cv.md',
        out='dossier-mcdaniel.html',
        title='Ward McDaniel — File 290-McDaniel',
        desc='Open-source dossier on Ward McDaniel: Gulf County District 2 commissioner from 2010 to 2022, repeated board chairman, the man in the only “Gulf seat” headline on record — and now a volunteer fire chief.',
        fileno='File 290-McDaniel',
        h1='Ward McDaniel',
        sub='The Gulf Seat. Gulf County’s District 2 commissioner for twelve years, repeated chairman of the board, and now chief of the Wetappo Creek Fire Department. Compiled from open sources only.',
        photo='assets/badge-192.png',
        photoalt='NS-FLUID badge — no verified photograph of the subject was found in open sources',
        caption='No verified photograph of the subject was found in open sources — the desk’s badge stands in.',
    ),
    dict(
        src='/home/hatch/workspace/your_files/scott-colom-osint-cv.md',
        out='dossier-colom.html',
        title='Scott Colom — File 498-Colom',
        desc='Open-source dossier on Scott Colom: the Mississippi district attorney whose federal judgeship was killed by a withheld blue slip in 2023 — and who answered by taking the seat of the senator who blocked him.',
        fileno='File 498-Colom',
        h1='Scott Colom',
        sub='The Blue Slip. District attorney of Mississippi’s 16th Judicial District since 2016, blocked from the federal bench in 2023 without a hearing — and now United States senator-elect from Mississippi. Compiled from open sources only.',
        photo='assets/colom.jpg',
        photoalt='Scott Colom in 2026',
        caption='Scott Colom, 2026 — photograph: The Contrarian, CC BY 4.0, via Wikimedia Commons',
    ),
]

for p in PAGES:
    md = pathlib.Path(p['src']).read_text(encoding='utf-8')
    body = convert(md)
    page = HEADER.format(body=body, **{k: v for k, v in p.items() if k not in ('src', 'out', 'body')})
    (SITE / p['out']).write_text(page, encoding='utf-8')
    print('wrote', p['out'], len(page), 'bytes, body lines:', body.count('\n') + 1)
