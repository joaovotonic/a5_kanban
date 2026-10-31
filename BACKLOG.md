# Backlog e Especificação de Funcionalidades - Kanban A5 Tecnologia

Documento oficial de registro, arquitetura e controle de demandas, novas regras operacionais e recursos do Sistema Kanban Local da A5 Tecnologia.

---

## 📌 Item 1: Liberação de Reabertura de Orçamento pelo Painel Admin (Recepção)

* **Status:** ✅ **Implementado e em Produção**
* **Solicitante:** Recepção / Gerência Operacional
* **Telas Impactadas:**
  - `templates/saida.html` (Bancada Mobile dos Técnicos)
  - `templates/admin.html` (Painel da Priscila / Recepção)
  - Backend Flask (`kanban/routes/cards.py`, `kanban/services/cards.py`, `kanban/realtime.py`, `kanban/database.py`)

### 1. Contexto e Motivação
Quando um técnico conclui a folha digital de orçamento na tela mobile (`/saida`), a O.S. passa para o estágio `waiting_approval` (aguardando cliente aprovar). Como a Priscila já pode ter enviado a proposta ao cliente, o técnico não pode reabrir o orçamento sozinho sem antes pedir liberação na recepção.

### 2. Comportamento Implementado
1. **Na Tela Mobile (`/saida`):**
   - O botão `✏️ Solicitar Reabertura do Orçamento (Pedir Liberação)` permanece visível.
   - Ao ser clicado, envia `POST /api/cards/<id>/request-reopen`, grava `reopen_requested = 1` com nome do técnico e horário, e exibe um aviso na tela mobile informando que aguarda a liberação da Priscila.
2. **No Painel Admin da Recepção (`/admin`):**
   - Dispara notificação em tempo real (`admin_notification` via Socket.IO) com alerta sonoro, toast flutuante, barra de pendências no topo do quadro, badge `🔓 Pede Reabertura` no cartão e caixa de decisão dentro do modal da O.S.
   - Priscila pode clicar em `✅ Liberar Edição do Orçamento` (que reabre o orçamento e destrava imediatamente a tela mobile do técnico) ou `✕ Recusar`.

---

## 📌 Item 2: Controle de Exclusão e Cancelamento de O.S. + Centralização do Nome do Cliente

* **Status:** ✅ **Implementado e em Produção**
* **Solicitante:** Recepção / Gerência Operacional
* **Telas Impactadas:**
  - `templates/admin.html` (Modal de Detalhes da O.S. e Modal de Autenticação)
  - Backend Flask (`kanban/routes/cards.py`, `kanban/services/cards.py`)

### 1. Comportamento Implementado
- **Nome do Cliente Centralizado:** Cabeçalho de destaque centralizado no modal da O.S. (`text-center`) para evitar quebra espremida à esquerda.
- **Cancelar O.S. (`🚫 Cancelar O.S.`):** Move a O.S. para a coluna `ORÇAMENTOS NÃO AUTORIZADOS` e aplica a etiqueta `NÃO AUTORIZADO`, preservando o histórico.
- **Excluir O.S. (`🗑️ Excluir O.S.`):** Protegido por modal de autenticação com **Login:** `admin` e **Senha:** `admin` (validado no frontend e no backend em `DELETE /api/cards/<id>`).

---

## 📌 Item 3: Notificação em Tempo Real para a Priscila quando a Análise Técnica é Concluída

* **Status:** ✅ **Implementado e em Produção**
* **Telas Impactadas:** `kanban/routes/cards.py`, `kanban/realtime.py`, `templates/admin.html`
* **Descrição:** Quando o técnico conclui o orçamento na bancada mobile (`/saida`), o sistema move o cartão para `ANALISES FEITAS` e emite imediatamente um alerta visual e sonoro na tela da Priscila (`/admin`) informando qual O.S., cliente e técnico acabaram de concluir a análise, com botão rápido `🔍 Abrir O.S.`.

---

