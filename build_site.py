# -*- coding: utf-8 -*-
"""把 wow_forever 目录下的 Markdown 构建成一个自包含的单文件网页 index.html。

用法：
    python build_site.py
输出：
    G:/ai/game/wow_forever/index.html

左侧导航为「树状索引」：
    分组（根） → 篇（一级节点） → 篇内小节（二级节点）
点小节即可切到对应篇并滚到该小节；还带关键词过滤、展开/收起全部。
新增/改名 .md 后自动出现在树里（未列出的排末尾）。
导航项格式：(文件名, 显示标题, 分组)  —— 分组为空时该篇作为根节点直接列出。
"""
import os
import re
import html
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))

# 导航顺序：文件名 -> (显示标题, 分组)
ORDER = [
    ("README.md", "首页 · 怎么读这个库", ""),
    ("leveling-and-gold.md", "★ 练级 · 技巧 · 打金", "玩法核心"),
    ("classes-and-gear.md", "★ 职业 · 天赋 · 配装", "玩法核心"),
    ("tools-and-ui.md", "★ 工具 · 插件 · 宏", "玩法核心"),
    ("launch-playbook.md", "★ 开局行动手册", "行动清单"),
    ("intel-digest.md", "★ 情报速报与实测", "情报追踪"),
    ("timeline.md", "关键时间线", "情报追踪"),
    ("update-playbook.md", "更新手册（内部）", "内部"),
]

TITLE_MAP = dict((f, t) for f, t, _ in ORDER)
GROUP_MAP = dict((f, g) for f, _, g in ORDER)


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
    """返回 (正文 HTML, 页内目录 [(层级, 文本, 锚点)])"""
    lines = text.split('\n')
    out = []
    toc = []
    counter = [0]
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

        # 标题（h2/h3 进目录并带锚点）
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            lv = len(m.group(1))
            txt = inline(m.group(2))
            if lv in (2, 3):
                counter[0] += 1
                anchor = 'sec%d' % counter[0]
                toc.append((lv, m.group(2).strip(), anchor))
                out.append('<h%d id="%s">%s</h%d>' % (lv, anchor, txt, lv))
            else:
                out.append('<h%d>%s</h%d>' % (lv, txt, lv))
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
                        om = re.match(r'^\s*(\d+)\.[ \t]+(.*)$', one)
                        txt = om.group(2) if om else re.sub(r'^\s*[\d.]+[ \t]*', '', one)
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

    return '\n'.join(out), toc


def collect_files():
    files = [f for f in os.listdir(BASE)
             if f.endswith('.md') and os.path.isfile(os.path.join(BASE, f))]
    ordered = [f for f, _, _ in ORDER if f in files]
    rest = sorted(f for f in files if f not in ordered)
    return [(f, TITLE_MAP.get(f, f.replace('.md', '')), GROUP_MAP.get(f, '其他')) for f in ordered + rest]


def load_css():
    for name in ('theme.css',):
        p = os.path.join(BASE, name)
        if os.path.isfile(p):
            return open(p, encoding='utf-8').read()
    return ''


NAV_JS = """
(function(){
  var btns  = [].slice.call(document.querySelectorAll('nav button[data-t]'));
  var docs  = [].slice.call(document.querySelectorAll('.doc'));
  var kids  = [].slice.call(document.querySelectorAll('a.kid'));
  var nodes = [].slice.call(document.querySelectorAll('details.node'));
  var roots = [].slice.call(document.querySelectorAll('details.root'));

  function show(id){
    btns.forEach(function(b){ b.classList.toggle('on', b.dataset.t === id); });
    docs.forEach(function(d){ d.classList.toggle('on', d.id === id); });
    reveal(id);
    window.scrollTo(0, 0);
  }
  function reveal(id){
    nodes.forEach(function(n){ if(n.dataset.k === id) n.open = true; });
    roots.forEach(function(r){
      if(r.querySelector('details.node[data-k="' + id + '"]')) r.open = true;
    });
  }
  function flash(a){
    kids.forEach(function(k){ k.classList.remove('hit'); });
    a.classList.add('hit');
    setTimeout(function(){ a.classList.remove('hit'); }, 1400);
  }
  function goto(a){
    var t = a.dataset.t, id = a.dataset.a;
    show(t); reveal(t);
    requestAnimationFrame(function(){
      var el = id ? document.getElementById(id) : null;
      var y = el ? el.getBoundingClientRect().top + window.scrollY - 64 : 0;
      window.scrollTo({ top: y < 0 ? 0 : y, behavior: 'smooth' });
    });
    flash(a);
  }
  btns.forEach(function(b){
    b.addEventListener('click', function(){ show(b.dataset.t); });
  });
  kids.forEach(function(a){
    a.addEventListener('click', function(e){ e.preventDefault(); goto(a); });
  });
  /* 小节高亮：滚动时把当前小节标出来 */
  var secs = [].slice.call(document.querySelectorAll('.doc.on h2[id], .doc.on h3[id]'));
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(e.isIntersecting && e.intersectionRatio > 0.55){
          var kid = document.querySelector('a.kid[data-a="' + e.target.id + '"]');
          kids.forEach(function(k){ k.classList.toggle('cur', k === kid); });
        }
      });
    }, { rootMargin: '-70px 0px -45% 0px', threshold: [0, 0.55, 1] });
    secs.forEach(function(s){ io.observe(s); });
  }

  /* 关键词过滤树 */
  var q = document.getElementById('q');
  if(q){
    q.addEventListener('input', function(){
      var v = q.value.trim().toLowerCase();
      if(!v){
        kids.concat(nodes, roots).forEach(function(x){ x.classList.remove('hide'); });
        return;
      }
      kids.forEach(function(a){
        var hit = a.textContent.toLowerCase().indexOf(v) >= 0;
        a.classList.toggle('hide', !hit);
        if(hit){ reveal(a.dataset.t); }
      });
      nodes.forEach(function(n){ n.classList.toggle('hide', !n.querySelector('a.kid:not(.hide)')); });
      roots.forEach(function(r){ r.classList.toggle('hide', !r.querySelector('a.kid:not(.hide)')); });
    });
  }
  /* 展开 / 收起全部 */
  var all = document.getElementById('expandAll');
  if(all){
    all.addEventListener('click', function(){
      var open = all.dataset.mode === 'open';
      nodes.concat(roots).forEach(function(n){ n.open = !open; });
      all.dataset.mode = open ? 'close' : 'open';
      all.textContent = open ? '展开全部' : '收起全部';
    });
  }
})();
"""

