#!/usr/bin/env python3
import random, re

with open('/home/user/Portfolio/index.html','r',encoding='utf-8') as f:
    old = f.read()

# Extract IMG block
img_s = old.index('const IMG')
img_e = old.index('\n};', img_s) + 3
IMG_BLOCK = old[img_s:img_e]

# Extract JS functions
def between(src, n1, n2):
    s = src.index(f'function {n1}')
    e = src.index(f'function {n2}')
    return src[s:e].rstrip()

SAE13_FN   = between(old,'buildSae13Extra','buildSae204Extra')
SAE204_FN  = between(old,'buildSae204Extra','buildFonderieExtra')
FONDERIE_FN= between(old,'buildFonderieExtra','openModal')

print(f"IMG={len(IMG_BLOCK)} sae13={len(SAE13_FN)} sae204={len(SAE204_FN)} fonderie={len(FONDERIE_FN)}")

# Generate random stars
random.seed(7)
def stars(n):
    return ', '.join(f'{random.randint(1,2560)}px {random.randint(1,1600)}px #fff' for _ in range(n))
S1=stars(700); S2=stars(200); S3=stars(80)

CSS = f"""
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --sky:#020b18;--sky2:#040f22;
  --blue:#4f7cff;--violet:#a855f7;--green:#22c55e;--gold:#f59e0b;
  --text:#e2e8f0;--muted:#64748b;--border:rgba(255,255,255,0.08);
  --card:rgba(255,255,255,0.04);--glass:rgba(10,20,50,0.7);
  --glow-blue:rgba(79,124,255,0.3);
}}
html{{scroll-behavior:smooth}}
body{{
  background:var(--sky);color:var(--text);
  font-family:'DM Sans',sans-serif;font-size:16px;
  overflow-x:hidden;min-height:100vh;
}}

/* ── STARS ── */
.stars{{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0}}
.stars.s1::after{{content:'';position:absolute;inset:0;box-shadow:{S1};border-radius:50%;width:1px;height:1px;animation:twinkle 4s infinite alternate}}
.stars.s2::after{{content:'';position:absolute;inset:0;box-shadow:{S2};border-radius:50%;width:2px;height:2px;animation:twinkle 6s 1s infinite alternate}}
.stars.s3::after{{content:'';position:absolute;inset:0;box-shadow:{S3};border-radius:50%;width:3px;height:3px;animation:twinkle 8s 2s infinite alternate}}
@keyframes twinkle{{0%{{opacity:.4}}100%{{opacity:1}}}}

/* ── CURSOR GLOW ── */
.cursor-glow{{
  position:fixed;width:400px;height:400px;border-radius:50%;
  background:radial-gradient(circle,rgba(79,124,255,0.06) 0%,transparent 70%);
  pointer-events:none;transform:translate(-50%,-50%);z-index:1;transition:opacity .3s;
}}

/* ── NAV ── */
nav{{
  position:fixed;top:0;left:0;right:0;z-index:100;
  background:rgba(2,11,24,0.85);backdrop-filter:blur(16px);
  border-bottom:1px solid var(--border);
  display:flex;align-items:center;justify-content:space-between;
  padding:0 2rem;height:60px;
}}
.nav-brand{{
  font-family:'Share Tech Mono',monospace;font-size:.85rem;
  color:var(--blue);letter-spacing:.15em;
  display:flex;align-items:center;gap:.5rem;
}}
.nav-brand .plane-spin{{display:inline-block;animation:planeSpin 8s linear infinite}}
@keyframes planeSpin{{0%{{transform:rotate(0deg)}}50%{{transform:rotate(15deg)}}100%{{transform:rotate(0deg)}}}}
.nav-links{{display:flex;align-items:center;gap:1.5rem}}
.nav-links a{{
  font-size:.78rem;color:var(--muted);text-decoration:none;
  font-family:'Share Tech Mono',monospace;letter-spacing:.08em;
  text-transform:uppercase;transition:color .2s;
  padding:.25rem .5rem;border-radius:4px;
}}
.nav-links a:hover,.nav-links a.active{{color:var(--blue)}}

/* ── SECTIONS ── */
section{{
  position:relative;z-index:2;
  padding:5rem 2rem;max-width:1100px;margin:0 auto;
}}

/* ── DESTINATION BADGE ── */
.dest-badge{{
  display:inline-flex;align-items:center;gap:.75rem;
  background:rgba(79,124,255,0.1);border:1px solid rgba(79,124,255,0.2);
  border-radius:8px;padding:.5rem 1rem;margin-bottom:2rem;
  font-family:'Share Tech Mono',monospace;font-size:.8rem;
}}
.dest-code{{color:var(--blue);font-size:1.1rem;font-weight:700;letter-spacing:.1em}}
.dest-arrow{{color:var(--muted)}}
.dest-name{{color:var(--muted);letter-spacing:.05em}}
.section-title{{font-family:'Syne',sans-serif;font-size:clamp(1.8rem,4vw,2.8rem);font-weight:800;line-height:1.15;margin-bottom:.5rem}}
.section-title span{{
  background:linear-gradient(135deg,var(--blue),var(--violet));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}}
.divider{{width:60px;height:3px;background:linear-gradient(90deg,var(--blue),var(--violet));border-radius:2px;margin:1rem 0 2.5rem}}

/* ── ROUTE DIVIDER (plane animation) ── */
.route-divider{{
  position:relative;z-index:2;height:80px;overflow:visible;
  display:flex;align-items:center;padding:0 2rem;
  max-width:1300px;margin:0 auto;
}}
.route-line{{
  flex:1;height:1px;
  background:repeating-linear-gradient(90deg,var(--blue) 0,var(--blue) 8px,transparent 8px,transparent 18px);
  opacity:0.25;
}}
.plane-fly{{
  position:absolute;left:0;
  animation:flyAcross 5s linear infinite;
  color:var(--blue);font-size:1.4rem;filter:drop-shadow(0 0 8px var(--blue));
  z-index:3;
}}
@keyframes flyAcross{{
  0%{{left:-60px;opacity:0}}
  5%{{opacity:1}}
  95%{{opacity:1}}
  100%{{left:calc(100% + 60px);opacity:0}}
}}
.route-stop{{
  position:absolute;right:2rem;
  font-family:'Share Tech Mono',monospace;font-size:.7rem;
  color:var(--blue);opacity:.5;letter-spacing:.12em;
}}

/* ══════════════════════════════════════════════
   HERO — BOARDING PASS
══════════════════════════════════════════════ */
#hero{{
  min-height:100vh;display:flex;align-items:center;justify-content:center;
  padding:80px 2rem 2rem;position:relative;overflow:hidden;
  max-width:100%;
}}
#hero canvas{{position:absolute;inset:0;z-index:0}}
.hero-glow{{
  position:absolute;top:20%;left:50%;transform:translateX(-50%);
  width:600px;height:300px;border-radius:50%;
  background:radial-gradient(ellipse,rgba(79,124,255,0.12),transparent 70%);
  pointer-events:none;
}}
.boarding-pass{{
  position:relative;z-index:1;
  display:grid;grid-template-columns:1fr auto;
  background:linear-gradient(135deg,rgba(10,20,48,0.95),rgba(5,12,32,0.98));
  border:1px solid rgba(79,124,255,0.3);border-radius:20px;
  box-shadow:0 0 60px rgba(79,124,255,0.15),0 30px 80px rgba(0,0,0,0.5);
  max-width:800px;width:100%;overflow:hidden;
  animation:boardingIn .8s ease both;
}}
@keyframes boardingIn{{from{{opacity:0;transform:translateY(30px)}}to{{opacity:1;transform:none}}}}
.bp-left{{padding:2.5rem;}}
.bp-right{{
  width:180px;
  border-left:2px dashed rgba(79,124,255,0.25);
  padding:2rem 1.5rem;
  display:flex;flex-direction:column;align-items:center;gap:1.2rem;
  background:rgba(79,124,255,0.04);
}}
.bp-airline{{
  font-family:'Share Tech Mono',monospace;font-size:.7rem;
  letter-spacing:.2em;color:var(--blue);margin-bottom:1rem;
  text-transform:uppercase;
}}
.bp-name{{
  font-family:'Syne',sans-serif;font-weight:800;
  font-size:clamp(1.6rem,4vw,2.4rem);
  background:linear-gradient(135deg,#fff,rgba(79,124,255,.8));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
  margin-bottom:1.5rem;
}}
.bp-route{{
  display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem;
}}
.bp-city{{
  font-family:'Share Tech Mono',monospace;font-size:2.2rem;font-weight:700;
  color:var(--blue);line-height:1;
}}
.bp-city-sub{{font-size:.65rem;color:var(--muted);letter-spacing:.05em;margin-top:.2rem}}
.bp-route-mid{{display:flex;flex-direction:column;align-items:center;gap:.25rem;flex:1}}
.bp-dashes{{
  width:100%;height:1px;
  background:repeating-linear-gradient(90deg,var(--blue) 0,var(--blue) 6px,transparent 6px,transparent 12px);
  opacity:.4;
}}
.bp-plane-icon{{color:var(--blue);font-size:1.2rem;animation:planeBounce 2s ease-in-out infinite}}
@keyframes planeBounce{{0%,100%{{transform:translateY(0) rotate(0)}}50%{{transform:translateY(-4px) rotate(5deg)}}}}
.bp-details{{
  display:flex;gap:1.5rem;margin-bottom:1.5rem;flex-wrap:wrap;
}}
.bp-detail{{display:flex;flex-direction:column;gap:.2rem}}
.bp-detail-label{{font-family:'Share Tech Mono',monospace;font-size:.6rem;color:var(--muted);letter-spacing:.12em}}
.bp-detail-val{{font-size:.95rem;font-weight:600;color:var(--text)}}
.bp-quote{{
  font-style:italic;color:var(--muted);font-size:.88rem;
  border-left:2px solid var(--blue);padding-left:1rem;margin-bottom:1.5rem;
  line-height:1.6;
}}
.bp-btns{{display:flex;gap:.75rem;flex-wrap:wrap}}
.btn-board{{
  padding:.7rem 1.4rem;border-radius:10px;font-size:.85rem;font-weight:600;
  background:linear-gradient(135deg,var(--blue),var(--violet));color:#fff;
  text-decoration:none;transition:transform .2s,box-shadow .2s;
  box-shadow:0 4px 20px rgba(79,124,255,.4);
}}
.btn-board:hover{{transform:translateY(-2px);box-shadow:0 8px 30px rgba(79,124,255,.5)}}
.btn-outline-board{{
  padding:.7rem 1.4rem;border-radius:10px;font-size:.85rem;font-weight:600;
  border:1px solid rgba(79,124,255,.4);color:var(--text);text-decoration:none;
  transition:all .2s;
}}
.btn-outline-board:hover{{background:rgba(79,124,255,.1);border-color:var(--blue)}}

/* stub */
.bp-stub-label{{font-family:'Share Tech Mono',monospace;font-size:.58rem;letter-spacing:.15em;color:var(--muted);text-align:center}}
.bp-stub-flight{{font-family:'Share Tech Mono',monospace;font-size:1.1rem;color:var(--blue);font-weight:700;text-align:center}}
.bp-stub-name{{font-family:'Syne',sans-serif;font-size:.8rem;font-weight:700;text-align:center;color:var(--text)}}
.bp-tags{{display:flex;flex-direction:column;gap:.4rem;width:100%}}
.bp-tag{{
  font-size:.62rem;padding:.3rem .6rem;border-radius:6px;text-align:center;
  background:rgba(79,124,255,.1);border:1px solid rgba(79,124,255,.2);
  color:var(--text);font-family:'Share Tech Mono',monospace;letter-spacing:.05em;
}}
.bp-barcode{{
  display:flex;gap:2px;align-items:flex-end;height:40px;width:100%;justify-content:center;
}}
.bp-barcode span{{
  background:rgba(79,124,255,.6);border-radius:1px;width:2px;
}}
.bp-iut{{
  font-size:.58rem;color:var(--muted);text-align:center;
  font-family:'Share Tech Mono',monospace;line-height:1.5;
}}

/* ══════════════════════════════════════════════
   PROFIL
══════════════════════════════════════════════ */
.profil-grid{{display:grid;grid-template-columns:1fr 340px;gap:3rem;align-items:start}}
.profil-text p{{color:var(--muted);line-height:1.8;margin-bottom:1rem;font-size:.95rem}}
.profil-text p strong{{color:var(--text)}}
.stats-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:1.5rem}}
.stat-card{{
  background:var(--card);border:1px solid var(--border);border-radius:14px;
  padding:1.2rem;text-align:center;
}}
.stat-number{{
  font-family:'Syne',sans-serif;font-size:2.2rem;font-weight:800;
  background:linear-gradient(135deg,var(--blue),var(--violet));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;
}}
.stat-label{{font-size:.75rem;color:var(--muted);margin-top:.25rem;line-height:1.3}}
.profile-card{{
  background:var(--card);border:1px solid var(--border);border-radius:20px;
  padding:2rem;
}}
.profile-avatar{{
  width:64px;height:64px;border-radius:18px;
  background:linear-gradient(135deg,var(--blue),var(--violet));
  display:flex;align-items:center;justify-content:center;
  font-family:'Syne',sans-serif;font-weight:800;font-size:1.6rem;color:#fff;
  box-shadow:0 8px 25px rgba(79,124,255,.4);
}}
.profile-info-row{{display:flex;align-items:center;gap:.75rem;font-size:.9rem;color:var(--muted);margin-bottom:.8rem}}
.profile-info-icon{{font-size:1rem}}
.profile-software{{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1rem}}

/* ══════════════════════════════════════════════
   VIE & ENGAGEMENTS
══════════════════════════════════════════════ */
.vie-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;margin-bottom:2rem}}
.vie-card{{
  background:var(--card);border:1px solid var(--border);border-radius:20px;
  padding:1.8rem;transition:transform .25s,border-color .25s,box-shadow .25s;
}}
.vie-card:hover{{transform:translateY(-4px);border-color:rgba(79,124,255,.3);box-shadow:0 12px 40px rgba(79,124,255,.1)}}
.vie-icon{{font-size:2.5rem;margin-bottom:1rem;display:block}}
.vie-title{{font-family:'Syne',sans-serif;font-weight:700;font-size:1.1rem;margin-bottom:.5rem}}
.vie-sub{{font-size:.8rem;color:var(--blue);margin-bottom:.75rem;font-family:'Share Tech Mono',monospace;letter-spacing:.05em}}
.vie-text{{font-size:.88rem;color:var(--muted);line-height:1.7}}
.vie-city{{
  background:linear-gradient(135deg,rgba(79,124,255,.08),rgba(168,85,247,.08));
  border:1px solid rgba(79,124,255,.15);border-radius:16px;padding:1.5rem 2rem;
  display:flex;align-items:center;gap:2rem;
}}
.vie-city-code{{font-family:'Share Tech Mono',monospace;font-size:3rem;font-weight:700;color:var(--blue);line-height:1}}
.vie-city-info h3{{font-family:'Syne',sans-serif;font-weight:700;font-size:1.1rem;margin-bottom:.25rem}}
.vie-city-info p{{font-size:.85rem;color:var(--muted)}}

/* ══════════════════════════════════════════════
   COMPÉTENCES
══════════════════════════════════════════════ */
.competences-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:1.5rem}}
.comp-card{{
  background:var(--card);border:1px solid var(--border);border-radius:20px;
  padding:1.8rem;transition:transform .25s,box-shadow .25s;
}}
.comp-card:hover{{transform:translateY(-3px);box-shadow:0 10px 35px rgba(0,0,0,.3)}}
.comp-header{{display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem}}
.comp-icon{{
  width:48px;height:48px;border-radius:14px;display:flex;align-items:center;
  justify-content:center;font-size:1.3rem;flex-shrink:0;
}}
.comp-icon-blue{{background:rgba(79,124,255,.15)}}
.comp-icon-violet{{background:rgba(168,85,247,.15)}}
.comp-icon-green{{background:rgba(34,197,94,.15)}}
.comp-icon-gold{{background:rgba(245,158,11,.15)}}
.comp-title{{font-family:'Syne',sans-serif;font-weight:700;font-size:1.05rem}}
.comp-ue{{font-size:.75rem;color:var(--muted)}}
.skill-row{{margin-bottom:.9rem}}
.skill-info{{display:flex;justify-content:space-between;font-size:.82rem;margin-bottom:.35rem;color:var(--muted)}}
.skill-bar{{height:5px;background:rgba(255,255,255,.06);border-radius:3px;overflow:hidden}}
.skill-fill{{height:100%;border-radius:3px;width:0;transition:width 1.2s cubic-bezier(.4,0,.2,1)}}

/* ══════════════════════════════════════════════
   RESSOURCES
══════════════════════════════════════════════ */
.ressources-grid{{display:grid;grid-template-columns:1fr 1fr;gap:2rem}}
.semestre-title{{
  display:flex;align-items:center;gap:.75rem;font-family:'Syne',sans-serif;
  font-weight:700;font-size:1.05rem;margin-bottom:1.2rem;
}}
.semestre-badge{{
  padding:.25rem .7rem;border-radius:8px;font-size:.75rem;font-weight:700;
  font-family:'Share Tech Mono',monospace;
}}
.badge-s1{{background:rgba(79,124,255,.15);color:var(--blue)}}
.badge-s2{{background:rgba(168,85,247,.15);color:var(--violet)}}
.chips-wrap{{display:flex;flex-wrap:wrap;gap:.5rem}}
.chip{{
  padding:.3rem .75rem;border-radius:20px;font-size:.75rem;
  background:rgba(255,255,255,.04);border:1px solid var(--border);
  color:var(--muted);transition:all .2s;cursor:default;
}}
.chip:hover{{background:rgba(79,124,255,.1);border-color:rgba(79,124,255,.3);color:var(--text)}}

/* ══════════════════════════════════════════════
   SAÉ
══════════════════════════════════════════════ */
.sae-section-title{{
  font-family:'Share Tech Mono',monospace;font-size:.75rem;letter-spacing:.2em;
  color:var(--blue);text-transform:uppercase;margin-bottom:1.2rem;margin-top:2rem;
  display:flex;align-items:center;gap:.75rem;
}}
.sae-section-title::after{{content:'';flex:1;height:1px;background:var(--border)}}
.sae-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:1.2rem;margin-bottom:1.5rem}}
.sae-card{{
  background:var(--card);border:1px solid var(--border);border-radius:18px;
  padding:1.5rem;cursor:pointer;transition:all .25s;position:relative;overflow:hidden;
}}
.sae-card::before{{
  content:'';position:absolute;inset:0;
  background:linear-gradient(135deg,rgba(79,124,255,.05),transparent);
  opacity:0;transition:opacity .25s;
}}
.sae-card:hover{{transform:translateY(-4px);border-color:rgba(79,124,255,.3);box-shadow:0 12px 40px rgba(79,124,255,.12)}}
.sae-card:hover::before{{opacity:1}}
.sae-card.featured{{border-color:rgba(79,124,255,.25);background:linear-gradient(135deg,rgba(79,124,255,.06),rgba(168,85,247,.04))}}
.sae-tag{{
  display:inline-block;padding:.2rem .6rem;border-radius:6px;font-size:.68rem;
  font-weight:600;margin-bottom:.75rem;font-family:'Share Tech Mono',monospace;letter-spacing:.04em;
}}
.sae-ue11{{background:rgba(79,124,255,.15);color:var(--blue)}}
.sae-ue12{{background:rgba(168,85,247,.15);color:var(--violet)}}
.sae-ue13{{background:rgba(34,197,94,.15);color:var(--green)}}
.sae-ue14{{background:rgba(245,158,11,.15);color:var(--gold)}}
.sae-ue21{{background:rgba(79,124,255,.12);color:#7aa3ff}}
.sae-ue22{{background:rgba(168,85,247,.12);color:#c084fc}}
.sae-ue23{{background:rgba(34,197,94,.12);color:#4ade80}}
.sae-ue24{{background:rgba(245,158,11,.12);color:#fbbf24}}
.sae-multi{{background:rgba(168,85,247,.12);color:var(--violet)}}
.sae-title{{font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;margin-bottom:.5rem;line-height:1.35}}
.sae-desc{{font-size:.82rem;color:var(--muted);line-height:1.6;margin-bottom:.75rem}}
.sae-resources{{display:flex;flex-wrap:wrap;gap:.35rem;margin-bottom:.75rem}}
.sae-res-chip{{
  padding:.2rem .5rem;border-radius:5px;font-size:.65rem;
  background:rgba(255,255,255,.04);border:1px solid var(--border);color:var(--muted);
}}
.sae-arrow{{
  position:absolute;bottom:1.2rem;right:1.2rem;
  color:var(--blue);font-size:1rem;opacity:.4;transition:all .25s;
}}
.sae-card:hover .sae-arrow{{opacity:1;transform:translate(2px,-2px)}}

/* ══════════════════════════════════════════════
   PARCOURS
══════════════════════════════════════════════ */
.parcours-grid{{display:grid;grid-template-columns:1fr 1fr;gap:3rem}}
.timeline-col-title{{
  font-family:'Share Tech Mono',monospace;font-size:.75rem;letter-spacing:.15em;
  color:var(--muted);text-transform:uppercase;margin-bottom:1.5rem;
}}
.timeline{{position:relative;padding-left:1.5rem}}
.timeline::before{{content:'';position:absolute;left:0;top:0;bottom:0;width:1px;background:var(--border)}}
.timeline-item{{
  position:relative;padding:1.2rem 1.2rem 1.2rem 1.5rem;margin-bottom:1rem;
  background:var(--card);border:1px solid var(--border);border-radius:14px;
  border-left-color:rgba(79,124,255,.3);border-left-width:2px;
}}
.timeline-item::before{{
  content:'';position:absolute;left:-1.75rem;top:1.4rem;
  width:8px;height:8px;border-radius:50%;
  background:var(--blue);box-shadow:0 0 0 3px rgba(79,124,255,.2);
}}
.timeline-date{{font-size:.72rem;color:var(--blue);font-family:'Share Tech Mono',monospace;letter-spacing:.05em;margin-bottom:.35rem}}
.timeline-title{{font-family:'Syne',sans-serif;font-weight:700;font-size:.95rem;margin-bottom:.25rem}}
.timeline-org{{font-size:.8rem;color:var(--muted);margin-bottom:.75rem}}
.timeline-tags{{display:flex;flex-wrap:wrap;gap:.35rem}}
.tl-tag{{
  padding:.2rem .5rem;border-radius:5px;font-size:.65rem;
  background:rgba(79,124,255,.08);border:1px solid rgba(79,124,255,.15);color:var(--muted);
}}

/* ══════════════════════════════════════════════
   PPP
══════════════════════════════════════════════ */
.ppp-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:1.2rem}}
.ppp-card{{
  background:var(--card);border:1px solid var(--border);border-radius:18px;padding:1.8rem;
  transition:transform .25s,border-color .25s;
}}
.ppp-card:hover{{transform:translateY(-3px);border-color:rgba(79,124,255,.25)}}
.ppp-icon{{font-size:1.8rem;margin-bottom:.75rem;display:block}}
.ppp-title{{font-family:'Syne',sans-serif;font-weight:700;font-size:1rem;margin-bottom:.5rem}}
.ppp-text{{font-size:.86rem;color:var(--muted);line-height:1.7}}

/* ══════════════════════════════════════════════
   OUVERTURE
══════════════════════════════════════════════ */
.ouv-quote{{
  background:linear-gradient(135deg,rgba(79,124,255,.08),rgba(168,85,247,.06));
  border:1px solid rgba(79,124,255,.15);border-radius:18px;
  padding:2rem;margin-bottom:2.5rem;
}}
.ouv-quote p{{font-style:italic;color:var(--muted);line-height:1.8;font-size:.95rem}}
.ouv-quote cite{{display:block;margin-top:.75rem;font-size:.8rem;color:var(--blue);font-family:'Share Tech Mono',monospace}}
.ouv-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem;margin-bottom:2.5rem}}
.ouv-card{{
  background:var(--card);border:1px solid var(--border);border-radius:18px;padding:1.6rem;
  transition:transform .25s;
}}
.ouv-card:hover{{transform:translateY(-3px)}}
.ouv-card-icon{{font-size:1.8rem;margin-bottom:.75rem}}
.ouv-card-title{{font-family:'Syne',sans-serif;font-weight:700;font-size:.95rem;margin-bottom:.5rem}}
.ouv-card-text{{font-size:.83rem;color:var(--muted);line-height:1.6}}
.roadmap{{display:grid;grid-template-columns:repeat(4,1fr);gap:1rem}}
.roadmap-item{{
  background:var(--card);border:1px solid var(--border);border-radius:14px;
  padding:1.2rem;position:relative;
}}
.roadmap-item::before{{
  content:'';position:absolute;top:50%;left:-1rem;width:1rem;height:1px;
  background:var(--border);
}}
.roadmap-item:first-child::before{{display:none}}
.roadmap-year{{
  font-family:'Share Tech Mono',monospace;font-size:.8rem;color:var(--blue);
  margin-bottom:.5rem;
}}
.roadmap-text{{font-size:.78rem;color:var(--muted);line-height:1.5}}

/* ══════════════════════════════════════════════
   CONTACT
══════════════════════════════════════════════ */
#contact{{text-align:center}}
.contact-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:1.2rem;max-width:600px;margin:2rem auto 0;text-align:left}}
.contact-card{{
  background:var(--card);border:1px solid var(--border);border-radius:18px;
  padding:1.5rem;display:flex;align-items:center;gap:1rem;
  text-decoration:none;color:var(--text);transition:all .25s;
}}
.contact-card:hover{{border-color:rgba(79,124,255,.4);background:rgba(79,124,255,.06);transform:translateY(-2px)}}
.contact-icon{{
  width:44px;height:44px;border-radius:12px;
  background:rgba(79,124,255,.12);display:flex;align-items:center;justify-content:center;
  font-size:1.2rem;flex-shrink:0;
}}
.contact-label{{font-size:.7rem;color:var(--muted);font-family:'Share Tech Mono',monospace;letter-spacing:.08em;margin-bottom:.2rem}}
.contact-val{{font-size:.88rem;font-weight:500}}

/* ══════════════════════════════════════════════
   FOOTER
══════════════════════════════════════════════ */
footer{{
  text-align:center;padding:2rem;color:var(--muted);font-size:.78rem;
  border-top:1px solid var(--border);position:relative;z-index:2;
  font-family:'Share Tech Mono',monospace;letter-spacing:.05em;
}}

/* ══════════════════════════════════════════════
   TAG CHIPS (hero)
══════════════════════════════════════════════ */
.tag{{
  padding:.3rem .8rem;border-radius:20px;font-size:.75rem;font-weight:500;
  font-family:'Share Tech Mono',monospace;
}}
.tag-blue{{background:rgba(79,124,255,.12);border:1px solid rgba(79,124,255,.25);color:var(--blue)}}
.tag-violet{{background:rgba(168,85,247,.12);border:1px solid rgba(168,85,247,.25);color:var(--violet)}}
.tag-green{{background:rgba(34,197,94,.12);border:1px solid rgba(34,197,94,.25);color:var(--green)}}
.tag-gold{{background:rgba(245,158,11,.12);border:1px solid rgba(245,158,11,.25);color:var(--gold)}}

/* ══════════════════════════════════════════════
   MODAL
══════════════════════════════════════════════ */
.modal-overlay{{
  position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:1000;
  display:flex;align-items:center;justify-content:center;padding:1.5rem;
  opacity:0;pointer-events:none;transition:opacity .25s;
}}
.modal-overlay.open{{opacity:1;pointer-events:all}}
.modal-box{{
  background:var(--sky2);border:1px solid var(--border);border-radius:24px;
  width:100%;max-width:780px;max-height:90vh;overflow-y:auto;
  position:relative;transform:translateY(20px);transition:transform .25s;
}}
.modal-overlay.open .modal-box{{transform:none}}
.modal-header{{padding:2rem 2rem 1.5rem;border-bottom:1px solid var(--border);position:sticky;top:0;background:var(--sky2);z-index:1}}
.modal-body{{padding:2rem}}
.modal-section{{margin-bottom:2rem}}
.modal-section-label{{
  font-family:'Share Tech Mono',monospace;font-size:.7rem;letter-spacing:.15em;
  color:var(--blue);text-transform:uppercase;margin-bottom:.75rem;
}}
.modal-text{{font-size:.88rem;color:var(--muted);line-height:1.7}}
.m-close{{
  position:absolute;top:1.2rem;right:1.5rem;
  background:none;border:1px solid var(--border);border-radius:8px;
  color:var(--muted);cursor:pointer;padding:.4rem .7rem;font-size:1rem;
  transition:all .2s;
}}
.m-close:hover{{color:var(--text);border-color:var(--text)}}
.gallery-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:.75rem;margin-top:.75rem}}
.gallery-item{{
  border-radius:12px;overflow:hidden;cursor:pointer;background:rgba(255,255,255,.03);
  border:1px solid var(--border);transition:transform .2s;
}}
.gallery-item:hover{{transform:scale(1.02)}}
.gallery-item img{{width:100%;height:140px;object-fit:cover;display:block}}
.gallery-full{{grid-column:1/-1}}
.gallery-full img{{height:200px}}
.gallery-item-label{{padding:.5rem .75rem;font-size:.72rem;color:var(--muted)}}
.data-table{{width:100%;border-collapse:collapse;font-size:.82rem}}
.data-table th,.data-table td{{padding:.6rem .8rem;border-bottom:1px solid var(--border);text-align:left}}
.data-table th{{color:var(--muted);font-size:.7rem;text-transform:uppercase;letter-spacing:.08em;font-weight:600}}
.data-table td{{color:var(--text)}}
.process-steps{{display:flex;flex-direction:column;gap:.75rem}}
.process-step{{display:flex;gap:1rem;align-items:flex-start}}
.step-num{{
  width:28px;height:28px;border-radius:50%;background:linear-gradient(135deg,var(--blue),var(--violet));
  display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:700;
  flex-shrink:0;margin-top:.1rem;
}}
.step-title{{font-weight:600;font-size:.88rem;margin-bottom:.2rem}}
.step-desc{{font-size:.8rem;color:var(--muted);line-height:1.5}}
#m-res{{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.5rem}}

/* ── LIGHTBOX ── */
.lightbox{{
  position:fixed;inset:0;background:rgba(0,0,0,.95);z-index:2000;
  display:flex;align-items:center;justify-content:center;
  opacity:0;pointer-events:none;transition:opacity .2s;cursor:zoom-out;
}}
.lightbox.open{{opacity:1;pointer-events:all}}
.lightbox img{{max-width:90vw;max-height:90vh;border-radius:8px;object-fit:contain}}

/* ── REVEAL ── */
.reveal{{opacity:0;transform:translateY(24px);transition:opacity .6s,transform .6s}}
.reveal.in{{opacity:1;transform:none}}

/* ── RESPONSIVE ── */
@media(max-width:900px){{
  .boarding-pass{{grid-template-columns:1fr;}}
  .bp-right{{width:100%;border-left:none;border-top:2px dashed rgba(79,124,255,.25);flex-direction:row;flex-wrap:wrap;}}
  .profil-grid,.competences-grid,.parcours-grid,.ressources-grid,.ouv-grid,.roadmap{{grid-template-columns:1fr}}
  .vie-grid,.ppp-grid,.contact-grid{{grid-template-columns:1fr}}
  .sae-grid{{grid-template-columns:1fr}}
}}
@media(max-width:600px){{
  nav{{padding:0 1rem}}
  .nav-links a{{display:none}}
  section{{padding:3.5rem 1rem}}
}}
"""

