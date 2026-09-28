# Aion 2 Guides Global - Portal da Comunidade Brasileira

Aplicação web completa desenvolvida em **Python (Flask)** com templates **Jinja2**, estilização moderna com **Tailwind CSS**, tema Dark Fantasy imersivo e banco de dados relacional **SQLite**. O projeto foi concebido especificamente para o lançamento global do MMORPG **Aion 2**.

---

## 🛡️ Regras de Idioma Aplicadas

Conforme os padrões oficiais adotados pela comunidade:
* **Interface do Usuário (UI):** Menus, navegação, tutoriais, explicações táticas e descrições textuais 100% em **Português do Brasil (pt-BR)**.
* **Nomenclaturas e Termos do Jogo:** Mantidos rigorosamente em **INGLÊS**:
  * **Classes:** *Gladiator*, *Templar*, *Assassin*, *Ranger*, *Sorcerer*, *Elementalist*, *Cleric*, *Chanter*.
  * **Sistemas:** *Stigmas*, *Daevanion*, *Monoliths*, *Inheritance*, *Soul Binding*, *Enhancement*.
  * **Atividades e Locais:** *Regional Quests*, *Main Story*, *Sealed Dungeons*, *Strongholds*, *Atreia*.
  * **Itens e Equipamentos:** *Manastones*, *Godstones*, *Enhancement Stones*, *Kina*.

---

## 🚀 Como Executar o Projeto Localmente

### 1. Pré-requisitos
* Python 3.10 ou superior instalado no seu sistema.

### 2. Instalação das Dependências
No terminal, dentro da pasta do projeto, instale o Flask:
```bash
pip install -r requirements.txt
```

### 3. Inicializar e Rodar a Aplicação
Execute o script amigável de inicialização:
```bash
python run.py
```
*(Alternativamente, você também pode executar `python app.py`)*

### 4. Acessar no Navegador
Abra o navegador e acesse:
```
http://127.0.0.1:5000
```
> O banco de dados SQLite (`aion2_guides.db`) é criado e populado automaticamente na primeira execução com todas as classes, dados de Stigmas, rotações e notícias.

### 5. Executar os Testes Automatizados
Para verificar a integridade de todas as rotas e regras do sistema:
```bash
python test_app.py
```

---

## 🗺️ Estrutura de Páginas e Rotas

| Rota | Descrição |
| :--- | :--- |
| `/` | **Página Inicial:** Hero banner com destaques do Lançamento Global, cards rápidos para as 8 classes e **Eventos Ativos In-Game**. |
| `/beginner-guide` | **Guia de Iniciantes:** Explicação do Level Cap inicial (Level 45), ordem de prioridades (*Main Story*, *Regional Quests*, *Sealed Dungeons*, *Strongholds*), navegação por voo livre tridimensional e captura de montarias/pets via combate. Inclui **checklist interativo com progresso salvo**. |
| `/classes` | **Diretório de Classes:** Catálogo completo com as 8 classes iniciais e filtros dinâmicos por função (*Tank*, *Melee DPS*, *Ranged DPS*, *Healer/Support*). |
| `/classes/<slug>` | **Guias Individuais de Classe:** Ex: `/classes/gladiator`, `/classes/assassin`, `/classes/chanter`, etc. Contém análise de armas, armaduras, rotações de skills, prós/contras, recomendações de *Daevanion* e **abas interativas para builds de Stigmas PvE vs PvP (6 slots)**. |
| `/progression` | **Sistemas de Progressão:** Guia completo de *Skills & Stigmas* (limite de até 6 Stigmas e impacto na jogabilidade), **explorador interativo de nós da Daevanion Board** (*Branco* - status, *Verde* - passivas, *Azul* - ativas, *Laranja* - bônus únicos) e *Monoliths*. |
| `/gearing` | **Guia de Equipamentos:** Regras matemáticas do sistema de *Enhancement* (100% de sucesso de +0 a +10 com *Enhancement Stones*, com queda drástica e risco posterior), alerta de economia para o Level 45, **simulador interativo de aprimoramento**, além de guias de *Manastones*, *Godstones*, *Soul Binding* e *Inheritance*. |
| `/ferramentas` (ou `/tools`) | **Central de Ferramentas:** Hub centralizado de utilitários nativos e ecossistema global da comunidade (*AionFlex*, *QuestLog*, *Shugo.gg*, *AION.ing*, *Gamers4Life*, *Craft Calculator*). |
| `/planner` (ou `/planejador`) | **Planejador de Builds:** Ferramenta interativa completa para montagem de builds das 8 classes, com tabuleiro *Daevanion Board* (alocação de pontos até o cap de 50), seleção de até 6 *Stigmas*, presets PvE/PvP, cálculo dinâmico de atributos e compartilhamento de links. *(Baseado no Daevanion Planner).* |
| `/tracker` (ou `/tarefas`) | **Controle de Tarefas Diárias & Semanais:** Acompanhamento de rotinas de *Main* e *Alts*, checklist diário (5 Missões, limite de 1M *Kina*, *Mercado Negro*, *Assalto de Veritra*, *Shugo*, *Rifts*), checklist semanal (*Sealed Dungeons*, *Nightmare*, *Ascension*, *Raids*, *Abyss*) e timers de reset em tempo real com persistência no navegador. *(Baseado no Lótus Tracker de Thiago Soares Ferreira).* |
| `/mapa` (ou `/map`) | **Mapa Interativo de Atreia:** Cartografia tridimensional completa para localização de *World Bosses*, entradas de *Sealed Dungeons*, baús, *Spacetime Rifts*, obelisks de teleporte e nós de coleta. *(Powered by QuestLog.gg).* |

