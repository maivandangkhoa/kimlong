const menu=document.querySelector('.menu-toggle'),nav=document.querySelector('#nav');if(menu){menu.addEventListener('click',()=>{const open=nav.classList.toggle('open');menu.setAttribute('aria-expanded',open)})}document.querySelectorAll('#nav a').forEach(a=>a.addEventListener('click',()=>nav.classList.remove('open')));const modal=document.querySelector('#quoteModal');const openModal=()=>{modal.classList.add('open');modal.setAttribute('aria-hidden','false');document.body.style.overflow='hidden'};const closeModal=()=>{modal.classList.remove('open');modal.setAttribute('aria-hidden','true');document.body.style.overflow=''};document.querySelectorAll('[data-open-quote]').forEach(b=>b.addEventListener('click',openModal));document.querySelectorAll('[data-close-quote]').forEach(b=>b.addEventListener('click',closeModal));document.addEventListener('keydown',e=>{if(e.key==='Escape'&&modal.classList.contains('open'))closeModal()});const form=document.querySelector('#quoteForm');form.addEventListener('submit',e=>{e.preventDefault();const d=new FormData(form);const subject=encodeURIComponent(`Yêu cầu báo giá - ${d.get('product')}`);const body=encodeURIComponent(`Họ tên: ${d.get('name')}\nCông ty: ${d.get('company')||'—'}\nSố điện thoại: ${d.get('phone')}\nSản phẩm: ${d.get('product')}\nSố lượng: ${d.get('quantity')||'—'}\nThời gian cần hàng: ${d.get('deadline')||'—'}\nGhi chú: ${d.get('note')||'—'}`);window.location.href=`mailto:kimlonggift@gmail.com?subject=${subject}&body=${body}`});const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('visible');observer.unobserve(entry.target)}}),{threshold:.12});document.querySelectorAll('.reveal').forEach(el=>observer.observe(el));


// Decap CMS Posts Loader
async function loadPosts() {
  const container = document.getElementById('newsList');
  if (!container) return;

  try {
    const listRes = await fetch('content/posts.json');
    if (!listRes.ok) {
      container.innerHTML = '<p style="text-align:center; color:#64748b; grid-column: 1 / -1;">Chưa có bài viết nào được đăng tải.</p>';
      return;
    }
    const postFiles = await listRes.json();
    if (!Array.isArray(postFiles) || postFiles.length === 0) {
      container.innerHTML = '<p style="text-align:center; color:#64748b; grid-column: 1 / -1;">Chưa có bài viết nào được đăng tải.</p>';
      return;
    }

    const posts = [];
    for (const file of postFiles) {
      try {
        const res = await fetch('content/posts/' + file);
        if (res.ok) {
          const data = await res.json();
          if (data.published !== false) {
            posts.push({ ...data, slug: file.replace('.json', '') });
          }
        }
      } catch (err) {
        console.warn('Lỗi đọc bài viết:', file, err);
      }
    }

    posts.sort((a, b) => new Date(b.date || 0) - new Date(a.date || 0));

    if (posts.length === 0) {
      container.innerHTML = '<p style="text-align:center; color:#64748b; grid-column: 1 / -1;">Chưa có bài viết nào được đăng tải.</p>';
      return;
    }

    window._loadedPosts = posts;

    container.innerHTML = posts.map((post, idx) => {
      const imgHtml = post.image ? `<img src="${post.image}" alt="${post.title}" class="news-card-img" loading="lazy">` : '';
      const dateDisplay = post.date ? new Date(post.date).toLocaleDateString('vi-VN', { year: 'numeric', month: 'short', day: 'numeric' }) : '';
      return `
        <article class="news-card reveal visible">
          ${imgHtml}
          <div class="news-card-body">
            ${dateDisplay ? `<div class="news-date">${dateDisplay}</div>` : ''}
            <h3 class="news-title">${post.title}</h3>
            <p class="news-summary">${post.summary || ''}</p>
            <button class="news-btn" type="button" onclick="viewPostByIndex(${idx})">Xem chi tiết &rarr;</button>
          </div>
        </article>
      `;
    }).join('');

  } catch (e) {
    console.error('Lỗi nạp danh sách bài viết:', e);
  }
}

window.viewPostByIndex = function(idx) {
  const post = window._loadedPosts && window._loadedPosts[idx];
  if (!post) return;

  let modalEl = document.getElementById('postDetailModal');
  if (!modalEl) {
    modalEl = document.createElement('div');
    modalEl.id = 'postDetailModal';
    modalEl.className = 'modal';
    modalEl.setAttribute('aria-hidden', 'true');
    modalEl.innerHTML = `
      <div class="modal-backdrop" onclick="closePostDetails()"></div>
      <div class="modal-panel post-detail-modal">
        <button class="modal-close" onclick="closePostDetails()" aria-label="Đóng">&times;</button>
        <div id="postModalContent"></div>
      </div>
    `;
    document.body.appendChild(modalEl);
  }

  const contentEl = document.getElementById('postModalContent');
  const dateDisplay = post.date ? new Date(post.date).toLocaleDateString('vi-VN', { year: 'numeric', month: 'long', day: 'numeric' }) : '';
  contentEl.innerHTML = `
    ${dateDisplay ? `<span class="section-kicker">${dateDisplay}</span>` : ''}
    <h2>${post.title}</h2>
    ${post.image ? `<img src="${post.image}" alt="${post.title}" style="width:100%; border-radius:8px; margin: 16px 0; max-height:400px; object-fit:cover;">` : ''}
    <div class="post-detail-content">${post.body || ''}</div>
  `;

  modalEl.classList.add('open');
  modalEl.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
};

window.closePostDetails = function() {
  const modalEl = document.getElementById('postDetailModal');
  if (modalEl) {
    modalEl.classList.remove('open');
    modalEl.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }
};

document.addEventListener('DOMContentLoaded', loadPosts);
