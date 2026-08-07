/**
 * YouTube Feed Integration for O Sopro de Sophia
 * Fetches latest videos from the channel RSS feed and renders them as embed cards.
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
          return await res.text();
        }
      } catch (e) {
        // try next proxy
      }
    }
    return null;
  }

  /**
   * Parse RSS XML and extract video entries
   */
  function parseRSS(xmlText) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(xmlText, 'application/xml');
    const entries = doc.querySelectorAll('entry');
    const videos = [];

    entries.forEach((entry, i) => {
      if (i >= MAX_VIDEOS) return;

      const videoId =
        entry.querySelector('videoId')?.textContent ||
        entry.querySelector('id')?.textContent?.replace('yt:video:', '') ||
        '';

      const title = entry.querySelector('title')?.textContent || '';

      const published = entry.querySelector('published')?.textContent || '';

      const thumbnail =
        entry.querySelector('thumbnail')?.getAttribute('url') ||
        `https://i.ytimg.com/vi/${videoId}/hqdefault.jpg`;

      const description =
        entry.querySelector('description')?.textContent || '';

      videos.push({ videoId, title, published, thumbnail, description });
    });

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
      <div class="yt-video-thumb" data-video-id="${video.videoId}">
        <img src="${video.thumbnail}" alt="${video.title}" loading="lazy">
        <div class="yt-play-overlay">
          <svg class="yt-play-btn" viewBox="0 0 68 48" width="68" height="48">
            <path class="yt-play-bg" d="M66.52 7.74c-.78-2.93-2.49-5.41-5.42-6.19C55.79 0 34 0 34 0S12.21 0 6.9 1.55c-2.93.78-4.63 3.26-5.42 6.19C0 13.05 0 24 0 24s0 10.95 1.48 16.26c.78 2.93 2.49 5.41 5.42 6.19C12.21 48 34 48 34 48s21.79 0 27.1-1.55c2.93-.78 4.64-3.26 5.42-6.19C68 34.95 68 24 68 24s0-10.95-1.48-16.26z" fill="#FF0000"/>
            <path d="M45 24 27 14v20" fill="#fff"/>
          </svg>
        </div>
      </div>
      <div class="yt-video-meta">
        <h4 class="yt-video-title">${video.title}</h4>
        <span class="yt-video-date">${formatDate(video.published)}</span>
      </div>
    `;

    // Click to replace thumbnail with embedded player
    const thumb = card.querySelector('.yt-video-thumb');
    thumb.addEventListener('click', () => {
      const iframe = document.createElement('iframe');
      iframe.src = `https://www.youtube.com/embed/${video.videoId}?autoplay=1&rel=0`;
      iframe.allow =
        'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
      iframe.allowFullscreen = true;
      iframe.className = 'yt-video-iframe';
      thumb.replaceWith(iframe);
    });

    return card;
  }

  /**
   * Render fallback (static embeds) if RSS fails
   */
  function renderFallback() {
    // Fallback: embed the channel's uploads playlist
    if (loading) loading.remove();

    grid.innerHTML = `
      <div class="yt-video-card yt-video-card--wide">
        <iframe
          class="yt-video-iframe"
          src="https://www.youtube.com/embed/videoseries?list=UUDokNUV4IMPnYxKM2izUQ9w&rel=0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen>
        </iframe>
      </div>
    `;
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
