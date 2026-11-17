# -*- coding: utf-8 -*-
"""Conteúdo do livreto da Seevia — 95% das mudanças acontecem AQUI.

Edite este arquivo e rode `python3 livreto/build.py` (+ `bash livreto/build_pdf.sh`).

FONTE DA VERDADE FACTUAL, nesta ordem de precedência:
  1. ~/workspace/seucondominio/app/services/vision/ROADMAP_seevia_app.md  ← o que RODA
  2. ~/workspace/seevia-app  (o app Flutter)
  3. ~/workspace/seucondominio/app/services/vision/CLAUDE.md  (motor de IA das câmeras)

⚠️ O `index.html` deste site NÃO é fonte da verdade. Ele é uma peça de campanha antiga e
afirma coisas que o produto não faz: "320 condomínios protegidos", "integrada à Polícia
Militar / Guarda Municipal / Detran / SAMU", "central 24h", "tecnologia do Vale do Silício",
"sem reconhecimento facial", depoimentos assinados e números de resultado.
Nada disso entra no livreto — o livreto vende DOR + MECANISMO, e só o que roda.

REGRAS DE COPY (herdadas de ~/workspace/seucondominio/livreto/CLAUDE.md):
  - PROIBIDO prova social. Nada de "X condomínios", "Y% de precisão", depoimento.
  - Só o que roda em produção. O que é roadmap vive no capítulo "O que a Seevia não faz".
  - Uma coisa por frase. Dor → alívio.
  - O vizinho não é vigilante e o morador não é suspeito: o ângulo é a RUA, nunca a pessoa.
  - Nunca dizer que o vizinho "vê a sua câmera" — por padrão ele vê o EVENTO (modelo Ring).
  - Nunca prometer: rastreio/rota de placa (Fase 3), push (bloqueado no Firebase), iOS,
    central humana 24h nossa, cobrança recorrente automática, marca própria por operação,
    áudio ao vivo, reconhecimento facial.
"""

WA = "https://wa.me/5562985673142"
WA_TXT = "?text=Ol%C3%A1%21%20Vi%20o%20livreto%20da%20Seevia%20e%20quero%20conhecer."
SITE = "https://seevia.com.br"

# ---------------------------------------------------------------- hero / credo
HERO = {
    "eyebrow": "Livreto",
    "h1": "As câmeras da sua rua, no seu bolso.",
    "sub": "A câmera entende o que vê e avisa só o que merece atenção. A gravação fica "
           "guardada longe de quem entra na sua casa. E o vizinho recebe o alerta da rua — "
           "se, e só se, você deixar.",
}

CREDO = ('A câmera não avisa quando alguém passa. '
         '<span class="g">Avisa quando vale a pena olhar.</span>')

# ---------------------------------------------------------------- storyboards
# chave: (cor, título, [(cena, título, legenda)])
BOARDS = {
    "evento": ("azul", "Do quadro na câmera ao aviso no celular", [
        ("cam",     "A câmera olha",     "Vinte e quatro horas, na chuva e no escuro — sem ninguém do outro lado assistindo."),
        ("ia",      "A IA lê a cena",    "Pessoa, veículo, arma, fogo, alagamento. O que é rotina não vira aviso."),
        ("regra",   "A regra decide",    "A sua câmera, o seu horário, o seu pedaço da imagem. Fora disso, silêncio."),
        ("celular", "Você recebe",       "WhatsApp, e-mail e o feed do app — com a imagem do instante junto."),
    ]),
    "instalacao": ("verde", "Do galpão ao muro, sem técnico de rede", [
        ("bancada", "Configurada antes", "A câmera já sai da bancada sabendo para onde mandar o vídeo."),
        ("cabo",    "Cabo e energia",    "No muro, o eletricista só fixa e liga. Nada de notebook."),
        ("qr",      "Um QR e pronto",    "O instalador bipa o código pelo app e a câmera passa a ser da sua casa."),
        ("aovivo",  "Aparece ao vivo",   "A imagem abre no seu celular antes de ele descer da escada."),
    ]),
    "vizinhanca": ("ciano", "Como a rua fica sabendo (e como não fica)", [
        ("cadeado", "Nasce privada",      "Ninguém vê a sua câmera. Nem o vizinho, nem o vizinho do vizinho."),
        ("toque",   "Você liga",          "Um toque no app compartilha. Outro toque, na mesma tela, desliga."),
        ("raio",    "Só quem está perto", "Quinhentos metros das suas câmeras. Não é a cidade: é o seu quarteirão."),
        ("casa",    "O vizinho recebe",   "Chega o evento com a imagem — não o seu ao vivo."),
    ]),
    "sos": ("ambar", "O botão de pânico que não dispara sem querer", [
        ("segura",  "Segure dois segundos", "O anel enche enquanto o dedo fica. Esbarrão não manda nada."),
        ("onda",    "O pedido sai",         "A casa de onde partiu e a hora vão junto."),
        ("familia", "Os outros recebem",    "WhatsApp e e-mail para os outros moradores da casa. Quem apertou já sabe."),
    ]),
}

