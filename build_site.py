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
    ("README.md", "导读 · 怎么读这个库", ""),
    ("leveling-and-gold.md", "★ 练级 · 技巧 · 打金", "玩法核心"),
    ("classes-and-gear.md", "★ 职业 · 天赋 · 配装", "玩法核心"),
    ("hunter.md", "★ 猎人专篇", "玩法核心"),
    ("tools-and-ui.md", "★ 工具 · 插件 · 宏", "玩法核心"),
    ("launch-playbook.md", "★ 开局行动手册", "行动清单"),
    ("intel-digest.md", "★ 情报速报与实测", "情报追踪"),
    ("timeline.md", "关键时间线", "情报追踪"),
    ("update-playbook.md", "更新手册（内部）", "内部"),
]

TITLE_MAP = dict((f, t) for f, t, _ in ORDER)
GROUP_MAP = dict((f, g) for f, _, g in ORDER)

# 顶部切换条用的短名（空间有限，只放 4 个字左右）
SHORT = {
    "README.md": "导读",
    "leveling-and-gold.md": "练级打金",
    "classes-and-gear.md": "职业天赋",
    "hunter.md": "猎人专篇",
    "tools-and-ui.md": "工具插件",
    "launch-playbook.md": "开局手册",
    "intel-digest.md": "情报速报",
    "timeline.md": "时间线",
    "update-playbook.md": "更新手册",
}


def short_of(fname, title):
    t = title[1:].lstrip() if title.startswith('★') else title
    return SHORT.get(fname, t[:6])


def brief(raw):
    """取正文第一段有效文字作为首页卡片摘要"""
    for line in raw.split('\n'):
        s = line.strip()
        if (not s or s.startswith('#') or s.startswith('|') or s.startswith('>')
                or s.startswith('- ') or s.startswith('* ') or s.startswith('```')
                or s.startswith('<!--') or re.match(r'^\d+\.', s)
                or re.match(r'^([-*_=])\1{2,}\s*$', s)):
            continue
        s = re.sub(r'\*\*([^*]+)\*\*', r'\1', s)
        s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
        return s.replace('`', '')[:76]
    return ''


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


def _is_sep_row(s):
    """表格分隔行：必须被 | 包围（单独一行的 --- 是水平线，不算）"""
    s = (s or '').strip()
    if not (s.startswith('|') and s.endswith('|')):
        return False
    cs = [c.strip().replace(' ', '') for c in s.strip('|').split('|')]
    cs = [c for c in cs if c]
    return bool(cs) and all(re.match(r'^:?-+:?$', c) for c in cs)


def _is_new_header(lines, k, n):
    """lines[k] 像新表表头：它后面第一个非空行是分隔行"""
    m = k + 1
    while m < n and not lines[m].strip():
        m += 1
    return m < n and _is_sep_row(lines[m])