# Generate barcode bars
bars = ''.join(f'<span style="height:{random.randint(20,40)}px"></span>' for _ in range(40))

HTML = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Anas El Hiss · Portfolio GMP SNRV</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=Share+Tech+Mono&display=swap">
<style>{CSS}</style>
</head>
<body>

<!-- Stars -->
<div class="stars s1"></div>
<div class="stars s2"></div>
<div class="stars s3"></div>
<div class="cursor-glow" id="glow"></div>

<!-- ══ NAV ══ -->
<nav id="nav">
  <div class="nav-brand"><span class="plane-spin">✈</span>&nbsp;AEH · PORTFOLIO</div>
  <div class="nav-links">
    <a href="#hero">Embarquement</a>
    <a href="#profil">Profil</a>
    <a href="#vie">Vie</a>
    <a href="#competences">Skills</a>
    <a href="#sae">SAÉ</a>
    <a href="#parcours">Parcours</a>
    <a href="#ppp">PPP</a>
    <a href="#ouverture">Avenir</a>
    <a href="#contact">Contact</a>
  </div>
</nav>

<!-- ══ HERO — BOARDING PASS ══ -->
<section id="hero">
  <canvas id="particles"></canvas>
  <div class="hero-glow"></div>
  <div class="boarding-pass">
    <div class="bp-left">
      <div class="bp-airline">✈ &nbsp;PORTFOLIO · BOARDING PASS &nbsp;·&nbsp; GMP SNRV 2025–2028</div>
      <div class="bp-name">Anas El Hiss</div>
      <div class="bp-route">
        <div>
          <div class="bp-city">MAF</div>
          <div class="bp-city-sub">Maisons-Alfort</div>
        </div>
        <div class="bp-route-mid">
          <div class="bp-plane-icon">✈</div>
          <div class="bp-dashes"></div>
        </div>
        <div style="text-align:right">
          <div class="bp-city">IND</div>
          <div class="bp-city-sub">Industrie</div>
        </div>
      </div>
      <div class="bp-details">
        <div class="bp-detail"><div class="bp-detail-label">VOL</div><div class="bp-detail-val">AEH-2028</div></div>
        <div class="bp-detail"><div class="bp-detail-label">CLASSE</div><div class="bp-detail-val">BUT GMP</div></div>
        <div class="bp-detail"><div class="bp-detail-label">SIÈGE</div><div class="bp-detail-val">SNRV</div></div>
        <div class="bp-detail"><div class="bp-detail-label">DÉPART</div><div class="bp-detail-val">Oct. 2025</div></div>
      </div>
      <div class="bp-quote">"La précision est une philosophie, pas seulement une exigence technique."</div>
      <div class="bp-btns">
        <a href="#contact" class="btn-board">Me contacter</a>
        <a href="#sae" class="btn-outline-board">Voir mes SAÉ</a>
      </div>
    </div>
    <div class="bp-right">
      <div class="bp-stub-label">COUPON PASSAGER</div>
      <div class="bp-stub-name">EL HISS / ANAS</div>
      <div class="bp-stub-flight">VOL AEH-2028</div>
      <div class="bp-tags">
        <span class="bp-tag">SolidWorks</span>
        <span class="bp-tag">3DExperience</span>
        <span class="bp-tag">CAO / DAO</span>
        <span class="bp-tag">SNRV</span>
        <span class="bp-tag">Apprentissage</span>
      </div>
      <div class="bp-barcode">{bars}</div>
      <div class="bp-iut">IUT Évry-Val-d'Essonne<br>CFA-EVE · Promo 2025–2028</div>
    </div>
  </div>