---

## 💎 Funcionalidades Interativas Inclusas

1. **Planejador de Builds Interativo (`/planner`):**
   * Compatível com todas as 8 classes (*Gladiator*, *Templar*, *Assassin*, *Ranger*, *Sorcerer*, *Elementalist*, *Cleric*, *Chanter*).
   * **Daevanion Board** interativo com nós classificados por raridade (*Branco*, *Verde*, *Azul*, *Laranja*), limite de 50 pontos e cálculo acumulado de atributos em tempo real.
   * **Slots de Stigmas** (até 6 habilidades equipáveis simultaneamente) com filtros e remoção com um clique.
   * Presets pré-configurados recomendados para PvE (*Sealed Dungeons*) e PvP (*Strongholds*).
   * Sistema de compartilhamento de builds via URL codificada na hash.
   * *Créditos comunitários: Baseado no [Daevanion Planner](https://daevanion-planner.info/).*

2. **Tracker de Tarefas Diárias & Semanais (`/tracker`):**
   * Timers de contagem regressiva em tempo real sincronizados com o servidor oficial: Reset Diário (05:00 UTC), Reset Semanal (Quartas-feiras), janelas de *Spacetime Rifts* e *Shugo Festival*.
   * Suporte a múltiplos personagens com gerenciamento de *Main* e até 7 *Alts*.
   * Checklist interativo com contadores numéricos (ex: 5 missões, 14 entradas de masmorras, 20 contratos de *Abyss*).
   * Barra de progresso visual acumulada por personagem e persistência automática em `localStorage`.
   * *Créditos comunitários: Baseado no [Lótus Tracker](https://thiagosoaresferreira.github.io/lotus-tracker/) de Thiago Soares Ferreira.*

3. **Mapa Interativo de Atreia (`/mapa`):**
   * Exploração do relevo tridimensional de *Atreia* com filtro rápido de pontos de interesse (POIs).
   * Modo tela cheia para utilização em segunda tela durante o jogo.
   * *Créditos comunitários: Powered by [QuestLog.gg](https://questlog.gg/aion-2/en/map).*

4. **Simulador de Enhancement Interativo (`/gearing`):**
   * Simulação em tempo real de taxas reais de sucesso (+0 a +15).
   * Contador de gastos de *Kina* e tentativas acumuladas.
   * Feedback visual dinâmico com mudança de brilho do item (normal, ciano, dourado e mítico).
   * Aviso de zonas seguras e zonas de risco.

5. **Explorador de Nós de Daevanion (`/progression`):**
   * Navegador visual onde o usuário clica nos nós *Branco*, *Verde*, *Azul* ou *Laranja* e visualiza em tempo real a categoria de poder e atributos gerados.

6. **Checklist de Nivelamento Salvo no Navegador (`/beginner-guide`):**
   * Lista de checagem do Level 1 ao 45 com barra de progresso em tempo real e persistência automática via `localStorage`.

7. **Filtros Dinâmicos de Classes (`/classes`):**
   * Filtragem instantânea sem recarregar a página por arquétipos de combate.

8. **Abas PvE vs PvP para Stigmas (`/classes/<slug>`):**
   * Permite alternar instantaneamente entre a configuração ótima de 6 Stigmas para masmorras (*Sealed Dungeons*) e combates de facção (*Strongholds*).

9. **Demonstração em Vídeo & Gameplay das Classes (`/classes/<slug>`):**
   * Seção de showcase audiovisual integrada em cada guia de classe.
   * Player embutido responsivo em 16:9 sem sair do portal.
   * Campo para créditos completos do criador de conteúdo e link direto para o canal.
   * Botão de acesso direto para assistir ao vídeo original no YouTube.
   * Estado de fallback elegante (*"Vídeo em Curadoria"*) enquanto os vídeos das 8 classes estão sendo selecionados.
   * Endpoint de API `POST /api/classes/<slug>/video` para cadastrar ou atualizar URLs, títulos e créditos facilmente.

10. **Macros In-Game da Comunidade (.txt) para Boss & Auto-Mode (`/classes/<slug>`):**
    * Conjunto completo de scripts de macros oficiais permitidos no jogo para todas as 8 classes.
    * Macros dedicados para:
      * **Rotação de Boss / Burst DPS (Single Target)**: Encadeamento ótimo de combos, quebras de defesa e finalizadores com compensação de GCD (`/Delay`).
      * **Auto-Mode & Missões Regionais**: Automação legítima de farming sem bot (`/AutomaticSelection`, `Auto Target on Skill Use` e `Closest Target`).
      * **Auto-Buff & Defensivos**: Ativação rápida de posturas, mantram e auras protetoras.
    * Botão de **"Copiar Macro (.txt)"** com 1 clique (para colar direto na janela de macros do jogo, atalho `U`).
    * Botão de download direto do arquivo `.txt`.
    * Guia explicativo das regras in-game e parâmetros de latência.
    * Endpoint de API `GET /api/classes/<slug>/macros` e rota de download `/api/classes/<slug>/macros/<id>/download`.

---

## 📁 Estrutura de Diretórios do Projeto

```
guias aion2/
├── app.py                 # Aplicação Flask principal, rotas web e endpoints de API
├── database.py            # Criação do banco SQLite e seeding de dados completos
├── models.py              # Camada de abstração de dados (Classes, Vídeos, Macros, Eventos)
├── run.py                 # Script de inicialização rápido
├── test_app.py            # Suíte de testes automatizados com unittest (15 testes)
├── requirements.txt       # Dependências Python (Flask)
├── README.md              # Documentação completa do projeto
├── static/
│   ├── css/
│   │   └── custom.css     # Estilos Dark Fantasy, glassmorphism e efeitos de glow
│   └── js/
│       ├── main.js        # Lógica de interatividade (accordions, modais, simulador, checklist)
│       └── planner.js     # Engine reativa do Planejador de Builds (Daevanion Board & Stigmas)
└── templates/
    ├── base.html          # Template master (Header moderno, navegação dropdown, footer rico)
    ├── index.html         # Página inicial com Eventos Ativos
    ├── beginner_guide.html# Guia de iniciantes (Level cap 45, voo livre, captura de pets)
    ├── classes.html       # Diretório com filtros das 8 classes
    ├── class_detail.html  # Detalhes da classe com tabs de Stigmas PvE/PvP e Daevanion
    ├── progression.html   # Stigmas e Daevanion Boards
    ├── gearing.html       # Enhancement e sistemas extras de armas
    ├── tools.html         # Central de ferramentas & Hub de utilitários comunitários
    ├── planner.html       # Interface do Planejador de Builds com créditos
    ├── tracker.html       # Interface do Tracker de Tarefas com timers e gestão de Alts
    ├── map.html           # Interface do Mapa Interativo de Atreia com tela cheia
    └── 404.html           # Página de erro 404 temática
```