PRINT_JS = """
window.addEventListener('beforeprint', function(){
  document.querySelectorAll('.doc').forEach(function(d){ d.classList.add('on'); });
  document.querySelectorAll('nav,.bar').forEach(function(n){ n.style.display='none'; });
});
"""


def build_node(key, title, toc, first):
    star = ''
    if title.startswith('★'):
        star = '<span class="star">★</span>'
        title = title[1:].lstrip()
    kids = ''.join(
        '<a class="kid l%d" data-t="%s" data-a="%s" href="#%s" title="%s">%s</a>' % (
            lv - 2, key, anchor, anchor,
            esc(text).replace('"', '&quot;'), esc(text))
        for lv, text, anchor in toc)
    return ('<details class="node%s" data-k="%s"%s><summary>'
            '<span class="car"></span><button class="nt" type="button" data-t="%s">%s%s</button>'
            '<i class="cnt">%d</i></summary>%s</details>') % (
        ' on' if first else '', key, ' open' if first else '',
        key, star, esc(title), len(toc), kids)


def main():
    items = collect_files()
    CSS = load_css()

    parsed = []
    for fname, title, group in items:
        path = os.path.join(BASE, fname)
        raw = open(path, encoding='utf-8').read()
        # 去掉首个一级标题（已用作导航标题）
        raw = re.sub(r'^#\s+.*\n?', '', raw, count=1)
        body, toc = md_to_html(raw)
        key = re.sub(r'\W', '_', fname)
        parsed.append({
            'key': key, 'title': title, 'group': group or 'START',
            'body': body, 'toc': toc,
        })

    nav_html, doc_html = [], []
    first = True
    seen_groups = []
    group_nodes = {}
    for it in parsed:
        it['node'] = build_node(it['key'], it['title'], it['toc'], first)
        nav_html.append(it['node'])  # 占位，稍后按分组重排
        doc_html.append(
            '<section class="doc%s" id="%s"><h1>%s</h1>%s%s</section>' % (
                ' on' if first else '', it['key'], esc(it['title']),
                '', it['body']))
        key = it['key']
        if it['group'] not in seen_groups:
            seen_groups.append(it['group'])
            group_nodes[it['group']] = []
        group_nodes[it['group']].append(it)
        first = False

    # 重新组装树：分组（根） → 篇（节点） → 小节（叶子）
    tree = []
    for g in seen_groups:
        nodes = group_nodes[g]
        inner = ''.join(n['node'] for n in nodes)
        if g == 'START':
            tree.append(inner)
        else:
            tree.append(
                '<details class="root" open><summary><span class="car"></span>%s'
                '<i class="rn">%d</i></summary><div class="treebody">%s</div></details>' % (
                    esc(g), len(nodes), inner))

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
    <span>共 <i>%d</i> 篇</span>
    <span>国服上线 <i>2026-11-05 约 07:00</i></span>
    <span>生成于 <i>%s</i></span>
  </div>
  <div class="diamond"></div>
</header>
<div id="app">
  <nav class="tree">
    <div class="ttl">
      <span>树状目录 · Tree</span>
      <span class="acts"><i class="act" id="expandAll" data-mode="open">收起全部</i></span>
    </div>
    <div class="search"><input id="q" placeholder="过滤小节 / 关键词…" autocomplete="off"></div>
    <div class="treebody root">%s</div>
  </nav>
  <main>
    <div class="bar">
      <button onclick="window.print()">打印 / 导出 PDF</button>
      <span class="info">离线可用 · 单文件 · 点左侧小节直达</span>
    </div>
    %s
    <footer>数据源：国服官网/商城、BlizzCon 2026 座谈、外服 Beta 实测报道 · 更新方式见「更新手册」</footer>
  </main>
</div>
<button id="totop" title="回到顶部">↑</button>
<script>%s</script>
<script>%s</script></body></html>""" % (CSS, len(items), stamp,
                                        '\n'.join(tree), '\n'.join(doc_html), NAV_JS, PRINT_JS)

    out = os.path.join(BASE, 'index.html')
    open(out, 'w', encoding='utf-8').write(html_doc)
    print('built ->', out)
    print('docs  ->', len(items), [t for _, t, _ in items])
    print('size  ->', os.path.getsize(out), 'bytes')


if __name__ == '__main__':
    main()