</section>

<!-- ROUTE DIVIDER -->
<div class="route-divider"><div class="route-line"></div><div class="plane-fly">✈</div><div class="route-stop">PRF · 01</div></div>

<!-- ══ PROFIL ══ -->
<section id="profil">
  <div class="dest-badge reveal"><span class="dest-code">PRF</span><span class="dest-arrow">→</span><span class="dest-name">Profil Voyageur</span></div>
  <h2 class="section-title reveal">Mon <span>Profil</span></h2>
  <div class="divider reveal"></div>
  <div class="profil-grid">
    <div class="profil-text reveal">
      <p>Étudiant en première année de BUT Génie Mécanique et Productique (parcours SNRV), je suis en apprentissage chez <strong>Losange</strong> depuis octobre 2025 en tant qu'opérateur-régleur joaillerie.</p>
      <p>Passionné par la conception assistée par ordinateur, la modélisation 3D et les méthodes de fabrication, je développe des compétences solides à travers des SAÉ concrètes couvrant les quatre blocs de compétences du BUT GMP.</p>
      <p>Mon objectif : maîtriser les outils numériques de l'ingénieur (SolidWorks, 3DExperience) et m'orienter vers la simulation numérique et la réalité virtuelle appliquées à l'industrie.</p>
      <div class="stats-grid">
        <div class="stat-card"><div class="stat-number" data-target="4">0</div><div class="stat-label">Blocs de<br>compétences</div></div>
        <div class="stat-card"><div class="stat-number" data-target="9">0</div><div class="stat-label">SAÉ<br>réalisées</div></div>
        <div class="stat-card"><div class="stat-number" data-target="3">0</div><div class="stat-label">Années de<br>formation</div></div>
      </div>
    </div>
    <div class="reveal" style="transition-delay:.15s">
      <div class="profile-card">
        <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.5rem">
          <div class="profile-avatar">A</div>
          <div>
            <div style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.1rem">Anas El Hiss</div>
            <div style="font-size:.82rem;color:var(--muted)">BUT GMP SNRV · 1ère année</div>
          </div>
        </div>
        <div class="profile-info-row"><span class="profile-info-icon">📍</span><span>Maisons-Alfort (94)</span></div>
        <div class="profile-info-row"><span class="profile-info-icon">🎓</span><span>IUT Évry-Val-d'Essonne / CFA-EVE</span></div>
        <div class="profile-info-row"><span class="profile-info-icon">🏭</span><span>Apprenti Opérateur-Régleur · Losange</span></div>
        <div class="profile-info-row"><span class="profile-info-icon">📅</span><span>Promotion 2025–2028</span></div>
        <div style="margin-top:1rem;padding-top:1rem;border-top:1px solid var(--border)">
          <div style="font-size:.72rem;color:var(--muted);margin-bottom:.6rem;text-transform:uppercase;letter-spacing:.1em">Logiciels</div>
          <div class="profile-software">
            <span class="tag tag-blue" style="font-size:.72rem">SolidWorks</span>
            <span class="tag tag-violet" style="font-size:.72rem">3DExperience</span>
            <span class="tag tag-green" style="font-size:.72rem">CAO/DAO</span>
            <span class="tag tag-gold" style="font-size:.72rem">Catia</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ROUTE DIVIDER -->