## 📌 Item 4: Nova Lista `BALANÇAS PRONTAS` e Botão de Finalização pela Priscila

* **Status:** ✅ **Implementado e em Produção**
* **Telas Impactadas:** `kanban/database.py`, `kanban/rules.py`, `kanban/services/cards.py`, `kanban/routes/cards.py`, `templates/admin.html`
* **Descrição:**
  - Criada automaticamente a lista `BALANÇAS PRONTAS` (`role = 'pronta'`) posicionada antes de `FINALIZADAS`.
  - Quando o técnico finaliza o serviço na bancada (`/saida`), a balança é enviada para `BALANÇAS PRONTAS` (com notificação na tela da Priscila), mantendo total acesso para conferência administrativa.
  - Dentro do modal da O.S. em `/admin`, a Priscila possui o botão `🏁 Finalizar O.S. (Enviar p/ FINALIZADAS)` (`POST /api/cards/<id>/finalize-admin`) para transferir o cartão para `FINALIZADAS` após revisar tudo.

---

## 📌 Item 5: Botão `📤 Enviar Orçamento` (`ANALISES FEITAS` → `ORÇAMENTOS ENVIADOS`)

* **Status:** ✅ **Implementado e em Produção**
* **Telas Impactadas:** `kanban/services/cards.py`, `kanban/routes/cards.py`, `templates/admin.html`
* **Descrição:** Quando a análise técnica está pronta na lista `ANALISES FEITAS`, o modal da O.S. exibe o botão em destaque `📤 Enviar Orçamento`. Ao clicar nele (`POST /api/cards/<id>/send-quote`), o cartão é movido automaticamente para a lista `ORÇAMENTOS ENVIADOS`, recebe a etiqueta `AGUARDANDO` e registra o envio no histórico.

---

## 📌 Item 6: Aba de Anotações Internas da Recepção (`admin_notes`)

* **Status:** ✅ **Implementado e em Produção**
* **Telas Impactadas:** `kanban/database.py`, `kanban/services/board.py`, `kanban/services/cards.py`, `templates/admin.html`
* **Descrição:** Adicionada a seção `📝 Aba de Anotações da Recepção (Priscila)` dentro do modal da O.S. em `/admin`, permitindo registrar e salvar observações livres (negociação, prazos, recados do cliente) com indicador `📝` no cartão do quadro.

---

## 📌 Item 7: Criação de Cartões Diretamente Dentro de Qualquer Lista do Kanban

* **Status:** ✅ **Implementado e em Produção**
* **Telas Impactadas:** `templates/admin.html`
* **Descrição:** Cada coluna do quadro Kanban possui agora o botão `➕` no cabeçalho e `➕ Adicionar Cartão aqui` no rodapé da lista, abrindo o modal de criação com aquela lista já pré-selecionada, caso a Priscila queira criar o cartão diretamente em uma lista específica sem passar por `NOVA O.S.`.

---

## 📌 Item 8: Edição Completa da Ordem de Serviço Dentro do Cartão Já Criado

* **Status:** ✅ **Implementado e em Produção**
* **Telas Impactadas:** `kanban/services/cards.py`, `kanban/routes/cards.py`, `templates/admin.html`
* **Descrição:** Adicionado botão rápido `🛠️ Editar O.S.` no topo do modal e expandida a seção de edição cadastral para permitir corrigir qualquer campo da O.S. já criada: **Nº da O.S.** (com validação de duplicidade e atualização do histórico), **Cliente**, **Tipo de Equipamento**, **Modelo / Capacidade**, **Nº de Série**, **Local / Prateleira**, **Defeito Relatado** e **Serviço Feito Anteriormente**.

---

## 📌 Item 9: Botões Rápidos de Defeitos na Criação e Edição da O.S.

