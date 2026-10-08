// One audio engine per browser tab, independent of question reruns.
export default function(component) {
  const {parentElement, data} = component;
  let engine = window.__addmathStudyMusic;
  if (!engine) {
    const audio = new Audio(new URL('app/static/study_music.mp3', window.location.href).href);
    audio.loop = true;
    audio.autoplay = true;
    audio.preload = 'auto';
    audio.volume = 0.05;
    engine = {audio, userPaused:false, blocked:false, active:false};
    window.__addmathStudyMusic = engine;
  }
  const audio = engine.audio;
  const play = parentElement.querySelector('[data-play]');
  const volume = parentElement.querySelector('[data-volume]');
  const status = parentElement.querySelector('[data-status]');
  const heading = parentElement.querySelector('[data-heading]');
  const volumeLabel = parentElement.querySelector('[data-volume-label]');
  let disposed = false;
  function label(en,bm) {
    return data.language === 'English' ? en : data.language === 'Bahasa Melayu' ? bm : en+' / '+bm;
  }
  heading.textContent = label('Study music','Muzik belajar');
  volumeLabel.textContent = label('Volume','Kelantangan');
  function update() {
    if (disposed) return;
    play.textContent = audio.paused ? label('▶ Play','▶ Main') : label('Ⅱ Pause','Ⅱ Jeda');
    play.disabled = !engine.active;
    volume.value = String(audio.volume);
    status.textContent = !engine.active ? label('Paused in Teacher view.','Dijeda dalam paparan Guru.') :
      engine.blocked ? label('Tap Play to allow sound.','Tekan Main untuk membenarkan bunyi.') :
      label('Loops continuously · starts at 5% volume','Berulang berterusan · bermula pada kelantangan 5%');
  }
  async function tryPlay() {
    if (!engine.active || engine.userPaused) return;
    try {await audio.play(); engine.blocked=false;}
    catch (error) {engine.blocked=true;}
    update();
  }
  // Data changes and widget reruns never reload the source or reset currentTime.
  const wasActive = engine.active;
  engine.active = data.active;
  if (!engine.active) audio.pause();
  else if (!wasActive && !engine.userPaused) tryPlay();
  play.onclick = () => {
    if (audio.paused) {engine.userPaused=false; tryPlay();}
    else {engine.userPaused=true; audio.pause(); update();}
  };
  volume.oninput = () => {audio.volume=Number(volume.value); update();};
  const gesture = () => {
    if (audio.paused && !engine.userPaused && engine.active) tryPlay();
  };
  // A click on Start or another app control can unlock browser audio permissions.
  document.addEventListener('pointerdown',gesture,true);
  document.addEventListener('keydown',gesture,true);
  audio.addEventListener('play',update);
  audio.addEventListener('pause',update);
  audio.addEventListener('volumechange',update);
  const failed = () => {
    if (!disposed) status.textContent=label('Music unavailable. Check static/study_music.mp3 and static serving.','Muzik tidak tersedia. Semak static/study_music.mp3 dan penyajian statik.');
  };
  audio.addEventListener('error',failed);
  update();
  return () => {
    disposed=true;
    document.removeEventListener('pointerdown',gesture,true);
    document.removeEventListener('keydown',gesture,true);
    audio.removeEventListener('play',update);
    audio.removeEventListener('pause',update);
    audio.removeEventListener('volumechange',update);
    audio.removeEventListener('error',failed);
    // Keep the shared audio engine playing through Streamlit rerenders.
  };
}