<div class="route-divider"><div class="route-line"></div><div class="plane-fly" style="animation-delay:-2s">✈</div><div class="route-stop">VIE · 02</div></div>

<!-- ══ VIE & ENGAGEMENTS ══ -->
<section id="vie">
  <div class="dest-badge reveal"><span class="dest-code">VIE</span><span class="dest-arrow">→</span><span class="dest-name">Escales Personnelles</span></div>
  <h2 class="section-title reveal">Vie &amp; <span>Engagements</span></h2>
  <div class="divider reveal"></div>
  <div class="vie-grid">
    <div class="vie-card reveal">
      <span class="vie-icon">⚽</span>
      <div class="vie-title">Football en club</div>
      <div class="vie-sub">MAF FC · Depuis 2010</div>
      <div class="vie-text">Licencié dans un club de football à Maisons-Alfort depuis l'âge de 10 ans. Plus de 15 ans de pratique en équipe, une école de discipline, d'effort collectif et de dépassement de soi. Le terrain m'a autant formé que la classe.</div>
    </div>
    <div class="vie-card reveal" style="transition-delay:.1s">
      <span class="vie-icon">🤝</span>
      <div class="vie-title">Association humanitaire</div>
      <div class="vie-sub">Bénévolat · Engagement citoyen</div>
      <div class="vie-text">Membre actif d'une association humanitaire. Cet engagement m'a appris à mettre mes compétences au service des autres et à sortir de ma zone de confort. Une expérience qui donne du sens à ce que je construis techniquement.</div>
    </div>
    <div class="vie-card reveal" style="transition-delay:.2s">
      <span class="vie-icon">🌊</span>
      <div class="vie-title">Voyage à Essaouira</div>
      <div class="vie-sub">Maroc · Mission humanitaire</div>
      <div class="vie-text">Voyage en lien avec mon association au Maroc, dans la ville d'Essaouira. Une rencontre avec d'autres réalités, d'autres cultures. Ce voyage m'a ouvert les yeux sur le monde et renforcé mon sens des responsabilités.</div>
    </div>
  </div>
  <div class="vie-city reveal">
    <div class="vie-city-code">MAF</div>
    <div class="vie-city-info">
      <h3>Maisons-Alfort, ma ville</h3>
      <p>Val-de-Marne (94) · Île-de-France · C'est ici que tout a commencé — le foot, les amitiés, l'engagement. Une ville qui m'a façonné autant que mes études.</p>
    </div>
  </div>
