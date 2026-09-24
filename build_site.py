# -*- coding: utf-8 -*-
"""把 wow_forever 目录下的 Markdown 全部构建成一个自包含的单文件网页 index.html。

用法：
    python build_site.py
输出：
    G:/ai/game/wow_forever/index.html
新增/改名 .md 后自动出现在导航（未列出的文件排在末尾）。
"""
import os
import re
import html
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))

# 导航顺序：文件名 -> 显示标题（未列出的自动追加到末尾）
ORDER = [
    ("README.md", "项目总览"),
    ("beta-findings.md", "★ 外服实测与捷径"),
    ("leveling-gold-route.md", "★ 升级赚钱路线"),
    ("talents-and-gear.md", "★ 天赋配点与装备"),
    ("stats-and-gear.md", "★ 属性体系与配装"),
    ("macros-and-ui.md", "★ 一键输出与宏"),
    ("efficiency-guide.md", "效率指南"),
    ("timeline.md", "关键时间线"),
    ("reference-sites.md", "参考网站"),
    ("prep-checklist.md", "准备检查表"),
    ("intel-digest.md", "情报摘要"),
    ("update-playbook.md", "更新待命手册"),
]

TITLE_MAP = dict((f, t) for f, t in ORDER)


def esc(s):
    return html.escape(s, quote=False)


def _mk_link(url, text):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, text)


_TAIL = '.,;:!?。，、；：！？）'


def inline(s):
    """行内格式：先占位保护代码块与 Markdown 链接，再加粗/斜体，最后把裸网址变成可点击链接"""
    s = esc(s)
    store = []

    def keep(h):
        store.append(h)
        return '\x00%d\x00' % (len(store) - 1)

    def code_rep(m):
        return keep('<code>%s</code>' % m.group(1))

    s = re.sub(r'`([^`]+)`', code_rep, s)

    def link_rep(m):
        return keep(_mk_link(m.group(2), m.group(1)))

    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', link_rep, s)

    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)

    def url_rep(m):
        u = m.group(0)
        while u and u[-1] in _TAIL:
            u = u[:-1]
        return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (u, u)

    s = re.sub(r'(?<!["\'=])https?://[^\s<>"\'()\[\]]+', url_rep, s)

    return re.sub('\x00(\\d+)\x00', lambda m: store[int(m.group(1))], s)


def list_item_html(line):
    m = re.match(r'^(\s*)[-*] (.*)$', line)
    if not m:
        return None, None
    indent = len(m.group(1)) // 2
    body = m.group(2)
    check = ''
    cm = re.match(r'^\[([ xX])\]\s*(.*)$', body)
    if cm:
        cls = 'checked' if cm.group(1).lower() == 'x' else ''
        check = '<span class="cb %s"></span>' % cls
        body = cm.group(2)
    return indent, '<li>%s%s</li>' % (check, inline(body))


def md_to_html(text):
    lines = text.split('\n')
    out = []
    i = 0
    n = len(lines)

    while i < n:
        raw = lines[i]
        line = raw.rstrip()

        # 代码块
        if line.startswith('```'):
            i += 1
            buf = []
            while i < n and not lines[i].startswith('```'):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append('<pre><code>%s</code></pre>' % esc('\n'.join(buf)))
            continue

        # 注释
        if line.strip().startswith('<!--'):
            i += 1
            continue

        # 空行
        if not line.strip():
            i += 1
            continue

        # 分隔线
        if re.match(r'^-{3,}$', line.strip()) or re.match(r'^\*{3,}$', line.strip()):
            out.append('<hr>')
            i += 1
            continue

        # 表格
        if line.lstrip().startswith('|'):
            rows = []
            while i < n and lines[i].lstrip().startswith('|'):
                rows.append(lines[i].strip())
                i += 1
            cells = []
            for r in rows:
                parts = [c.strip() for c in r.strip('|').split('|')]
                cells.append(parts)
            if re.match(r'^[-: ]+$', ''.join(cells[1])) if len(cells) > 1 else False:
                cells.pop(1)
            head = cells[0]
            body = cells[1:]
            h = '<div class="tw"><table><thead><tr>'
            for c in head:
                h += '<th>%s</th>' % inline(c)
            h += '</tr></thead><tbody>'
            for row in body:
                h += '<tr>'
                for idx, c in enumerate(row):
                    h += '<td>%s</td>' % inline(c)
                h += '</tr>'
            h += '</tbody></table></div>'
            out.append(h)
            continue

        # 标题
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            lv = len(m.group(1))
            out.append('<h%d>%s</h%d>' % (lv, inline(m.group(2)), lv))
            i += 1
            continue

        # 引用
        if line.lstrip().startswith('>'):
            buf = []
            while i < n and lines[i].lstrip().startswith('>'):
                buf.append(re.sub(r'^\s*>\s?', '', lines[i]))
                i += 1
            out.append('<blockquote>%s</blockquote>' % inline(' '.join(
                b.strip() for b in buf if b.strip())).replace('\n', '<br>'))
            continue

        # 列表（按同类型连续分组，容忍 ul/ol 混排）
        if re.match(r'^\s*[-*] ', line) or re.match(r'^\s*\d+\.[ \t]', line):
            def kind(s):
                if re.match(r'^\s*[-*] ', s):
                    return 'ul'
                if re.match(r'^\s*\d+\.[ \t]', s):
                    return 'ol'
                return None

            while i < n and kind(lines[i]):
                k = kind(lines[i])
                buf = []
                while i < n and kind(lines[i]) == k:
                    one = lines[i]
                    if k == 'ol':
                        om = re.match(r'^\s*\d+\.[ \t]+(.*)$', one)
                        txt = om.group(1) if om else re.sub(r'^\s*\d+\.[ \t]*', '', one)
                        buf.append('<li>%s</li>' % inline(txt.strip()))
                    else:
                        ind, li = list_item_html(one)
                        buf.append('  ' * (ind or 0) + li)
                    i += 1
                out.append('<%s>%s</%s>' % (k, ''.join(buf), k))
            continue

        # 段落
        buf = []
        while i < n and lines[i].strip() and not re.match(
                r'^(\s*[-*] |\s*\d+\.\s|#{1,6}\s|>|```|\s*\|)', lines[i]):
            buf.append(lines[i].strip())
            i += 1
        if buf:
            out.append('<p>%s</p>' % inline(' '.join(buf)))
        else:
            i += 1

    return '\n'.join(out)