# ---------------------------------------------------------------- capítulos
# (título, texto, selo)  — selo "" = produção. "IA" = onde o sistema decide.
# Nunca vender roadmap como pronto: se não roda hoje, vai pro NAO_FAZ.

CAMERA = [
    ("Ninguém assiste doze horas para achar dez segundos",
     "A câmera comum grava e espera você procurar. Aqui a análise roda quadro a quadro e "
     "separa o trecho que merece ser visto — o resto continua sendo só imagem parada.", "IA"),
    ("O que ela reconhece",
     "Pessoa, veículo, arma, fogo, alagamento, aglomeração e alguém rondando o mesmo ponto. "
     "Cada um vira um alerta com o nível de urgência que você definiu.", "IA"),
    ("A regra é sua, não do fabricante",
     "Cada alerta tem câmera, horário, pedaço da imagem que vale, tempo mínimo de permanência "
     "e intervalo até repetir. Alguém no portão às três da manhã não é a mesma coisa que às "
     "três da tarde.", ""),
    ("Silenciar sem desligar",
     "Festa, obra, mudança: a regra dorme pelas horas que você marcar e acorda sozinha. "
     "Ninguém esquece a câmera desligada no dia seguinte.", ""),
    ("O aviso chega onde você lê",
     "WhatsApp, e-mail e o feed do app — com a foto do instante, a câmera e a hora.", ""),
    ("O que aconteceu fica registrado",
     "Cada alerta guarda a imagem do momento, a regra que disparou e o horário. É o que "
     "sobra depois, quando alguém precisa reconstruir a noite.", ""),
]

GRAVACAO = [
    ("Grava quando acontece",
     "O trecho com movimento é recortado e sobe para a nuvem. Não é preciso vasculhar um "
     "arquivo de vinte e quatro horas para achar o carro que parou na esquina.", ""),
    ("A linha do tempo do dia",
     "Um player só, com a fita das 00h às 24h: os blocos mostram onde houve movimento, o "
     "toque pula para o instante e a velocidade vai de meia a oito vezes.", ""),
    ("Ao vivo e gravação na mesma tela",
     "A pílula “AO VIVO” fica acesa; um botão volta no tempo e outro devolve para agora. "
     "Sem trocar de tela, sem trocar de aplicativo.", ""),
    ("Quanto tempo guardar é escolha de plano",
     "Dois, sete, quinze ou trinta dias, câmera a câmera. A da frente pode guardar mais "
     "do que a do quintal.", ""),
    ("Longe de quem entra na sua casa",
     "O ladrão que leva o gravador não leva a prova: o trecho já saiu de casa antes de ele "
     "chegar à tomada.", ""),
    ("Momentos",
     "Uma tira de miniaturas mostra o que o dia teve, para o dedo ir direto ao trecho certo.", ""),
]

VIZINHANCA = [
    ("Nasce privada. Sempre.",
     "Nenhuma câmera é compartilhada por padrão. Enquanto você não ligar, ninguém no bairro "
     "sabe que ela existe.", ""),
    ("O vizinho vê o evento, não a sua casa",
     "Compartilhar não entrega a sua imagem ao vivo: entrega o que a câmera detectou — a foto "
     "do instante, o que foi e quando. A sua sala continua sendo sua.", ""),
    ("Só quem está perto",
     "O alcance é de quinhentos metros das suas câmeras. Quem mora do outro lado da cidade "
     "não entra na sua vizinhança — nem você na dele.", ""),
    ("O mapa do bairro",
     "As câmeras aparecem como pinos no mapa: as suas e as compartilhadas por perto. "
     "Um toque no pino abre a câmera.", ""),
    ("Desligar é um toque",
     "O mesmo botão que compartilhou desfaz. Sem ligar para ninguém e sem pedir para o "
     "instalador voltar.", ""),
    ("Quanto mais vizinhos, menos ponto cego",
     "Cobrir a rua inteira não depende de um morador comprar dez câmeras. Depende de dez "
     "vizinhos ligarem a que já têm.", ""),
]