</section>

<!-- ROUTE DIVIDER -->
<div class="route-divider"><div class="route-line"></div><div class="plane-fly" style="animation-delay:-1s">✈</div><div class="route-stop">SKL · 03</div></div>

<!-- ══ COMPÉTENCES ══ -->
<section id="competences">
  <div class="dest-badge reveal"><span class="dest-code">SKL</span><span class="dest-arrow">→</span><span class="dest-name">Équipement du Voyageur</span></div>
  <h2 class="section-title reveal">Blocs de <span>Compétences</span></h2>
  <div class="divider reveal"></div>
  <div class="competences-grid">
    <div class="comp-card reveal">
      <div class="comp-header"><div class="comp-icon comp-icon-blue">🔍</div><div><div class="comp-title">Spécifier</div><div class="comp-ue">UE11 · UE21</div></div></div>
      <div class="skill-row"><div class="skill-info"><span>Analyse fonctionnelle</span></div><div class="skill-bar"><div class="skill-fill" style="background:linear-gradient(90deg,var(--blue),var(--violet))" data-w="75"></div></div></div>
      <div class="skill-row"><div class="skill-info"><span>Expression du besoin</span></div><div class="skill-bar"><div class="skill-fill" style="background:linear-gradient(90deg,var(--blue),var(--violet))" data-w="70"></div></div></div>
      <div class="skill-row"><div class="skill-info"><span>Cahier des charges</span></div><div class="skill-bar"><div class="skill-fill" style="background:linear-gradient(90deg,var(--blue),var(--violet))" data-w="65"></div></div></div>
    </div>
    <div class="comp-card reveal" style="transition-delay:.1s">
      <div class="comp-header"><div class="comp-icon comp-icon-violet">⚙️</div><div><div class="comp-title">Développer</div><div class="comp-ue">UE12 · UE22</div></div></div>
      <div class="skill-row"><div class="skill-info"><span>CAO / Modélisation 3D</span></div><div class="skill-bar"><div class="skill-fill" style="background:linear-gradient(90deg,var(--violet),var(--blue))" data-w="80"></div></div></div>
      <div class="skill-row"><div class="skill-info"><span>SolidWorks / 3DExperience</span></div><div class="skill-bar"><div class="skill-fill" style="background:linear-gradient(90deg,var(--violet),var(--blue))" data-w="75"></div></div></div>
      <div class="skill-row"><div class="skill-info"><span>Simulation numérique</span></div><div class="skill-bar"><div class="skill-fill" style="background:linear-gradient(90deg,var(--violet),var(--blue))" data-w="60"></div></div></div>
    </div>
    <div class="comp-card reveal" style="transition-delay:.15s">
      <div class="comp-header"><div class="comp-icon comp-icon-green">🏭</div><div><div class="comp-title">Réaliser</div><div class="comp-ue">UE13 · UE23</div></div></div>
      <div class="skill-row"><div class="skill-info"><span>Fabrication / Usinage</span></div><div class="skill-bar"><div class="skill-fill" style="background:linear-gradient(90deg,var(--green),var(--blue))" data-w="72"></div></div></div>
      <div class="skill-row"><div class="skill-info"><span>Métrologie</span></div><div class="skill-bar"><div class="skill-fill" style="background:linear-gradient(90deg,var(--green),var(--blue))" data-w="65"></div></div></div>
      <div class="skill-row"><div class="skill-info"><span>Prototypage rapide</span></div><div class="skill-bar"><div class="skill-fill" style="background:linear-gradient(90deg,var(--green),var(--blue))" data-w="68"></div></div></div>
    </div>
    <div class="comp-card reveal" style="transition-delay:.2s">
      <div class="comp-header"><div class="comp-icon comp-icon-gold">📊</div><div><div class="comp-title">Piloter</div><div class="comp-ue">UE14 · UE24</div></div></div>
      <div class="skill-row"><div class="skill-info"><span>Gestion de production</span></div><div class="skill-bar"><div class="skill-fill" style="background:linear-gradient(90deg,var(--gold),var(--green))" data-w="65"></div></div></div>
      <div class="skill-row"><div class="skill-info"><span>Organisation industrielle</span></div><div class="skill-bar"><div class="skill-fill" style="background:linear-gradient(90deg,var(--gold),var(--green))" data-w="60"></div></div></div>
      <div class="skill-row"><div class="skill-info"><span>Lean / Amélioration continue</span></div><div class="skill-bar"><div class="skill-fill" style="background:linear-gradient(90deg,var(--gold),var(--green))" data-w="55"></div></div></div>
    </div>
  </div>
</section>

<!-- ROUTE DIVIDER -->
<div class="route-divider"><div class="route-line"></div><div class="plane-fly" style="animation-delay:-3s">✈</div><div class="route-stop">RES · 04</div></div>

<!-- ══ RESSOURCES ══ -->
<section id="ressources">
  <div class="dest-badge reveal"><span class="dest-code">RES</span><span class="dest-arrow">→</span><span class="dest-name">Bagages Pédagogiques</span></div>
  <h2 class="section-title reveal">Ressources <span>Pédagogiques</span></h2>
  <div class="divider reveal"></div>
  <div class="ressources-grid">
    <div class="reveal">
      <div class="semestre-title"><span class="semestre-badge badge-s1">S1</span> Semestre 1</div>
      <div class="chips-wrap">
        <span class="chip">R1.01 Mécanique</span><span class="chip">R1.03 Science des matériaux</span>
        <span class="chip">R1.04 Maths &amp; outils scientifiques</span><span class="chip">R1.05 Ingénierie de construction mécanique</span>
        <span class="chip">R1.06 Outils pour l'ingénierie</span><span class="chip">R1.07 Production · Méthodes</span>
        <span class="chip">R1.08 Métrologie</span><span class="chip">R1.10 Systèmes cyberphysiques</span>
        <span class="chip">R1.13 Expression · Communication</span><span class="chip">R1.14 Langues</span><span class="chip">R1.15 PPP</span>
      </div>
    </div>
    <div class="reveal" style="transition-delay:.15s">
      <div class="semestre-title"><span class="semestre-badge badge-s2">S2</span> Semestre 2</div>
      <div class="chips-wrap">
        <span class="chip">R2.01 Mécanique</span><span class="chip">R2.02 Dimensionnement des structures</span>
        <span class="chip">R2.03 Science des matériaux</span><span class="chip">R2.04 Maths</span>
        <span class="chip">R2.05 Ingénierie construction mécanique</span><span class="chip">R2.06 Outils pour l'ingénierie</span>
        <span class="chip">R2.07 Production · Méthodes</span><span class="chip">R2.08 Métrologie</span>
        <span class="chip">R2.09 Organisation et pilotage industriel</span><span class="chip">R2.10 Systèmes cyberphysiques</span>
        <span class="chip">R2.12 Informatique &amp; BDD</span><span class="chip">R2.13 Expression · Communication</span>
        <span class="chip">R2.14 Langues</span><span class="chip">R2.15 PPP</span>
        <span class="chip" style="color:var(--gold);border-color:rgba(245,158,11,.4);background:rgba(245,158,11,.08)">POR2 Portfolio</span>
      </div>
    </div>
  </div>
