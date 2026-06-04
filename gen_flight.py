#!/usr/bin/env python3
"""
Flight GMP-2028 — Immersive 3D Portfolio Generator
Three.js · GSAP · WebGL · Anas El Hiss · BUT GMP SNRV
"""
import random

# ══════════════════════════════════════════════════════════
# STEP 1 — Extract preserved JS content from previous build
# ══════════════════════════════════════════════════════════
with open('/home/user/Portfolio/index.html','r',encoding='utf-8') as f:
    old = f.read()

img_s = old.index('const IMG')
img_e = old.index('\n};', img_s) + 3
IMG_BLOCK = old[img_s:img_e]

def between(src, n1, n2):
    s = src.index(f'function {n1}')
    e = src.index(f'function {n2}')
    return src[s:e].rstrip()

SAE13_FN    = between(old, 'buildSae13Extra',    'buildSae204Extra')
SAE204_FN   = between(old, 'buildSae204Extra',   'buildFonderieExtra')
FONDERIE_FN = between(old, 'buildFonderieExtra', 'openModal')

print(f"IMG={len(IMG_BLOCK)} | sae13={len(SAE13_FN)} | sae204={len(SAE204_FN)} | fonderie={len(FONDERIE_FN)}")

# ══════════════════════════════════════════════════════════
# STEP 2 — CSS
# ══════════════════════════════════════════════════════════
CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --night:   #081120;
  --sky:     #0f2747;
  --route:   #58c6ff;
  --gold:    #ffb84d;
  --cloud:   #f5f8ff;
  --glass:   rgba(8,17,32,0.75);
  --border:  rgba(88,198,255,0.18);
  --text:    #e8f4ff;
  --muted:   #6a8fab;
}

html { scroll-behavior: smooth; }

body {
  background: var(--night);
  color: var(--text);
  font-family: 'DM Sans', sans-serif;
  overflow-x: hidden;
}

/* ─── SCROLL DRIVER (tall container behind fixed canvas) ─── */
#scroll-driver {
  position: relative;
  z-index: 0;
  height: 700vh;
  pointer-events: none;
}

/* ─── THREE.JS CANVAS ─── */
#three-canvas {
  position: fixed;
  inset: 0;
  z-index: 0;
  width: 100%;
  height: 100%;
}

/* ─── SECTIONS LAYER ─── */
#sections {
  position: fixed;
  inset: 0;
  z-index: 10;
  pointer-events: none;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 4vw;
}

.panel {
  pointer-events: all;
  width: min(520px, 90vw);
  background: var(--glass);
  backdrop-filter: blur(20px) saturate(1.4);
  border: 1px solid var(--border);
  border-radius: 24px;
  padding: 2.5rem;
  opacity: 0;
  transform: translateX(60px);
  transition: opacity 0.6s cubic-bezier(.4,0,.2,1), transform 0.6s cubic-bezier(.4,0,.2,1);
  max-height: 85vh;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(88,198,255,0.3) transparent;
}

.panel.visible { opacity: 1; transform: none; }

.panel-badge {
  display: inline-flex; align-items: center; gap: 0.6rem;
  background: rgba(88,198,255,0.1);
  border: 1px solid rgba(88,198,255,0.25);
  border-radius: 8px; padding: 0.35rem 0.9rem;
  font-family: 'Share Tech Mono', monospace;
  font-size: 0.7rem; letter-spacing: 0.18em;
  color: var(--route); margin-bottom: 1.2rem;
}

.panel h2 {
  font-family: 'Syne', sans-serif;
  font-weight: 800; font-size: clamp(1.4rem, 3vw, 2rem);
  line-height: 1.15; margin-bottom: 0.4rem;
}
.panel h2 span {
  background: linear-gradient(135deg, var(--route), var(--gold));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}

.panel-divider {
  height: 2px; width: 50px; margin: 0.8rem 0 1.5rem;
  background: linear-gradient(90deg, var(--route), var(--gold));
  border-radius: 2px;
}

/* ─── HUD ─── */
#hud {
  position: fixed; top: 0; left: 0; right: 0; z-index: 20;
  padding: 1.2rem 2rem;
  display: flex; align-items: center; justify-content: space-between;
  background: linear-gradient(180deg, rgba(8,17,32,0.85) 0%, transparent 100%);
  opacity: 0; pointer-events: none;
  transition: opacity 0.6s;
}
#hud.visible { opacity: 1; pointer-events: all; }
.hud-brand {
  font-family: 'Share Tech Mono', monospace; font-size: 0.8rem;
  letter-spacing: 0.2em; color: var(--route);
}
.hud-stats {
  display: flex; gap: 2rem;
  font-family: 'Share Tech Mono', monospace; font-size: 0.72rem;
  color: var(--muted);
}
.hud-stat span { color: var(--route); font-size: 0.85rem; margin-left: 0.3rem; }
.hud-nav { display: flex; gap: 1.2rem; }
.hud-nav a {
  font-family: 'Share Tech Mono', monospace; font-size: 0.65rem;
  letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--muted); text-decoration: none; transition: color 0.2s;
}
.hud-nav a:hover { color: var(--route); }

/* ─── INTRO OVERLAY ─── */
#intro {
  position: fixed; inset: 0; z-index: 100;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  pointer-events: none;
  text-align: center;
}
.intro-flight-number {
  font-family: 'Share Tech Mono', monospace; font-size: 0.8rem;
  letter-spacing: 0.3em; color: var(--route); margin-bottom: 1.5rem;
  opacity: 0;
}
.intro-title {
  font-family: 'Syne', sans-serif; font-weight: 800;
  font-size: clamp(3rem, 8vw, 6rem); line-height: 1;
  letter-spacing: -0.02em; margin-bottom: 0.5rem;
  opacity: 0;
  background: linear-gradient(135deg, #fff 30%, var(--route) 60%, var(--gold));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.intro-subtitle {
  font-size: clamp(0.9rem, 2vw, 1.15rem); color: var(--muted);
  letter-spacing: 0.05em; margin-bottom: 0.5rem; opacity: 0;
}
.intro-dest {
  display: flex; align-items: center; gap: 1rem;
  margin: 1.5rem 0 2.5rem; opacity: 0;
}
.intro-dest-city {
  font-family: 'Share Tech Mono', monospace; font-size: 1.5rem;
  color: var(--route); line-height: 1;
}
.intro-dest-sub { font-size: 0.65rem; color: var(--muted); margin-top: 0.2rem; }
.intro-dest-arrow {
  font-size: 1.5rem; color: var(--gold);
  animation: pulse 1.5s ease-in-out infinite;
}
@keyframes pulse { 0%,100%{opacity:0.5} 50%{opacity:1} }

.btn-board {
  pointer-events: all; cursor: pointer;
  padding: 1rem 2.5rem; border-radius: 50px;
  background: linear-gradient(135deg, var(--route), #2a7aff);
  color: #fff; font-family: 'Syne', sans-serif;
  font-weight: 700; font-size: 1rem; letter-spacing: 0.05em;
  border: none; opacity: 0;
  box-shadow: 0 0 40px rgba(88,198,255,0.4);
  transition: transform 0.2s, box-shadow 0.2s;
}
.btn-board:hover {
  transform: translateY(-3px) scale(1.03);
  box-shadow: 0 0 60px rgba(88,198,255,0.6);
}

/* ─── SCROLL PROGRESS ─── */
#scroll-progress {
  position: fixed; bottom: 2rem; left: 50%; transform: translateX(-50%);
  z-index: 20; display: flex; align-items: center; gap: 0.75rem;
  opacity: 0; transition: opacity 0.6s;
  pointer-events: none;
}
#scroll-progress.visible { opacity: 1; }
.scroll-bar {
  width: 140px; height: 2px; background: rgba(88,198,255,0.2);
  border-radius: 2px; overflow: hidden;
}
.scroll-fill { height: 100%; background: var(--route); width: 0%; transition: width 0.1s; }
.scroll-pct {
  font-family: 'Share Tech Mono', monospace; font-size: 0.65rem;
  color: var(--route); letter-spacing: 0.1em;
}

/* ─── PASSPORT ─── */
.passport {
  background: linear-gradient(135deg, #1a0a3e, #0d1b4a);
  border: 1px solid rgba(88,198,255,0.3);
  border-radius: 12px; padding: 1.8rem;
  margin-bottom: 1.2rem;
}
.passport-header {
  display: flex; align-items: center; gap: 1rem; margin-bottom: 1.2rem;
}
.passport-avatar {
  width: 56px; height: 56px; border-radius: 10px;
  background: linear-gradient(135deg, var(--route), #2a7aff);
  display: flex; align-items: center; justify-content: center;
  font-family: 'Syne', sans-serif; font-weight: 800;
  font-size: 1.5rem; color: #fff;
  box-shadow: 0 0 20px rgba(88,198,255,0.4);
}
.passport-info-row {
  display: flex; gap: 0.75rem; align-items: flex-start; margin-bottom: 0.8rem;
  font-size: 0.85rem;
}
.passport-key {
  font-family: 'Share Tech Mono', monospace; font-size: 0.62rem;
  color: var(--muted); letter-spacing: 0.1em; width: 80px; flex-shrink: 0;
  padding-top: 0.15rem;
}
.passport-val { color: var(--text); font-weight: 500; }
.passport-mrz {
  margin-top: 1.2rem; padding-top: 1rem; border-top: 1px solid rgba(88,198,255,0.15);
  font-family: 'Share Tech Mono', monospace; font-size: 0.6rem;
  color: rgba(88,198,255,0.4); letter-spacing: 0.05em; line-height: 1.6;
}
.visa-stamp {
  display: inline-flex; flex-direction: column; align-items: center;
  border: 2px solid rgba(88,198,255,0.5); border-radius: 50%;
  width: 90px; height: 90px; justify-content: center;
  transform: rotate(-15deg); float: right; margin: -0.5rem 0 1rem 1rem;
  color: var(--route); font-family: 'Share Tech Mono', monospace;
  font-size: 0.55rem; letter-spacing: 0.08em; text-align: center;
  box-shadow: 0 0 15px rgba(88,198,255,0.2);
  animation: stampAppear 0.5s 0.8s both;
}
@keyframes stampAppear {
  from { transform: rotate(-15deg) scale(3); opacity: 0; }
  to   { transform: rotate(-15deg) scale(1); opacity: 1; }
}
.visa-stamp .vs-approved { font-size: 0.72rem; font-weight: 700; color: var(--gold); }

/* ─── SKILLS / BAGGAGE ─── */
.bag-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.9rem; }
.bag-item {
  background: rgba(88,198,255,0.06);
  border: 1px solid rgba(88,198,255,0.15);
  border-radius: 14px; padding: 1.1rem;
  cursor: pointer; transition: all 0.25s;
}
.bag-item:hover { background: rgba(88,198,255,0.12); transform: translateY(-2px); }
.bag-icon { font-size: 1.5rem; margin-bottom: 0.5rem; }
.bag-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.85rem; margin-bottom: 0.5rem; }
.bag-bar { height: 4px; background: rgba(255,255,255,0.08); border-radius: 2px; overflow: hidden; margin-top: 0.6rem; }
.bag-fill { height: 100%; border-radius: 2px; transition: width 1.2s cubic-bezier(.4,0,.2,1); width: 0%; }

/* ─── BOARDING PASS ─── */
.bp-list { display: flex; flex-direction: column; gap: 0.9rem; }
.bp-card {
  background: linear-gradient(135deg, rgba(15,39,71,0.9), rgba(8,17,32,0.9));
  border: 1px solid rgba(88,198,255,0.2); border-radius: 14px;
  padding: 1.1rem 1.3rem; cursor: pointer; transition: all 0.25s;
  position: relative; overflow: hidden;
}
.bp-card::before {
  content: ''; position: absolute;
  left: -1px; top: 20%; bottom: 20%;
  width: 3px; border-radius: 0 3px 3px 0;
  background: linear-gradient(180deg, var(--route), var(--gold));
}
.bp-card:hover { border-color: rgba(88,198,255,0.4); transform: translateX(-3px); }
.bp-card-top {
  display: flex; justify-content: space-between; align-items: flex-start;
  margin-bottom: 0.6rem;
}
.bp-flight-num {
  font-family: 'Share Tech Mono', monospace; font-size: 0.72rem;
  color: var(--route); letter-spacing: 0.1em;
}
.bp-ue-tag {
  font-size: 0.6rem; padding: 0.15rem 0.5rem; border-radius: 5px;
  font-family: 'Share Tech Mono', monospace; letter-spacing: 0.04em;
}
.bp-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.88rem; margin-bottom: 0.3rem; }
.bp-desc { font-size: 0.75rem; color: var(--muted); line-height: 1.5; }
.bp-res { display: flex; flex-wrap: wrap; gap: 0.3rem; margin-top: 0.6rem; }
.bp-res-chip {
  font-size: 0.6rem; padding: 0.15rem 0.4rem; border-radius: 4px;
  background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
  color: var(--muted);
}

