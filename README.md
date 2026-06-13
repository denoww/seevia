# seevia

Site institucional da **Seevia** — plataforma de câmeras com IA (`câmera + IA = pegar ladrão`).

Atualmente: página **coming-soon** estática (`index.html` + `assets/`).

## Stack

- Site estático puro (HTML/CSS), **sem build, sem servidor**.
- Hospedagem: **AWS Amplify Hosting** (CloudFront + ACM + CI do GitHub embutidos).
- DNS: **Route53** (hosted zone `seevia.com.br`, NS delegados do registro.br).
- Deploy: **automático no push** pra `master` (Amplify observa este repo).

## Local

```bash
# pré-visualizar
python3 -m http.server 8080
# abrir http://localhost:8080
```

## Estrutura

```
index.html        # coming-soon
amplify.yml       # config de build do Amplify (artefato = raiz, sem build step)
assets/           # logos, favicon, og image (brand kit Seevia)
```

## Marca

- Azul Seevia: `#104fd4`
- Escuro: `#0b1020`
- Fonte: Inter
- Kit completo: ver brand kit Seevia.