</section>

<!-- ROUTE DIVIDER -->
<div class="route-divider"><div class="route-line"></div><div class="plane-fly" style="animation-delay:-1.5s">✈</div><div class="route-stop">SAÉ · 05</div></div>

<!-- ══ SAÉ ══ -->
<section id="sae">
  <div class="dest-badge reveal"><span class="dest-code">SAÉ</span><span class="dest-arrow">→</span><span class="dest-name">Missions de Terrain</span></div>
  <h2 class="section-title reveal">Mes <span>SAÉ</span></h2>
  <div class="divider reveal"></div>

  <div class="sae-section-title reveal">Semestre 1</div>
  <div class="sae-grid">
    <div class="sae-card reveal" data-sae="1" data-sem="Semestre 1" data-ref="SAÉ 1.1" data-ue="UE11 — Spécifier" data-title="Analyse d'un produit grand public" data-desc="Analyser un produit de grande consommation pour identifier ses fonctions, sa structure et les matériaux. Rédiger un dossier d'analyse fonctionnelle et technique structuré." data-res="R1.03, R1.04, R1.07, R1.10, R1.13, R1.14" data-obj="Identifier et analyser les fonctions d'un produit existant. Mettre en œuvre les méthodes d'analyse de la valeur et de décomposition fonctionnelle.">
      <span class="sae-tag sae-ue11">UE11 — Spécifier</span>
      <div class="sae-title">Analyse d'un produit grand public</div>
      <div class="sae-desc">Analyse fonctionnelle et technique d'un produit de grande consommation.</div>
      <div class="sae-resources"><span class="sae-res-chip">R1.03</span><span class="sae-res-chip">R1.04</span><span class="sae-res-chip">R1.07</span><span class="sae-res-chip">R1.10</span></div>
      <span class="sae-arrow">↗</span>
    </div>
    <div class="sae-card reveal" data-sae="2" data-sem="Semestre 1" data-ref="SAÉ 1.2" data-ue="UE12 — Développer" data-title="Modification d'un système mécanique" data-desc="Proposer et modéliser une modification sur un système mécanique existant en utilisant des outils de CAO. Justifier les choix techniques par des calculs et des simulations." data-res="R1.01, R1.04, R1.05, R1.06" data-obj="Maîtriser les outils CAO pour modifier un mécanisme existant. Justifier les choix de conception par le calcul mécanique.">
      <span class="sae-tag sae-ue12">UE12 — Développer</span>
      <div class="sae-title">Modification d'un système mécanique</div>
      <div class="sae-desc">Modélisation CAO et justification des modifications sur un système existant.</div>
      <div class="sae-resources"><span class="sae-res-chip">R1.01</span><span class="sae-res-chip">R1.04</span><span class="sae-res-chip">R1.05</span><span class="sae-res-chip">R1.06</span></div>
      <span class="sae-arrow">↗</span>
    </div>
    <div class="sae-card featured reveal" data-sae="3" data-sem="Semestre 1" data-ref="SAÉ 1.3" data-ue="UE13 — Réaliser" data-title="De la maquette numérique au prototype physique" data-desc="Conception d'une pièce centrale de bras articulé sur SolidWorks, préparation du contrat de phase, choix du matériau (AlSi10Mg EN AC-43000) et fabrication du prototype. Analyse des sollicitations mécaniques et justification industrielle." data-res="R1.05, R1.06, R1.07, R1.08" data-obj="Maîtriser la chaîne numérique complète : CAO → contrat de phase → fabrication → contrôle métrologique. Raisonner comme un bureau d'études en intégrant les contraintes industrielles." data-has-gallery="1">
      <span class="sae-tag sae-ue13">UE13 — Réaliser</span>
      <div class="sae-title">De la maquette numérique au prototype physique</div>
      <div class="sae-desc">Conception bras articulé, AlSi10Mg, contrat de phase, fabrication. Rapport complet avec visuels SolidWorks.</div>
      <div class="sae-resources"><span class="sae-res-chip">R1.05</span><span class="sae-res-chip">R1.06</span><span class="sae-res-chip">R1.07</span><span class="sae-res-chip">R1.08</span></div>
      <span class="sae-arrow">↗</span>
    </div>
    <div class="sae-card reveal" data-sae="4" data-sem="Semestre 1" data-ref="SAÉ 1.4" data-ue="UE14 — Piloter" data-title="Découverte des métiers" data-desc="Explorer les différents métiers du GMP à travers des rencontres professionnelles et visites d'entreprises. Construire son projet professionnel." data-res="R1.13, R1.14, R1.15" data-obj="Identifier les débouchés accessibles après le BUT GMP et construire les premières bases de son PPP.">
      <span class="sae-tag sae-ue14">UE14 — Piloter</span>
      <div class="sae-title">Découverte des métiers</div>
      <div class="sae-desc">Rencontres professionnelles et premières bases du projet professionnel.</div>
      <div class="sae-resources"><span class="sae-res-chip">R1.13</span><span class="sae-res-chip">R1.14</span><span class="sae-res-chip">R1.15</span></div>
      <span class="sae-arrow">↗</span>
    </div>
  </div>

  <div class="sae-section-title reveal">Semestre 2</div>
  <div class="sae-grid">
    <div class="sae-card reveal" data-sae="5" data-sem="Semestre 2" data-ref="SAÉ 2.01" data-ue="UE21 — Spécifier" data-title="Spécification des processus d'élaboration d'une pièce" data-desc="Analyser une pièce et définir les processus d'élaboration : choix des procédés, gamme de fabrication, spécifications dimensionnelles et géométriques." data-res="R2.03, R2.06, R2.07, R2.13, POR2" data-obj="Spécifier un processus de fabrication en tenant compte des contraintes matériaux, géométriques et économiques.">
      <span class="sae-tag sae-ue21">UE21 — Spécifier</span>
      <div class="sae-title">Spécification des processus d'élaboration d'une pièce</div>
      <div class="sae-desc">Gamme de fabrication, procédés et spécifications dimensionnelles.</div>
      <div class="sae-resources"><span class="sae-res-chip">R2.03</span><span class="sae-res-chip">R2.06</span><span class="sae-res-chip">R2.07</span><span class="sae-res-chip">POR2</span></div>
      <span class="sae-arrow">↗</span>
    </div>
    <div class="sae-card reveal" data-sae="6" data-sem="Semestre 2" data-ref="SAÉ 2.02" data-ue="UE22 — Développer" data-title="Implantation d'un îlot robotisé de production" data-desc="Concevoir et simuler l'implantation d'un îlot robotisé : choix des équipements, programmation du robot, optimisation du flux de production." data-res="R2.01, R2.05, R2.09, R2.10, POR2" data-obj="Concevoir une cellule robotisée intégrée, programmer un robot industriel et évaluer la performance de la solution.">
      <span class="sae-tag sae-ue22">UE22 — Développer</span>
      <div class="sae-title">Implantation d'un îlot robotisé de production</div>
      <div class="sae-desc">Conception, simulation et programmation d'un îlot robotisé industriel.</div>
      <div class="sae-resources"><span class="sae-res-chip">R2.01</span><span class="sae-res-chip">R2.05</span><span class="sae-res-chip">R2.09</span><span class="sae-res-chip">R2.10</span></div>
      <span class="sae-arrow">↗</span>
    </div>
    <div class="sae-card reveal" data-sae="7" data-sem="Semestre 2" data-ref="SAÉ 2.03" data-ue="UE23 — Réaliser" data-title="Fabrication d'une pièce unitaire" data-desc="Réaliser une pièce unitaire de précision sur machine-outil selon le dessin de définition. Contrôle métrologique de conformité. Inclut les TP de fonderie R2.07 : moulage en sable de l'alliage AS13, analyse du diagramme Al-Si, étude des défauts." data-res="R2.05, R2.06, R2.07, R2.08, POR2" data-obj="Maîtriser la réalisation complète d'une pièce unitaire, de la préparation à la vérification métrologique finale." data-has-fonderie="1">
      <span class="sae-tag sae-ue23">UE23 — Réaliser</span>
      <div class="sae-title">Fabrication d'une pièce unitaire</div>
      <div class="sae-desc">Usinage de précision + TP fonderie AS13 moulage sable. Contrôle métrologique.</div>
      <div class="sae-resources"><span class="sae-res-chip">R2.05</span><span class="sae-res-chip">R2.06</span><span class="sae-res-chip">R2.07</span><span class="sae-res-chip">R2.08</span></div>
      <span class="sae-arrow">↗</span>
    </div>
    <div class="sae-card reveal" data-sae="8" data-sem="Semestre 2" data-ref="SAÉ 2.04" data-ue="UE24 — Piloter" data-title="Piloter une production stabilisée" data-desc="OPI FA — Étude chez SMP BALTZER : gestion d'une commande de 70 pointes tournantes T301. Processus de fabrication, calcul coût prévisionnel/devis, ordonnancement Gantt, management de la production et communication client." data-res="R2.09, R2.12, R2.13, R2.14, POR2" data-obj="Piloter une production en tant que responsable d'atelier : établir un processus industriel, calculer un devis complet (TVA 19,6%, marge 20%), planifier la production sur diagramme de Gantt, et communiquer avec les équipes et clients." data-has-sae204="1">
      <span class="sae-tag sae-ue24">UE24 — Piloter</span>
      <div class="sae-title">Piloter une production stabilisée</div>
      <div class="sae-desc">OPI FA · SMP BALTZER — 70 pointes tournantes T301, Gantt, devis, management.</div>
      <div class="sae-resources"><span class="sae-res-chip">R2.09</span><span class="sae-res-chip">R2.12</span><span class="sae-res-chip">R2.13</span><span class="sae-res-chip">R2.14</span></div>
      <span class="sae-arrow">↗</span>
    </div>
    <div class="sae-card reveal" data-sae="9" data-sem="Semestre 2" data-ref="SAÉ 2.05" data-ue="UE22 + UE23" data-title="Conception d'une pièce de sécurité en traction" data-desc="Concevoir et dimensionner une pièce soumise à traction. Simulation numérique par éléments finis et validation de la conception." data-res="R2.01, R2.02, R2.05, POR2" data-obj="Concevoir une pièce de sécurité en intégrant le calcul RDM, la simulation EF et les normes de sécurité.">
      <span class="sae-tag sae-multi">UE22 + UE23</span>
      <div class="sae-title">Conception d'une pièce de sécurité en traction</div>
      <div class="sae-desc">Dimensionnement RDM, simulation éléments finis, validation conception.</div>
      <div class="sae-resources"><span class="sae-res-chip">R2.01</span><span class="sae-res-chip">R2.02</span><span class="sae-res-chip">R2.05</span><span class="sae-res-chip">POR2</span></div>
      <span class="sae-arrow">↗</span>
    </div>
  </div>