/* ─── TIMELINE ─── */
.tl-item {
  display: flex; gap: 1.2rem; padding: 1rem 0; position: relative;
}
.tl-item:not(:last-child)::after {
  content: ''; position: absolute;
  left: 1.1rem; top: 2.8rem; bottom: -0.5rem;
  width: 1px; background: rgba(88,198,255,0.15);
}
.tl-dot {
  width: 22px; height: 22px; border-radius: 50%; flex-shrink: 0;
  background: var(--night); border: 2px solid var(--route);
  display: flex; align-items: center; justify-content: center;
  font-size: 0.6rem; color: var(--route); margin-top: 0.1rem;
  box-shadow: 0 0 10px rgba(88,198,255,0.3);
}
.tl-year {
  font-family: 'Share Tech Mono', monospace; font-size: 0.65rem;
  color: var(--route); letter-spacing: 0.1em; margin-bottom: 0.25rem;
}
.tl-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.9rem; margin-bottom: 0.2rem; }
.tl-org { font-size: 0.75rem; color: var(--muted); }

/* ─── CONTACT BOARD ─── */
.board-title {
  font-family: 'Share Tech Mono', monospace; font-size: 0.65rem;
  letter-spacing: 0.2em; color: var(--route); margin-bottom: 1rem;
  text-transform: uppercase;
}
.board-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; }
.board-card {
  display: flex; align-items: center; gap: 0.9rem;
  background: rgba(88,198,255,0.06); border: 1px solid rgba(88,198,255,0.12);
  border-radius: 12px; padding: 1rem; text-decoration: none; color: var(--text);
  transition: all 0.22s;
}
.board-card:hover { background: rgba(88,198,255,0.13); border-color: rgba(88,198,255,0.3); transform: translateY(-2px); }
.board-icon {
  width: 36px; height: 36px; border-radius: 9px;
  background: rgba(88,198,255,0.1); display: flex; align-items: center;
  justify-content: center; font-size: 1rem; flex-shrink: 0;
}
.board-label { font-family: 'Share Tech Mono', monospace; font-size: 0.55rem; color: var(--muted); letter-spacing: 0.1em; margin-bottom: 0.2rem; }
.board-val { font-size: 0.8rem; font-weight: 500; }

