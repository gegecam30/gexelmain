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

  function toggle(forcePlay) {
    if (api.playing && !forcePlay) {
      music.pause();
      if (icon) icon.textContent = '🔇';
      if (wrapper) wrapper.classList.remove('is-active');
      api.playing = false;
      api.mutedManually = true;
    } else {
      music.play().then(() => {
        if (icon) icon.textContent = '🔊';
        if (wrapper) wrapper.classList.add('is-active');
        api.playing = true;
        api.mutedManually = false;
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