</section>

<!-- ROUTE DIVIDER -->
<div class="route-divider"><div class="route-line"></div><div class="plane-fly" style="animation-delay:-.5s">✈</div><div class="route-stop">PAR · 06</div></div>

<!-- ══ PARCOURS ══ -->
<section id="parcours">
  <div class="dest-badge reveal"><span class="dest-code">PAR</span><span class="dest-arrow">→</span><span class="dest-name">Itinéraire du Voyageur</span></div>
  <h2 class="section-title reveal">Mon <span>Parcours</span></h2>
  <div class="divider reveal"></div>
  <div class="parcours-grid">
    <div class="reveal">
      <div class="timeline-col-title">💼 Expériences</div>
      <div class="timeline">
        <div class="timeline-item">
          <div class="timeline-date">Oct. 2025 — Aujourd'hui</div>
          <div class="timeline-title">Apprenti Opérateur-Régleur Joaillerie</div>
          <div class="timeline-org">Losange · Île-de-France</div>
          <div class="timeline-tags"><span class="tl-tag">Usinage</span><span class="tl-tag">Précision</span><span class="tl-tag">Apprentissage</span></div>
        </div>
        <div class="timeline-item">
          <div class="timeline-date">Avr. 2025 — Août 2025</div>
          <div class="timeline-title">Animateur Sportif</div>
          <div class="timeline-org">Ville de Maisons-Alfort · 94</div>
          <div class="timeline-tags"><span class="tl-tag">Animation</span><span class="tl-tag">Sport</span></div>
        </div>
      </div>
    </div>
    <div class="reveal" style="transition-delay:.15s">
      <div class="timeline-col-title">🎓 Formation</div>
      <div class="timeline">
        <div class="timeline-item" style="border-left-color:rgba(79,124,255,.4)">
          <div class="timeline-date">2025 — 2028</div>
          <div class="timeline-title">BUT GMP · Parcours SNRV</div>
          <div class="timeline-org">IUT Évry-Val-d'Essonne / CFA-EVE · Évry (91)</div>
          <div class="timeline-tags"><span class="tl-tag">CAO/DAO</span><span class="tl-tag">SolidWorks</span><span class="tl-tag">Alternance</span></div>
        </div>
        <div class="timeline-item">
          <div class="timeline-date">2024 — 2025</div>
          <div class="timeline-title">BUT 1 Informatique</div>
          <div class="timeline-org">IUT Créteil-Vitry · Créteil (94)</div>
          <div class="timeline-tags"><span class="tl-tag">Informatique</span></div>
        </div>
        <div class="timeline-item">
          <div class="timeline-date">2021 — 2024</div>
          <div class="timeline-title">Baccalauréat STI2D</div>
          <div class="timeline-org">Lycée Maximilien Perret · Alfortville (94)</div>
          <div class="timeline-tags"><span class="tl-tag">STI2D</span><span class="tl-tag">Mécanique</span></div>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ROUTE DIVIDER -->
<div class="route-divider"><div class="route-line"></div><div class="plane-fly" style="animation-delay:-2.5s">✈</div><div class="route-stop">PPP · 07</div></div>

<!-- ══ PPP ══ -->
<section id="ppp">
  <div class="dest-badge reveal"><span class="dest-code">PPP</span><span class="dest-arrow">→</span><span class="dest-name">Journal de Bord</span></div>
  <h2 class="section-title reveal">Projet <span>Personnel &amp; Professionnel</span></h2>
  <div class="divider reveal"></div>
  <div class="ppp-grid">
    <div class="ppp-card reveal">
      <span class="ppp-icon">🎯</span>
      <div class="ppp-title">Objectif Professionnel</div>
      <div class="ppp-text">Devenir ingénieur en simulation numérique ou en conception mécanique avancée. Je vise les secteurs de l'aéronautique, du luxe ou de l'automobile — des domaines où la précision n'est pas négociable.</div>
    </div>
    <div class="ppp-card reveal" style="transition-delay:.1s">
      <span class="ppp-icon">🔬</span>
      <div class="ppp-title">Problématique</div>
      <div class="ppp-text">Comment la simulation numérique et la réalité virtuelle peuvent-elles transformer les méthodes de conception et de validation en industrie ? C'est la question qui guide mon parcours SNRV.</div>
    </div>
    <div class="ppp-card reveal" style="transition-delay:.15s">
      <span class="ppp-icon">💻</span>
      <div class="ppp-title">Identité Numérique</div>
      <div class="ppp-text">Ce portfolio, c'est moi — pas seulement mes diplômes ou mes SAÉ, mais aussi mes engagements, mes voyages, ma ville. Maisons-Alfort m'a formé autant que l'IUT.</div>
    </div>
    <div class="ppp-card reveal" style="transition-delay:.2s">
      <span class="ppp-icon">⚡</span>
      <div class="ppp-title">Vie Extra-Professionnelle</div>
      <div class="ppp-text">Licencié en foot à Maisons-Alfort depuis 2010, bénévole dans une association humanitaire qui m'a emmené jusqu'à Essaouira au Maroc. Ces expériences nourrissent mon regard sur le monde.</div>
    </div>
  </div>
</section>

<!-- ROUTE DIVIDER -->
<div class="route-divider"><div class="route-line"></div><div class="plane-fly" style="animation-delay:-4s">✈</div><div class="route-stop">OUV · 08</div></div>

<!-- ══ OUVERTURE ══ -->
<section id="ouverture">
  <div class="dest-badge reveal"><span class="dest-code">OUV</span><span class="dest-arrow">→</span><span class="dest-name">Prochains Vols</span></div>
  <h2 class="section-title reveal">Vers l'<span>Avenir</span></h2>
  <div class="divider reveal"></div>
  <div class="ouv-quote reveal">
    <p>"Ces deux premières années ne sont qu'un point de départ. Chaque pièce usinée, chaque rapport rédigé, chaque défi technique relevé m'amène un pas de plus vers l'ingénieur que je veux devenir. Je ne choisis pas encore la destination finale — je construis les outils pour y arriver."</p>
    <cite>— Anas El Hiss, juin 2026</cite>
  </div>
  <div class="ouv-grid">
    <div class="ouv-card reveal">
      <div class="ouv-card-icon">📐</div>
      <div class="ouv-card-title">BUT 2 &amp; 3 — Approfondissement</div>
      <div class="ouv-card-text">Simulation numérique par éléments finis, réalité virtuelle industrielle, conception avancée. Le parcours SNRV me donne les outils de demain.</div>
    </div>
    <div class="ouv-card reveal" style="transition-delay:.1s">
      <div class="ouv-card-icon">🏭</div>
      <div class="ouv-card-title">L'entreprise comme laboratoire</div>
      <div class="ouv-card-text">Chez Losange, chaque jour est une occasion d'apprendre. L'apprentissage transforme la théorie en réflexe professionnel, en savoir-faire du geste et de la machine.</div>
    </div>
    <div class="ouv-card reveal" style="transition-delay:.2s">
      <div class="ouv-card-icon">🚀</div>
      <div class="ouv-card-title">Vision long terme</div>
      <div class="ouv-card-text">Ingénieur bureau d'études, spécialisé en simulation. Aéronautique, luxe, automobile — les secteurs où la rigueur technique rencontre l'innovation.</div>
    </div>
  </div>
  <div class="roadmap reveal">
    <div class="roadmap-item">
      <div class="roadmap-year">2025–2026</div>
      <div class="roadmap-text">BUT1 GMP SNRV — fondamentaux, CAO, premières SAÉ, début apprentissage Losange</div>
    </div>
    <div class="roadmap-item">
      <div class="roadmap-year">2026–2027</div>
      <div class="roadmap-text">BUT2 — simulation numérique, éléments finis, réalité virtuelle industrielle</div>
    </div>
    <div class="roadmap-item">
      <div class="roadmap-year">2027–2028</div>
      <div class="roadmap-text">BUT3 — projet fin d'études, stage longue durée, mémoire et soutenance</div>
    </div>
    <div class="roadmap-item">
      <div class="roadmap-year">2028+</div>
      <div class="roadmap-text">École d'ingénieur (ICAM, ESTACA…) ou bureau d'études — destination finale à définir</div>
    </div>
  </div>
</section>

<!-- ROUTE DIVIDER -->
<div class="route-divider"><div class="route-line"></div><div class="plane-fly" style="animation-delay:-3.5s">✈</div><div class="route-stop">CTR · 09</div></div>