def md_to_html(text, prefix=''):
    """返回 (正文 HTML, 页内目录 [(层级, 文本, 锚点)])
    prefix 为篇级前缀，保证多篇文章之间的锚点 id 不冲突"""
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

        # 表格（容忍行间空行：只有确认是「新表头 + 分隔行」才断开成另一张表）
        if line.lstrip().startswith('|'):
            rows = []
            while i < n:
                s = lines[i]
                if s.lstrip().startswith('|'):
                    rows.append(s.strip())
                    i += 1
                elif not s.strip():
                    j = i
                    while j < n and not lines[j].strip():
                        j += 1
                    same_table = (j < n and lines[j].lstrip().startswith('|')
                                  and not (any(_is_sep_row(r) for r in rows)
                                           and _is_new_header(lines, j, n)))
                    if same_table:
                        i = j
                    else:
                        break
                else:
                    break
            cells = []
            for r in rows:
                parts = [c.strip() for c in r.strip('|').split('|')]
                cells.append(parts)
            if len(cells) > 1 and _is_sep_row(rows[1]):
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
                anchor = '%ssec%d' % (prefix, counter[0])
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
  var DATA = __DATA__;
  var HOME='home';
  var chips=[].slice.call(document.querySelectorAll('.chip'));
  var docs=[].slice.call(document.querySelectorAll('.doc'));
  var tocList=document.getElementById('tocList');
  var pagerEl=document.getElementById('pager');
  var topBtn=document.getElementById('totop');
  var cur=HOME;
  var seq=DATA.map(function(d){return d.k;});
  var io=null;

  function byKey(k){for(var i=0;i<DATA.length;i++){if(DATA[i].k===k)return DATA[i];}return null;}
  function topOff(){return 76;}

  function item(k,t,i){
    return '<a class="l'+(t[0]-2)+'" data-i="'+i+'" data-k="'+k+'" data-a="'+t[2]+'" href="#'+t[2]+'" title="'+t[1]+'">'+t[1]+'</a>';
  }
  var sideT=document.querySelector('.side-t');
  function renderToc(k){
    tocList.classList.remove('res');
    if(k===HOME){
      if(sideT){sideT.innerHTML='全部 <b>篇目</b>';}
      var g='<div class="tocgroup">全部篇目</div>';
      DATA.forEach(function(d){
        g+='<a class="l0" data-i="0" data-k="'+d.k+'" data-a="" href="#" title="'+d.t+'">'+d.t+'</a>';
      });
      tocList.innerHTML=g;bindToc();return;
    }
    if(sideT){sideT.innerHTML='本篇 <b>目录</b>';}
    var d=byKey(k);
    if(!d){tocList.innerHTML='<div class="side-empty">暂无小节</div>';return;}
    var h='';
    d.toc.forEach(function(t,i){h+=item(k,t,i);});
    tocList.innerHTML=h;bindToc();expandAround(-1);
  }
  /* Apple 文档式：只列一级，阅读到哪一段才展开它的子项，保证侧栏始终短 */
  function expandAround(i){
    var d=byKey(cur);
    if(!d)return;
    var toc=d.toc,p=0;
    if(i>=0){
      p=i;
      while(p>0&&toc[p][0]!==2)p--;
    }
    var q=p+1;
    while(q<toc.length&&toc[q][0]===3)q++;
    [].slice.call(tocList.querySelectorAll('a')).forEach(function(a){
      var j=parseInt(a.getAttribute('data-i'),10);
      if(a.className.indexOf('l1')>=0){a.classList.toggle('sub-show',j>p&&j<q);}
    });
  }
  function bindToc(){
    [].slice.call(tocList.querySelectorAll('a')).forEach(function(a){
      a.addEventListener('click',function(e){
        e.preventDefault();
        var k=a.getAttribute('data-k'),id=a.getAttribute('data-a');
        expandAround(parseInt(a.getAttribute('data-i'),10));
        if(k!==cur){show(k,id);}else{scrollToId(id);}
        [].slice.call(tocList.querySelectorAll('a')).forEach(function(x){x.classList.remove('hit');});
        a.classList.add('hit');
      });
    });
  }
  function scrollToId(id){
    if(!id){window.scrollTo(0,0);return;}
    var el=document.getElementById(id);
    if(!el)return;
    var y=el.getBoundingClientRect().top+window.pageYOffset-topOff();
    window.scrollTo(0,Math.max(0,y));   /* 平滑度交给 CSS scroll-behavior */
  }
  function updatePager(k){
    if(!pagerEl)return;
    if(k===HOME){pagerEl.innerHTML='';return;}
    var i=seq.indexOf(k),h='';
    var p=i>0?byKey(seq[i-1]):null,n=(i>-1&&i<seq.length-1)?byKey(seq[i+1]):null;
    if(p)h+='<a class="prev" href="#" data-k="'+p.k+'"><span class="lab">上一篇</span><span class="nm">'+p.t+'</span></a>';
    if(n)h+='<a class="next" href="#" data-k="'+n.k+'"><span class="lab">下一篇</span><span class="nm">'+n.t+'</span></a>';
    pagerEl.innerHTML=h;
    [].slice.call(pagerEl.querySelectorAll('a')).forEach(function(a){
      a.addEventListener('click',function(e){e.preventDefault();show(a.getAttribute('data-k'));});
    });
  }
  function observe(){
    if(!('IntersectionObserver' in window))return;
    if(io)io.disconnect();
    var secs=[].slice.call(document.querySelectorAll('.doc.on h2[id],.doc.on h3[id]'));
    io=new IntersectionObserver(function(es){
      es.forEach(function(e){
        if(e.isIntersecting&&e.intersectionRatio>0.5){
          var a=tocList.querySelector('a[data-a="'+e.target.id+'"]');
          if(a){expandAround(parseInt(a.getAttribute('data-i'),10));}
          [].slice.call(tocList.querySelectorAll('a')).forEach(function(x){x.classList.toggle('cur',x===a);});
        }
      });
    },{rootMargin:'-84px 0px -55% 0px',threshold:[0,0.5,1]});
    secs.forEach(function(s){io.observe(s);});
  }
  function show(k,anchor){
    cur=k;
    chips.forEach(function(c){c.classList.toggle('on',c.getAttribute('data-k')===k);});
    docs.forEach(function(d){d.classList.toggle('on',d.id===k);});
    renderToc(k);updatePager(k);
    var q=document.getElementById('q');
    if(q&&q.value){q.value='';}
    if(anchor){requestAnimationFrame(function(){scrollToId(anchor);});}
    else{window.scrollTo(0,0);}
    observe();
  }
  chips.forEach(function(c){c.addEventListener('click',function(){show(c.getAttribute('data-k'));});});
  [].slice.call(document.querySelectorAll('.brand')).forEach(function(b){
    b.addEventListener('click',function(e){e.preventDefault();show(HOME);});
  });
  [].slice.call(document.querySelectorAll('.card')).forEach(function(c){
    c.addEventListener('click',function(){show(c.getAttribute('data-k'));});
  });
  var q=document.getElementById('q');
  if(q){
    q.addEventListener('input',function(){
      var v=q.value.trim().toLowerCase();
      if(!v){renderToc(cur);return;}
      var h='',n=0;
      DATA.forEach(function(d){
        var inT=d.t.toLowerCase().indexOf(v)>=0;
        var hits=d.toc.filter(function(t){return inT||t[1].toLowerCase().indexOf(v)>=0;});
        if(inT)hits=hits.slice(0,8);
        if(!hits.length)return;
        h+='<div class="tocgroup">'+d.t+'</div>';
        hits.forEach(function(t){n++;h+=item(d.k,t);});
      });
      tocList.classList.toggle('res',n>0);
      tocList.innerHTML=n?h:'<div class="side-empty">没有匹配的小节</div>';
      bindToc();
    });
  }
  var tb=document.getElementById('themeBtn');
  if(tb){
    tb.addEventListener('click',function(){
      var now=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';
      document.documentElement.setAttribute('data-theme',now);
      try{localStorage.setItem('wf-theme',now);}catch(e){}
      tb.textContent=now==='dark'?'\u2600':'\u263E';
    });
  }
  document.addEventListener('keydown',function(e){
    if(e.key==='/'&&document.activeElement!==q){e.preventDefault();if(q)q.focus();}
    if(e.key==='Escape'&&document.activeElement===q){q.value='';q.dispatchEvent(new Event('input'));q.blur();}
  });
  window.addEventListener('scroll',function(){
    if(!topBtn)return;
    topBtn.classList.toggle('show',window.pageYOffset>420);
  });
  if(topBtn)topBtn.addEventListener('click',function(){window.scrollTo(0,0);});

  var hash=(location.hash||'').replace('#','');
  var wantAnchor=null;
  if(hash&&hash!=='home'){
    if(byKey(hash)){show(hash);}
    else{
      var el=document.getElementById(hash);
      var sec=(el&&el.closest)?el.closest('.doc'):null;
      if(sec){show(sec.id,hash);wantAnchor=hash;}else{show(HOME);}
    }
  }else{show(HOME);}

  /* 浏览器对 #篇名 的自动滚动会把篇标题顶出视口，加载完成后多帧重置 */
  var booting=true;
  function fixScroll(){
    if(!booting)return;
    if(wantAnchor&&cur!==HOME){scrollToId(wantAnchor);}
    else{window.scrollTo(0,0);}
  }
  document.addEventListener('click',function(){booting=false;},true);  /* 用户一旦操作就不再干预 */
  window.addEventListener('load',function(){
    if(!hash||hash==='home'){booting=false;return;}  /* 无 # 进入：初始就在顶部，无需纠正 */
    fixScroll();
    setTimeout(fixScroll,60);
    setTimeout(fixScroll,320);
    setTimeout(function(){booting=false;},520);
  });
  window.addEventListener('hashchange',function(){
    var k=(location.hash||'').replace('#','');
    if(!k||k==='home'){wantAnchor=null;show(HOME);return;}
    if(byKey(k)){wantAnchor=null;show(k);return;}
    var el=document.getElementById(k);
    var sec=(el&&el.closest)?el.closest('.doc'):null;
    if(sec){wantAnchor=k;show(sec.id,k);}
  });
})();
"""

PRINT_JS = """
window.addEventListener('beforeprint', function(){
  if(document.documentElement.getAttribute('data-theme')==='dark'){
    document.documentElement.setAttribute('data-theme','light');
  }
});
"""

THEME_JS = """
(function(){try{
  var t=localStorage.getItem('wf-theme');
  if(!t){t=(window.matchMedia&&window.matchMedia('(prefers-color-scheme: dark)').matches)?'dark':'light';}
  document.documentElement.setAttribute('data-theme',t);
}catch(e){}})();
"""


def main():
    import json
    items = collect_files()
    CSS = load_css()

    parsed = []
    for idx, (fname, title, group) in enumerate(items):
        path = os.path.join(BASE, fname)
        raw = open(path, encoding='utf-8').read()
        # 去掉首个一级标题（已用作导航标题）
        raw = re.sub(r'^#\s+.*\n?', '', raw, count=1)
        body, toc = md_to_html(raw, 'p%d_' % (idx + 1))
        key = re.sub(r'\W', '_', fname)
        parsed.append({
            'key': key, 'title': title,
            'name': title[1:].lstrip() if title.startswith('★') else title,
            'short': short_of(fname, title),
            'group': group or 'START', 'body': body, 'toc': toc,
            'brief': brief(raw),
        })
    for it in parsed:
        if not it['brief']:
            it['brief'] = '共 %d 个小节，点开查看完整内容。' % len(it['toc'])

    def escq(s):
        return html.escape(s, quote=True)

    def label_of(g):
        return '快速上手' if g == 'START' else g

    # 顶部切换条：概览 + 各篇短名
    chips = ['<button class="chip on" type="button" data-k="home">概览</button>']
    for it in parsed:
        chips.append('<button class="chip" type="button" data-k="%s">%s</button>' % (
            it['key'], esc(it['short'])))
    chips_html = ''.join(chips)

    # 首页卡片：按分组分块
    seen = []
    for it in parsed:
        if it['group'] not in seen:
            seen.append(it['group'])
    blocks = []
    for g in seen:
        nodes = [x for x in parsed if x['group'] == g]
        cards = []
        for n in nodes:
            nm = n['name']
            cards.append(
                '<div class="card" data-k="%s" role="button" tabindex="0">'
                '<div class="no">%02d</div><h3>%s</h3><p>%s</p>'
                '<div class="meta"><b>%d 节</b><i>·</i><span>%s</span>'
                '<span class="arrow">&#8250;</span></div></div>' % (
                    n['key'], parsed.index(n) + 1, esc(nm), esc(n['brief']),
                    len(n['toc']), esc(label_of(g))))
        blocks.append('<div class="sec-t">%s</div><div class="grid">%s</div>' % (
            esc('从这里开始' if g == 'START' else g), ''.join(cards)))
    home_body = ''.join(blocks)

    total_sec = sum(len(it['toc']) for it in parsed)
    stamp = datetime.now().strftime('%Y-%m-%d %H:%M')

    home_html = (
        '<section class="doc home on" id="home">'
        '<div class="hero">'
        '<div class="eyebrow">World of Warcraft: Forever &#183; Classic+ &#183; 等级上限锁 60</div>'
        '<h1>开荒资料库</h1>'
        '<p class="lede">单人开荒可用的完整口径：练级、打金、职业配装、工具插件与情报追踪。'
        '所有结论都标注来源与不确定处，没有官方口径的地方如实留白。</p>'
        '<div class="facts">'
        '<span><b>%d</b> 篇</span><span><b>%d</b> 节</span>'
        '<span>国服上线 <b>2026-11-05</b></span><span>更新 <b>%s</b></span>'
        '</div></div>%s</section>') % (len(parsed), total_sec, stamp, home_body)

    doc_html = []
    for it in parsed:
        nm = it['name']
        doc_html.append(
            '<section class="doc" id="%s"><div class="title">%s</div>'
            '<div class="sub"><span>%s</span><span>%d 节</span></div>%s</section>' % (
                it['key'], esc(nm), esc(label_of(it['group'])), len(it['toc']), it['body']))
    docs_html = ''.join(doc_html)

    data = [{'k': it['key'], 't': it['name'],
             'toc': [[lv, escq(tx), a] for lv, tx, a in it['toc']]} for it in parsed]
    nav_js = NAV_JS.replace('__DATA__', json.dumps(data, ensure_ascii=False))

    html_doc = """<!DOCTYPE html>
