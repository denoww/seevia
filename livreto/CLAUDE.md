# Livreto da Seevia — playbook

Peça de vendas do comercial: página pública (`/livreto`) + PDF baixável (`/livreto.pdf`).
Documento de vida longa.

Herda a doutrina do livreto do SeuCondomínio (`~/workspace/seucondominio/livreto/CLAUDE.md`),
mas **na marca da Seevia e no domínio dela** — mesmo caminho de `baterponto-site` e
`atendeaqui-site`. Produto com marca e domínio próprios não se hospeda sob
`seucondominio.com.br`: o build de lá tem a marca cravada (logo, WhatsApp, rodapé, SEO,
JSON-LD) e a peça sairia com o remetente errado.

## Como regenerar

```bash
python3 livreto/build.py     # → livreto/index.html
bash    livreto/build_pdf.sh # → livreto.pdf (Chromium headless)
```

Rodar os **dois** e commitar os dois. Não há CI de espelho aqui (ainda): o site é estático
no **AWS Amplify** (`amplify.yml` sem build step, output `/`), então o que está commitado é
o que vai pro ar. O SeuCondomínio gera o PDF em runtime (Gotenberg) porque tem servidor —
aqui não tem.

Deploy = `git push` na `master` (Amplify builda sozinho). ⚠️ Validar mexida no Amplify sempre
com **canary de conteúdo**, nunca commit vazio — commit vazio produz output idêntico tanto se
o build funciona quanto se falha (o CDN mantém o build anterior).

## Onde editar (nunca no HTML gerado)

| Quero mudar | Arquivo |
|---|---|
| Texto (cards, storyboards, tiles, hero, CTA) — **95% das mudanças** | `content.py` |
| Um capítulo (composição de blocos), CSS, print CSS | `build.py` |
| Cenas dos storyboards (line-art SVG) | `build.py` → `SCENES` |
| Fotos | `../assets/*.jpg` (as mesmas do site) |

`livreto/index.html` e `livreto.pdf` são **gerados** — nunca edite à mão.

## Conteúdo é aterrado (não invente)

**Fonte da verdade, nesta ordem:**
1. `~/workspace/seucondominio/app/services/vision/ROADMAP_seevia_app.md` — o que roda
2. `~/workspace/seevia-app` — o app Flutter
3. `~/workspace/seucondominio/app/services/vision/CLAUDE.md` — o motor de IA das câmeras

> ⚠️ **O `index.html` deste repo NÃO é fonte da verdade.** Ele é uma peça de campanha antiga
> e afirma o que o produto não faz: "320 condomínios protegidos", "integrada à Polícia
> Militar / Guarda Municipal / Detran / SAMU", "central de inteligência 24h", "tecnologia
> importada do Vale do Silício", "sem reconhecimento facial", depoimentos assinados por
> pessoas e números de resultado (furtos, veículos recuperados, precisão da IA).
> **Nada disso entrou no livreto** — e quando o site for reescrito, esse é o débito a pagar.

**Regras de copy (não negociáveis):**

- **PROIBIDO prova social.** Nem número de clientes, nem percentual de acerto, nem
  depoimento. Vende-se a **dor** e o **mecanismo**.
- **Só o que roda em produção.** Selo `IA` marca onde o sistema decide sozinho. O que não
  roda vive no capítulo **"O que a Seevia não faz"** — que é o capítulo mais importante.
- **Uma coisa por frase.** Dor → alívio.
- **O vizinho não é vigilante; o morador não é suspeito.** O ângulo é a rua, nunca a pessoa.
- **Nunca dizer que o vizinho "vê a sua câmera".** Por padrão (`vizinhanca_ao_vivo=false`)
  ele vê o **evento** — modelo Ring. Ao vivo do vizinho é uma flag por operador.

**⛔ Nunca prometer** (verificado jul/2026 no `ROADMAP_seevia_app.md`):
**rastreio/rota de placa** (Fase 3, não construída) · **push/FCM** (Onda (c) bloqueada por
setup do Firebase Console) · **iOS** (o app é Android) · **central humana 24h nossa** (quem
monta plantão é a operação regional) · **cobrança recorrente automática** (hoje o gestor
emite e bloqueia na mão) · **marca própria por operação / white-label** (o
`IdentidadeVisualService` ainda devolve Seevia para todo tenant) · **áudio ao vivo** ·
**reconhecimento facial** (o kill switch de indexação está vazio) · **ao vivo instantâneo**
(HLS ~10s; WebRTC só na câmera em foco do muro).

## Pegadinhas do PDF (quebram em silêncio)

As três travas vivem no `@media print` do `build.py > CSS`:

1. `.rev{opacity:1!important}` — sem isso o PDF sai **em branco** (o reveal só dispara com
   scroll, e a impressão não rola a página).
2. `print-color-adjust:exact` — sem isso hero, CTA e fotos saem sem cor.
3. `break-inside:avoid` **só nas unidades atômicas** (`.fc`, `.bp`, `.tile`, `.board`,
   `.shot`). Nunca por capítulo nem na media row inteira — gera página quase vazia.
4. `@page{size:A4}` — sem isso o Chrome imprime em Letter.

**Como conferir** depois de rodar o build (o teste que pega os 4 casos acima):

```bash
pdftoppm -png -r 55 livreto.pdf /tmp/pg && python3 - <<'EOF'
from PIL import Image; import glob
for f in sorted(glob.glob('/tmp/pg*.png')):
    px=list(Image.open(f).convert('L').getdata())
    print(f, f"tinta={100*sum(1 for p in px if p<240)/len(px):.1f}%")
EOF
```

Página com **tinta < 3%** é página em branco — o build quebrou.

Referência da última geração: **19 páginas**, ~1,5 MB, nenhuma página abaixo de 6%.

## Validação no navegador

O reveal (`.rev`) esconde tudo até o scroll, então screenshot direto sai vazio. Gere uma
cópia temporária com o reveal forçado:

```bash
python3 -c "h=open('livreto/index.html').read(); open('livreto/_preview.html','w').write(
  h.replace('</head>','<style>.rev{opacity:1!important;transform:none!important}</style></head>'))"
python3 -m http.server 8894 &            # o file:// quebra as imagens /assets/...
google-chrome --headless=new --no-sandbox --hide-scrollbars --window-size=1280,7000 \
  --screenshot=/tmp/web.png --virtual-time-budget=12000 http://localhost:8894/livreto/_preview.html
rm livreto/_preview.html
```

⚠️ **Chrome headless tem largura mínima de ~500px** — pedir `--window-size=390` renderiza a
500 e **corta** a captura, o que parece overflow horizontal e não é. Para conferir overflow
de verdade, injete uma sonda que imprima `document.documentElement.scrollWidth` vs
`innerWidth` na própria página (SW > IW = overflow real).

## Marca

Azul `#104fd4` (`--azul-claro #3a78ff`, `--azul-neon #7aa2ff`), fundo escuro `#0b1020` —
os mesmos tokens do `index.html` do site. Logo em `/assets/seevia_azul.png` (fundo claro) e
`/assets/seevia_branco.png` (fundo escuro). Fotos noturnas em `/assets/`: `hero`, `camera`,
`central`, `app`, `ia_vision`.