<!-- ══ CONTACT ══ -->
<section id="contact">
  <div class="dest-badge reveal" style="margin:0 auto 2rem"><span class="dest-code">CTR</span><span class="dest-arrow">→</span><span class="dest-name">Terminal d'Arrivée</span></div>
  <h2 class="section-title reveal">Me <span>Contacter</span></h2>
  <div class="divider reveal" style="margin:1rem auto"></div>
  <p class="reveal" style="color:var(--muted);margin-bottom:0;font-size:.95rem">Disponible en apprentissage · IUT Évry-Val-d'Essonne · Promotion 2025–2028</p>
  <div class="contact-grid">
    <a href="tel:0622584724" class="contact-card reveal">
      <div class="contact-icon">📞</div>
      <div><div class="contact-label">Téléphone</div><div class="contact-val">06 22 58 47 24</div></div>
    </a>
    <a href="mailto:elhissanas@gmail.com" class="contact-card reveal" style="transition-delay:.1s">
      <div class="contact-icon">✉️</div>
      <div><div class="contact-label">Email</div><div class="contact-val">elhissanas@gmail.com</div></div>
    </a>
    <a href="https://linkedin.com/in/anas-el-hiss" target="_blank" class="contact-card reveal" style="transition-delay:.15s">
      <div class="contact-icon">💼</div>
      <div><div class="contact-label">LinkedIn</div><div class="contact-val">@anas-el-hiss</div></div>
    </a>
    <div class="contact-card reveal" style="transition-delay:.2s;cursor:default">
      <div class="contact-icon">📍</div>
      <div><div class="contact-label">Localisation</div><div class="contact-val">Maisons-Alfort (94)</div></div>
    </div>
  </div>
</section>

<footer>
  © 2026 Anas El Hiss &nbsp;·&nbsp; BUT GMP SNRV &nbsp;·&nbsp; IUT Évry-Val-d'Essonne &nbsp;·&nbsp; Vol AEH-2028
</footer>

<!-- ══ MODAL SAÉ ══ -->
<div class="modal-overlay" id="modal">
  <div class="modal-box">
    <div class="modal-header">
      <button class="m-close" id="mClose">✕</button>
      <div style="margin-bottom:.5rem"><span id="m-tag" class="sae-tag"></span>&nbsp;<span style="font-size:.78rem;color:var(--muted);font-family:'Share Tech Mono',monospace" id="m-sem"></span>&nbsp;<span style="font-size:.78rem;color:var(--muted)" id="m-ref"></span></div>
      <h3 style="font-family:'Syne',sans-serif;font-weight:700;font-size:1.25rem;margin-bottom:.5rem" id="m-title"></h3>
      <div style="font-size:.82rem;color:var(--muted)" id="m-ue"></div>
    </div>
    <div class="modal-body">
      <div class="modal-section">
        <div class="modal-section-label">Description</div>
        <div class="modal-text" id="m-desc"></div>
      </div>
      <div class="modal-section">
        <div class="modal-section-label">Objectifs</div>
        <div class="modal-text" id="m-obj"></div>
      </div>
      <div class="modal-section">
        <div class="modal-section-label">Ressources mobilisées</div>
        <div id="m-res"></div>
      </div>
      <div id="m-extra"></div>
    </div>
  </div>
</div>

<!-- LIGHTBOX -->
<div class="lightbox" id="lightbox">
  <img id="lb-img" src="" alt="">
</div>

<script>
{IMG_BLOCK}

{SAE13_FN}

{SAE204_FN}

{FONDERIE_FN}

function openModal(card){{
  document.getElementById('m-sem').textContent = card.dataset.sem||'';
  document.getElementById('m-ref').textContent = card.dataset.ref||'';
  document.getElementById('m-title').textContent = card.dataset.title||'';
  document.getElementById('m-ue').textContent = card.dataset.ue||'';
  document.getElementById('m-desc').textContent = card.dataset.desc||'';
  document.getElementById('m-obj').textContent = card.dataset.obj||'';
  const tag = document.getElementById('m-tag');
  tag.textContent = (card.dataset.ue||'').split('—')[0].trim();
  tag.className = 'sae-tag';
  const k = (card.dataset.ue||'').replace(/[^0-9]/g,'').slice(0,2);
  const cm = {{'11':'sae-ue11','12':'sae-ue12','13':'sae-ue13','14':'sae-ue14','21':'sae-ue21','22':'sae-ue22','23':'sae-ue23','24':'sae-ue24'}};
  tag.classList.add(cm[k]||'sae-multi');
  const resEl = document.getElementById('m-res');
  resEl.innerHTML = '';
  (card.dataset.res||'').split(',').map(s=>s.trim()).filter(Boolean).forEach(r => {{
    const c = document.createElement('span'); c.className='chip'; c.style.cursor='default'; c.textContent=r; resEl.appendChild(c);
  }});
  const extra = document.getElementById('m-extra');
  extra.innerHTML = card.dataset.hasGallery ? buildSae13Extra() : (card.dataset.hasSae204 ? buildSae204Extra() : (card.dataset.hasFonderie ? buildFonderieExtra() : ''));
  document.getElementById('modal').classList.add('open');
  document.body.style.overflow='hidden';
}}
function closeModal(){{ document.getElementById('modal').classList.remove('open'); document.body.style.overflow=''; }}

document.querySelectorAll('.sae-card').forEach(c => {{
  c.setAttribute('tabindex','0'); c.setAttribute('role','button');
  c.addEventListener('click', ()=>openModal(c));
  c.addEventListener('keydown', e=>{{ if(e.key==='Enter'||e.key===' ') openModal(c); }});
}});
document.getElementById('mClose').addEventListener('click', closeModal);
document.getElementById('modal').addEventListener('click', e=>{{ if(e.target===document.getElementById('modal')) closeModal(); }});

// Lightbox
function openLightbox(src){{ document.getElementById('lb-img').src=src; document.getElementById('lightbox').classList.add('open'); }}
document.getElementById('lightbox').addEventListener('click', ()=>document.getElementById('lightbox').classList.remove('open'));

// Cursor glow
document.addEventListener('mousemove', e=>{{
  const g = document.getElementById('glow');
  g.style.left = e.clientX+'px'; g.style.top = e.clientY+'px';
}});

// Particles (hero sky)
(function(){{
  const canvas = document.getElementById('particles');
  if(!canvas) return;
  const ctx = canvas.getContext('2d');
  let W,H,pts=[];
  function resize(){{ W=canvas.width=canvas.offsetWidth; H=canvas.height=canvas.offsetHeight; }}
  function init(){{
    pts=[];
    for(let i=0;i<60;i++) pts.push({{
      x:Math.random()*W, y:Math.random()*H,
      vx:(Math.random()-.5)*.3, vy:(Math.random()-.5)*.3,
      r:Math.random()*1.5+.5
    }});
  }}
  function draw(){{
    ctx.clearRect(0,0,W,H);
    pts.forEach(p=>{{
      p.x+=p.vx; p.y+=p.vy;
      if(p.x<0)p.x=W; if(p.x>W)p.x=0;
      if(p.y<0)p.y=H; if(p.y>H)p.y=0;
      ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
      ctx.fillStyle='rgba(255,255,255,0.6)'; ctx.fill();
    }});
    pts.forEach((a,i)=>pts.slice(i+1).forEach(b=>{{
      const d=Math.hypot(a.x-b.x,a.y-b.y);
      if(d<100){{ ctx.beginPath(); ctx.moveTo(a.x,a.y); ctx.lineTo(b.x,b.y);
        ctx.strokeStyle=`rgba(79,124,255,${{(1-d/100)*.15}})`; ctx.lineWidth=.8; ctx.stroke(); }}
    }}));
    requestAnimationFrame(draw);
  }}
  window.addEventListener('resize',()=>{{resize();init();}});
  resize(); init(); draw();
}})();

// Scroll reveal
const io = new IntersectionObserver(entries=>entries.forEach(e=>{{
  if(e.isIntersecting){{ e.target.classList.add('in'); io.unobserve(e.target); }}
}}),{{threshold:.12}});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

// Skill bars
const sio = new IntersectionObserver(entries=>entries.forEach(e=>{{
  if(e.isIntersecting){{
    e.target.querySelectorAll('.skill-fill').forEach(b=>b.style.width=(b.dataset.w||0)+'%');
    sio.unobserve(e.target);
  }}
}}),{{threshold:.2}});
document.querySelectorAll('.comp-card').forEach(c=>sio.observe(c));

// Counter
const cio = new IntersectionObserver(entries=>entries.forEach(e=>{{
  if(e.isIntersecting){{
    e.target.querySelectorAll('.stat-number[data-target]').forEach(el=>{{
      const t=+el.dataset.target, dur=1200, start=performance.now();
      const tick=now=>{{ const p=Math.min((now-start)/dur,1); el.textContent=Math.round(p*t);
        if(p<1) requestAnimationFrame(tick); }};
      requestAnimationFrame(tick);
    }});
    cio.unobserve(e.target);
  }}
}}),{{threshold:.3}});
document.querySelectorAll('.stats-grid').forEach(el=>cio.observe(el));

// Active nav
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-links a');
const nio = new IntersectionObserver(entries=>{{
  entries.forEach(e=>{{
    if(e.isIntersecting){{
      navLinks.forEach(a=>a.classList.remove('active'));
      const a = document.querySelector(`.nav-links a[href="#${{e.target.id}}"]`);
      if(a) a.classList.add('active');
    }}
  }});
}},{{threshold:.4}});
sections.forEach(s=>nio.observe(s));
</script>
</body>
</html>"""

with open('/home/user/Portfolio/index.html','w',encoding='utf-8') as f:
    f.write(HTML)

kb = len(HTML)//1024
print(f"Done — {kb} KB")
