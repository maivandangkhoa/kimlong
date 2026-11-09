import os
import json
import html
import re
from datetime import datetime

SITE_URL = "https://quatangdoanhnghiepdanang.com"
POSTS_DIR = "content/posts"
OUTPUT_DIR = "bai-viet"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs("content", exist_ok=True)

# 1. Update content/posts.json
files = [f for f in os.listdir(POSTS_DIR) if f.endswith('.json')]
files.sort(reverse=True)
with open('content/posts.json', 'w', encoding='utf-8') as f:
    json.dump(files, f, ensure_ascii=False, indent=2)

def markdown_to_html(md_text):
    if not md_text:
        return ""
    lines = md_text.split('\n')
    html_lines = []
    in_list = False
    for line in lines:
        line_str = line.strip()
        if not line_str:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            continue
        
        # Headers
        if line_str.startswith('### '):
            if in_list:
                html_lines.append('</ul>'); in_list = False
            html_lines.append(f'<h3>{html.escape(line_str[4:])}</h3>')
        elif line_str.startswith('## '):
            if in_list:
                html_lines.append('</ul>'); in_list = False
            html_lines.append(f'<h2>{html.escape(line_str[3:])}</h2>')
        elif line_str.startswith('# '):
            if in_list:
                html_lines.append('</ul>'); in_list = False
            html_lines.append(f'<h1>{html.escape(line_str[2:])}</h1>')
        elif line_str.startswith('- ') or line_str.startswith('* '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{format_inline(line_str[2:])}</li>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append(f'<p>{format_inline(line_str)}</p>')
    if in_list:
        html_lines.append('</ul>')
    return '\n'.join(html_lines)

def format_inline(text):
    text = html.escape(text)
    # Images: ![alt](/path) (before links/italic so '*' and '[' don't clash)
    text = re.sub(r'!\[(.*?)\]\(([^\s)]+)\)', r'<img src="\2" alt="\1" loading="lazy">', text)
    # Bold: **text**
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic: *text*
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Links: [text](url)
    text = re.sub(r'\[(.+?)\]\((https?://[^\s]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    return text

posts_data = []
for file in files:
    filepath = os.path.join(POSTS_DIR, file)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            slug = file[:-5]
            data['slug'] = slug
            data['filename'] = file
            posts_data.append(data)
    except Exception as e:
        print(f"Error reading {file}: {e}")

template = """<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="theme-color" content="#0b162b">
  
  <title>{seo_title}</title>
  <meta name="description" content="{seo_description}">
  <link rel="canonical" href="{canonical_url}">
  
  <!-- Open Graph / Facebook -->
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{seo_title}">
  <meta property="og:description" content="{seo_description}">
  {og_image_tag}
  
  <!-- Twitter -->
  <meta property="twitter:card" content="summary_large_image">
  <meta property="twitter:url" content="{canonical_url}">
  <meta property="twitter:title" content="{seo_title}">
  <meta property="twitter:description" content="{seo_description}">
  {twitter_image_tag}

  <link rel="icon" href="/assets/logo-mark.jpg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&family=Inter:wght@400;600;700;800&display=swap&subset=vietnamese,latin">
  <link rel="stylesheet" href="/styles.css">
  
  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {schema_json}
  </script>
</head>
<body class="single-post-page">
  <div class="topbar">
    <div class="container topbar-inner">
      <span>QUÀ TẶNG DOANH NGHIỆP &amp; IN ẤN TẠI ĐÀ NẴNG</span>
      <div class="top-links">
        <a href="tel:+84913515077">0913 515 077</a>
        <span>•</span>
        <a href="mailto:kimlonggift@gmail.com">kimlonggift@gmail.com</a>
      </div>
    </div>
  </div>

  <header class="site-header">
    <div class="container nav-wrap">
      <a class="brand" href="/">
        <img src="/assets/logo-mark.jpg" alt="Kim Long Gift" class="brand-logo">
        <div class="brand-copy"><strong>KIM LONG</strong><span>GIFT CO., LTD</span></div>
      </a>
      <button class="menu-toggle" aria-label="Mở menu" aria-expanded="false">☰</button>
      <nav class="nav" id="nav">
        <a href="/#products">Sản phẩm</a>
        <a href="/#solutions">Giải pháp</a>
        <a href="/#projects">Dự án</a>
        <a href="/#process">Quy trình</a>
        <a href="/#news">Tin tức</a>
        <a href="/#about">Về Kim Long</a>
        <a href="/#contact">Liên hệ</a>
        <button class="btn btn-gold nav-cta" data-open-quote>Nhận báo giá</button>
      </nav>
    </div>
  </header>

  <main class="post-single-main">
    <div class="container post-container">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/">Trang chủ</a> <span>/</span> <a href="/#news">Tin tức</a> <span>/</span> <span aria-current="page">{title_escaped}</span>
      </nav>

      <article class="post-article">
        <header class="post-header">
          {date_html}
          <h1 class="post-title">{title_escaped}</h1>
        </header>

        {image_html}

        {summary_html}

        <div class="post-body">
          {body_html}
        </div>

        <div class="post-share-banner">
          <div class="share-copy">
            <strong>Bạn đang cần tư vấn quà tặng doanh nghiệp?</strong>
            <p>Kim Long Gift tư vấn giải pháp, thiết kế demo miễn phí và báo giá tận xưởng.</p>
          </div>
          <button class="btn btn-gold" data-open-quote>Nhận báo giá ngay ↗</button>
        </div>
      </article>

      {recent_posts_html}
    </div>
  </main>

  <footer class="footer">
    <div class="container footer-grid">
      <div class="footer-brand">
        <img src="/assets/logo-mark.jpg" alt="Kim Long Gift">
        <h3>KIM LONG GIFT</h3>
        <p>Quà tặng doanh nghiệp &amp; in ấn tại Đà Nẵng.</p>
      </div>
      <div>
        <span class="footer-title">KHÁM PHÁ</span>
        <a href="/#products">Sản phẩm</a>
        <a href="/#solutions">Giải pháp</a>
        <a href="/#projects">Dự án</a>
        <a href="/#process">Quy trình</a>
      </div>
      <div>
        <span class="footer-title">LIÊN HỆ</span>
        <a href="tel:+84913515077">0913 515 077</a>
        <a href="tel:+84915129579">0915 129 579</a>
        <a href="mailto:kimlonggift@gmail.com">kimlonggift@gmail.com</a>
      </div>
      <div>
        <span class="footer-title">ĐỊA CHỈ</span>
        <p>Lô 32. B2.101 KĐT Ven sông Hòa Quý – Đồng Nò, P. Hòa Quý, Q. Ngũ Hành Sơn, TP. Đà Nẵng</p>
        <a href="https://www.facebook.com/kimlonggift" target="_blank" rel="noopener">Facebook Kim Long Gift ↗</a>
      </div>
    </div>
    <div class="container footer-bottom">
      <span>© 2026 Kim Long Gift Co., Ltd.</span>
      <span>Quà tặng • In ấn • Đà Nẵng</span>
    </div>
  </footer>

  <div class="mobile-bar">
    <a href="tel:+84913515077">☎ Gọi ngay</a>
    <a href="https://zalo.me/0913515077" target="_blank" rel="noopener">Zalo</a>
    <button data-open-quote>Báo giá</button>
  </div>

  <div class="modal" id="quoteModal" aria-hidden="true">
    <div class="modal-backdrop" data-close-quote></div>
    <div class="modal-panel">
      <button class="modal-close" data-close-quote aria-label="Đóng">×</button>
      <span class="section-kicker">NHẬN BÁO GIÁ</span>
      <h2>Hãy cho Kim Long biết<br><em>bạn đang cần gì.</em></h2>
      <form id="quoteForm">
        <div class="form-grid">
          <label>Họ tên *<input name="name" required placeholder="Nguyễn Văn A"></label>
          <label>Công ty<input name="company" placeholder="Tên doanh nghiệp"></label>
        </div>
        <div class="form-grid">
          <label>Số điện thoại *<input name="phone" required type="tel" placeholder="09xx xxx xxx"></label>
          <label>Sản phẩm cần tìm
            <select name="product">
              <option>Mũ bảo hiểm</option>
              <option>Ô / dù</option>
              <option>Cốc / ly</option>
              <option>Bình giữ nhiệt</option>
              <option>Bút quà tặng</option>
              <option>Sản phẩm khác</option>
            </select>
          </label>
        </div>
        <div class="form-grid">
          <label>Số lượng dự kiến<input name="quantity" placeholder="Ví dụ: 500 sản phẩm"></label>
          <label>Thời gian cần hàng<input name="deadline" placeholder="Ví dụ: 20/10/2026"></label>
        </div>
        <label>Ghi chú<textarea name="note" rows="3" placeholder="Màu sắc, logo, ngân sách hoặc yêu cầu đặc biệt..."></textarea></label>
        <button class="btn btn-gold btn-lg full" type="submit">Gửi yêu cầu qua email ↗</button>
      </form>
    </div>
  </div>

  <script src="/script.js"></script>
</body>
</html>
"""

published_urls = []

for post in posts_data:
    if post.get('published') is False:
        continue
    
    slug = post['slug']
    title = post.get('title', 'Bài viết')
    summary = post.get('summary', '')
    body = post.get('body', '')
    image = post.get('image', '')
    date_str = post.get('date', '')

    # Normalize image path for web root
    if image and not image.startswith('http'):
        if not image.startswith('/'):
            image_url = '/' + image
        else:
            image_url = image
        full_image_url = SITE_URL + image_url
    elif image.startswith('http'):
        image_url = image
        full_image_url = image
    else:
        image_url = ''
        full_image_url = f"{SITE_URL}/assets/logo-mark.jpg"

    canonical_url = f"{SITE_URL}/bai-viet/{slug}.html"
    published_urls.append((canonical_url, date_str))

    seo_title = f"{title} | Kim Long Gift Đà Nẵng"
    seo_description = html.escape((summary or body[:160]).replace('\n', ' ').strip())

    og_image_tag = f'<meta property="og:image" content="{full_image_url}">' if full_image_url else ''
    twitter_image_tag = f'<meta property="twitter:image" content="{full_image_url}">' if full_image_url else ''

    # Date formatted
    date_html = ""
    iso_date = ""
    if date_str:
        try:
            dt = datetime.strptime(date_str[:16], "%Y-%m-%d %H:%M" if len(date_str) >= 16 else "%Y-%m-%d")
            date_display = dt.strftime("%d/%m/%Y")
            iso_date = dt.isoformat()
            date_html = f'<div class="post-meta-date"><time datetime="{iso_date}">Ngày đăng: {date_display}</time></div>'
        except Exception:
            date_html = f'<div class="post-meta-date"><span>{html.escape(date_str)}</span></div>'

    image_html = f'<div class="post-feature-img"><img src="{image_url}" alt="{html.escape(title)}" loading="lazy"></div>' if image_url else ''
    summary_html = f'<div class="post-lead-summary"><p>{html.escape(summary)}</p></div>' if summary else ''
    body_html = markdown_to_html(body)

    # Schema JSON-LD
    schema_data = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "description": seo_description,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": canonical_url
        },
        "publisher": {
            "@type": "Organization",
            "name": "Kim Long Gift",
            "logo": {
                "@type": "ImageObject",
                "url": f"{SITE_URL}/assets/logo-mark.jpg"
            }
        }
    }
    if full_image_url:
        schema_data["image"] = full_image_url
    if iso_date:
        schema_data["datePublished"] = iso_date
        schema_data["dateModified"] = iso_date

    # Other posts
    other_posts = [p for p in posts_data if p['slug'] != slug and p.get('published') is not False][:3]
    recent_posts_html = ""
    if other_posts:
        cards_html = []
        for op in other_posts:
            op_title = html.escape(op.get('title', ''))
            op_img = op.get('image', '')
            if op_img and not op_img.startswith('http') and not op_img.startswith('/'):
                op_img = '/' + op_img
            img_part = f'<img src="{op_img}" alt="{op_title}">' if op_img else ''
            cards_html.append(f"""
            <a href="/bai-viet/{op['slug']}.html" class="related-post-card">
              {img_part}
              <h4>{op_title}</h4>
            </a>
            """)
        recent_posts_html = f"""
        <section class="related-posts">
          <h3>Bài viết khác</h3>
          <div class="related-posts-grid">
            {''.join(cards_html)}
          </div>
        </section>
        """

    rendered_html = template.format(
        seo_title=html.escape(seo_title),
        seo_description=seo_description,
        canonical_url=canonical_url,
        og_image_tag=og_image_tag,
        twitter_image_tag=twitter_image_tag,
        schema_json=json.dumps(schema_data, ensure_ascii=False, indent=2),
        title_escaped=html.escape(title),
        date_html=date_html,
        image_html=image_html,
        summary_html=summary_html,
        body_html=body_html,
        recent_posts_html=recent_posts_html
    )

    out_file = os.path.join(OUTPUT_DIR, f"{slug}.html")
    with open(out_file, 'w', encoding='utf-8') as out_f:
        out_f.write(rendered_html)

# Generate sitemap.xml
today = datetime.now().strftime("%Y-%m-%d")
sitemap_entries = [
    f"""  <url>
    <loc>{SITE_URL}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>"""
]

for url, date_str in published_urls:
    mod_date = date_str[:10] if date_str and len(date_str) >= 10 else today
    sitemap_entries.append(f"""  <url>
    <loc>{url}</loc>
    <lastmod>{mod_date}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>""")

sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_entries)}
</urlset>
"""
with open("sitemap.xml", "w", encoding="utf-8") as sm:
    sm.write(sitemap_content)

# Generate robots.txt
robots_content = f"""User-agent: *
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
"""
with open("robots.txt", "w", encoding="utf-8") as rb:
    rb.write(robots_content)

print(f"Generated {len(published_urls)} posts, sitemap.xml, and robots.txt successfully!")
