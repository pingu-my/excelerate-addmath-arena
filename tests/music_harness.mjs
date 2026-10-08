import assert from 'node:assert/strict';
import player from '../music_player.js';
let count=0, allowed=false;
class AudioMock {
  constructor(src) {this.src=src;this.paused=true;this.currentTime=0;this.events=new Map();count++;}
  async play() {if(!allowed) throw Error('Autoplay blocked');this.paused=false;this.emit('play');}
  pause() {this.paused=true;this.emit('pause');}
  addEventListener(type, fn) {if(!this.events.has(type))this.events.set(type,new Set());this.events.get(type).add(fn);}
  removeEventListener(type, fn) {this.events.get(type)?.delete(fn);}
  emit(type) {for(const fn of this.events.get(type)||[])fn();}
}
globalThis.Audio=AudioMock;
globalThis.window={location:{href:'https://example.com/'}};
const listeners=new Map();
globalThis.document={
  addEventListener(type,fn){if(!listeners.has(type))listeners.set(type,new Set());listeners.get(type).add(fn);},
  removeEventListener(type,fn){listeners.get(type)?.delete(fn);},
};
function mount(language='English',active=true) {
  const elements=Object.fromEntries(['play','volume','status','heading','volume-label'].map(k=>[k,{}]));
  const cleanup=player({data:{language,active},parentElement:{querySelector:s=>elements[s.slice(6,-1)]}});
  return {elements,cleanup};
}
const flush=async()=>{await Promise.resolve();await Promise.resolve();};
let view=mount();await flush();
const engine=window.__addmathStudyMusic;
assert.equal(engine.audio.volume,.05);assert.equal(engine.audio.loop,true);assert.equal(engine.audio.autoplay,true);
assert.equal(engine.audio.src,'https://example.com/app/static/study_music.mp3');
assert.match(view.elements.status.textContent,/Tap Play/);
allowed=true;
for(const fn of listeners.get('pointerdown'))fn();await flush();
assert.equal(engine.audio.paused,false);
engine.audio.currentTime=42;view.cleanup();view=mount('Bahasa Melayu');await flush();
assert.equal(count,1);assert.equal(engine.audio.currentTime,42);assert.equal(engine.audio.paused,false);
assert.equal(listeners.get('pointerdown').size,1);assert.match(view.elements.heading.textContent,/Muzik/);
view.elements.play.onclick();assert.equal(engine.audio.paused,true);assert.equal(engine.userPaused,true);
view.cleanup();view=mount();await flush();
for(const fn of listeners.get('pointerdown'))fn();await flush();assert.equal(engine.audio.paused,true);
view.elements.play.onclick();await flush();assert.equal(engine.audio.paused,false);
view.elements.volume.value='.02';view.elements.volume.oninput();assert.equal(engine.audio.volume,.02);
view.cleanup();view=mount('English',false);assert.equal(engine.audio.paused,true);
view.cleanup();view=mount('English',true);await flush();assert.equal(engine.audio.paused,false);
assert.equal(engine.audio.volume,.02);assert.equal(engine.audio.currentTime,42);assert.equal(count,1);
view.cleanup();assert.equal(listeners.get('pointerdown').size,0);
console.log('Music lifecycle: autoplay fallback, looping, low volume, reruns, pause and navigation passed.');
