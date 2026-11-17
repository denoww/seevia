#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o livreto da Seevia → livreto/index.html (rota /livreto).

    python3 livreto/build.py
    bash    livreto/build_pdf.sh     # espelho em PDF (Chromium headless)

Doutrina herdada do livreto do SeuCondomínio (~/workspace/seucondominio/livreto/CLAUDE.md),
na marca e no domínio da Seevia — mesmo caminho de baterponto-site e atendeaqui-site:
  - Long-scroll Apple, capítulos alternando branco/névoa, storyboards de fluxo.
  - A cor vem do produto (fotos noturnas, azul da marca), não de fundo colorido.
  - Selo só onde é verdade. Roadmap nunca se vende como pronto → capítulo "O que não faz".
  - NUNCA editar o HTML gerado. Edita-se `content.py` (95% das mudanças) ou este arquivo.

Infra: o site é estático (AWS Amplify, `amplify.yml` sem build step), então o PDF é gerado
no build por Chromium headless e commitado — diferente do SeuCondomínio, que gera em runtime
pelo Gotenberg. Ao mudar conteúdo, rodar os dois.

PEGADINHAS DO PRINT (custaram correção no repo original — não mexer sem entender):
  - `@media print` PRECISA forçar `.rev{opacity:1}` — senão o PDF sai EM BRANCO.
  - `print-color-adjust:exact` — senão hero/CTA/fotos saem sem cor.
  - `break-inside:avoid` só nas unidades atômicas (card, painel). NUNCA por capítulo:
    gera páginas quase vazias.
  - Traço de SVG com `stroke` explícito no elemento (classe utilitária com `stroke:none`
    apaga o traço em silêncio).
  - `@page{size:A4}` — sem isso o Chrome imprime em Letter.
