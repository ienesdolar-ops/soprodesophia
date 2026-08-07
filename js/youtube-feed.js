/**
 * YouTube Feed Integration for O Sopro de Sophia
 * Fetches latest videos from the channel RSS feed and renders them as cards.
 */
(function () {
  'use strict';

  const CHANNEL_ID = 'UCDokNUV4IMPnYxKM2izUQ9w';
  const RSS_URL = `https://www.youtube.com/feeds/videos.xml?channel_id=${CHANNEL_ID}`;
  const MAX_VIDEOS = 6;

  // CORS proxies (try in order)
  const CORS_PROXIES = [
    (url) => `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`,
    (url) => `https://corsproxy.io/?${encodeURIComponent(url)}`,
  ];

  const grid = document.getElementById('ytVideosGrid');
  const loading = document.getElementById('ytLoading');

  if (!grid) return;

  /**
   * Try fetching through multiple CORS proxies
   */
  async function fetchWithProxy(url) {
    for (const proxyFn of CORS_PROXIES) {
      try {
        const proxyUrl = proxyFn(url);
        const res = await fetch(proxyUrl);
        if (res.ok) {
          const text = await res.text();
          // Verify we got XML, not an error page
          if (text.includes('<feed') && text.includes('<entry')) {
            return text;
          }
        }
      } catch (e) {
        // try next proxy
      }
    }
    return null;
  }

  /**
   * Parse RSS XML and extract video entries
   * Uses getElementsByTagName which handles XML namespaces properly
   */
  function parseRSS(xmlText) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(xmlText, 'application/xml');

    // Check for parse errors
    if (doc.querySelector('parsererror')) {
      console.warn('YouTube RSS: XML parse error');
      return [];
    }

    // getElementsByTagName works with namespaced elements
    const entries = doc.getElementsByTagName('entry');
    const videos = [];

    for (let i = 0; i < Math.min(entries.length, MAX_VIDEOS); i++) {
      const entry = entries[i];

      // Extract videoId (yt:videoId)
      const videoIdEl = entry.getElementsByTagName('yt:videoId')[0];
      let videoId = videoIdEl ? videoIdEl.textContent : '';

      // Fallback: extract from <id> tag
      if (!videoId) {
        const idEl = entry.getElementsByTagName('id')[0];
        if (idEl) {
          videoId = idEl.textContent.replace('yt:video:', '');
        }
      }

      if (!videoId) continue;

      // Extract title
      const titleEl = entry.getElementsByTagName('title')[0];
      const title = titleEl ? titleEl.textContent : '';

      // Extract published date
      const pubEl = entry.getElementsByTagName('published')[0];
      const published = pubEl ? pubEl.textContent : '';

      // Extract thumbnail (media:thumbnail)
      const thumbEl = entry.getElementsByTagName('media:thumbnail')[0];
      const thumbnail = thumbEl
        ? thumbEl.getAttribute('url')
        : `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`;

      videos.push({ videoId, title, published, thumbnail });
    }

    return videos;
  }

  /**
   * Format date nicely
   */
  function formatDate(dateStr) {
    try {
      const d = new Date(dateStr);
      return d.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
      });
    } catch {
      return '';
    }
  }

  /**
   * Build video card HTML
   */
  function buildVideoCard(video) {
    const card = document.createElement('div');
    card.className = 'yt-video-card';

    card.innerHTML = `
      <a href="https://www.youtube.com/watch?v=${video.videoId}" target="_blank" rel="noopener" class="yt-video-thumb">
        <img src="${video.thumbnail}" alt="${video.title}" loading="lazy">
        <div class="yt-play-overlay">
          <svg class="yt-play-btn" viewBox="0 0 68 48" width="68" height="48">
            <path class="yt-play-bg" d="M66.52 7.74c-.78-2.93-2.49-5.41-5.42-6.19C55.79 0 34 0 34 0S12.21 0 6.9 1.55c-2.93.78-4.63 3.26-5.42 6.19C0 13.05 0 24 0 24s0 10.95 1.48 16.26c.78 2.93 2.49 5.41 5.42 6.19C12.21 48 34 48 34 48s21.79 0 27.1-1.55c2.93-.78 4.64-3.26 5.42-6.19C68 34.95 68 24 68 24s0-10.95-1.48-16.26z" fill="#FF0000"/>
            <path d="M45 24 27 14v20" fill="#fff"/>
          </svg>
        </div>
      </a>
      <div class="yt-video-meta">
        <h4 class="yt-video-title">${video.title}</h4>
        <span class="yt-video-date">${formatDate(video.published)}</span>
      </div>
    `;

    return card;
  }

  /**
   * Render fallback with hardcoded recent videos if RSS fails
   */
  function renderFallback() {
    if (loading) loading.remove();

    const fallbackVideos = [
      { videoId: 'IWlbZiH05qk', title: 'Sophia para Crianças - Episódio 03: Aham Mukti', published: '2026-08-01', thumbnail: 'https://i.ytimg.com/vi/IWlbZiH05qk/hqdefault.jpg' },
      { videoId: 'w4O0t7ahFME', title: 'Sophia para Crianças - Episódio 02: O Véu das Lágrimas', published: '2026-07-25', thumbnail: 'https://i.ytimg.com/vi/w4O0t7ahFME/hqdefault.jpg' },
      { videoId: 'wS0APVVVuS0', title: 'Textos de Sophia', published: '2026-07-22', thumbnail: 'https://i.ytimg.com/vi/wS0APVVVuS0/hqdefault.jpg' },
      { videoId: 'N7Dig3Q3Vp4', title: 'Livros de Sophia', published: '2026-07-21', thumbnail: 'https://i.ytimg.com/vi/N7Dig3Q3Vp4/hqdefault.jpg' },
      { videoId: 'do-uBkjnjcM', title: '18 de julho de 2026', published: '2026-07-18', thumbnail: 'https://i.ytimg.com/vi/do-uBkjnjcM/hqdefault.jpg' },
      { videoId: '0lDLCPahkv8', title: 'Episódio 15 - Você é a Chave e a Porta', published: '2026-07-18', thumbnail: 'https://i.ytimg.com/vi/0lDLCPahkv8/hqdefault.jpg' },
    ];

    fallbackVideos.forEach((video) => {
      grid.appendChild(buildVideoCard(video));
    });
  }

  /**
   * Main: fetch and render
   */
  async function init() {
    const xmlText = await fetchWithProxy(RSS_URL);

    if (!xmlText) {
      renderFallback();
      return;
    }

    const videos = parseRSS(xmlText);

    if (videos.length === 0) {
      renderFallback();
      return;
    }

    // Remove loading spinner
    if (loading) loading.remove();

    // Render video cards
    videos.forEach((video) => {
      grid.appendChild(buildVideoCard(video));
    });
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