* **Status:** ✅ **Implementado e em Produção**
* **Telas Impactadas:** `templates/admin.html`
* **Descrição:** Na aba de defeito informado (tanto no cadastro de Nova O.S. quanto na edição de O.S. existente), foram adicionados botões rápidos clicáveis além do campo de escrita livre:
  - `⚖️ Diferença de peso`
  - `📉 Oscilando o peso`
  - `🖨️ Falha na impressão`
  - `⌨️ Falha no teclado`
  - `🔌 Falha na comunicação`
  - `⚡ Não liga`
  - `🖥️ Display apagado`

---

## 📌 Item 10: Formatação Automática do Número do Selo (`00.000.000-0`)

* **Status:** ✅ **Implementado e em Produção**
* **Telas Impactadas:** `templates/saida.html`
* **Descrição:** O campo de número do Selo na aba de orçamento (`#incomingStampNum`) aplica automaticamente a máscara `00.000.000-0` durante a digitação (`formatStampMask`).

---

## 📌 Item 11: Pesagem em Gramas (`g`) para Balanças Analíticas e Alerta de `DIFERENÇA DE PESO` (Fora da Especificação)

* **Status:** ✅ **Implementado e em Produção**
* **Telas Impactadas:** `kanban/services/board.py`, `templates/saida.html`, `templates/admin.html`, `templates/folha.html`
* **Descrição:**
  - **Suporte a Gramas (`g`) e Quilos (`kg`):** Quando a balança é Analítica / Precisão ou tem capacidade em gramas (ex.: `Marte 510g`), ou ao alternar o seletor `KG / GRAMAS (g)`, os campos de pesos iniciais e finais mudam automaticamente para gramas (`1g`, `10g`, `100g`, `500g`, `5g`, `50g`, `20g`, `200g`, `1000g`, `2000g`).
  - **Comparação Automática e Alerta de Diferença de Peso:** Ao preencher os pesos iniciais (ex.: peso de `1g` ou `1kg`), o sistema compara o valor nominal com o peso medido e exibe em destaque na tela do técnico e na tela da Priscila (`/admin`):
    > `⚠️ FORA DA ESPECIFICAÇÃO: 1kg - 0,098kg DIFERENÇA DE PESO` (ou `1g - 0,95g DIFERENÇA DE PESO`).

---

## 📌 Item 12: Regra Metrológica de Tolerância em Oficina (Limite de 2 Incrementos ±2e)

* **Status:** ✅ **Implementado e em Produção**
* **Telas Impactadas:** `kanban/services/scales.py`, `templates/saida.html`, `templates/admin.html`
* **Descrição:**
  - Implementação da regra metrológica oficial de calibração em oficina para balanças comerciais Toledo Prix, industriais e analíticas.
  - **Critério de Tolerância:** Limite de até **2 incrementos (divisões $e$)** para mais ou para menos ($\pm 2e$).
    - Se a divisão $e$ da balança na carga for de $2\text{g}$, um desvio de até $\pm 4\text{g}$ (ex: $1.002\text{kg}$ ou $0.998\text{kg}$) é considerado **DENTRO DA TOLERÂNCIA** (`✓ Na tolerância: +2g ≤ ±4g • e=2g`).
    - Se o desvio atingir 3 ou mais incrementos ($> 2e$, ex: $1.006\text{kg}$ ou $0.994\text{kg}$ ou $0.098\text{kg}$), a balança é classificada como **FORA DA TOLERÂNCIA — DIFERENÇA DE PESO (requer calibração)**.
  - **Faixas Toledo Prix Comercial (30kg/32kg Tripla Faixa):**
    - 0 a 6kg: $e = 2\text{g} \to$ tolerância máx. $\pm 4\text{g}$
    - 6 a 15kg: $e = 5\text{g} \to$ tolerância máx. $\pm 10\text{g}$
    - 15 a 32kg: $e = 10\text{g} \to$ tolerância máx. $\pm 20\text{g}$
  - **Balanças Analíticas (Marte 510g):**
    - $e = 0.01\text{g} \to$ tolerância máx. $\pm 0.02\text{g}$
  - **Plataformas Industriais (Toledo 2180 50kg a 3000kg):**
    - Divisões automáticas de $10\text{g}$, $20\text{g}$, $50\text{g}$, $100\text{g}$, $200\text{g}$, $500\text{g}$ e $1\text{kg}$.