/* ─── ARRIVAL SCREEN ─── */
#arrival {
  position: fixed; inset: 0; z-index: 50;
  background: rgba(8,17,32,0.96); display: flex;
  flex-direction: column; align-items: center; justify-content: center;
  opacity: 0; pointer-events: none; transition: opacity 1s;
  text-align: center;
}
#arrival.visible { opacity: 1; pointer-events: all; }
.arrival-status {
  font-family: 'Share Tech Mono', monospace; font-size: 0.75rem;
  letter-spacing: 0.3em; color: var(--gold); margin-bottom: 1.5rem;
  animation: blink 2s step-end infinite;
}
@keyframes blink { 50% { opacity: 0.3; } }
.arrival-title {
  font-family: 'Syne', sans-serif; font-weight: 800;
  font-size: clamp(2rem,5vw,4rem); margin-bottom: 0.75rem;
  background: linear-gradient(135deg, #fff, var(--route), var(--gold));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  background-clip: text;
}
.arrival-sub { font-size: 1rem; color: var(--muted); max-width: 450px; margin: 0 auto 2.5rem; line-height: 1.7; }

/* ─── MODAL ─── */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.88);
  z-index: 200; display: flex; align-items: center; justify-content: center;
  padding: 1.5rem; opacity: 0; pointer-events: none; transition: opacity 0.25s;
}
.modal-overlay.open { opacity: 1; pointer-events: all; }
.modal-box {
  background: #0a1628; border: 1px solid rgba(88,198,255,0.2);
  border-radius: 24px; width: 100%; max-width: 780px;
  max-height: 90vh; overflow-y: auto; position: relative;
  transform: translateY(20px); transition: transform 0.25s;
}
.modal-overlay.open .modal-box { transform: none; }
.modal-header {
  padding: 2rem 2rem 1.5rem; border-bottom: 1px solid rgba(88,198,255,0.12);
  position: sticky; top: 0; background: #0a1628; z-index: 1;
}
.modal-body { padding: 2rem; }
.modal-section { margin-bottom: 2rem; }
.modal-section-label {
  font-family: 'Share Tech Mono', monospace; font-size: 0.68rem;
  letter-spacing: 0.15em; color: var(--route); text-transform: uppercase; margin-bottom: 0.75rem;
}
.modal-text { font-size: 0.88rem; color: var(--muted); line-height: 1.7; }
.m-close {
  position: absolute; top: 1.2rem; right: 1.5rem;
  background: none; border: 1px solid rgba(88,198,255,0.2); border-radius: 8px;
  color: var(--muted); cursor: pointer; padding: 0.4rem 0.7rem; font-size: 1rem; transition: all 0.2s;
}
.m-close:hover { color: var(--text); border-color: var(--route); }
.gallery-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 0.75rem; margin-top: 0.75rem; }
.gallery-item { border-radius: 12px; overflow: hidden; cursor: pointer; background: rgba(255,255,255,0.03); border: 1px solid rgba(88,198,255,0.1); transition: transform 0.2s; }
.gallery-item:hover { transform: scale(1.02); }
.gallery-item img { width: 100%; height: 140px; object-fit: cover; display: block; }
.gallery-full { grid-column: 1/-1; }
.gallery-full img { height: 200px; }
.gallery-item-label { padding: 0.5rem 0.75rem; font-size: 0.72rem; color: var(--muted); }
.data-table { width: 100%; border-collapse: collapse; font-size: 0.82rem; }
.data-table th, .data-table td { padding: 0.6rem 0.8rem; border-bottom: 1px solid rgba(88,198,255,0.08); text-align: left; }
.data-table th { color: var(--muted); font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }
.data-table td { color: var(--text); }
.process-steps { display: flex; flex-direction: column; gap: 0.75rem; }
.process-step { display: flex; gap: 1rem; align-items: flex-start; }
.step-num { width: 28px; height: 28px; border-radius: 50%; background: linear-gradient(135deg, var(--route), #2a7aff); display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 700; flex-shrink: 0; margin-top: 0.1rem; }
.step-title { font-weight: 600; font-size: 0.88rem; margin-bottom: 0.2rem; }
.step-desc { font-size: 0.8rem; color: var(--muted); line-height: 1.5; }
#m-res { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.5rem; }
.chip { padding: 0.25rem 0.65rem; border-radius: 20px; font-size: 0.72rem; background: rgba(88,198,255,0.06); border: 1px solid rgba(88,198,255,0.15); color: var(--muted); cursor: default; }
.sae-tag { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 6px; font-size: 0.68rem; font-weight: 600; margin-bottom: 0.75rem; font-family: 'Share Tech Mono', monospace; }
.sae-ue11{background:rgba(88,198,255,.15);color:var(--route)} .sae-ue12{background:rgba(168,85,247,.15);color:#a855f7}
.sae-ue13{background:rgba(34,197,94,.15);color:#22c55e} .sae-ue14{background:rgba(245,158,11,.15);color:#f59e0b}
.sae-ue21{background:rgba(88,198,255,.12);color:#7dd3fc} .sae-ue22{background:rgba(168,85,247,.12);color:#c084fc}
.sae-ue23{background:rgba(34,197,94,.12);color:#4ade80} .sae-ue24{background:rgba(245,158,11,.12);color:#fbbf24}
.sae-multi{background:rgba(168,85,247,.12);color:#a855f7}

/* ─── LIGHTBOX ─── */
.lightbox { position:fixed;inset:0;background:rgba(0,0,0,.95);z-index:300;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity .2s;cursor:zoom-out; }
.lightbox.open{opacity:1;pointer-events:all;}
.lightbox img{max-width:90vw;max-height:90vh;border-radius:8px;object-fit:contain;}

/* ─── RESPONSIVE ─── */
@media(max-width:768px){
  #sections { justify-content: center; align-items: flex-end; padding-bottom: 1rem; }
  .panel { width: 95vw; max-height: 60vh; padding: 1.5rem; }
  .hud-stats { display: none; }
  .bag-grid { grid-template-columns: 1fr; }
  .board-grid { grid-template-columns: 1fr; }
}
"""

# ══════════════════════════════════════════════════════════
# STEP 3 — JavaScript (Three.js + GSAP)
# ══════════════════════════════════════════════════════════
JS = """
// ════════════════════════════════════════════════════════
// Flight GMP-2028 · Three.js + GSAP · Anas El Hiss
// ════════════════════════════════════════════════════════
import * as THREE from 'three';
import { EffectComposer }   from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass }       from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass }  from 'three/addons/postprocessing/UnrealBloomPass.js';
import { OutputPass }       from 'three/addons/postprocessing/OutputPass.js';
import { LensflareElement, Lensflare } from 'three/addons/objects/Lensflare.js';

const gsap = window.gsap;
const ScrollTrigger = window.ScrollTrigger;
gsap.registerPlugin(ScrollTrigger);

// ── RENDERER ──────────────────────────────────────────
const renderer = new THREE.WebGLRenderer({
  canvas: document.getElementById('three-canvas'),
  antialias: true, alpha: false,
  powerPreference: 'high-performance'
});
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// ── SCENE + CAMERA ────────────────────────────────────
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, window.innerWidth/window.innerHeight, 0.05, 5000);
camera.position.set(0, 2, 12);

// ── POST-PROCESSING ────────────────────────────────────
const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
const bloom = new UnrealBloomPass(
  new THREE.Vector2(window.innerWidth, window.innerHeight), 0.8, 0.4, 0.85
);
composer.addPass(bloom);
composer.addPass(new OutputPass());

// ── RESIZE ────────────────────────────────────────────
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
  composer.setSize(window.innerWidth, window.innerHeight);
});

// ══════════════════════════════════════════════════════
// SKY DOME — custom shader
// ══════════════════════════════════════════════════════
const skyUniforms = {
  uSunDir:   { value: new THREE.Vector3(0.3, 0.2, -1).normalize() },
  uZenith:   { value: new THREE.Color(0x0a1e3f) },
  uHorizon:  { value: new THREE.Color(0xb05820) },
  uGround:   { value: new THREE.Color(0x050b18) },
  uSunColor: { value: new THREE.Color(0xfff0c0) },
  uTime:     { value: 0.0 },
};
const skyMat = new THREE.ShaderMaterial({
  uniforms: skyUniforms,
  vertexShader: `
    varying vec3 vWorldPos;
    void main() {
      vWorldPos = (modelMatrix * vec4(position,1.0)).xyz;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.0);
    }
  `,
  fragmentShader: `
    varying vec3 vWorldPos;
    uniform vec3 uSunDir, uZenith, uHorizon, uGround, uSunColor;
    void main() {
      vec3 d = normalize(vWorldPos);
      float h = d.y;
      vec3 sky = mix(uHorizon, uZenith, smoothstep(-0.05, 0.5, h));
      sky = mix(uGround, sky, smoothstep(-0.3, 0.0, h));
      float sun = max(dot(d, uSunDir), 0.0);
      sky += uSunColor * pow(sun, 128.0) * 3.0;
      sky += uSunColor * pow(sun, 8.0) * 0.25;
      float horizon = 1.0 - abs(h);
      sky += vec3(0.4, 0.55, 0.8) * pow(horizon, 6.0) * 0.15;
      gl_FragColor = vec4(sky, 1.0);
    }
  `,
  side: THREE.BackSide,
  depthWrite: false,
});
const skyMesh = new THREE.Mesh(new THREE.SphereGeometry(2000, 32, 16), skyMat);
scene.add(skyMesh);

// ══════════════════════════════════════════════════════
// SUN + LENSFLARE
// ══════════════════════════════════════════════════════
const sunLight = new THREE.DirectionalLight(0xfff0d0, 4);
sunLight.position.set(60, 40, -80);
sunLight.castShadow = true;
sunLight.shadow.mapSize.setScalar(2048);
sunLight.shadow.camera.far = 500;
scene.add(sunLight);
scene.add(new THREE.AmbientLight(0x0a1830, 2));

// Lensflare
const flareLoader = new THREE.TextureLoader();
const lensflare = new Lensflare();
// Create simple flare texture
const fCanvas = document.createElement('canvas');
fCanvas.width = fCanvas.height = 128;
const fCtx = fCanvas.getContext('2d');
const fGrad = fCtx.createRadialGradient(64,64,0,64,64,64);
fGrad.addColorStop(0,'rgba(255,240,200,1)');
fGrad.addColorStop(0.3,'rgba(255,200,100,0.6)');
fGrad.addColorStop(1,'rgba(255,180,50,0)');
fCtx.fillStyle = fGrad; fCtx.fillRect(0,0,128,128);
const flareTex = new THREE.CanvasTexture(fCanvas);
lensflare.addElement(new LensflareElement(flareTex, 300, 0));
lensflare.addElement(new LensflareElement(flareTex, 60, 0.6));
lensflare.addElement(new LensflareElement(flareTex, 30, 0.8));
const lensLight = new THREE.PointLight(0xfff0c0, 1, 2000);
lensLight.position.copy(sunLight.position).multiplyScalar(10);
lensLight.add(lensflare);
scene.add(lensLight);

// ══════════════════════════════════════════════════════
// STARS
// ══════════════════════════════════════════════════════
function createStars() {
  const n = 3000;
  const pos = new Float32Array(n * 3);
  const col = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    const theta = Math.random() * Math.PI * 2;
    const phi   = Math.acos(2 * Math.random() - 1);
    const r = 1800 + Math.random() * 150;
    pos[i*3]   = r * Math.sin(phi) * Math.cos(theta);
    pos[i*3+1] = r * Math.sin(phi) * Math.sin(theta);
    pos[i*3+2] = r * Math.cos(phi);
    const b = 0.5 + Math.random() * 0.5;
    col[i*3] = b; col[i*3+1] = b; col[i*3+2] = b * 1.1;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  geo.setAttribute('color', new THREE.BufferAttribute(col, 3));
  const mat = new THREE.PointsMaterial({ size: 1.2, vertexColors: true, transparent: true, opacity: 0.0, depthWrite: false });
  return new THREE.Points(geo, mat);
}
const stars = createStars();
scene.add(stars);

// ══════════════════════════════════════════════════════
// CLOUDS
// ══════════════════════════════════════════════════════
function makeCloudTexture() {
  const c = document.createElement('canvas');
  c.width = c.height = 256;
  const ctx = c.getContext('2d');
  function blob(x, y, r, a) {
    const g = ctx.createRadialGradient(x,y,0,x,y,r);
    g.addColorStop(0, `rgba(235,242,255,${a})`);
    g.addColorStop(0.5, `rgba(235,242,255,${a*0.5})`);
    g.addColorStop(1, 'rgba(235,242,255,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.fill();
  }
  blob(128,128,100,0.9); blob(60,115,75,0.8); blob(195,118,70,0.8);
  blob(100,85,60,0.7);  blob(158,80,55,0.6);  blob(40,130,50,0.5);
  return new THREE.CanvasTexture(c);
}
const cloudTex = makeCloudTexture();
const cloudGroup = new THREE.Group();
const cloudMat = new THREE.SpriteMaterial({ map: cloudTex, transparent: true, depthWrite: false, opacity: 0.45 });
for (let i = 0; i < 40; i++) {
  const s = new THREE.Sprite(cloudMat.clone());
  const scale = 40 + Math.random() * 80;
  s.scale.set(scale, scale * 0.5, 1);
  s.position.set(
    (Math.random() - 0.5) * 800,
    -5 + Math.random() * 30,
    (Math.random() - 0.5) * 800
  );
  s.userData.speed = 0.2 + Math.random() * 0.4;
  cloudGroup.add(s);
}
scene.add(cloudGroup);

// ══════════════════════════════════════════════════════
// BOEING 777 — geometric build
// ══════════════════════════════════════════════════════
function createBoeing777() {
  const plane = new THREE.Group();

  const whiteMat = new THREE.MeshPhysicalMaterial({
    color: 0xf0f5ff, metalness: 0.45, roughness: 0.32, envMapIntensity: 1.0
  });
  const darkMat = new THREE.MeshPhysicalMaterial({
    color: 0x0c1e3e, metalness: 0.7, roughness: 0.2
  });
  const accentMat = new THREE.MeshPhysicalMaterial({
    color: 0x58c6ff, metalness: 0.3, roughness: 0.4, emissive: 0x1a5080, emissiveIntensity: 0.3
  });
  const glassMat = new THREE.MeshPhysicalMaterial({
    color: 0x88ccff, transparent: true, opacity: 0.55, roughness: 0.05, metalness: 0.1
  });

  // ── FUSELAGE (LatheGeometry = revolution of profile)
  const fp = [];
  // nose cone
  for (let i = 0; i <= 18; i++) {
    const t = i / 18;
    fp.push(new THREE.Vector2(Math.pow(t, 0.6) * 0.85, t * 2.8));
  }
  // cylindrical body
  fp.push(new THREE.Vector2(0.85, 2.8));
  fp.push(new THREE.Vector2(0.85, 9.5));
  // tail cone
  for (let i = 0; i <= 12; i++) {
    const t = i / 12;
    fp.push(new THREE.Vector2(0.85 * (1 - Math.pow(t,0.7)*0.92), 9.5 + t * 3.5));
  }
  const fuseGeo = new THREE.LatheGeometry(fp, 48);
  const fuse = new THREE.Mesh(fuseGeo, whiteMat);
  fuse.rotation.z = -Math.PI / 2;
  fuse.position.x = 2.5;
  fuse.castShadow = true;
  plane.add(fuse);

  // Cockpit windows strip
  const cockpitGeo = new THREE.TorusGeometry(0.3, 0.08, 4, 16, Math.PI * 0.6);
  const cockpit = new THREE.Mesh(cockpitGeo, glassMat);
  cockpit.position.set(-3.0, 0.25, 0);
  cockpit.rotation.y = Math.PI / 2;
  plane.add(cockpit);

  // Airline stripe
  const stripeGeo = new THREE.CylinderGeometry(0.86, 0.86, 6.5, 48, 1, true, 1.6, 1.0);
  const stripeMat = new THREE.MeshBasicMaterial({ color: 0x0d3060, side: THREE.BackSide });
  const stripe = new THREE.Mesh(stripeGeo, stripeMat);
  stripe.rotation.z = -Math.PI / 2;
  stripe.position.x = 1.0;
  plane.add(stripe);

  // ── WINGS (ExtrudeGeometry)
  function makeWing(flip) {
    const wShape = new THREE.Shape();
    wShape.moveTo(0, 0);
    wShape.lineTo(0.7, 0.1);
    wShape.lineTo(0.2, flip*8.5);    // tip leading
    wShape.lineTo(-0.3, flip*8.6);   // tip
    wShape.lineTo(-1.0, flip*7.5);   // tip trailing
    wShape.lineTo(-0.9, 0.2);        // root trailing
    wShape.lineTo(0, 0);
    const extrudeSettings = { depth: 0.06, bevelEnabled: true, bevelSize: 0.02, bevelThickness: 0.02, bevelSegments: 2 };
    const geo = new THREE.ExtrudeGeometry(wShape, extrudeSettings);
    const mesh = new THREE.Mesh(geo, whiteMat);
    mesh.rotation.x = -Math.PI / 2;
    mesh.position.y = -0.05;
    mesh.position.x = -0.5;
    mesh.castShadow = true;
    return mesh;
  }
  plane.add(makeWing(1));
  plane.add(makeWing(-1));

  // Winglets
  function makeWinglet(side) {
    const wlShape = new THREE.Shape();
    wlShape.moveTo(0,0); wlShape.lineTo(0.4, 0.7); wlShape.lineTo(0.15, 0.9); wlShape.lineTo(-0.15, 0.1); wlShape.lineTo(0,0);
    const wlGeo = new THREE.ExtrudeGeometry(wlShape, { depth: 0.03, bevelEnabled: false });
    const wl = new THREE.Mesh(wlGeo, accentMat);
    wl.position.set(-0.2, 0.0, side * 8.5);
    wl.rotation.y = side > 0 ? -0.2 : 0.2;
    return wl;
  }
  plane.add(makeWinglet(1), makeWinglet(-1));

  // ── ENGINES (x2)
  function makeEngine(zPos) {
    const eng = new THREE.Group();
    // Nacelle (outer casing)
    const nacelleGeo = new THREE.CylinderGeometry(0.26, 0.21, 1.6, 24);
    const nacelle = new THREE.Mesh(nacelleGeo, whiteMat);
    nacelle.rotation.z = Math.PI / 2;
    eng.add(nacelle);
    // Inlet ring
    const ringGeo = new THREE.TorusGeometry(0.26, 0.03, 8, 24);
    const ring = new THREE.Mesh(ringGeo, accentMat);
    ring.rotation.y = Math.PI / 2;
    ring.position.x = -0.82;
    eng.add(ring);
    // Fan disc
    const fanGeo = new THREE.CircleGeometry(0.23, 24);
    const fan = new THREE.Mesh(fanGeo, darkMat);
    fan.rotation.y = Math.PI / 2;
    fan.position.x = -0.78;
    eng.add(fan);
    eng.userData.fan = fan;
    // Pylon
    const pylonGeo = new THREE.BoxGeometry(0.7, 0.08, 0.2);
    const pylon = new THREE.Mesh(pylonGeo, whiteMat);
    pylon.position.set(0, 0.2, 0);
    eng.add(pylon);
    eng.position.set(-0.8, -0.45, zPos);
    eng.castShadow = true;
    return eng;
  }
  const eng1 = makeEngine(-3.2);
  const eng2 = makeEngine(3.2);
  plane.add(eng1, eng2);
  plane.userData.engines = [eng1.userData.fan, eng2.userData.fan];

  // ── VERTICAL TAIL
  const vtShape = new THREE.Shape();
  vtShape.moveTo(0,0); vtShape.lineTo(-1.4,0); vtShape.lineTo(-2.0,1.8);
  vtShape.lineTo(-0.6,2.4); vtShape.lineTo(0,1.2); vtShape.lineTo(0,0);
  const vtGeo = new THREE.ExtrudeGeometry(vtShape, { depth: 0.05, bevelEnabled: false });
  const vTail = new THREE.Mesh(vtGeo, whiteMat);
  vTail.rotation.x = Math.PI / 2;
  vTail.position.set(4.2, 0.6, -0.025);
  vTail.castShadow = true;
  plane.add(vTail);

  // ── HORIZONTAL STABILIZERS
  function makeHStab(side) {
    const hsShape = new THREE.Shape();
    hsShape.moveTo(0,0); hsShape.lineTo(-0.6,0); hsShape.lineTo(-1.5, side*3.2);
    hsShape.lineTo(-0.4, side*3.3); hsShape.lineTo(0.1, side*1.0); hsShape.lineTo(0,0);
    const hsGeo = new THREE.ExtrudeGeometry(hsShape, { depth: 0.04, bevelEnabled: false });
    const hs = new THREE.Mesh(hsGeo, whiteMat);
    hs.rotation.x = -Math.PI / 2;
    hs.position.set(4.3, 0.7, 0);
    return hs;
  }
  plane.add(makeHStab(1), makeHStab(-1));

  // ── NAVIGATION LIGHTS
  const navRed   = new THREE.PointLight(0xff2222, 3, 6);  navRed.position.set(-0.3, 0, -8.6);
  const navGreen = new THREE.PointLight(0x22ff44, 3, 6);  navGreen.position.set(-0.3, 0, 8.6);
  const navWhite = new THREE.PointLight(0xffffff, 4, 8);  navWhite.position.set(5.5, 0.5, 0);
  const navStrobeL = new THREE.PointLight(0xffffff, 0, 5); navStrobeL.position.set(0, -0.5, -8.6);
  const navStrobeR = new THREE.PointLight(0xffffff, 0, 5); navStrobeR.position.set(0, -0.5, 8.6);
  plane.add(navRed, navGreen, navWhite, navStrobeL, navStrobeR);
  plane.userData.strobeLights = [navStrobeL, navStrobeR];

  // Window dots along fuselage
  const windowMat = new THREE.MeshBasicMaterial({ color: 0xffd080, transparent: true, opacity: 0.9 });
  for (let row = 0; row < 28; row++) {
    for (let side = 0; side < 2; side++) {
      const angle = (side === 0 ? -0.62 : 0.62);
      const wGeo = new THREE.CircleGeometry(0.04, 6);
      const w = new THREE.Mesh(wGeo, windowMat);
      const rx = -2.5 + row * 0.38;
      w.position.set(rx, Math.sin(angle) * 0.86, Math.cos(angle) * 0.86);
      w.lookAt(w.position.clone().add(new THREE.Vector3(0, Math.sin(angle), Math.cos(angle))));
      plane.add(w);
    }
  }

  return plane;
}

const airplane = createBoeing777();
airplane.scale.setScalar(1.5);
scene.add(airplane);

// ══════════════════════════════════════════════════════
// CONTRAIL SYSTEM
// ══════════════════════════════════════════════════════
const TRAIL_MAX = 300;
const trailPos  = new Float32Array(TRAIL_MAX * 3);
const trailAlph = new Float32Array(TRAIL_MAX);
const trailGeo  = new THREE.BufferGeometry();
trailGeo.setAttribute('position', new THREE.BufferAttribute(trailPos, 3));
trailGeo.setAttribute('alpha', new THREE.BufferAttribute(trailAlph, 1));
const trailMat = new THREE.ShaderMaterial({
  uniforms: {},
  vertexShader: `
    attribute float alpha;
    varying float vAlpha;
    void main() {
      vAlpha = alpha;
      gl_PointSize = 12.0 * (1.0 - gl_Position.z / gl_Position.w * 0.5);
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    varying float vAlpha;
    void main() {
      float d = length(gl_PointCoord - vec2(0.5));
      if(d > 0.5) discard;
      float a = vAlpha * smoothstep(0.5, 0.0, d);
      gl_FragColor = vec4(0.9, 0.95, 1.0, a);
    }
  `,
  transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
});
const trail = new THREE.Points(trailGeo, trailMat);
scene.add(trail);
let trailHead = 0;

function addTrailPoint(pos) {
  const i = trailHead % TRAIL_MAX;
  trailPos[i*3]   = pos.x;
  trailPos[i*3+1] = pos.y;
  trailPos[i*3+2] = pos.z;
  trailAlph[i] = 1.0;
  trailHead++;
  for (let j = 0; j < TRAIL_MAX; j++) {
    if (trailAlph[j] > 0) trailAlph[j] = Math.max(0, trailAlph[j] - 0.003);
  }
  trailGeo.attributes.position.needsUpdate = true;
  trailGeo.attributes.alpha.needsUpdate = true;
}

// ══════════════════════════════════════════════════════
// FLIGHT PATH (spline)
// ══════════════════════════════════════════════════════
const FLIGHT_PATH = new THREE.CatmullRomCurve3([
  new THREE.Vector3(-300, -20, 0),    // approach
  new THREE.Vector3(-150, 0, 30),     // climbing
  new THREE.Vector3(-50, 15, 0),      // levelling
  new THREE.Vector3(0, 18, -20),      // bank
  new THREE.Vector3(80, 22, 10),      // cruise
  new THREE.Vector3(160, 18, -15),    // bank left
  new THREE.Vector3(240, 25, 0),      // climbing
  new THREE.Vector3(320, 20, 20),     // slight bank
  new THREE.Vector3(400, 14, 0),      // descending
  new THREE.Vector3(480, 6, 0),       // approach
  new THREE.Vector3(540, 2, 0),       // final
], false, 'catmullrom', 0.5);

const CAM_OFFSET = new THREE.Vector3(0, 3.5, 18);  // behind & above
let scrollProgress = 0;
let introPlayed = false;
let inFlight = false;
const clock = new THREE.Clock();

// ══════════════════════════════════════════════════════
// GSAP SCROLL DRIVER
// ══════════════════════════════════════════════════════
const scrollTween = ScrollTrigger.create({
  trigger: '#scroll-driver',
  start: 'top top',
  end: 'bottom bottom',
  scrub: 2.5,
  onUpdate: (self) => {
    if (!inFlight) return;
    scrollProgress = self.progress;
    document.querySelector('.scroll-fill').style.width = (scrollProgress * 100) + '%';
    document.querySelector('.scroll-pct').textContent = Math.round(scrollProgress * 100) + '%';
    updateFlight(scrollProgress);
    updateSections(scrollProgress);
    updateSky(scrollProgress);
    updateHUD(scrollProgress);
  }
});

// ══════════════════════════════════════════════════════
// FLIGHT UPDATER
// ══════════════════════════════════════════════════════
function updateFlight(t) {
  const safeT = Math.max(0, Math.min(1, t));
  const pos  = FLIGHT_PATH.getPointAt(safeT);
  const tan  = FLIGHT_PATH.getTangentAt(safeT);
  airplane.position.copy(pos);
  // Face direction of travel with banking
  const up = new THREE.Vector3(0, 1, 0);
  const q = new THREE.Quaternion().setFromUnitVectors(new THREE.Vector3(1, 0, 0), tan);
  airplane.quaternion.copy(q);
  // Camera follow
  const camTarget = pos.clone().add(CAM_OFFSET.clone().applyQuaternion(q));
  camera.position.lerp(camTarget, 0.08);
  const lookAt = pos.clone().add(tan.clone().multiplyScalar(20));
  camera.lookAt(lookAt);
  skyMesh.position.copy(camera.position);
}

// ══════════════════════════════════════════════════════
// SKY TRANSITION
// ══════════════════════════════════════════════════════
const SKY_PHASES = [
  { t: 0.0, zenith: new THREE.Color(0x0a1830), horizon: new THREE.Color(0xb05820), sun: new THREE.Vector3(0.3, 0.15, -1).normalize() },
  { t: 0.2, zenith: new THREE.Color(0x0c2245), horizon: new THREE.Color(0xf0a060), sun: new THREE.Vector3(0.5, 0.35, -0.8).normalize() },
  { t: 0.45, zenith: new THREE.Color(0x0d3060), horizon: new THREE.Color(0x6aabdd), sun: new THREE.Vector3(0.6, 0.6, -0.5).normalize() },
  { t: 0.65, zenith: new THREE.Color(0x051228), horizon: new THREE.Color(0x9060a0), sun: new THREE.Vector3(-0.2, 0.1, -1).normalize() },
  { t: 0.85, zenith: new THREE.Color(0x020810), horizon: new THREE.Color(0x302860), sun: new THREE.Vector3(-0.5, -0.1, -0.8).normalize() },
  { t: 1.0,  zenith: new THREE.Color(0x0a1e3f), horizon: new THREE.Color(0xb05820), sun: new THREE.Vector3(0.3, 0.2, -1).normalize() },
];

function updateSky(t) {
  let i = 0;
  while (i < SKY_PHASES.length - 2 && SKY_PHASES[i+1].t < t) i++;
  const a = SKY_PHASES[i], b = SKY_PHASES[i+1];
  const alpha = (t - a.t) / (b.t - a.t);
  skyUniforms.uZenith.value.lerpColors(a.zenith, b.zenith, alpha);
  skyUniforms.uHorizon.value.lerpColors(a.horizon, b.horizon, alpha);
  skyUniforms.uSunDir.value.lerpVectors(a.sun, b.sun, alpha).normalize();
  sunLight.position.copy(skyUniforms.uSunDir.value).multiplyScalar(100);
  stars.material.opacity = t > 0.6 ? Math.min((t - 0.6) / 0.15, 1.0) * 0.8 : 0.0;
  cloudGroup.children.forEach(c => {
    c.material.opacity = 0.2 + (1 - Math.abs(t - 0.4)) * 0.35;
  });
}

// ══════════════════════════════════════════════════════
// SECTIONS VISIBILITY
// ══════════════════════════════════════════════════════
const SECTION_MAP = [
  { id: 'panel-passport',  show: 0.08, hide: 0.28 },
  { id: 'panel-skills',    show: 0.30, hide: 0.52 },
  { id: 'panel-sae',       show: 0.54, hide: 0.72 },
  { id: 'panel-timeline',  show: 0.74, hide: 0.92 },
  { id: 'panel-contact',   show: 0.93, hide: 1.01 },
];

function updateSections(t) {
  SECTION_MAP.forEach(s => {
    const el = document.getElementById(s.id);
    if (!el) return;
    const active = t >= s.show && t < s.hide;
    el.classList.toggle('visible', active);
  });
  // Arrival screen at very end
  if (t >= 0.96) {
    document.getElementById('arrival').classList.add('visible');
  }
}

// ══════════════════════════════════════════════════════
// HUD DATA
// ══════════════════════════════════════════════════════
const HUD_ALT   = document.getElementById('hud-alt');
const HUD_SPD   = document.getElementById('hud-spd');
const HUD_HDG   = document.getElementById('hud-hdg');
const HUD_PHASE = document.getElementById('hud-phase');
const PHASES = ['DÉCOLLAGE','MONTÉE','CROISIÈRE','APPROCHE','FINAL'];

function updateHUD(t) {
  const alt = Math.round(100 + t * 38000 * Math.sin(t * Math.PI));
  const spd = Math.round(180 + t * 480 * Math.sin(t * Math.PI));
  const hdg = Math.round(240 + t * 120) % 360;
  if (HUD_ALT) HUD_ALT.textContent = alt.toString().padStart(5,'0');
  if (HUD_SPD) HUD_SPD.textContent = spd.toString().padStart(3,'0');
  if (HUD_HDG) HUD_HDG.textContent = hdg.toString().padStart(3,'0');
  const pi = Math.min(Math.floor(t * PHASES.length), PHASES.length-1);
  if (HUD_PHASE) HUD_PHASE.textContent = PHASES[pi];
}

// ══════════════════════════════════════════════════════
// INTRO SEQUENCE
// ══════════════════════════════════════════════════════
function playIntro() {
  // Start plane in distance
  airplane.position.set(-300, -20, 0);
  airplane.scale.setScalar(0.01);
  camera.position.set(0, 3, 18);
  camera.lookAt(0, 0, 0);

  const tl = gsap.timeline({ delay: 0.5 });

  // Plane approaches from far away
  tl.to(airplane.position, { x: -60, y: 1, z: 0, duration: 4, ease: 'power2.in' }, 0);
  tl.to(airplane.scale, { x: 1.5, y: 1.5, z: 1.5, duration: 4, ease: 'power2.in' }, 0);

  // Title appears
  tl.to('.intro-flight-number', { opacity: 1, y: 0, duration: 0.8, ease: 'power2.out' }, 1.8);
  tl.to('.intro-title',    { opacity: 1, y: 0, duration: 0.9, ease: 'power3.out' }, 2.3);
  tl.to('.intro-subtitle', { opacity: 1, y: 0, duration: 0.7, ease: 'power2.out' }, 2.9);
  tl.to('.intro-dest',     { opacity: 1, y: 0, duration: 0.7, ease: 'power2.out' }, 3.3);
  tl.to('.btn-board',      { opacity: 1, y: 0, duration: 0.6, ease: 'power2.out' }, 3.8);

  // Plane hovers gently
  tl.to(airplane.position, { y: 1.5, duration: 2, yoyo: true, repeat: -1, ease: 'sine.inOut' }, 5);
}

// ── EMBARK button
document.getElementById('btn-embark').addEventListener('click', () => {
  inFlight = true;
  gsap.to('#intro', { opacity: 0, duration: 1.2, onComplete: () => {
    document.getElementById('intro').style.display = 'none';
  }});
  gsap.to('#hud', { opacity: 1, duration: 1, delay: 0.5 });
  document.getElementById('hud').classList.add('visible');
  document.getElementById('scroll-progress').classList.add('visible');

  // Plane takes off
  gsap.to(airplane.position, { x: -30, y: 5, z: -5, duration: 2, ease: 'power2.inOut' });
  gsap.to(airplane.rotation, { z: -0.15, duration: 1, ease: 'power2.inOut' });

  window.scrollTo({ top: 0, behavior: 'instant' });
});

// ══════════════════════════════════════════════════════
// SKILL BARS ANIMATION (when panel appears)
// ══════════════════════════════════════════════════════
const skillsPanel = document.getElementById('panel-skills');
const skillsObserver = new MutationObserver(() => {
  if (skillsPanel.classList.contains('visible')) {
    document.querySelectorAll('.bag-fill').forEach(bar => {
      const w = bar.dataset.w || '0';
      setTimeout(() => bar.style.width = w + '%', 300);
    });
  }
});
skillsObserver.observe(skillsPanel, { attributes: true });

// ══════════════════════════════════════════════════════
// ANIMATION LOOP
// ══════════════════════════════════════════════════════
let frameCount = 0;
const tmpVec = new THREE.Vector3();

function animate() {
  requestAnimationFrame(animate);
  const delta = clock.getDelta();
  const elapsed = clock.getElapsedTime();
  frameCount++;

  // Rotate engine fans
  if (airplane.userData.engines) {
    airplane.userData.engines.forEach(fan => { fan.rotation.y += delta * 25; });
  }

  // Strobe lights
  if (airplane.userData.strobeLights) {
    const strobe = Math.floor(elapsed * 2) % 3 === 0 ? 8 : 0;
    airplane.userData.strobeLights.forEach(l => l.intensity = strobe);
  }

  // Drift clouds slowly
  cloudGroup.children.forEach((c, i) => {
    c.position.x -= delta * c.userData.speed;
    if (c.position.x < airplane.position.x - 400) {
      c.position.x = airplane.position.x + 400;
    }
  });

  // Add trail every few frames
  if (inFlight && frameCount % 3 === 0) {
    tmpVec.copy(airplane.position);
    tmpVec.x -= 6;
    addTrailPoint(tmpVec);
  }

  // Gentle plane hover when not scrolling
  if (!inFlight) {
    airplane.position.y = Math.sin(elapsed * 0.7) * 0.3;
  }

  // Time uniform for sky
  skyUniforms.uTime.value = elapsed;

  composer.render();
}

// ── START
playIntro();
animate();

// ══════════════════════════════════════════════════════
// SAÉ MODAL SYSTEM
// ══════════════════════════════════════════════════════
__IMG_BLOCK__

__SAE13_FN__

__SAE204_FN__

__FONDERIE_FN__

function openModal(card) {
  document.getElementById('m-sem').textContent   = card.dataset.sem || '';
  document.getElementById('m-ref').textContent   = card.dataset.ref || '';
  document.getElementById('m-title').textContent = card.dataset.title || '';
  document.getElementById('m-ue').textContent    = card.dataset.ue || '';
  document.getElementById('m-desc').textContent  = card.dataset.desc || '';
  document.getElementById('m-obj').textContent   = card.dataset.obj || '';
  const tag = document.getElementById('m-tag');
  tag.textContent = (card.dataset.ue || '').split('—')[0].trim();
  tag.className = 'sae-tag';
  const k = (card.dataset.ue || '').replace(/[^0-9]/g, '').slice(0,2);
  const cm = {'11':'sae-ue11','12':'sae-ue12','13':'sae-ue13','14':'sae-ue14','21':'sae-ue21','22':'sae-ue22','23':'sae-ue23','24':'sae-ue24'};
  tag.classList.add(cm[k] || 'sae-multi');
  const resEl = document.getElementById('m-res');
  resEl.innerHTML = '';
  (card.dataset.res || '').split(',').map(s => s.trim()).filter(Boolean).forEach(r => {
    const c = document.createElement('span'); c.className = 'chip'; c.style.cursor = 'default'; c.textContent = r; resEl.appendChild(c);
  });
  const extra = document.getElementById('m-extra');
  extra.innerHTML = card.dataset.hasGallery ? buildSae13Extra() : (card.dataset.hasSae204 ? buildSae204Extra() : (card.dataset.hasFonderie ? buildFonderieExtra() : ''));
  document.getElementById('modal').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeModal() { document.getElementById('modal').classList.remove('open'); document.body.style.overflow = ''; }

document.querySelectorAll('.bp-card[data-sae]').forEach(c => {
  c.addEventListener('click', () => openModal(c));
  c.setAttribute('tabindex', '0');
  c.addEventListener('keydown', e => { if (e.key === 'Enter') openModal(c); });
});
document.getElementById('mClose').addEventListener('click', closeModal);
document.getElementById('modal').addEventListener('click', e => { if (e.target === document.getElementById('modal')) closeModal(); });

// Lightbox
function openLightbox(src) {
  document.getElementById('lb-img').src = src;
  document.getElementById('lightbox').classList.add('open');
}
document.getElementById('lightbox').addEventListener('click', () => document.getElementById('lightbox').classList.remove('open'));
"""

# ══════════════════════════════════════════════════════════
# STEP 4 — HTML
# ══════════════════════════════════════════════════════════

SAE_CARDS_HTML = """
        <div class="bp-card" data-sae="1" data-sem="Semestre 1" data-ref="SAÉ 1.1" data-ue="UE11 — Spécifier" data-title="Analyse d'un produit grand public" data-desc="Analyser un produit de grande consommation pour identifier ses fonctions, sa structure et les matériaux. Rédiger un dossier d'analyse fonctionnelle et technique structuré." data-res="R1.03, R1.04, R1.07, R1.10, R1.13, R1.14" data-obj="Identifier et analyser les fonctions d'un produit existant. Mettre en œuvre les méthodes d'analyse de la valeur et de décomposition fonctionnelle.">
          <div class="bp-card-top"><div class="bp-flight-num">VOL S1-11</div><span class="bp-ue-tag sae-ue11">UE11 Spécifier</span></div>
          <div class="bp-title">Analyse d'un produit grand public</div>
          <div class="bp-desc">Analyse fonctionnelle et technique.</div>
          <div class="bp-res"><span class="bp-res-chip">R1.03</span><span class="bp-res-chip">R1.04</span><span class="bp-res-chip">R1.07</span></div>
        </div>
        <div class="bp-card" data-sae="2" data-sem="Semestre 1" data-ref="SAÉ 1.2" data-ue="UE12 — Développer" data-title="Modification d'un système mécanique" data-desc="Proposer et modéliser une modification sur un système mécanique existant en utilisant des outils de CAO. Justifier les choix techniques par des calculs et des simulations." data-res="R1.01, R1.04, R1.05, R1.06" data-obj="Maîtriser les outils CAO pour modifier un mécanisme existant. Justifier les choix de conception par le calcul mécanique.">
          <div class="bp-card-top"><div class="bp-flight-num">VOL S1-12</div><span class="bp-ue-tag sae-ue12">UE12 Développer</span></div>
          <div class="bp-title">Modification d'un système mécanique</div>
          <div class="bp-desc">CAO + calcul mécanique justifié.</div>
          <div class="bp-res"><span class="bp-res-chip">R1.01</span><span class="bp-res-chip">R1.04</span><span class="bp-res-chip">R1.05</span></div>
        </div>
        <div class="bp-card" data-sae="3" data-sem="Semestre 1" data-ref="SAÉ 1.3" data-ue="UE13 — Réaliser" data-title="De la maquette numérique au prototype physique" data-desc="Conception d'une pièce centrale de bras articulé sur SolidWorks, préparation du contrat de phase, choix du matériau (AlSi10Mg EN AC-43000) et fabrication du prototype. Analyse des sollicitations mécaniques et justification industrielle." data-res="R1.05, R1.06, R1.07, R1.08" data-obj="Maîtriser la chaîne numérique complète : CAO → contrat de phase → fabrication → contrôle métrologique." data-has-gallery="1">
          <div class="bp-card-top"><div class="bp-flight-num">VOL S1-13 ★</div><span class="bp-ue-tag sae-ue13">UE13 Réaliser</span></div>
          <div class="bp-title">Maquette numérique → Prototype</div>
          <div class="bp-desc">Bras articulé · AlSi10Mg · SolidWorks → Visuels CAO disponibles</div>
          <div class="bp-res"><span class="bp-res-chip">R1.05</span><span class="bp-res-chip">R1.06</span><span class="bp-res-chip">R1.07</span><span class="bp-res-chip">R1.08</span></div>
        </div>
        <div class="bp-card" data-sae="4" data-sem="Semestre 1" data-ref="SAÉ 1.4" data-ue="UE14 — Piloter" data-title="Découverte des métiers" data-desc="Explorer les différents métiers du GMP à travers des rencontres professionnelles et visites d'entreprises. Construire son projet professionnel." data-res="R1.13, R1.14, R1.15" data-obj="Identifier les débouchés accessibles après le BUT GMP et construire les premières bases de son PPP.">
          <div class="bp-card-top"><div class="bp-flight-num">VOL S1-14</div><span class="bp-ue-tag sae-ue14">UE14 Piloter</span></div>
          <div class="bp-title">Découverte des métiers GMP</div>
          <div class="bp-desc">Rencontres pro · Construction du PPP.</div>
          <div class="bp-res"><span class="bp-res-chip">R1.13</span><span class="bp-res-chip">R1.15</span></div>
        </div>
        <div class="bp-card" data-sae="7" data-sem="Semestre 2" data-ref="SAÉ 2.03" data-ue="UE23 — Réaliser" data-title="Fabrication d'une pièce unitaire" data-desc="Réaliser une pièce unitaire de précision sur machine-outil selon le dessin de définition. Contrôle métrologique de conformité. Inclut les TP de fonderie R2.07 : moulage en sable de l'alliage AS13, analyse du diagramme Al-Si, étude des défauts." data-res="R2.05, R2.06, R2.07, R2.08, POR2" data-obj="Maîtriser la réalisation complète d'une pièce unitaire." data-has-fonderie="1">
          <div class="bp-card-top"><div class="bp-flight-num">VOL S2-23 ★</div><span class="bp-ue-tag sae-ue23">UE23 Réaliser</span></div>
          <div class="bp-title">Fabrication pièce unitaire + Fonderie AS13</div>
          <div class="bp-desc">Usinage précision + TP fonderie moulage sable → Rapport disponible</div>
          <div class="bp-res"><span class="bp-res-chip">R2.07</span><span class="bp-res-chip">R2.08</span><span class="bp-res-chip">POR2</span></div>
        </div>
        <div class="bp-card" data-sae="8" data-sem="Semestre 2" data-ref="SAÉ 2.04" data-ue="UE24 — Piloter" data-title="Piloter une production stabilisée" data-desc="OPI FA — Étude chez SMP BALTZER : gestion d'une commande de 70 pointes tournantes T301. Processus de fabrication, calcul coût prévisionnel/devis, ordonnancement Gantt, management de la production et communication client." data-res="R2.09, R2.12, R2.13, R2.14, POR2" data-obj="Piloter une production : devis, Gantt, management." data-has-sae204="1">
          <div class="bp-card-top"><div class="bp-flight-num">VOL S2-24 ★</div><span class="bp-ue-tag sae-ue24">UE24 Piloter</span></div>
          <div class="bp-title">OPI FA · SMP BALTZER · T301</div>
          <div class="bp-desc">70 pièces · Gantt · Devis · Management → Documents disponibles</div>
          <div class="bp-res"><span class="bp-res-chip">R2.09</span><span class="bp-res-chip">R2.12</span><span class="bp-res-chip">POR2</span></div>
        </div>
"""

HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Flight GMP-2028 · Anas El Hiss</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&family=Share+Tech+Mono&display=swap">
<style>
__CSS__
</style>
</head>
<body>

<!-- ── THREE.JS CANVAS (fixed, full screen) ── -->
<canvas id="three-canvas"></canvas>

<!-- ── INTRO OVERLAY ── -->
<div id="intro">
  <div class="intro-flight-number">FLIGHT GMP-2028 &nbsp;·&nbsp; BOARDING &nbsp;·&nbsp; IUT ÉVRY → INDUSTRIE</div>
  <div class="intro-title">Anas<br>El Hiss</div>
  <div class="intro-subtitle">BUT Génie Mécanique &amp; Productique · Parcours SNRV</div>
  <div class="intro-dest">
    <div>
      <div class="intro-dest-city">MAF</div>
      <div class="intro-dest-sub">Maisons-Alfort</div>
    </div>
    <div class="intro-dest-arrow">✈</div>
    <div style="text-align:right">
      <div class="intro-dest-city">IND</div>
      <div class="intro-dest-sub">Simulation &amp; VR</div>
    </div>
  </div>
  <button class="btn-board" id="btn-embark">✈ &nbsp;Embarquer</button>
</div>

<!-- ── HUD ── -->
<nav id="hud">
  <div class="hud-brand">✈ FLIGHT GMP-2028</div>
  <div class="hud-stats">
    <div>ALT <span id="hud-alt">00100</span> ft</div>
    <div>SPD <span id="hud-spd">180</span> kts</div>
    <div>HDG <span id="hud-hdg">240</span>°</div>
    <div style="color:var(--gold)"><span id="hud-phase">DÉCOLLAGE</span></div>
  </div>
  <div class="hud-nav">
    <a href="javascript:void(0)" onclick="showPanel('panel-passport')">Passeport</a>
    <a href="javascript:void(0)" onclick="showPanel('panel-skills')">Compétences</a>
    <a href="javascript:void(0)" onclick="showPanel('panel-sae')">SAÉ</a>
    <a href="javascript:void(0)" onclick="showPanel('panel-timeline')">Parcours</a>
    <a href="javascript:void(0)" onclick="showPanel('panel-contact')">Contact</a>
  </div>
</nav>

<!-- ── SCROLL DRIVER (tall, makes scroll happen) ── -->
<div id="scroll-driver"></div>

<!-- ── FIXED PANELS LAYER ── -->
<div id="sections">

  <!-- PANEL 1 · PASSEPORT -->
  <div class="panel" id="panel-passport">
    <div class="panel-badge">✈ ESCALE 01 · PRF · Passeport</div>
    <h2>Profil <span>Voyageur</span></h2>
    <div class="panel-divider"></div>
    <div class="passport">
      <div class="passport-header">
        <div class="passport-avatar">A</div>
        <div>
          <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.1rem">Anas El Hiss</div>
          <div style="font-size:0.78rem;color:var(--muted)">BUT GMP SNRV · 1ère année</div>
        </div>
        <div class="visa-stamp">
          <span>GMP</span>
          <span class="vs-approved">APPROUVÉ</span>
          <span>2025</span>
        </div>
      </div>
      <div class="passport-info-row"><span class="passport-key">NOM</span><span class="passport-val">EL HISS, Anas</span></div>
      <div class="passport-info-row"><span class="passport-key">ORIGINE</span><span class="passport-val">Maisons-Alfort (94)</span></div>
      <div class="passport-info-row"><span class="passport-key">FORMATION</span><span class="passport-val">BUT GMP · Parcours SNRV</span></div>
      <div class="passport-info-row"><span class="passport-key">EMPLOYEUR</span><span class="passport-val">Losange · Apprenti Op-Régleur</span></div>
      <div class="passport-info-row"><span class="passport-key">DEST.</span><span class="passport-val">Simulation Numérique &amp; VR</span></div>
      <div class="passport-info-row"><span class="passport-key">VALIDITÉ</span><span class="passport-val">2025 → 2028</span></div>
      <div class="passport-info-row"><span class="passport-key">LOGICIELS</span>
        <span class="passport-val" style="display:flex;flex-wrap:wrap;gap:.35rem">
          <span class="chip">SolidWorks</span><span class="chip">3DExperience</span><span class="chip">CAO/DAO</span><span class="chip">Catia</span>
        </span>
      </div>
      <div class="passport-mrz">
        P&lt;FRA EL HISS&lt;&lt;ANAS&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;&lt;<br>
        GMP2028&lt;9FRA9410012M2807313&lt;&lt;&lt;&lt;&lt;&lt;4
      </div>
    </div>
    <p style="font-size:0.8rem;color:var(--muted);margin-top:1rem;line-height:1.6">
      Passionné par la CAO, la simulation numérique et la fabrication industrielle. En apprentissage chez Losange depuis octobre 2025. Football depuis 2010 à Maisons-Alfort · Association humanitaire · Essaouira (Maroc).
    </p>
  </div>

  <!-- PANEL 2 · COMPÉTENCES / BAGAGES -->
  <div class="panel" id="panel-skills">
    <div class="panel-badge">✈ ESCALE 02 · SKL · Bagages</div>
    <h2>Compétences <span>Embarquées</span></h2>
    <div class="panel-divider"></div>
    <p style="font-size:0.8rem;color:var(--muted);margin-bottom:1rem">4 blocs de compétences BUT GMP · Ouverture de bagage</p>
    <div class="bag-grid">
      <div class="bag-item">
        <div class="bag-icon">🔍</div>
        <div class="bag-title">Spécifier</div>
        <div style="font-size:0.75rem;color:var(--muted)">Analyse fonctionnelle · Cahier des charges</div>
        <div class="bag-bar"><div class="bag-fill" data-w="72" style="background:linear-gradient(90deg,var(--route),#2a7aff)"></div></div>
      </div>
      <div class="bag-item">
        <div class="bag-icon">⚙️</div>
        <div class="bag-title">Développer</div>
        <div style="font-size:0.75rem;color:var(--muted)">CAO 3D · SolidWorks · Simulation</div>
        <div class="bag-bar"><div class="bag-fill" data-w="80" style="background:linear-gradient(90deg,#a855f7,var(--route))"></div></div>
      </div>
      <div class="bag-item">
        <div class="bag-icon">🏭</div>
        <div class="bag-title">Réaliser</div>
        <div style="font-size:0.75rem;color:var(--muted)">Usinage · Métrologie · Fonderie</div>
        <div class="bag-bar"><div class="bag-fill" data-w="75" style="background:linear-gradient(90deg,#22c55e,var(--route))"></div></div>
      </div>
      <div class="bag-item">
        <div class="bag-icon">📊</div>
        <div class="bag-title">Piloter</div>
        <div style="font-size:0.75rem;color:var(--muted)">Gestion prod · Gantt · Devis</div>
        <div class="bag-bar"><div class="bag-fill" data-w="68" style="background:linear-gradient(90deg,var(--gold),#f97316)"></div></div>
      </div>
      <div class="bag-item">
        <div class="bag-icon">💻</div>
        <div class="bag-title">SolidWorks</div>
        <div style="font-size:0.75rem;color:var(--muted)">Modélisation · Assemblage · Mise en plan</div>
        <div class="bag-bar"><div class="bag-fill" data-w="82" style="background:linear-gradient(90deg,var(--route),#a855f7)"></div></div>
      </div>
      <div class="bag-item">
        <div class="bag-icon">🔬</div>
        <div class="bag-title">Métrologie</div>
        <div style="font-size:0.75rem;color:var(--muted)">Contrôle · Tolérances · GPS</div>
        <div class="bag-bar"><div class="bag-fill" data-w="65" style="background:linear-gradient(90deg,#22c55e,var(--gold))"></div></div>
      </div>
    </div>
  </div>

  <!-- PANEL 3 · SAÉ BOARDING PASSES -->
  <div class="panel" id="panel-sae">
    <div class="panel-badge">✈ ESCALE 03 · SAÉ · Missions</div>
    <h2>Cartes <span>d'Embarquement</span></h2>
    <div class="panel-divider"></div>
    <p style="font-size:0.78rem;color:var(--muted);margin-bottom:1rem">Cliquer pour ouvrir le dossier de mission ↗</p>
    <div class="bp-list">
__SAE_CARDS__
    </div>
  </div>

  <!-- PANEL 4 · PARCOURS / TIMELINE -->
  <div class="panel" id="panel-timeline">
    <div class="panel-badge">✈ ESCALE 04 · PAR · Itinéraire</div>
    <h2>Itinéraire <span>de Vol</span></h2>
    <div class="panel-divider"></div>
    <div>
      <div class="tl-item">
        <div class="tl-dot">●</div>
        <div>
          <div class="tl-year">Oct. 2025 — Aujourd'hui</div>
          <div class="tl-title">Apprenti Opérateur-Régleur Joaillerie</div>
          <div class="tl-org">Losange · Île-de-France</div>
        </div>
      </div>
      <div class="tl-item">
        <div class="tl-dot">●</div>
        <div>
          <div class="tl-year">2025 — 2028</div>
          <div class="tl-title">BUT GMP · Parcours SNRV</div>
          <div class="tl-org">IUT Évry-Val-d'Essonne / CFA-EVE</div>
        </div>
      </div>
      <div class="tl-item">
        <div class="tl-dot">●</div>
        <div>
          <div class="tl-year">Avr. — Août 2025</div>
          <div class="tl-title">Animateur Sportif</div>
          <div class="tl-org">Ville de Maisons-Alfort</div>
        </div>
      </div>
      <div class="tl-item">
        <div class="tl-dot">●</div>
        <div>
          <div class="tl-year">2024 — 2025</div>
          <div class="tl-title">BUT 1 Informatique</div>
          <div class="tl-org">IUT Créteil-Vitry</div>
        </div>
      </div>
      <div class="tl-item">
        <div class="tl-dot">●</div>
        <div>
          <div class="tl-year">2021 — 2024</div>
          <div class="tl-title">Baccalauréat STI2D</div>
          <div class="tl-org">Lycée Maximilien Perret · Alfortville</div>
        </div>
      </div>
    </div>
    <div style="margin-top:1.5rem;padding:1rem;background:rgba(88,198,255,0.06);border:1px solid rgba(88,198,255,0.12);border-radius:12px">
      <div style="font-family:'Share Tech Mono',monospace;font-size:0.65rem;color:var(--route);margin-bottom:0.5rem">VIE &amp; ENGAGEMENTS</div>
      <div style="font-size:0.8rem;color:var(--muted);line-height:1.6">⚽ Football club Maisons-Alfort depuis 2010 · 🤝 Association humanitaire · 🌊 Voyage Essaouira, Maroc</div>
    </div>
  </div>

  <!-- PANEL 5 · CONTACT -->
  <div class="panel" id="panel-contact">
    <div class="panel-badge">✈ ESCALE 05 · CTR · Terminal</div>
    <h2>Prendre <span>Contact</span></h2>
    <div class="panel-divider"></div>
    <div class="board-title">── DÉPARTS DISPONIBLES ──────────────</div>
    <div class="board-grid">
      <a href="tel:0622584724" class="board-card">
        <div class="board-icon">📞</div>
        <div><div class="board-label">TÉLÉPHONE</div><div class="board-val">06 22 58 47 24</div></div>
      </a>
      <a href="mailto:elhissanas@gmail.com" class="board-card">
        <div class="board-icon">✉️</div>
        <div><div class="board-label">EMAIL</div><div class="board-val">elhissanas@gmail.com</div></div>
      </a>
      <a href="https://linkedin.com/in/anas-el-hiss" target="_blank" class="board-card">
        <div class="board-icon">💼</div>
        <div><div class="board-label">LINKEDIN</div><div class="board-val">@anas-el-hiss</div></div>
      </a>
      <div class="board-card" style="cursor:default">
        <div class="board-icon">📍</div>
        <div><div class="board-label">LOCALISATION</div><div class="board-val">Maisons-Alfort (94)</div></div>
      </div>
    </div>
    <div style="margin-top:1.5rem;padding:1rem;background:rgba(88,198,255,0.06);border-radius:12px;border:1px solid rgba(88,198,255,0.1);font-family:'Share Tech Mono',monospace;font-size:0.7rem;color:var(--muted);line-height:2">
      STATUT: DISPONIBLE EN APPRENTISSAGE<br>
      PROCHAIN VOL: BUT2 · 2026–2027<br>
      DESTINATION: SIMULATION EF &amp; VR<br>
      COMPAGNIE: IUT ÉVRY + CFA-EVE
    </div>
  </div>

</div>

<!-- ── SCROLL PROGRESS ── -->
<div id="scroll-progress">
  <div class="scroll-bar"><div class="scroll-fill"></div></div>
  <span class="scroll-pct">0%</span>
</div>

<!-- ── ARRIVAL SCREEN ── -->
<div id="arrival">
  <div class="arrival-status">● DESTINATION ATTEINTE</div>
  <div class="arrival-title">FLIGHT GMP-2028<br>TERMINÉ</div>
  <div class="arrival-sub">Merci d'avoir voyagé à travers mon parcours. Le voyage continue désormais dans le monde professionnel.</div>
  <div style="display:flex;gap:1rem;flex-wrap:wrap;justify-content:center">
    <a href="tel:0622584724" class="btn-board">📞 Appeler</a>
    <a href="mailto:elhissanas@gmail.com" class="btn-board" style="background:linear-gradient(135deg,var(--gold),#f97316)">✉️ Email</a>
  </div>
</div>

<!-- ── MODAL SAÉ ── -->
<div class="modal-overlay" id="modal">
  <div class="modal-box">
    <div class="modal-header">
      <button class="m-close" id="mClose">✕</button>
      <div style="margin-bottom:0.5rem"><span id="m-tag" class="sae-tag"></span>&nbsp;<span style="font-size:0.78rem;color:var(--muted);font-family:'Share Tech Mono',monospace" id="m-sem"></span>&nbsp;<span style="font-size:0.78rem;color:var(--muted)" id="m-ref"></span></div>
      <h3 style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.2rem;margin-bottom:0.4rem" id="m-title"></h3>
      <div style="font-size:0.82rem;color:var(--muted)" id="m-ue"></div>
    </div>
    <div class="modal-body">
      <div class="modal-section"><div class="modal-section-label">Description</div><div class="modal-text" id="m-desc"></div></div>
      <div class="modal-section"><div class="modal-section-label">Objectifs</div><div class="modal-text" id="m-obj"></div></div>
      <div class="modal-section"><div class="modal-section-label">Ressources mobilisées</div><div id="m-res"></div></div>
      <div id="m-extra"></div>
    </div>
  </div>
</div>

<!-- ── LIGHTBOX ── -->
<div class="lightbox" id="lightbox"><img id="lb-img" src="" alt=""></div>

<!-- ── GSAP (must load before ES module) ── -->
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js"></script>

<!-- ── THREE.JS importmap ── -->
<script type="importmap">
{"imports":{"three":"https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.min.js","three/addons/":"https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/"}}
</script>

<script>
// Helper: toggle panels from HUD nav
function showPanel(id) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('visible'));
  const el = document.getElementById(id);
  if (el) el.classList.add('visible');
}
</script>

<!-- ── MAIN 3D MODULE ── -->
<script type="module">
__JS__
</script>

</body>
</html>"""

# ══════════════════════════════════════════════════════════
# STEP 5 — Inject all content
# ══════════════════════════════════════════════════════════
HTML = HTML.replace('__CSS__', CSS)
HTML = HTML.replace('__JS__', JS)
HTML = HTML.replace('__SAE_CARDS__', SAE_CARDS_HTML)
HTML = HTML.replace('__IMG_BLOCK__', IMG_BLOCK)
HTML = HTML.replace('__SAE13_FN__', SAE13_FN)
HTML = HTML.replace('__SAE204_FN__', SAE204_FN)
HTML = HTML.replace('__FONDERIE_FN__', FONDERIE_FN)

with open('/home/user/Portfolio/index.html', 'w', encoding='utf-8') as f:
    f.write(HTML)

print(f"Done — {len(HTML)//1024} KB")
