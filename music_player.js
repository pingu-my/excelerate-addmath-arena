// One audio engine per browser tab, independent of question reruns.
export default function(component) {
  const {parentElement, data, setStateValue} = component;
  let engine = window.__addmathStudyMusic;
  if (data.source && (!engine || engine.trackId !== data.track_id)) {
    const previous=engine;
    if (previous) previous.audio.pause();
    const audio = new Audio(data.source);
    audio.loop = true;
    audio.autoplay = true;
    audio.preload = 'auto';
    audio.volume = previous ? previous.audio.volume : 0.05;
    engine = {audio, trackId:data.track_id, userPaused:previous ? previous.userPaused : false, blocked:false, active:false, failed:false};
    window.__addmathStudyMusic = engine;
  }
  if (!engine) {
    // A reconnected page may retain Python's acknowledgement but lose its Audio.
    setStateValue('loaded','');
    const message=parentElement.querySelector('[data-status]');
    message.textContent='Music is loading. / Muzik sedang dimuatkan.';
    return;
  }
  if (data.source) setStateValue('loaded',data.track_id);
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
      engine.failed ? label('The audio could not be decoded. Reload the page or check the MP3.','Audio tidak dapat dinyahkod. Muat semula halaman atau semak MP3.') :
      engine.blocked ? label('Tap Play to allow sound.','Tekan Main untuk membenarkan bunyi.') :
      label('Loops continuously · starts at 5% volume','Berulang berterusan · bermula pada kelantangan 5%');
  }
  async function tryPlay() {
    if (!engine.active || engine.userPaused) return;
    try {await audio.play(); engine.blocked=false;}
    catch (error) {engine.failed=error.name==='NotSupportedError';engine.blocked=!engine.failed;}
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
  const gesture = (event) => {
    // Do not auto-start on this player's controls: pointerdown happens before
    // click, and could otherwise turn a Play click into an immediate Pause.
    const path=event?.composedPath?.() || [];
    if (path.includes(play) || path.includes(volume) || path.includes(parentElement)) return;
    if (audio.paused && !engine.userPaused && engine.active) tryPlay();
  };
  // A click on Start or another app control can unlock browser audio permissions.
  document.addEventListener('pointerdown',gesture,true);
  document.addEventListener('keydown',gesture,true);
  audio.addEventListener('play',update);
  audio.addEventListener('pause',update);
  audio.addEventListener('volumechange',update);
  const failed = () => {
    engine.failed=true;
    update();
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