---

## 📌 Item 13: Banco de Dados de Modelos de Balança Toledo e Autocomplete Dinâmico

* **Status:** ✅ **Implementado e em Produção**
* **Telas Impactadas:** `kanban/database.py`, `kanban/services/scales.py`, `kanban/routes/cards.py`, `templates/admin.html`
* **Descrição:**
  - Criada a tabela SQLite `scale_models` contendo o catálogo completo de balanças da Toledo do Brasil (Prix 3, 4, 5, 6, 7, 2090 Baby/PP, 2180 Plataforma 50-3000kg, 9094, 3400), Balanças Analíticas Marte (510g, 210g) e outras marcas homologadas.
  - Endpoint REST `/api/scales/search?q=...` com busca rápida por modelo, capacidade e marca.
  - **Autocomplete no Cadastro de Nova O.S. e na Edição da O.S.:**
    - Ao começar a digitar no campo `Modelo / Capacidade` (ex.: "prix", "fit", "2180", "marte"), abre instantaneamente um dropdown inteligente com o modelo, capacidade, marca e descrição das divisões.
    - Ao selecionar uma balança, o modelo é preenchido e o seletor `Tipo de Equipamento` é ajustado automaticamente (ex.: "Balança Toledo Prix", "Balança Industrial / Plataforma", "Balança Analítica / Precisão").

---

## 📌 Item 14: Lacre Compacto e Visível + Laudo Técnico e Peças no Topo do Modal Admin

* **Status:** ✅ **Implementado e em Produção**
* **Telas Impactadas:** `templates/admin.html`
* **Descrição:**
  - **Redimensionamento do Lacre:** O bloco do Lacre não ocupa mais espaço excessivo. Quando pendente, exibe uma barra discreta e elegante (`🛡️ Lacre: Aguardando finalização técnica`). Quando preenchido pelo técnico, apresenta um badge verde esmeralda com o número em destaque mono, técnico finalizador e o botão rápido `📋 Copiar Lacre p/ Teorema`.
  - **Laudo Técnico e Peças Orçadas no Topo:** O bloco `📋 Laudo Técnico & Solução` e `⚙️ Peças Substituídas / Códigos Toledo` foi movido para o topo do modal da O.S., logo abaixo da identificação e do lacre. O laudo do técnico para o cliente agora possui moldura destacada de alta visibilidade e botão `📋 Copiar p/ Vendas`, permitindo à Priscila repassar o diagnóstico e valores com máxima rapidez sem precisar rolar a tela.

---

## 📌 Item 15: Laudo em Destaque na Bancada Mobile e Estufa Exclusiva na Finalização

* **Status:** ✅ **Implementado e em Produção**
* **Telas Impactadas:** `templates/saida.html`
* **Descrição:**
  - **Laudo Técnico Evidente no Celular:** Na tela mobile (`/saida`), durante a fase de aguardando aprovação do cliente ou finalização, o Laudo Técnico é renderizado em um card com borda iluminada azul e tipografia em negrito, exibindo com total clareza o diagnóstico do avaliador.
  - **Remoção da Estufa na Fase de Orçamento:** O bloco `⏱️ Cronômetro de Estufa / Teste na TV` foi removido do cabeçalho de orçamento e transferido exclusivamente para o formulário de **Finalização do Serviço** (`#finishForm`), momento adequado em que o reparo já foi executado e a placa/balança entra no teste de bancada ou estufa.

---

## 📌 Item 16: Painel Dinâmico da TV: Base Limpa (Orçamentos & Aprovadas) + Técnicos Ativos Horizontais