<html lang="zh-CN" data-theme="light"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>《魔兽世界》：无限 · 开荒资料库</title>
<style>%s</style>
<script>%s</script></head><body>
<header class="top"><div class="top-in">
  <a class="brand" href="#home">魔兽世界：无限<em>Forever</em></a>
  <nav class="chips">%s</nav>
  <div class="tools">
    <div class="search">
      <svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4">
        <circle cx="11" cy="11" r="7"></circle><path d="M20 20l-3.6-3.6"></path></svg>
      <input id="q" placeholder="搜索小节" autocomplete="off">
    </div>
    <button type="button" id="themeBtn" title="切换深浅">&#9788;</button>
    <button type="button" onclick="window.print()">打印</button>
  </div>
</div></header>
<div id="app">
  <aside class="side">
    <div class="side-t">本篇 <b>目录</b></div>
    <div class="toclist" id="tocList"></div>
    <div class="side-hint">按 <kbd>/</kbd> 搜索小节，<kbd>Esc</kbd> 清空<br>点右上角切换深浅色</div>
  </aside>
  <main>
    %s%s
    <div class="pager" id="pager"></div>
    <footer>数据源：国服官网 / 商城、BlizzCon 2026 座谈、外服 Beta 实测报道 · 更新方式见「更新手册」</footer>
  </main>
</div>
<button id="totop" title="回到顶部">&#8593;</button>
<script>%s</script>
<script>%s</script></body></html>""" % (CSS, THEME_JS, chips_html, home_html, docs_html,
                                        nav_js, PRINT_JS)

    out = os.path.join(BASE, 'index.html')
    open(out, 'w', encoding='utf-8').write(html_doc)
    print('built ->', out)
    print('docs  ->', len(items), [t for _, t, _ in items])
    print('secs  ->', total_sec)
    print('size  ->', os.path.getsize(out), 'bytes')


if __name__ == '__main__':
    main()
