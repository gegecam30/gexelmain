/* JS compartido del sitio Gexel (usado por index.html y plugins.html).
   Cada pieza comprueba que el elemento exista antes de usarlo. */

// ── Partículas flotantes ──
(function () {
  const container = document.getElementById('particles');
  if (!container) return;
  for (let i = 0; i < 40; i++) {
    const p = document.createElement('div');
    p.className = 'particle';
    const big = Math.random() < 0.25;
    p.style.cssText = [
      'left:' + (Math.random() * 100) + '%',
      'bottom:' + (Math.random() * 20) + '%',
      'width:' + (big ? 4 : 2) + 'px',
      'height:' + (big ? 4 : 2) + 'px',
      'animation-duration:' + (6 + Math.random() * 8) + 's',
      'animation-delay:' + (Math.random() * 5) + 's',
    ].join(';');
    container.appendChild(p);
  }
})();

// ── Música de fondo ──
window.GexelAudio = (function () {
  const music = document.getElementById('bg-music');
  const btn = document.getElementById('music-toggle');
  const icon = document.getElementById('music-icon');
  const wrapper = document.querySelector('.music-wrapper');
  const api = { playing: false, mutedManually: false, toggle() {}, startIfAllowed() {} };
  if (!music || !btn) return api;

  music.volume = 0.2;

  const SVG_OFF = '<svg class="ico-off" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 5 6 9H3v6h3l5 4z"/><path d="m22 9-6 6"/><path d="m16 9 6 6"/></svg>';
  const SVG_ON = '<svg class="ico-on" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 5 6 9H3v6h3l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M18.5 5.5a9 9 0 0 1 0 13"/></svg>';
  if (icon) icon.innerHTML = SVG_OFF + SVG_ON;
  function label() {
    btn.setAttribute('aria-label', api.playing ? 'Silenciar música' : 'Activar música');
    btn.setAttribute('aria-pressed', api.playing ? 'true' : 'false');
  }
  label();

  function toggle(forcePlay) {
    if (api.playing && !forcePlay) {
      music.pause();
      if (wrapper) wrapper.classList.remove('is-active');
      api.playing = false;
      api.mutedManually = true;
      label();
    } else {
      music.play().then(() => {
        if (wrapper) wrapper.classList.add('is-active');
        api.playing = true;
        api.mutedManually = false;
        label();
      }).catch(err => console.log('Audio autostart wait:', err));
    }
  }

  btn.addEventListener('click', (e) => { e.stopPropagation(); toggle(); });
  api.toggle = toggle;
  api.startIfAllowed = function () {
    if (!api.playing && !api.mutedManually) toggle(true);
  };
  return api;
})();