INSTALACAO = [
    ("O eletricista não mexe na sua internet",
     "A câmera sai da bancada já configurada. No muro é cabo, energia e um QR — ninguém "
     "pede a senha do seu Wi-Fi nem entra na sua rede.", ""),
    ("Rede de visitante, rede isolada, tanto faz",
     "A câmera fala para fora, não para dentro. É por isso que ela funciona onde o "
     "aplicativo do fabricante trava.", ""),
    ("Bipou, é sua",
     "O QR liga aquela câmera à sua casa e ao ponto do mapa onde ela está. O ao vivo abre "
     "na hora, para conferir o ângulo antes de o instalador ir embora.", ""),
    ("Cada visita é uma ordem",
     "Instalação, manutenção e câmera nova viram tarefa com responsável, data e histórico. "
     "Nada mora no WhatsApp do técnico.", ""),
    ("A instalação termina testando",
     "Para fechar a ordem, o instalador abre câmera por câmera e confirma que a imagem está "
     "no ar. Não existe “deixei funcionando” sem prova.", ""),
    ("Uma câmera a mais é uma ordem a mais",
     "Ampliar não é refazer: a casa já existe no sistema e a câmera nova entra no mesmo "
     "grupo, com o mesmo login.", ""),
]

ALARME = [
    ("Alarme e câmera no mesmo aplicativo",
     "Os eventos da central chegam onde você já vê as câmeras: disparo, pânico, arme, "
     "desarme e falha.", ""),
    ("O estado da central, sem adivinhação",
     "Armada, desarmada — e, quando a central ainda não disse nada, o app diz que não sabe "
     "em vez de chutar “desarmada”. Casa aberta não se supõe.", ""),
    ("A central avisa quando ELA está mal",
     "Sem energia, bateria fraca, falha de comunicação. O problema que ninguém percebe é "
     "justamente o que deixa a casa desprotegida na hora errada.", ""),
    ("Em casa · Saindo · Desarmar",
     "Três botões em português, sem código de instalador. Desarmar pede confirmação — é a "
     "ação que baixa a guarda.", ""),
    ("O painel é quem manda",
     "O app não finge que armou: o cartão só muda quando o evento volta da central. O que "
     "você lê na tela é o que o equipamento fez.", ""),
    ("Pânico com dois segundos de dedo",
     "Segure o botão e o anel enche; solte antes e nada acontece. Ao completar, os outros "
     "moradores da casa recebem WhatsApp e e-mail.", ""),
]

OPERACAO = [
    ("O muro",
     "Dezenas de câmeras numa grade só — e, quando a IA detecta algo, a grade foca sozinha "
     "na câmera do evento. A ronda por tempo continua correndo por baixo.", "IA"),
    ("A carteira da operação",
     "Casas, comércios e condomínios com suas câmeras, seus moradores e suas ordens abertas. "
     "Uma tela para saber o que está instalado e o que está pendente.", ""),
    ("A equipe de campo",
     "O gerente abre a ordem e escolhe o instalador. O instalador abre “Minhas ordens” e vê "
     "exatamente o que fazer hoje.", ""),
    ("A cobrança da casa",
     "Cada casa tem um pagador — que pode não ser o dono. Dele saem o boleto e o PIX, com a "
     "conciliação acontecendo dentro do sistema.", ""),
    ("Inadimplência tem consequência",
     "Casa bloqueada some das câmeras e recebe o aviso para regularizar. O caixa da operação "
     "não depende de cobrança por telefone.", ""),
    ("Quem chega pelo WhatsApp vira cadastro",
     "O panfleto leva a um número. A conversa é atendida, o pedido é registrado numa linha do "
     "tempo e o gerente lê o recado já resumido.", "IA"),
]

