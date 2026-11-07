#!/usr/bin/env python3
"""Apply the Pediatric APP Academy theme to the CICU simulator repos.

Idempotent: re-running replaces the previously injected block.
Usage: python3 tools/reskin.py /path/to/Claude   (folder holding the lab repos)
"""
import re, sys, pathlib

HUB = "https://kayleighatodd-88.github.io/pediatric-app-academy/"
FONT_HREF = "https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;500;700;800&display=swap"
SANS = '"Atkinson Hyperlegible Next", "Segoe UI", "Helvetica Neue", Arial, sans-serif'

# Academy tokens (light, dark) — mirror of the design system's tokens.json
T = {
 'paper': ('#F4F5F6', '#14191E'), 'surface': ('#FFFFFF', '#1C232A'), 'sunken': ('#E9ECEE', '#232B33'),
 'panel2': ('#F9FAFA', '#232B33'),
 'ink': ('#232A30', '#E8ECEF'), 'muted': ('#5A646C', '#9FAAB4'), 'line': ('#DADFE3', '#313B45'),
 'action': ('#232A30', '#F2C230'), 'on-action': ('#FFFFFF', '#14191E'), 'tint': ('#E6E9EC', '#2A3239'),
 'deep': ('#232A30', '#26313B'), 'deep-ink': ('#F4F5F6', '#F4F5F6'), 'deep-muted': ('#AEB8C1', '#AEB8C1'),
 'hl': ('#F2C230', '#F2C230'), 'hl-deep': ('#A57A00', '#F2C230'),
 'good': ('#2A7347', '#6FCF97'), 'goodbg': ('#E5F1E9', '#17301F'), 'warn': ('#9A5F00', '#F2B84B'),
 'bad': ('#B3261E', '#FF8A80'), 'badbg': ('#FCEDEB', '#3A1D1A'),
}

# per-lab: old variable -> Academy token (or literal (light, dark))
MAPS = {
 'pacing': {'bg':'paper','panel':'surface','panel2':'panel2','ink':'ink','muted':'muted','line':'line','navy':'ink',
            'orange':'action','on-accent':'on-action','good':'good','amber':'warn','red':'bad','chip':'tint','focus':'action',
            'hdr':'deep','hdr-ink':'deep-ink','hdr-muted':'deep-muted'},
 'waveform': {'bg':'paper','panel':'surface','panel2':'panel2','ink':'ink','muted':'muted','line':'line',
            'orange':'action','on-accent':'on-action','good':'good','goodbg':'goodbg','red':'bad','redbg':'badbg','chip':'tint','focus':'action',
            'hdr':'deep','hdr-ink':'deep-ink','hdr-muted':'deep-muted','w-lv':'ink','w-cursor':'hl-deep','w-axis':'line',
            'w-band1':('rgba(242,194,48,.16)','rgba(242,194,48,.12)')},
 'vent': {'room':'paper','room2':'surface','panel':'surface','panel2':'sunken','ink':'ink','ink2':'muted','line':'line',
            'accent':'action','accent-ink':'on-action','accent-soft':'tint','charcoal':('#232A30','#232A30'),'limestone':('#DADFE3','#DADFE3'),
            'shade':('#AEB8C1','#AEB8C1'),'head':'deep','head-ink':'deep-ink'},
 'tpn': {'room':'paper','panel':'surface','panel2':'sunken','ink':'ink','ink2':'muted','line':'line',
            'accent':'action','accent-ink':'on-action','charcoal':'deep','shade':('#AEB8C1','#AEB8C1')},
}
FONTVARS = {'pacing':['sans'], 'waveform':['sans'], 'vent':['font','serif'], 'tpn':['font','serif','mono']}

def val(v, i): return v[i] if isinstance(v, tuple) else T[v][i]
def decl(lab, i):
    d = ''.join(f'--{k}:{val(v,i)};' for k, v in MAPS[lab].items())
    d += ''.join(f'--{k}:{SANS};' for k in FONTVARS[lab]) if i == 0 else ''
    d += ''.join(f'--paa-{k}:{T[k][i]};' for k in ('deep','deep-ink','deep-muted','hl','hl-deep','ink','line','action','on-action'))
    return d

CHROME = """
/* --- Academy chrome --- */
body{font-family:%(sans)s;font-variant-numeric:tabular-nums}
h1,h2,h3,h4{font-family:%(sans)s;letter-spacing:-.01em}
.top,.topbar{background:var(--paa-deep)!important;border-bottom:3px solid var(--paa-hl)!important;color:var(--paa-deep-ink)}
.top h1,.topbar h1,.brand h1{font-family:%(sans)s!important;font-weight:800}
.paa-home{display:inline-flex;align-items:center;gap:10px;color:var(--paa-deep-ink)!important;text-decoration:none;padding:4px 16px 4px 0;margin-right:4px;border-right:1px solid rgba(244,245,246,.22);flex:none;line-height:1}
.paa-home svg{width:30px;height:30px;flex:none}
.paa-home .t{display:flex;flex-direction:column}
.paa-home small{font-size:11px;font-weight:500;color:var(--paa-deep-muted)}
.paa-home b{font-size:16px;font-weight:800;letter-spacing:-.01em;margin-top:2px}
.paa-home:hover b{text-decoration:underline;text-decoration-color:var(--paa-hl);text-decoration-thickness:2px;text-underline-offset:3px}
.paa-hdr{display:flex;align-items:center;gap:14px;min-width:0}
.toolnav a,.toolnav span,.top nav a,.sibs a{border-radius:6px!important}
.toolnav a:hover,.top nav a:hover{border-color:var(--paa-hl)!important}
.toolnav span[aria-current],.toolnav a[aria-current],.top nav a[aria-current=page],.sibs a[aria-current="page"]{background:var(--paa-hl)!important;color:#232A30!important;border-color:var(--paa-hl)!important;opacity:1}
.brand>svg{display:none}
:focus-visible{outline-color:var(--paa-action)}
@media (max-width:640px){.paa-home .t{display:none}.paa-home{padding-right:10px}}
"""