* **Status:** ✅ **Implementado e em Produção**
* **Solicitante:** Gerência Operacional / Técnicos de Bancada
* **Telas Impactadas:** `templates/tv.html`
* **Descrição:**
  - **Layout Base Limpo (Padrão):**
    - Por padrão (quando nenhuma bancada puxou balança), a tela da TV exibe **única e exclusivamente** as colunas `📋 ORÇAMENTOS` e `✅ APROVADAS`, centralizadas em grande formato, ocupando todo o espaço da TV com simetria e clareza total para a oficina.
    - Fim dos blocos vazios: nenhum técnico com 0 balanças fica ocupando espaço na TV.
  - **Entrada Dinâmica dos Técnicos (Horizontal):**
    - Assim que um técnico seleciona uma balança para fazer (seja para orçamento ou para finalização da O.S. aprovada), o nome dele entra instantaneamente na tela da TV em uma linha horizontal à direita (`👨‍🔧 TEC. [NOME]`).
    - Os cartões da bancada daquele técnico são dispostos horizontalmente com número da O.S., cliente, modelo, etiquetas (`URGENTE`, `EM GARANTIA`) e cronômetro em tempo real.
    - Múltiplos técnicos em atendimento aparecem empilhados como faixas horizontais de alto contraste.
  - **Remoção Automática:**
    - Assim que o técnico conclui o serviço ou a balança é movida, o técnico desaparece imediatamente da TV em tempo real (via WebSocket) e o painel volta suavemente para a base limpa de `ORÇAMENTOS` e `APROVADAS`.
  - Suporte completo aos temas **Dark Mode** e **Clean Mode**.

---

## 📌 Item 17: Áudio Ducking Real e Integração Total com o YouTube na TV da Oficina (Stream Nativo Sem Anúncios, Pesquisa de Músicas e Conta Premium)

* **Status:** ✅ **Implementado e em Produção**
* **Solicitante:** Técnicos da Oficina e Recepção
* **Telas Impactadas:** `templates/tv.html`, `kanban/services/youtube.py`, `kanban/routes/youtube.py`
* **Motivo / Problema Identificado:**
  - Os iframes embarcados tradicionais do YouTube (`youtube.com/embed` / `YT.Player`) bloqueiam vídeos musicais oficiais (como Kamisa 10, Queen, a-ha) quando carregados em servidores de rede local (`192.168.x.x` / `127.0.0.1`), exibindo o erro **"Este vídeo não está disponível (Código 150 / 152-18)"**.
  - Além disso, o usuário precisava de uma **barra de pesquisa direta de músicas** (e não apenas colar links) e suporte ao **YouTube Premium / Sem Anúncios**.
* **Solução Implementada:**
  - **Motor Backend de Stream Direto e Sem Anúncios (`kanban/services/youtube.py` + `kanban/routes/youtube.py`):**
    - Extração nativa de stream MP4 com áudio e vídeo via `yt-dlp` multi-cliente (`android`, `ios`, `web`) e proxy local com suporte completo a `HTTP 206 Partial Content (Range)` em `/api/youtube/stream/<video_id>`.
    - Elimina 100% do erro *"Este vídeo não está disponível"* e remove todos os anúncios antes e durante as músicas.
    - Cache inteligente em memória dos streams resolvidos para reprodução e avanço instantâneos.
  - **Barra de Pesquisa de Músicas em Tempo Real (`/api/youtube/search`):**
    - Substituída a antiga caixa de colar link por uma **Barra de Pesquisa do YouTube** completa (`🔍 Pesquisar música, cantor ou show no YouTube...`).
    - Retorna instantaneamente os resultados com miniatura (thumbnail), título da música, canal/artista e duração, montando fila automática de reprodução (`⏭️ Próx.`).
  - **Integração com Conta YouTube Premium (`👑 Premium`):**
    - Painel integrado no topo do player permitindo abrir o login oficial do Google/YouTube e sincronizar os cookies da sessão logada do navegador (`Firefox` ou `Chrome/Edge`) via `/api/youtube/account`.
  - **Presets Rápidos de 1 Clique Validados:**
    - 🎤 **Kamisa 10 (Ao Vivo)** (`GrH68P0o60U` + fila com shows completos `TJ-WAgH5hpk` e `pBb_87eaPDE`)
    - 🎸 **Rock Clássico** (`erfv9QasZAw` + `fJ9rUzIMcZQ`)
    - ☕ **Lo-Fi Oficina** (`lTRiuFIWV54` + `CFGLoQIhmow`)
    - 📻 **Flashback 80/90** (`JcrBHxWHX74` + `djV11Xbc914`)
  - **Mecanismo de Audio Ducking Nativo Instantâneo (0ms):**
    - Como o player agora utiliza um elemento `<video id="ytNativeVideo">` nativo alimentado pelo nosso servidor, o controle de volume (`video.volume = 0`) e pausa (`video.pause()`) durante alertas e voz TTS da TV é 100% síncrono, instantâneo e imune a bloqueios de navegador.