PRIVACIDADE = [
    ("Privado é o padrão, não a opção",
     "Compartilhar exige um ato explícito do dono da câmera, dentro do app. Ninguém liga isso "
     "por você — nem quem vende, nem quem instala.", ""),
    ("A câmera vê que há alguém, não quem é",
     "As regras olham o que acontece: pessoa, veículo, fogo, alagamento. Não há identificação "
     "de rosto de quem passa na rua.", ""),
    ("O alcance é o quarteirão",
     "A vizinhança se resolve por distância das suas câmeras, não por uma lista de moradores "
     "que alguém montou à mão.", ""),
    ("Cada um vê o que é dele",
     "Morador vê a própria casa e o que os vizinhos compartilharam. Instalador vê a ordem que "
     "está executando. Gerente vê a operação dele — e nada da operação do vizinho.", ""),
]

# ---------------------------------------------------------------- honestidade
# O capítulo mais importante do livreto. Sai direto do ROADMAP_seevia_app.md.
NAO_FAZ = [
    ("Não tem app de iPhone",
     "O aplicativo é Android. iOS está no plano — e plano não se vende como pronto.", ""),
    ("Não faz o celular apitar com o app fechado",
     "Hoje o aviso sai por WhatsApp e e-mail. A notificação empurrada ainda não está ligada.", ""),
    ("Não rastreia a rota de um carro",
     "Cruzar as câmeras da rede para montar o caminho de um veículo pelo bairro é o próximo "
     "capítulo. Hoje não existe.", ""),
    ("Não é uma central humana 24 horas nossa",
     "A Seevia entrega a tecnologia: a IA que separa o evento, o muro que foca sozinho e o "
     "alerta que chega. Quem monta plantão é a operação da sua região.", ""),
    ("O ao vivo não é instantâneo",
     "A imagem ao vivo chega com alguns segundos de atraso. O que já aconteceu, a gravação "
     "entrega na hora.", ""),
    ("Não tem áudio",
     "Não dá para ouvir nem falar pela câmera. O que ela entrega é imagem.", ""),
    ("A cobrança não se repete sozinha",
     "O gestor emite a cobrança e bloqueia quem não pagou. A mensalidade automática ainda "
     "está sendo construída.", ""),
    ("Não serve qualquer câmera",
     "A câmera precisa mandar o vídeo para o nosso servidor no formato certo. Câmera antiga "
     "mal configurada até aparece ao vivo, mas não grava.", ""),
]

# ---------------------------------------------------------------- lineup
# (nome, descrição, cor, selo)
TILES = [
    ("Detecção por IA",     "Pessoa, veículo, arma, fogo, alagamento, aglomeração.", "azul",  "IA"),
    ("Regras por câmera",   "Horário, área da imagem, permanência e repetição.",     "azul",  ""),
    ("Silenciar regra",     "Festa e obra sem desligar a câmera.",                   "azul",  ""),
    ("Clipe por movimento", "O trecho sobe para a nuvem sozinho.",                   "verde", ""),
    ("Linha do tempo 24h",  "Toque para pular ao instante, de 0,5× a 8×.",           "verde", ""),
    ("Retenção por plano",  "2, 7, 15 ou 30 dias, câmera a câmera.",                 "verde", ""),
    ("Vizinhança opt-in",   "Privada por padrão; o dono liga e desliga.",            "ciano", ""),
    ("Mapa do bairro",      "As suas câmeras e as compartilhadas por perto.",        "ciano", ""),
    ("Alarme no app",       "Eventos, estado e saúde da central.",                   "ambar", ""),
    ("Armar e desarmar",    "Em casa, Saindo, Desarmar — pelo celular.",             "ambar", ""),
    ("Pânico SOS",          "Dois segundos de dedo avisam a casa inteira.",          "ambar", ""),
    ("Ordem de serviço",    "Instalação, manutenção e expansão com responsável.",    "roxo",  ""),
    ("Bipar o QR",          "A câmera vira sua sem ninguém tocar na sua rede.",      "roxo",  ""),
    ("Muro do operador",    "A grade que foca sozinha na câmera do evento.",         "roxo",  "IA"),
    ("Cobrança por casa",   "Pagador, boleto, PIX e bloqueio por inadimplência.",    "roxo",  ""),
]

CTA = ("Sua rua pode enxergar hoje à noite.",
       "Conte quantas câmeras você tem, onde elas ficam e quem mais na rua toparia entrar. "
       "A gente mostra funcionando.")