MARK = ('<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M8 42 L24 6 L40 42" fill="none" stroke="#F4F5F6" stroke-width="4.5" stroke-linejoin="round" stroke-linecap="round"/>'
        '<path d="M12.5 30 H19.5 L21.75 24 L25 36 L27.25 30 H35.5" fill="none" stroke="#F2C230" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/></svg>')
HOME = f'<!--paa-home--><a class="paa-home" href="{HUB}" aria-label="Pediatric APP Academy home">{MARK}<span class="t"><small>The Pediatric</small><b>APP Academy</b></span></a><!--/paa-home-->'

def theme_css(lab, dark_selector_style):
    light, dark = decl(lab, 0), decl(lab, 1)
    if dark_selector_style == 'plain':   # TPN: @media dark { :root{} }
        dk = f'@media (prefers-color-scheme: dark){{:root{{{dark}color-scheme:dark}}}}'
    else:
        dk = (f'@media (prefers-color-scheme: dark){{:root:not([data-theme="light"]){{{dark}}}}}'
              f':root[data-theme="dark"]{{{dark}}}')
    return f':root{{{light}}}{dk}' + CHROME % {'sans': SANS}

BEGIN, END = '/* PAA-THEME:BEGIN — generated by pediatric-app-academy/tools/reskin.py */', '/* PAA-THEME:END */'

def strip_old(s):
    s = re.sub(re.escape('<style id="paa-theme">') + r'.*?</style>\n?', '', s, flags=re.S)
    s = re.sub(re.escape(BEGIN) + r'.*?' + re.escape(END) + r'\n?', '', s, flags=re.S)
    return re.sub(r'<!--paa-home-->.*?<!--/paa-home-->', '', s, flags=re.S)

def fix_literals(s):
    s = re.sub(r'#BF5700', '#A57A00', s, flags=re.I)
    s = re.sub(r'#F8971F', '#F2C230', s, flags=re.I)
    s = s.replace('Libre Franklin, Arial', 'Atkinson Hyperlegible Next, Arial').replace('"Libre Franklin"', '"Atkinson Hyperlegible Next"').replace("'Libre Franklin'", "'Atkinson Hyperlegible Next'")
    return s

def fonts(s, keep_cond=False):
    href = FONT_HREF if not keep_cond else FONT_HREF.replace('&display', '&family=Barlow+Semi+Condensed:wght@400;500;600;700&display')
    return re.sub(r'https://fonts\.googleapis\.com/css2\?family=[^"]+', href, s, count=1)

def html_page(path, lab, wrap=None, keep_cond=False):
    """wrap: (open_old, open_new, close_old, close_new) header edits applied once; HOME goes where '{HOME}' is."""
    s = path.read_text(encoding='utf-8')
    s = strip_old(s); s = fonts(s, keep_cond); s = fix_literals(s)
    s = s.replace('</head>', f'<style id="paa-theme">\n{BEGIN}\n{theme_css(lab, "attr")}\n{END}\n</style>\n</head>', 1)
    if wrap and 'paa-slot' not in s:
        o_old, o_new, c_old, c_new = wrap
        assert o_old in s and c_old in s, (path, 'header markup not found')
        s = s.replace(o_old, o_new, 1).replace(c_old, c_new, 1)
    s = s.replace('<span class="paa-slot"></span>', '<span class="paa-slot"></span>' + HOME, 1)
    assert 'paa-home' in s, (path, 'no home link')
    path.write_text(s, encoding='utf-8'); print('themed', path)

SLOT = '<span class="paa-slot"></span>'

def main(root):
    R = pathlib.Path(root)
    for f in ('teach.html', 'practice.html', 'checkoff.html'):
        html_page(R/'temporary-pacing-lab'/f, 'pacing', ('<header class="top">\n  <div><h1>', '<header class="top">\n  <div class="paa-hdr">' + SLOT + '<div><h1>',
                                                        '</p></div>\n  <nav class="toolnav"', '</p></div></div>\n  <nav class="toolnav"'))
    for f in ('teach.html', 'learn.html', 'check.html'):
        html_page(R/'cicu-ventilation-lab'/f, 'vent', ('<div class="brand">', '<div class="brand paa-hdr">' + SLOT, '<div class="brand">', '<div class="brand">'), keep_cond=True)
    html_page(R/'cicu-waveform-lab'/'src'/'app.html', 'waveform', ('<header class="top">\n  <div>\n    <h1>', '<header class="top">\n  <div class="paa-hdr">' + SLOT + '<div>\n    <h1>',
                                                        'providers</p>\n  </div>', 'providers</p>\n  </div></div>'))
    css = R/'cicu-tpn-lab'/'src'/'style.css'; s = strip_old(css.read_text(encoding='utf-8'))
    s = fix_literals(s).rstrip() + f'\n{BEGIN}\n{theme_css("tpn", "plain")}\n{END}\n'
    css.write_text(s, encoding='utf-8'); print('themed', css)
    sh = R/'cicu-tpn-lab'/'src'/'shell.js'; s = strip_old(sh.read_text(encoding='utf-8'))
    if 'paa-slot' not in s:
        old = '<div class="in"><a class="brand" href="index.html">TPN Lab</a>'
        assert old in s; s = s.replace(old, '<div class="in">' + SLOT + '<a class="brand" href="index.html">TPN Lab</a>', 1)
    s = s.replace(SLOT, SLOT + HOME, 1)
    sh.write_text(s, encoding='utf-8'); print('themed', sh)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '..')
