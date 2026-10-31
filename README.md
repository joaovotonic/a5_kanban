# A5 Kanban - Sistema Operacional de Oficina e Gestão de OS

Sistema completo de gestão visual (Kanban), rastreamento de Ordens de Serviço (OS), consulta de balcão, expedição, painel para TV com locução por voz (TTS), catálogo de peças Toledo e central multimídia YouTube integrada com Ducking de áudio automático.

---

## 🚀 Funcionalidades Principais

- **Quadro Kanban em Tempo Real:**
  - Fluxo completo de manutenção de balanças e equipamentos industriais.
  - Atualizações instantâneas via WebSockets (`Flask-SocketIO`).
  - Arrastar e soltar (Drag and Drop) ágil e responsivo.
  - Regras de negócio automáticas (registro de peças, técnicos responsáveis, motivos de pausa e status).

- **Painel TV Interativo (`/painel-tv`):**
  - Exibição de chamados em tela cheia com modo escuro industrial.
  - Sintetizador de voz (TTS) para chamadas automáticas de técnicos e anúncios de bancada.
  - **Central de Música YouTube Nativa:**
    - Busca instantânea por termo (músicas, artistas, shows).
    - Suporte a contas YouTube Premium.
    - Streaming contínuo com suporte a *Audio Ducking* (o volume da música baixa automaticamente durante os avisos sonoros e locuções).

- **Consulta Rápida de Balcão (`/consulta`):**
  - Busca ágil por número de OS, cliente ou número de série.
  - Visualização resumida com status da bancada em tempo real.

- **Recepção e Fotos (`/recepcao-fotos`):**
  - Upload de fotos de entrada dos equipamentos direto da bancada/celular.
  - Armazenamento particionado por número de OS.

- **Gerência e Relatórios (`/gerencia`):**
  - Indicadores de tempo de ciclo, distribuição de chamados por técnico e faturamento de peças.
  - Exportação de dados e relatórios gerenciais.

- **Impressão de Etiquetas e Folhas de OS (`/etiqueta/<id>`, `/folha/<id>`):**
  - Formatação pronta para impressoras térmicas (Zebra, Elgin) e impressoras padrão A4.

- **Segurança e Resiliência:**
  - Backup automático e sob demanda do banco de dados SQLite e dumps JSON.
  - Catálogo de peças Toledo integrado.

---

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.11+, Flask, Flask-SocketIO, SQLite3
- **Streaming & YouTube:** `yt-dlp`, Innertube API, HTTP 206 Partial Content Proxy
- **Frontend:** HTML5, CSS3 moderno (Design Dark Industrial), Vanilla JavaScript, SortableJS
- **Comunicação em Tempo Real:** WebSockets (Engine.IO / Socket.IO)

---

## 📦 Instalação e Execução

### 1. Clonar o Repositório
```bash
git clone https://github.com/<seu-usuario>/a5_kanban.git
cd a5_kanban
```

### 2. Criar e Ativar Ambiente Virtual (Recomendado)
```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação
```bash
python app.py
```

A aplicação estará disponível em:
- **Painel Principal (Kanban):** `http://localhost:5000/`
- **Painel TV:** `http://localhost:5000/painel-tv`
- **Consulta de Balcão:** `http://localhost:5000/consulta`
- **Painel Gerencial:** `http://localhost:5000/gerencia`

---

## 📂 Estrutura do Projeto

```text
a5_kanban/
├── app.py                      # Ponto de entrada do servidor Flask
├── kanban/                     # Pacote modular da aplicação
│   ├── config.py               # Configurações de caminhos e ambiente
│   ├── database.py             # Camada de banco de dados SQLite
│   ├── realtime.py             # Eventos e broadcasts WebSocket
│   ├── routes/                 # Blueprints de rotas (pages, cards, youtube, etc.)
│   └── services/               # Serviços de negócio (cards, youtube, backup, parts)
├── database/                   # Dados locais e catálogo de peças
├── static/                     # CSS, JavaScript e efeitos sonoros
├── templates/                  # Templates Jinja2 das telas do sistema
├── requirements.txt            # Dependências Python
└── README.md                   # Documentação do projeto
```

---

## 📄 Licença

Propriedade privada de A5 Kanban / Oficina Toledo. Todos os direitos reservados.