---

## 📌 Item 18: Modernização Visual Premium do Frontend (Design System Linear/shadcn, Tailwind CSS, Lucide Icons e Microinterações Fluidas)

* **Status:** ✅ **Implementado e Homologado em Produção em 100% das Telas**
* **Solicitante:** Diretoria / Usuário
* **Telas Impactadas:**
  - `templates/admin.html` (Quadro Kanban Principal, Modal Nova O.S. com integração Fotos Celular e Toasts)
  - `templates/tv.html` (Painel TV Oficina com Overlay de Notificação Broadcast, Som YouTube e TTS)
  - `templates/saida.html` (Bancada Mobile dos Técnicos, Wizard de Orçamento e Finalização)
  - `templates/consulta.html` (Balcão de Atendimento e Consulta Rápida)
  - `templates/gerencia.html` (Painel Executivo de Indicadores, Produtividade e Auditoria)
  - `templates/recepcao_fotos.html` (Recepção Mobile e Fila de Fotos Pré-Teorema)
* **Objetivo Concluído:**
  - Estética SaaS soberba, limpa e premium no padrão Linear.app / shadcn/ui.
  - Tipografia de alta precisão com Plus Jakarta Sans e JetBrains Mono para códigos e números tabulares.
  - Ícones vetoriais modernos (Lucide Icons) em todas as interfaces.
  - Sistema de notificações redesenhado com alta visibilidade: Toasts flutuantes no Admin e Banner de Transmissão de Impacto na TV da Oficina.
  - Correção e homologação completa da integração das fotos pré-entrada do celular no cadastro de Nova O.S.
  - Cobertura de 100% dos testes unitários e de integração aprovados.
* **Objetivo:**
  - Eliminar a estética artificial/genérica ("cara de IA", gradientes roxos/azuis neon excessivos e poluição visual).
  - Implementar uma interface SaaS moderna, sóbria e ultra-profissional inspirada no padrão de excelência de produtos como **Linear.app** e **shadcn/ui**.
  - Melhorar a fluidez visual com transições suaves e microinterações de clique e arrasto.
* **Pilares de Engenharia do Novo Design:**
  1. **Paleta Zinc/Neutral Profunda:**
     - Fundo escuro com camadas refinadas (`#09090b` -> `#121215` -> `#18181b`), bordas sutis com transparência (`border-zinc-800` / `border-white/5`) e alto contraste de legibilidade.
  2. **Tipografia Técnica e Números Tabulares:**
     - Fonte **Inter / Geist Sans** com renderização subpixel perfeita e `font-variant-numeric: tabular-nums` para alinhamento de números de O.S. e pesagens.
  3. **Ícones Vetoriais Profissionais (Lucide Icons):**
     - Substituição de emojis por ícones vetoriais uniformes e elegantes.
  4. **Microinterações e AutoAnimate:**
     - Animações físicas naturais ao mover cards entre colunas, abrir modais e filtrar O.S. sem flashes ou quebras de layout.
  5. **Preservação de 100% das Funcionalidades:**
     - Todas as integrações com backend (SortableJS, WebSockets, modais, autenticação de exclusão, reaberturas, links da TV e balcão) são mantidas intactas.