def collect_files():
    files = [f for f in os.listdir(BASE)
             if f.endswith('.md') and os.path.isfile(os.path.join(BASE, f))]
    ordered = [f for f, _ in ORDER if f in files]
    rest = sorted(f for f in files if f not in ordered)
    return [(f, TITLE_MAP.get(f, f.replace('.md', ''))) for f in ordered + rest]


def load_css():
    for name in ('theme.css',):
        p = os.path.join(BASE, name)
        if os.path.isfile(p):
            return open(p, encoding='utf-8').read()
    return ''
JS = """
var btns=document.querySelectorAll('nav button[data-t]');
var docs=document.querySelectorAll('.doc');
function show(id){
  btns.forEach(function(b){b.classList.toggle('on',b.dataset.t===id)});
  docs.forEach(function(d){d.classList.toggle('on',d.id===id)});
  window.scrollTo(0,0);
}
btns.forEach(function(b){b.addEventListener('click',function(){show(b.dataset.t)})});
"""


def main():
    items = collect_files()
    CSS = load_css()
    nav_html, doc_html = [], []
    first = True
    for fname, title in items:
        path = os.path.join(BASE, fname)
        raw = open(path, encoding='utf-8').read()
        # 去掉首个一级标题（已用作导航标题）
        raw = re.sub(r'^#\s+.*\n?', '', raw, count=1)
        body = md_to_html(raw)
        key = re.sub(r'\W', '_', fname)
        t_safe = esc(title)
        if t_safe.startswith('★'):
            t_safe = '<span class="star">★</span>' + t_safe[1:].lstrip()
        nav_html.append('<button data-t="%s" class="%s">%s</button>' % (
            key, 'on' if first else '', t_safe))
        doc_html.append(
            '<section class="doc %s" id="%s"><h1>%s</h1>%s</section>' % (
                'on' if first else '', key, esc(title), body))
        first = False

    stamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    html_doc = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>《魔兽世界》：无限 · 开荒资料库</title>
<style>%s</style></head><body>
<div class="topbar">
  <b>WORLD OF WARCRAFT</b><span>FOREVER · CLASSIC+</span>
  <span class="sp">国服上线 2026-11-05</span>
</div>
<header class="hero">
  <div class="crest"></div>
  <div class="eyebrow">Classic+ 永久分支 · 等级上限锁 60</div>
  <h1>《魔兽世界》：无限</h1>
  <div class="sub">World of Warcraft: Forever — 单人开荒资料库</div>
  <div class="meta">
    <span>共 <i>%d</i> 份文档</span>
    <span>国服上线 <i>2026-11-05 约 07:00</i></span>
    <span>生成于 <i>%s</i></span>
  </div>
  <div class="diamond"></div>
</header>
<div id="app">
  <nav><div class="ttl">目录 / Contents</div>%s</nav>
  <main>
    <div class="bar">
      <button onclick="window.print()">打印 / 导出 PDF</button>
      <span class="info">离线可用 · 单文件 · 点击左侧切换</span>
    </div>
    %s
    <footer>数据源：国服官网/商城、BlizzCon 2026 座谈、外服 Beta 实测报道 · 更新方式见「更新待命手册」</footer>
  </main>
</div>
<script>%s</script></body></html>""" % (CSS, len(items), stamp,
                                        '\n'.join(nav_html), '\n'.join(doc_html), JS)

    out = os.path.join(BASE, 'index.html')
    open(out, 'w', encoding='utf-8').write(html_doc)
    print('built ->', out)
    print('docs  ->', len(items), [t for _, t in items])
    print('size  ->', os.path.getsize(out), 'bytes')


if __name__ == '__main__':
    main()