"""
import pathlib, importlib.util, datetime, hashlib

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
OUT  = REPO / "livreto" / "index.html"

sp = importlib.util.spec_from_file_location("content", str(ROOT / "content.py"))
C = importlib.util.module_from_spec(sp); sp.loader.exec_module(C)

WA = C.WA + C.WA_TXT

# --------------------------------------------------------------------- cenas
# Line-art dos storyboards. `stroke="currentColor"` explícito e `fill="none"`.
SCENES = {
 "cam":     '<rect x="10" y="16" width="24" height="12" rx="6"/><circle cx="17" cy="22" r="4"/>'
            '<path d="M34 22h7"/><path d="M41 11v22"/>',
 "ia":      '<rect x="19" y="15" width="18" height="14" rx="3"/><rect x="25" y="20" width="6" height="4" rx="1"/>'
            '<path d="M23 15v-4M28 15v-4M33 15v-4M23 29v4M28 29v4M33 29v4M19 19h-5M19 25h-5M37 19h5M37 25h5"/>',
 "regra":   '<path d="M13 12h30L31 25v10l-6 3V25z"/><path d="M40 32l3 3 6-7"/>',
 "celular": '<rect x="20" y="7" width="17" height="30" rx="4"/><path d="M25 12h7"/>'
            '<path d="M24 21h9M24 26h6"/><path d="M26 33h5"/>',
 "bancada": '<rect x="13" y="15" width="17" height="12" rx="2"/><circle cx="18" cy="21" r="3"/>'
            '<path d="M36 20l4-4 3 3-4 4z"/><path d="M36 20l-4 5"/><path d="M9 33h38"/>',
 "cabo":    '<path d="M11 31c9 0 8-18 17-18s8 18 17 18"/><rect x="6" y="27" width="6" height="8" rx="2"/>'
            '<rect x="44" y="27" width="6" height="8" rx="2"/>',
 "qr":      '<rect x="13" y="9" width="10" height="10" rx="2"/><rect x="33" y="9" width="10" height="10" rx="2"/>'
            '<rect x="13" y="25" width="10" height="10" rx="2"/><path d="M33 25h4v4h-4z"/>'
            '<path d="M39 31h4v4h-4z"/><path d="M33 33h3"/>',
 "aovivo":  '<rect x="11" y="11" width="34" height="21" rx="3"/><path d="M25 18l8 4-8 4z"/>'
            '<path d="M22 37h12"/>',
 "cadeado": '<rect x="18" y="20" width="20" height="15" rx="3"/><path d="M23 20v-5a5 5 0 0 1 10 0v5"/>'
            '<path d="M28 26v4"/>',
 "toque":   '<rect x="12" y="16" width="26" height="12" rx="6"/><circle cx="31" cy="22" r="4"/>'
            '<path d="M42 30l4 4M45 26l3 3"/>',
 "raio":    '<circle cx="27" cy="22" r="12"/><circle cx="27" cy="22" r="3.5"/>'
            '<path d="M27 10V6M27 38v-4M15 22h-4M43 22h-4"/>',
 "casa":    '<path d="M9 23l9-7 9 7"/><path d="M12 23v11h12V23"/><path d="M31 27l7-6 7 6"/>'
            '<path d="M33 27v7h10v-7"/>',
 "segura":  '<circle cx="26" cy="22" r="11"/><path d="M15 22a11 11 0 0 1 11-11"/>'
            '<path d="M34 30l6 6"/><circle cx="26" cy="22" r="3"/>',
 "onda":    '<circle cx="28" cy="27" r="3"/><path d="M20 27a8 8 0 0 1 16 0"/>'
            '<path d="M13 27a15 15 0 0 1 30 0"/>',
 "familia": '<circle cx="19" cy="17" r="4"/><path d="M11 32c1.4-4.6 4.4-6.9 8-6.9s6.6 2.3 8 6.9"/>'
            '<circle cx="37" cy="19" r="3.4"/><path d="M30 32c1.2-3.8 3.8-5.7 7-5.7s5.8 1.9 7 5.7"/>',
}
def scene(n):
    return ('<svg class="scene" viewBox="0 0 56 44" aria-hidden="true">'
            f'<g fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            f'stroke-linejoin="round">{SCENES[n]}</g></svg>')

# ---------------------------------------------------------------- componentes
_CHAP = [0]
def chapter(cid, eyebrow, h2, lead, *blocks):
    bg = "nevoa" if _CHAP[0] % 2 else ""   # alterna sozinho — não passe bg
    _CHAP[0] += 1
    return f'''<section class="cap {bg}" id="{cid}" aria-label="{eyebrow}">
  <div class="cap-in">
    <div class="cap-head rev"><span class="eyebrow">{eyebrow}</span><h2>{h2}</h2>
      {f'<p class="lead">{lead}</p>' if lead else ''}</div>
    {"".join(blocks)}
  </div>
</section>'''

def tag(t):
    return f'<span class="tg">{t}</span>' if t else ''

def cards(items, cor):
    cs = "".join(f'<article class="fc"><span class="fc-mk"></span><h3>{t}{tag(g)}</h3><p>{d}</p></article>'
                 for t, d, g in items)
    return f'<div class="fgrid c-{cor} rev">{cs}</div>'

def board(key):
    cor, titulo, panels = C.BOARDS[key]
    cells = []
    for i, (sc, h, cap) in enumerate(panels):
        cells.append(f'<li class="bp"><span class="bp-n">{i+1}</span>'
                     f'<span class="bp-art">{scene(sc)}</span><b>{h}</b><i>{cap}</i></li>')
        if i < len(panels) - 1:
            cells.append('<li class="bp-arr" aria-hidden="true">→</li>')
    return (f'<figure class="board c-{cor} rev"><figcaption class="board-cap">'
            f'<span class="eyebrow">Como funciona</span><b>{titulo}</b></figcaption>'
            f'<ol class="board-strip">{"".join(cells)}</ol></figure>')

def foto(slug, alt):
    return (f'<figure class="shot"><img src="/assets/{slug}.jpg" alt="{alt}" '
            f'loading="lazy" decoding="async"></figure>')

def mrow(media, h, p, flip=False):
    return (f'<div class="mrow{" flip" if flip else ""} rev"><div class="m-media">{media}</div>'
            f'<div class="m-copy"><h3>{h}</h3><p>{p}</p></div></div>')

# ---------------------------------------------------------------------- CSS
CSS = """
:root{
  --branco:#fff;--nevoa:#f4f6fb;--preto:#0b1020;
  --tinta:#141a2e;--tinta-2:#5b6683;--claro:#eef3ff;--claro-2:#9aa6c4;
  --azul:#104fd4;--azul-claro:#3a78ff;--azul-neon:#7aa2ff;--azul-leve:#e8effe;
  --verde:#1E9E63;--ciano:#0e7490;--ambar:#B45309;--roxo:#6b2bd6;
  --linha:rgba(10,20,50,.12);--maxw:1120px;
  --sec:var(--azul);
  --ease:cubic-bezier(.45,0,.55,1);
}
.c-azul{--sec:#104fd4;--soft:#e8effe}
.c-verde{--sec:#1E9E63;--soft:#E4F5EC}
.c-ciano{--sec:#0e7490;--soft:#E0F1F6}
.c-ambar{--sec:#B45309;--soft:#FBF0E2}
.c-roxo{--sec:#6b2bd6;--soft:#EFE8FD}
*{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:var(--branco);color:var(--tinta);
  font-family:'Inter',-apple-system,BlinkMacSystemFont,system-ui,sans-serif;
  font-size:17px;line-height:1.47;letter-spacing:-.02em;-webkit-font-smoothing:antialiased}
h1,h2,h3{margin:0;font-weight:600;line-height:1.06;letter-spacing:-.018em;text-wrap:balance}
p{margin:0}ul,ol{margin:0;padding:0;list-style:none}
a{color:var(--azul);text-decoration:none}
img{display:block;max-width:100%}
:focus-visible{outline:3px solid var(--azul-claro);outline-offset:3px;border-radius:6px}
.eyebrow{display:block;font-size:20px;font-weight:600;letter-spacing:.01em;color:var(--sec);margin-bottom:8px}
.lead{font-size:21px;line-height:1.38;letter-spacing:.01em;color:var(--tinta-2);margin-top:14px}

.nav{position:sticky;top:0;z-index:50;height:56px;display:flex;align-items:center;justify-content:space-between;
  padding:0 clamp(20px,4vw,40px);background:rgba(255,255,255,.75);
  backdrop-filter:saturate(180%) blur(20px);-webkit-backdrop-filter:saturate(180%) blur(20px);
  border-bottom:1px solid rgba(10,20,50,.08)}
.nav .brand{display:flex;align-items:center}
.nav .brand img{height:22px;width:auto}
.nav-r{display:flex;align-items:center;gap:clamp(14px,3vw,26px);font-size:13px}
/* os <a> vivem DENTRO de .nav-links — sem inline-flex aqui eles saem colados,
   porque o gap do .nav-r só separa os filhos diretos. */
.nav-links{display:inline-flex;align-items:center;gap:clamp(14px,2.2vw,24px)}
.nav-r a{color:var(--tinta);opacity:.85}
.nav-r a:hover{opacity:1;color:var(--azul)}
.nav-cta{background:var(--azul);color:#fff!important;padding:7px 15px;border-radius:980px;font-weight:600}
@media(max-width:820px){.nav-links{display:none}}

.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;background:var(--azul);color:#fff;
  padding:12px 22px;border-radius:980px;font-weight:500;font-size:17px;letter-spacing:-.02em;
  transition:background-color .12s linear,transform .12s ease}
.btn:hover{background:#0b3ea8;transform:translateY(-1px)}
.btn-branco{background:#fff;color:var(--tinta)}
.btns{display:flex;flex-wrap:wrap;gap:12px;justify-content:center;margin-top:32px}

/* hero */
.hero{background:var(--preto);color:var(--claro);text-align:center;padding:clamp(64px,9vh,104px) 24px 0;
  overflow:hidden;background-image:radial-gradient(900px 500px at 50% -10%,rgba(58,120,255,.45),transparent 62%)}
.hero .eyebrow{color:var(--azul-neon)}
.hero h1{font-size:clamp(40px,4.4vw+14px,74px);color:#fff;max-width:17ch;margin:0 auto}
.hero .sub{margin:22px auto 0;max-width:58ch;font-size:20px;line-height:1.45;color:var(--claro-2);letter-spacing:.01em}
.hero-stage{margin:56px auto 0;max-width:940px}
/* a foto sobe do hero e é cortada pelo fim da seção (o corte é de propósito).
   Sem aspect-ratio ela entra inteira e o corte cai em lugar aleatório. */
.hero-stage img{width:100%;aspect-ratio:16/8;object-fit:cover;object-position:50% 42%;
  border-radius:24px 24px 0 0;box-shadow:0 -10px 60px rgba(58,120,255,.28)}

.credo{max-width:960px;margin:0 auto;padding:clamp(80px,10vw,130px) 24px;text-align:center}
.credo h2{font-size:clamp(30px,3.4vw+10px,52px);letter-spacing:-.02em}
.credo .g{color:var(--azul)}

/* capítulos */
.cap{padding:clamp(72px,9vw,120px) 0}
.cap.nevoa{background:var(--nevoa)}
.cap-in{max-width:var(--maxw);margin:0 auto;padding:0 24px}
.cap-head{max-width:780px}
.cap-head h2{font-size:clamp(30px,2.4vw+14px,48px);letter-spacing:-.012em;margin-top:2px}

.fgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-top:44px}
.fc{background:var(--branco);border:1px solid var(--linha);border-radius:20px;padding:26px 24px;break-inside:avoid}
.cap.nevoa .fc{background:#fff;border-color:rgba(10,20,50,.07)}
.fc-mk{display:block;width:26px;height:3px;border-radius:3px;background:var(--sec);margin-bottom:16px}
.fc h3{font-size:20px;letter-spacing:-.012em}
.fc p{margin-top:8px;color:var(--tinta-2);font-size:16px;line-height:1.5}
.tg{display:inline-block;margin-left:8px;font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
  color:var(--sec);background:var(--soft);padding:3px 8px;border-radius:980px;vertical-align:middle}

/* storyboard */
.board{margin:48px 0 0;padding:30px;border-radius:24px;background:var(--soft);break-inside:avoid}
.board-cap{margin-bottom:22px}
.board-cap b{display:block;font-size:22px;font-weight:600;letter-spacing:-.012em}
.board-strip{display:flex;align-items:stretch;gap:10px;flex-wrap:wrap}
.bp{flex:1 1 180px;background:#fff;border-radius:16px;padding:20px 18px;position:relative;break-inside:avoid}
.bp-n{position:absolute;top:14px;right:16px;font-size:12px;font-weight:700;color:var(--sec)}
.bp-art{display:block;color:var(--sec)}
.scene{width:56px;height:44px}
.bp b{display:block;margin-top:12px;font-size:17px;font-weight:600;letter-spacing:-.012em}
.bp i{display:block;margin-top:6px;font-style:normal;font-size:14.5px;line-height:1.45;color:var(--tinta-2)}
.bp-arr{display:flex;align-items:center;color:var(--sec);font-size:20px;opacity:.55}
@media(max-width:860px){.bp-arr{display:none}}

/* media row */
.mrow{display:grid;grid-template-columns:1.05fr .95fr;gap:44px;align-items:center;margin-top:48px}
.mrow.flip .m-media{order:2}
@media(max-width:860px){.mrow{grid-template-columns:1fr}.mrow.flip .m-media{order:0}}
.m-copy h3{font-size:26px;letter-spacing:-.014em}
.m-copy p{margin-top:12px;color:var(--tinta-2);font-size:17px;line-height:1.5}
.shot img{width:100%;border-radius:20px}

/* lineup */
.lineup{background:var(--preto);color:var(--claro);padding:clamp(80px,10vw,130px) 0;
  background-image:radial-gradient(800px 400px at 80% 0%,rgba(107,43,214,.28),transparent 60%)}
.lineup-in{max-width:var(--maxw);margin:0 auto;padding:0 24px}
.lineup h2{font-size:clamp(30px,2.4vw+14px,48px);color:#fff}
.lineup .lead{color:var(--claro-2)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px;margin-top:44px}
.tile{background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.13);border-radius:20px;padding:24px;break-inside:avoid}
.tile h3{font-size:18px;color:#fff}
.tile p{margin-top:8px;font-size:15px;line-height:1.5;color:var(--claro-2)}
.tile-mk{display:block;width:26px;height:3px;border-radius:3px;background:var(--sec);margin-bottom:14px}
.tile .tg{color:#fff;background:rgba(255,255,255,.16)}

/* cta / download / rodapé */
.cta{text-align:center;padding:clamp(88px,11vw,140px) 24px;background:
  radial-gradient(1100px 560px at 50% 0%,rgba(58,120,255,.5),transparent 65%),#080c18;color:var(--claro)}
.cta h2{font-size:clamp(30px,3vw+12px,52px);color:#fff;max-width:18ch;margin:0 auto}
.cta p{margin:20px auto 0;max-width:54ch;font-size:19px;line-height:1.5;color:var(--claro-2)}
.cta .sub2{margin-top:22px;font-size:15px;color:var(--claro-2)}
.cta .sub2 a{color:var(--azul-neon)}
.dl{text-align:center;padding:clamp(64px,8vw,96px) 24px;background:var(--nevoa)}
.dl h2{font-size:30px}
.dl p{margin-top:12px;color:var(--tinta-2)}
.foot{border-top:1px solid var(--linha);padding:36px 24px;background:var(--nevoa)}
.foot-in{max-width:var(--maxw);margin:0 auto;display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;
  color:var(--tinta-2);font-size:13px}

/* reveal */
.rev{opacity:0;transform:translateY(30px);transition:opacity .9s var(--ease),transform .9s var(--ease)}
.rev.vis{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){.rev{opacity:1;transform:none}html{scroll-behavior:auto}}

/* ======================= IMPRESSÃO / PDF =======================
   As travas do playbook. Mexer aqui quebra o PDF em silêncio. */
@media print{
  /* 1. sem isto o PDF sai EM BRANCO (o reveal nunca dispara sem scroll) */
  .rev{opacity:1!important;transform:none!important}
  /* 2. sem isto hero/CTA/fotos saem sem cor */
  *{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important}
  /* 3. só nas unidades atômicas — NUNCA por capítulo nem na media row inteira
        (foto + texto ocupam quase uma página: forçar avoid ali abre buraco branco) */
  .fc,.bp,.tile,.board,.shot{break-inside:avoid}
  .nav,.dl,.btns{display:none!important}
  .cap{padding:28px 0}
  .hero{padding-top:36px}
  .hero-stage{margin-top:28px}
  .credo{padding:44px 24px}
  .lineup{padding:36px 0}
  .cta{padding:44px 24px}
  body{font-size:11.5pt}
  a{color:inherit;text-decoration:none}
  /* sem isto o Chrome imprime em Letter (padrão americano) — no Brasil é A4 */
  @page{size:A4;margin:14mm}
}
"""

SCRIPT = """<script>
(function(){
  if(matchMedia("(prefers-reduced-motion: reduce)").matches){
    document.querySelectorAll(".rev").forEach(function(e){e.classList.add("vis")});return;}
  var io=new IntersectionObserver(function(es){es.forEach(function(e){
    if(e.isIntersecting){e.target.classList.add("vis");io.unobserve(e.target)}})},
    {threshold:0,rootMargin:"0px 0px -12% 0px"});
  document.querySelectorAll(".rev").forEach(function(e){io.observe(e)});
})();
</script>"""

# --------------------------------------------------------------------- montagem
def build():
    _CHAP[0] = 0
    wa_svg = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" style="width:18px;height:18px">'
              '<path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2c-1.6 0-3.1-.4-4.4-1.2'
              'l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Z"/></svg>')

    nav = f'''<nav class="nav">
  <a class="brand" href="/"><img src="/assets/seevia_azul.png" alt="Seevia"></a>
  <span class="nav-r"><span class="nav-links">
    <a href="#camera">A câmera</a><a href="#vizinhanca">A vizinhança</a>
    <a href="#alarme">Alarme</a><a href="#limites">O que não faz</a></span>
  <a class="nav-cta" href="{WA}">Falar no WhatsApp</a></span>
</nav>'''

    hero = f'''<header class="hero">
  <span class="eyebrow">{C.HERO["eyebrow"]}</span>
  <h1>{C.HERO["h1"]}</h1>
  <p class="sub">{C.HERO["sub"]}</p>
  <div class="btns"><a class="btn btn-branco" href="{WA}">{wa_svg} Falar no WhatsApp</a></div>
  <div class="hero-stage rev"><img src="/assets/hero.jpg" width="1280" height="853"
    alt="Rua residencial à noite vista por uma câmera de segurança instalada no poste."></div>
</header>'''

    credo = f'<section class="credo rev"><h2>{C.CREDO}</h2></section>'

    cap_camera = chapter("camera", "A câmera", "A câmera entende o que vê.",
        "Gravar todo mundo já é fácil e não resolve nada: o problema é achar os dez segundos "
        "que importam. A análise roda em cima da imagem e decide o que merece o seu telefone "
        "tocando.",
        mrow(foto("ia_vision", "Rua à noite com pessoas e um carro destacados por retângulos de detecção."),
             "Ela não só grava. Ela reconhece.",
             "Uma pessoa parada no muro, um carro que encostou e não saiu, fogo, água subindo. "
             "É a diferença entre um arquivo de vídeo e um aviso.", True),
        board("evento"), cards(C.CAMERA, "azul"))

    cap_gravacao = chapter("gravacao", "A gravação", "O dia inteiro cabe numa barra.",
        "Quando algo acontece, a pergunta é sempre a mesma: “dá para ver?”. A gravação está no "
        "celular, organizada por hora, e o trecho com movimento já vem marcado.",
        cards(C.GRAVACAO, "verde"))

    cap_vizinhanca = chapter("vizinhanca", "A vizinhança", "A rua vê junto — sem ninguém vigiar ninguém.",
        "Uma câmera protege uma casa. Um quarteirão de câmeras que conversam protege a rua. "
        "A parte difícil é fazer isso sem transformar a vizinhança num circuito de espiar a "
        "vida alheia — e é aí que o produto toma partido.",
        board("vizinhanca"), cards(C.VIZINHANCA, "ciano"))

    cap_instalacao = chapter("instalacao", "A instalação", "Cabo, energia e um QR.",
        "A instalação costuma travar no mesmo ponto: alguém precisa entrar na rede da casa "
        "para configurar a câmera. Aqui esse passo não existe — ele já aconteceu na bancada.",
        mrow(foto("camera", "Câmera de segurança compacta fotografada em fundo escuro."),
             "A câmera chega pronta para falar com a nuvem.",
             "Ela sai da bancada configurada e, ao ligar, sozinha manda o vídeo para o "
             "servidor. Rede de visitante, roteador do vizinho, Wi-Fi trancado: nada disso "
             "atrapalha, porque ela só precisa de saída para a internet."),
        board("instalacao"), cards(C.INSTALACAO, "verde"))

    cap_alarme = chapter("alarme", "Alarme", "O alarme mora no mesmo app.",
        "Ter câmera num aplicativo e alarme em outro é como ter duas fechaduras e uma chave "
        "só. Os eventos da central de alarme chegam onde você já olha as câmeras — e os botões "
        "de armar e desarmar estão ali do lado.",
        mrow(foto("app", "Pessoa segurando o celular com o aplicativo de segurança aberto à noite."),
             "Armar de longe, desarmar com confirmação.",
             "“Em casa”, “Saindo” e “Desarmar” — em português, sem código de instalador. E o "
             "cartão só muda de estado quando a central confirma que fez.", True),
        cards(C.ALARME, "ambar"), board("sos"))

    cap_operacao = chapter("operacao", "Quem opera", "Atrás da sua rua tem uma operação.",
        "A Seevia não é só o app do morador: é a plataforma de quem instala, atende e cobra "
        "por essa proteção — a operação da sua cidade, com a ferramenta que ela precisa para "
        "não perder câmera, ordem nem mensalidade de vista.",
        mrow(foto("central", "Operadores diante de um painel com dezenas de câmeras e mapas."),
             "O muro que se move sozinho.",
             "Dezenas de câmeras numa grade; quando a IA aponta alguma coisa, a tela foca "
             "nela. O operador não fica caçando quadradinho."),
        cards(C.OPERACAO, "roxo"))

    cap_privacidade = chapter("privacidade", "Privacidade", "Câmera de rua é assunto sério.",
        "Rede de vizinhos vira problema quando alguém consegue olhar a vida do outro. Por "
        "isso as escolhas mais importantes do produto são as que limitam o que dá para ver.",
        cards(C.PRIVACIDADE, "ciano"))

    cap_limites = chapter("limites", "Honestidade", "O que a Seevia não faz.",
        "Um livreto que só lista virtude não ajuda ninguém a decidir. Isto aqui é o que ela "
        "<b>não</b> resolve — para você não descobrir depois de instalar.",
        cards(C.NAO_FAZ, "ambar"))

    tiles = "".join(f'<article class="tile c-{c}"><span class="tile-mk"></span>'
                    f'<h3>{n}{tag(g)}</h3><p>{d}</p></article>' for n, d, c, g in C.TILES)
    lineup = f'''<section class="lineup" id="tudo">
  <div class="lineup-in">
    <h2 class="rev">Tudo o que ela faz.</h2>
    <p class="lead rev">Cada item desta lista roda hoje. O que ainda não roda está no capítulo anterior.</p>
    <div class="tiles rev">{tiles}</div>
  </div>
</section>'''

    h2, p = C.CTA
    cta = f'''<section class="cta">
  <h2 class="rev">{h2}</h2>
  <p class="rev">{p}</p>
  <div class="btns rev"><a class="btn btn-branco" href="{WA}">{wa_svg} Falar no WhatsApp</a></div>
  <p class="sub2 rev">ou <a href="mailto:contato@seevia.com.br">contato@seevia.com.br</a> · seevia.com.br</p>
</section>'''

    dl = '''<section class="dl">
  <h2>Leve o livreto com você.</h2>
  <p>Baixe o PDF para apresentar offline ou mandar por e-mail.</p>
  <div class="btns"><a class="btn" href="/livreto.pdf" download="livreto-seevia.pdf">
    Baixar o livreto (PDF)</a></div>
</section>'''

    body = "\n".join([nav, hero, credo, cap_camera, cap_gravacao, cap_vizinhanca,
                      cap_instalacao, cap_alarme, cap_operacao, cap_privacidade,
                      cap_limites, lineup, cta, dl])

    hoje = datetime.date.today().strftime("%d/%m/%Y")
    sha = hashlib.sha1(body.encode()).hexdigest()[:7]
    foot = (f'<footer class="foot"><div class="foot-in">'
            f'<span>Seevia · câmeras com IA e vizinhança conectada</span>'
            f'<span>Livreto v{hoje} · {sha}</span></div></footer>')

    desc = ("Livreto da Seevia: câmeras com IA que avisam só o que importa, gravação com linha "
            "do tempo de 24h, vizinhança compartilhada por opt-in (privada por padrão), alarme "
            "e pânico no mesmo app e instalação sem tocar na rede da casa.")
    url = f"{C.SITE}/livreto"
    head = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Livreto da Seevia — a câmera que avisa só o que importa</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" sizes="64x64" href="/assets/favicon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Seevia">
<meta property="og:locale" content="pt_BR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="Livreto da Seevia">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{C.SITE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"SoftwareApplication",
"name":"Seevia","applicationCategory":"SecurityApplication","operatingSystem":"Android",
"url":"{url}","inLanguage":"pt-BR","description":"{desc}",
"featureList":["Detecção por IA de pessoa, veículo, arma, fogo, alagamento e aglomeração",
"Regras por câmera com horário, área da imagem, permanência e intervalo",
"Alerta por WhatsApp, e-mail e feed do aplicativo",
"Gravação por movimento com linha do tempo de 24 horas e retenção de 2 a 30 dias",
"Vizinhança compartilhada por opt-in, privada por padrão, com alcance de 500 metros",
"Mapa do bairro com as câmeras próprias e as compartilhadas",
"Alarme no aplicativo: eventos, estado e saúde da central, armar e desarmar",
"Botão de pânico que avisa os outros moradores da casa",
"Instalação por leitura de QR, sem acesso à rede da casa",
"Ordem de serviço de instalação, manutenção e expansão"],
"publisher":{{"@type":"Organization","name":"Seevia","url":"{C.SITE}"}}}}</script>
<style>{CSS}</style>
</head>
<body>
'''
    doc = head + body + "\n" + foot + "\n" + SCRIPT + "\n</body>\n</html>\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(doc)
    print(f"[livreto] {OUT} — {len(doc)//1024} KB · v{hoje} · {sha}")

build()
