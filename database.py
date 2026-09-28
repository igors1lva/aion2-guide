"""
database.py - Inicialização e gerenciamento do banco de dados SQLite para o portal Aion 2 Guides.
Gera e popula automaticamente os dados detalhados das 8 classes, notícias do Lançamento Global
e informações dos sistemas de jogo.
"""

import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aion2_guides.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabela de Classes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            role TEXT NOT NULL,
            role_category TEXT NOT NULL,
            primary_weapon TEXT NOT NULL,
            secondary_weapon TEXT,
            armor_type TEXT NOT NULL,
            difficulty INTEGER NOT NULL,
            badge_color TEXT NOT NULL,
            summary TEXT NOT NULL,
            lore TEXT NOT NULL,
            playstyle TEXT NOT NULL,
            strengths TEXT NOT NULL,
            weaknesses TEXT NOT NULL,
            stigmas_pve TEXT NOT NULL,
            stigmas_pvp TEXT NOT NULL,
            daevanion_priority TEXT NOT NULL,
            skill_rotation TEXT NOT NULL,
            image_placeholder TEXT
        )
    ''')

    # Tabela de Notícias
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            date_published TEXT NOT NULL,
            summary TEXT NOT NULL,
            content TEXT NOT NULL,
            is_featured INTEGER DEFAULT 0
        )
    ''')

    # Tabela de Eventos Ativos In-Game
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL,
            badge_color TEXT NOT NULL,
            period TEXT NOT NULL,
            summary TEXT NOT NULL,
            rewards TEXT NOT NULL,
            is_active INTEGER DEFAULT 1
        )
    ''')

    # Tabela de Sistemas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS systems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            subtitle TEXT NOT NULL,
            description TEXT NOT NULL,
            details_json TEXT NOT NULL
        )
    ''')

    # Migração automática e idempotente: Adicionar colunas de vídeo se não existirem
    cursor.execute("PRAGMA table_info(classes)")
    existing_cols = [row[1] for row in cursor.fetchall()]
    new_cols = [
        ('video_url', 'TEXT'),
        ('video_embed_url', 'TEXT'),
        ('video_title', 'TEXT'),
        ('video_credits', 'TEXT'),
        ('video_author_url', 'TEXT')
    ]
    for col_name, col_type in new_cols:
        if col_name not in existing_cols:
            cursor.execute(f"ALTER TABLE classes ADD COLUMN {col_name} {col_type}")

    conn.commit()

    # Verificar se as classes já foram inseridas
    cursor.execute('SELECT COUNT(*) as count FROM classes')
    if cursor.fetchone()['count'] == 0:
        seed_data(cursor)
        conn.commit()

    # Vídeo do Gladiator - Guia completo de Build PvE, Stigmas e Macros por Carneiro MMO
    cursor.execute('''
        UPDATE classes 
        SET video_url = 'https://www.youtube.com/watch?v=SrTJoAgvppg',
            video_embed_url = 'https://www.youtube.com/embed/SrTJoAgvppg',
            video_title = 'AION 2: DESTRUA COM O GLADIATOR! Build PVE, Skills, Estigmas e Macro!',
            video_credits = 'Carneiro MMO',
            video_author_url = 'https://www.youtube.com/@CarneiroMMO'
        WHERE slug = 'gladiator'
    ''')
    conn.commit()

    # Vídeo do Templar - Guia completo de Build PvE, Stigmas e Macros por Carneiro MMO
    cursor.execute('''
        UPDATE classes 
        SET video_url = 'https://www.youtube.com/watch?v=IAdq5uXPXuQ',
            video_embed_url = 'https://www.youtube.com/embed/IAdq5uXPXuQ',
            video_title = 'AION 2: TEMPLAR SEM ERRO! Build PVE, Skills, Stigmas e Macro',
            video_credits = 'Carneiro MMO',
            video_author_url = 'https://www.youtube.com/@CarneiroMMO'
        WHERE slug = 'templar'
    ''')
    conn.commit()

    # Vídeo do Assassin - Guia completo de Skills, Stigmas e Combos por Carneiro MMO
    cursor.execute('''
        UPDATE classes 
        SET video_url = 'https://www.youtube.com/watch?v=EcsnvDSBaJM',
            video_embed_url = 'https://www.youtube.com/embed/EcsnvDSBaJM',
            video_title = 'AION 2: ASSASSIN - GUIA COMPLETO! Skills, Stigmas e Combos',
            video_credits = 'Carneiro MMO',
            video_author_url = 'https://www.youtube.com/@CarneiroMMO'
        WHERE slug = 'assassin'
    ''')
    conn.commit()

    # Vídeo do Ranger - Guia Best Ranger PvE Build por FRESHY
    cursor.execute('''
        UPDATE classes 
        SET video_url = 'https://www.youtube.com/watch?v=xMeJ204VUbI',
            video_embed_url = 'https://www.youtube.com/embed/xMeJ204VUbI',
            video_title = 'AION 2 Best Ranger PvE Build Guide | Everything You Need To Know',
            video_credits = 'FRESHY',
            video_author_url = 'https://www.youtube.com/@FRESHY_GG'
        WHERE slug = 'ranger'
    ''')
    conn.commit()

    # Vídeo do Sorcerer - Guia completo de Skills, Stigmas e Daevanion por aLuckyRO
    cursor.execute('''
        UPDATE classes 
        SET video_url = 'https://www.youtube.com/watch?v=s-pYR_fmMDk',
            video_embed_url = 'https://www.youtube.com/embed/s-pYR_fmMDk',
            video_title = 'AION 2 Sorcerer Guide For Skills & Stigmas | Macros & Daevanion Setup | Ultimate Beginners Guide',
            video_credits = 'aLuckyRO',
            video_author_url = 'https://www.youtube.com/@aLuckyRo'
        WHERE slug = 'sorcerer'
    ''')
    conn.commit()

    # Vídeo do Elementalist - Guia Spirit Master Skill Build & Specialty por Storyteller
    cursor.execute('''
        UPDATE classes 
        SET video_url = 'https://www.youtube.com/watch?v=5DCJtBFzVZM',
            video_embed_url = 'https://www.youtube.com/embed/5DCJtBFzVZM',
            video_title = 'AION2 Spirit Master Skill Build & Specialty PERFECT GUIDE',
            video_credits = 'Storyteller (스토리텔러)',
            video_author_url = 'https://www.youtube.com/@storyteller_tv'
        WHERE slug = 'elementalist'
    ''')
    conn.commit()

    # Vídeo do Chanter - Guia Definitivo de Chanter (Build, Rotação e Macros) por Mour4SB
    cursor.execute('''
        UPDATE classes 
        SET video_url = 'https://www.youtube.com/watch?v=Gyy9fgFotjA',
            video_embed_url = 'https://www.youtube.com/embed/Gyy9fgFotjA',
            video_title = 'Aion 2 - Guia Definitivo de Chanter (Build, Rotação e Macros)',
            video_credits = 'Mour4SB',
            video_author_url = 'https://www.youtube.com/@Mour4SB'
        WHERE slug = 'chanter'
    ''')
    conn.commit()

    # Vídeo do Cleric - Guia completo de Skills, Stigmas e Combos por Carneiro MMO
    cursor.execute('''
        UPDATE classes 
        SET video_url = 'https://www.youtube.com/watch?v=JLYdIsd32SA',
            video_embed_url = 'https://www.youtube.com/embed/JLYdIsd32SA',
            video_title = 'AION 2 - CLERIC: GUIA COMPLETO! Skills, Stigmas e Combos',
            video_credits = 'Carneiro MMO',
            video_author_url = 'https://www.youtube.com/@CarneiroMMO'
        WHERE slug = 'cleric'
    ''')
    conn.commit()

    # Verificar se os eventos já foram inseridos
    cursor.execute('SELECT COUNT(*) as count FROM events')
    if cursor.fetchone()['count'] == 0:
        seed_events(cursor)
        conn.commit()

    conn.close()


def seed_data(cursor):
    """Insere o conteúdo inicial completo respeitando todas as regras de idioma e termos em inglês."""

    classes_data = [
        {
            "slug": "gladiator",
            "name": "Gladiator",
            "role": "Tank / Melee DPS",
            "role_category": "Melee DPS & Off-Tank",
            "primary_weapon": "Greatsword (Espadão de duas mãos)",
            "secondary_weapon": "Polearm & Dual Wielding (Swords/Daggers)",
            "armor_type": "Plate (Armadura de Placas)",
            "difficulty": 2,
            "badge_color": "from-red-600 to-amber-600",
            "summary": "Guerreiro de combate brutal corpo a corpo que empunha um pesado espadão de duas mãos. Possui altíssimo dano em área (AoE), derrubadas (Knockdowns) devastadoras e excelente capacidade de atuar como Off-Tank.",
            "lore": "Mestres implacáveis do campo de batalha físico em Atreia. Os Gladiators canalizam sua força primordial através de lâminas colossais, cortando linhas inimigas inteiras com ferocidade inigualável.",
            "playstyle": "Combate ofensivo direto focado em controle de grupo e derrubada de alvos. Alterna entre posturas de ataque feroz e sobrevivência de Plate, dominando lutas contra múltiplos alvos em Sealed Dungeons e conflitos de facção em Strongholds.",
            "strengths": json.dumps([
                "Dano em área (AoE) massivo e limpezas rápidas de ondas de monstros",
                "Múltiplas habilidades de Knockdown e controle de multidões",
                "Alta durabilidade natural graças ao uso de Plate Armor",
                "Excelente versatilidade entre dano consistente e função de Off-Tank"
            ], ensure_ascii=False),
            "weaknesses": json.dumps([
                "Suscetível a kiting por classes com alta mobilidade de longo alcance como Ranger",
                "Velocidade de ataque mais lenta se comparada ao Assassin",
                "Dependência de conectar combos de derrubada para maximizar dano de finalização"
            ], ensure_ascii=False),
            "stigmas_pve": json.dumps([
                {"name": "Severe Precision Cut", "type": "Active", "desc": "Golpe descendente de imenso dano que causa dano bônus em alvos caídos (Knocked Down)."},
                {"name": "Whirlwind Strike", "type": "Active AoE", "desc": "Ataque giratório contínuo atingindo todos os inimigos em 7m, gerando alto Aggro e quebrando armadura."},
                {"name": "Ankle Snare", "type": "Crowd Control", "desc": "Imobiliza alvos no solo, impedindo a fuga de chefes e elites em masmorras."},
                {"name": "Berserking", "type": "Buff", "desc": "Aumenta drasticamente o Attack Power físico em 80% ao custo de reduzir ligeiramente as defesas."},
                {"name": "Draining Blow", "type": "Sustain", "desc": "Causa dano e recupera 30% do dano infligido na forma de HP imediato."},
                {"name": "Armor Murder", "type": "Debuff", "desc": "Reduz a Physical Defense do alvo principal em 35% por 15 segundos."}
            ], ensure_ascii=False),
            "stigmas_pvp": json.dumps([
                {"name": "Severe Precision Cut", "type": "Active", "desc": "Crítico fulminante em alvos que sofreram Knockdown."},
                {"name": "Lockdown", "type": "Crowd Control", "desc": "Impede o oponente de utilizar habilidades físicas durante o combate direto."},
                {"name": "Dauntless Charge", "type": "Mobility", "desc": "Avanço instantâneo contra o alvo, causando Stun de 1.5s e quebrando barreiras."},
                {"name": "Berserking", "type": "Burst Buff", "desc": "Potencializa o dano explosivo para abates rápidos em confrontos de facção."},
                {"name": "Second Wind", "type": "Survival", "desc": "Cura instantânea de emergência de 35% do HP máximo e aumento de resistência a Stun."},
                {"name": "Tendonslice", "type": "Debuff", "desc": "Reduz drasticamente a velocidade de movimento do adversário em 50%."}
            ], ensure_ascii=False),
            "daevanion_priority": "Priorizar nós Laranja de aumento de dano em alvos derrubados (Knockdown Amplification). Nos nós Verdes, focar em redução de cooldown de habilidades de investida e nos nós Brancos acumular Physical Attack e Physical Critical Hit.",
            "skill_rotation": "1. Iniciar com Dauntless Charge para encurtar a distância -> 2. Aplicar Armor Murder para quebrar defesas -> 3. Usar Ferocious Strike gerando chance de Knockdown -> 4. Ao derrubar o alvo, desferir Severe Precision Cut seguido de Draining Blow para dano massivo e autocura.",
            "image_placeholder": "gladiator.svg"
        },
        {
            "slug": "templar",
            "name": "Templar",
            "role": "Main Tank",
            "role_category": "Main Tank",
            "primary_weapon": "Sword & Shield (Espada e Escudo)",
            "secondary_weapon": "Mace & Shield ou Greatsword",
            "armor_type": "Plate (Armadura de Placas)",
            "difficulty": 3,
            "badge_color": "from-sky-500 to-indigo-700",
            "summary": "O guardião supremo de Atreia e a espinha dorsal de qualquer grupo em Sealed Dungeons e disputas territoriais em Strongholds. Apresenta a maior defesa física e mágica de Aion 2, escudos impenetráveis e habilidades vitais de puxão (Taunt & Pull).",
            "lore": "Cavaleiros sagrados agraciados pelo poder divino de Aion. Posicionam-se como muralhas inabaláveis entre as garras do perigo e seus companheiros de equipe, sacrificando-se pela sobrevivência do grupo.",
            "playstyle": "Focado em gerenciar Aggro absoluto de chefes, bloquear ataques com o Shield e redirecionar dano de aliados frágeis com auras protetoras. Em PvP, puxa conjuradores inimigos e anula o avanço adversário.",
            "strengths": json.dumps([
                "Indiscutivelmente o melhor Main Tank para PvE de alto nível e Sealed Dungeons",
                "Capacidade de sobrevivência inigualável através de Shield Block e invulnerabilidades temporárias",
                "Controle de posicionamento invejável com ganchos e habilidades de Taunt",
                "Habilidade de proteger e absorver dano direcionado aos curandeiros do grupo"
            ], ensure_ascii=False),
            "weaknesses": json.dumps([
                "Dano ofensivo mais modesto quando comparado a classes puras de DPS",
                "Velocidade de nivelamento solo mais cadenciada",
                "Alta responsabilidade em mecânicas críticas de posicionamento de chefes"
            ], ensure_ascii=False),
            "stigmas_pve": json.dumps([
                {"name": "Iron Skin", "type": "Defensive", "desc": "Reduz todo o dano recebido em 50% e confere imunidade a todos os efeitos de controle de grupo por 15 segundos."},
                {"name": "Incite Rage", "type": "Taunt AoE", "desc": "Gera massivo Aggro instantâneo em todos os monstros ao redor, forçando o foco no Templar."},
                {"name": "Empyrean Armor", "type": "Buff", "desc": "Aumenta o Max HP em 25% e regenera 100 de HP a cada acerto recebido."},
                {"name": "Bodyguard", "type": "Party Protect", "desc": "Redireciona 70% do dano sofrido por um aliado selecionado para o Templar por 20 segundos."},
                {"name": "Shield Burst", "type": "Active Stun", "desc": "Golpe violento com o escudo que atordoa o chefe e interrompe conjurações perigosas."},
                {"name": "Righteous Punishment", "type": "Active Debuff", "desc": "Causa dano divino e reduz o poder de ataque do inimigo em 20%."}
            ], ensure_ascii=False),
            "stigmas_pvp": json.dumps([
                {"name": "Iron Skin", "type": "Defensive", "desc": "Imunidade indispensável para resistir ao burst coordenado de inimigos."},
                {"name": "Doom Lure", "type": "Pull / CC", "desc": "Dispara uma corrente etérea que puxa um inimigo a até 16m para perto de si e atordoa."},
                {"name": "Shield of Faith", "type": "Sustain", "desc": "Cria uma barreira sagrada equivalente a 40% do HP total que dura 12 segundos."},
                {"name": "Incite Rage", "type": "Disruption", "desc": "Desestabiliza formações inimigas e força a perda de mira de conjuradores."},
                {"name": "Break Power", "type": "Debuff", "desc": "Ataque que silencia e impede o uso de itens consumíveis de cura por 4 segundos."},
                {"name": "Bodyguard", "type": "Party Protect", "desc": "Salva o Cleric do time de focar e ser abatido por assassinos furtivos."}
            ], ensure_ascii=False),
            "daevanion_priority": "Focar em nós Laranja de ampliação de Threat/Aggro e redução do dano de ataques em área. Nos nós Verdes, priorizar aumento de taxa de Shield Block e nos nós Brancos maximizar HP total e Physical Defense.",
            "skill_rotation": "1. Avançar com Shield Charge para engajar -> 2. Disparar Incite Rage para consolidar o Aggro inicial -> 3. Manter a rotação de Shield Counter e Taunt Strike -> 4. Acionar Iron Skin antes de golpes especiais ou fases de pico de dano do chefe.",
            "image_placeholder": "templar.svg"
        },
        {
            "slug": "assassin",
            "name": "Assassin",
            "role": "Melee DPS",
            "role_category": "Melee DPS",
            "primary_weapon": "Daggers & Swords (Empunhadura Dupla)",
            "secondary_weapon": "Bow (Secundário tático)",
            "armor_type": "Leather (Armadura de Couro)",
            "difficulty": 5,
            "badge_color": "from-purple-600 to-rose-700",
            "summary": "O mestre das sombras e do dano explosivo (burst damage) concentrado. Especialista em Stealth, mobilidade absurda, envenenamentos letais e ataques nas costas do oponente com alta taxa de acertos críticos.",
            "lore": "Operando nas sombras entre a luz e o abismo, os Assassins são a lâmina silenciosa de sua facção. Eliminam ameaças prioritárias antes mesmo de o inimigo perceber sua presença.",
            "playstyle": "Altamente dinâmico e cirúrgico. Utiliza habilidades como Shadowstep para teleportar imediatamente atrás da vítima, infligindo séries de atordoamentos e finalizações rápidas com adagas envenenadas.",
            "strengths": json.dumps([
                "O maior dano de burst em alvo único de Aion 2",
                "Mecânica de Stealth (invisibilidade tática) para emboscadas perfeitas",
                "Habilidade icônica Shadowstep para re-posicionamento instantâneo",
                "Evasão e agilidade elevadas que permitem esquivar de ataques letais"
            ], ensure_ascii=False),
            "weaknesses": json.dumps([
                "Curva de aprendizado íngreme e baixa tolerância a erros de posicionamento",
                "Extremamente frágil se for pego em controles de multidão rígidos (Stun/Sleep)",
                "Dano cai consideravelmente se for forçado a atacar o alvo de frente"
            ], ensure_ascii=False),
            "stigmas_pve": json.dumps([
                {"name": "Shadowstep", "type": "Mobility / Active", "desc": "Teleporta instantaneamente para as costas do inimigo, concedendo 100% de chance crítica no próximo golpe."},
                {"name": "Flurry", "type": "Buff", "desc": "Aumenta a Attack Speed em 25% por 30 segundos, acelerando todos os combos de adaga."},
                {"name": "Quickening Gloom", "type": "Poison / Burst", "desc": "Aplica um veneno corrosivo que explode ao acumular 5 cargas de runas."},
                {"name": "Spelldodge", "type": "Defensive", "desc": "Esquiva com 100% de certeza das próximas 2 habilidades mágicas recebidas."},
                {"name": "Rune Carve", "type": "Active Combo", "desc": "Entalha runas no alvo para preparar a detonação com Rune Burst."},
                {"name": "Rune Burst", "type": "Finisher", "desc": "Detona todas as runas entalhadas, causando dano crítico massivo e Stun."}
            ], ensure_ascii=False),
            "stigmas_pvp": json.dumps([
                {"name": "Shadowstep", "type": "Gap Closer", "desc": "Habilidade essencial para aniquilar conjuradores à distância sem chance de resposta."},
                {"name": "Ambush", "type": "Crowd Control", "desc": "Ataque furtivo que causa Stun imediato de 2 segundos pelas costas."},
                {"name": "Smoke Screen", "type": "Disruption AoE", "desc": "Cria uma névoa que cega todos os alvos num raio de 6m por 5 segundos."},
                {"name": "Shadow Walk", "type": "Advanced Stealth", "desc": "Permite movimentar-se em velocidade normal durante a invisibilidade e resiste a revelações comuns."},
                {"name": "Spelldodge", "type": "Survival", "desc": "Anula ataques fatais de Sorcerers e Clerics."},
                {"name": "Rune Burst", "type": "Burst CC", "desc": "Detonação para selar o abate do alvo antes que receba curas da party."}
            ], ensure_ascii=False),
            "daevanion_priority": "Nós Laranja focados em Backstab Critical Damage e recarga rápida do Shadowstep ao abater inimigos. Nós Verdes em Attack Speed e chance de evasão, e nós Brancos em Physical Critical Hit e Physical Attack.",
            "skill_rotation": "1. Ativar Stealth -> 2. Posicionar-se e disparar Ambush pelas costas -> 3. Executar Rune Carve para empilhar runas -> 4. Usar Shadowstep caso o inimigo tente desengajar -> 5. Finalizar com Rune Burst para o abate.",
            "image_placeholder": "assassin.svg"
        },
        {
            "slug": "ranger",
            "name": "Ranger",
            "role": "Ranged DPS",
            "role_category": "Ranged DPS",
            "primary_weapon": "Bow (Arco Longo)",
            "secondary_weapon": "Traps & Dagger",
            "armor_type": "Leather (Armadura de Couro)",
            "difficulty": 3,
            "badge_color": "from-emerald-500 to-teal-700",
            "summary": "Arqueiro mestre com disparos de precisão cirúrgica a distâncias seguras e mobilidade contínua. Domina o uso de armadilhas táticas (Traps) para desacelerar, silenciar e desarticular qualquer avanço inimigo.",
            "lore": "Sentinelas das florestas e desfiladeiros de Atreia. Possuem olhos de águia capazes de identificar fraquezas a dezenas de metros, desferindo flechas letais antes mesmo de entrarem no campo de visão do adversário.",
            "playstyle": "Kiting constante (atacar em movimento mantendo distância máxima). Instala armadilhas no solo para controlar o campo e desfere sequências de flechadas perfurantes com alto índice de acerto crítico.",
            "strengths": json.dumps([
                "Capacidade de disparar a longas distâncias sem se expor ao perigo direto",
                "Mecânica superior de kiting e evasão de investidas",
                "Grande utilidade tática com Traps (Sleep Trap, Poison Trap, Snare)",
                "Excelente tanto no leveling solo quanto no combate aberto em PvPvE"
            ], ensure_ascii=False),
            "weaknesses": json.dumps([
                "Dano e sobrevivência caem consideravelmente se for encurralado em combate corpo a corpo",
                "Necessidade de gerenciar a munição de flechas e distância mínima de segurança",
                "Dano em área menos expressivo que o do Gladiator e Sorcerer"
            ], ensure_ascii=False),
            "stigmas_pve": json.dumps([
                {"name": "Arrow Deluge", "type": "Active AoE", "desc": "Chuva de flechas concentrada em área que atinge múltiplos alvos continuamente."},
                {"name": "Spiral Arrow", "type": "Piercing Shot", "desc": "Flechada perfurante de alto impacto que ignora 30% da Physical Defense do chefe."},
                {"name": "Mau Form", "type": "Buff", "desc": "Transformação que amplia a velocidade de ataque, mobilidade e dano físico por 45s."},
                {"name": "Sharpshooter Aim", "type": "Passive Buff", "desc": "Aumenta o dano crítico físico e o alcance de todas as habilidades de arco em 3m."},
                {"name": "Gale Arrow", "type": "Active Burst", "desc": "Disparo veloz de três flechas consecutivas com alta chance de Knockback."},
                {"name": "Nature's Resolve", "type": "Cleanse", "desc": "Remove imediatamente lentidões e imobilizações, concedendo imunidade temporária."}
            ], ensure_ascii=False),
            "stigmas_pvp": json.dumps([
                {"name": "Sleep Trap", "type": "Crowd Control", "desc": "Armadilha no solo que coloca o primeiro oponente que pisar em sono profundo por até 10s."},
                {"name": "Silence Arrow", "type": "Interrupt / CC", "desc": "Silencia o conjurador atingido por 6 segundos, neutralizando Sorcerers e Clerics."},
                {"name": "Mau Form", "type": "Burst Mobility", "desc": "Permite correr em velocidade máxima enquanto atira flechas sem interrupção."},
                {"name": "Entangling Shot", "type": "Snare", "desc": "Reduz a velocidade de movimento do adversário em 60% e inflige sangramento."},
                {"name": "Retreating Slash", "type": "Evasion / Gap Creator", "desc": "Salta 10m para trás atordoando qualquer um que estivesse à frente."},
                {"name": "Gale Arrow", "type": "Knockback", "desc": "Empurra inimigos que se aproximem demais do seu perímetro."}
            ], ensure_ascii=False),
            "daevanion_priority": "Nós Laranja que aumentam a distância máxima de ataque em 4 metros e dano à distância. Nós Verdes em Movement Speed e cooldown de traps, e nós Brancos em Physical Critical Hit e Accuracy.",
            "skill_rotation": "1. Posicionar armadilhas no caminho de recuo -> 2. Iniciar combate com Silence Arrow ou Snare -> 3. Disparar Spiral Arrow para quebrar defesas -> 4. Entrar em Mau Form para metralhar Gale Arrow enquanto se mantém em movimento lateral.",
            "image_placeholder": "ranger.svg"
        },
        {
            "slug": "sorcerer",
            "name": "Sorcerer",
            "role": "Ranged Magic DPS",
            "role_category": "Ranged Magic DPS",
            "primary_weapon": "Orb ou Spellbook",
            "secondary_weapon": "Nenhum (Foco em tomos arcanos)",
            "armor_type": "Cloth (Armadura de Tecido)",
            "difficulty": 4,
            "badge_color": "from-amber-500 to-red-700",
            "summary": "O clássico Glass Cannon de Aion 2. Detentor do maior dano mágico explosivo do jogo, com domínio dos elementos fogo, gelo e terra. Possui capacidades destrutivas capazes de aniquilar grupos inteiros em segundos.",
            "lore": "Estudiosos dos fluxos mais profundos de Éter no universo de Aion. Convertem a pura energia cósmica em tempestades de chamas fulminantes e avalanches gélidas.",
            "playstyle": "Manter posicionamento recuado seguro, protegendo-se com barreiras de mana (Stone Skin) enquanto carrega feitiços devastadores. Em PvP, utiliza controles rígidos como Sleep e Curse of Tree para ditar o ritmo.",
            "strengths": json.dumps([
                "O mais alto potencial de dano mágico em área e alvo único",
                "Controle de multidão de longa duração incomparável (Curse of Tree e Sleep)",
                "Capacidade de virar lutas inteiras com meteoros e tempestades em área",
                "Grande utilidade de desaceleração de inimigos com feitiços de gelo"
            ], ensure_ascii=False),
            "weaknesses": json.dumps([
                "Defesa física extremamente baixa devido ao uso de Cloth Armor",
                "Muitas habilidades exigem tempo de conjuração parado no local",
                "Alvo prioritário de Assassins e Rangers em confrontos PvPvE"
            ], ensure_ascii=False),
            "stigmas_pve": json.dumps([
                {"name": "Flame Spray", "type": "Active Burst", "desc": "Dispara jatos vulcânicos concentrados infligindo dano massivo de fogo."},
                {"name": "Glacial Shard", "type": "Heavy Burst", "desc": "Invoca uma lança colossal de gelo que desaba sobre o chefe, causando o maior dano único do jogo."},
                {"name": "Big Magma Eruption", "type": "Ultimate AoE", "desc": "Explosão de magma que derrete ondas inteiras de monstros em masmorras."},
                {"name": "Stone Skin", "type": "Defensive Shield", "desc": "Cria uma carapaça de éter que absorve até 3000 de dano e previne interrupções."},
                {"name": "Boon of Quickness", "type": "Buff", "desc": "Reduz o tempo de conjuração de todas as magias em 50% por 15 segundos."},
                {"name": "Aetheric Spellburst", "type": "Finisher", "desc": "Gera uma explosão de éter que recupera 20% do MP máximo do feiticeiro."}
            ], ensure_ascii=False),
            "stigmas_pvp": json.dumps([
                {"name": "Curse of Tree", "type": "Hard CC", "desc": "Transforma o inimigo em uma árvore por até 15 segundos, impossibilitando qualquer ação."},
                {"name": "Sleeping Storm", "type": "AoE Sleep", "desc": "Coloca múltiplos inimigos em sono profundo simultaneamente na área de efeito."},
                {"name": "Boon of Quickness", "type": "Burst Acceleration", "desc": "Essencial para conjurar magias pesadas antes que o inimigo consiga silenciar você."},
                {"name": "Stone Skin", "type": "Survival", "desc": "A barreira vital para não morrer com o primeiro golpe surpresa de um Assassin."},
                {"name": "Frost Barrier", "type": "Reflect / Defense", "desc": "Congela o feiticeiro em um casulo protetor, refletindo feitiços e curando MP."},
                {"name": "Flame Spray", "type": "Executioner", "desc": "Finaliza alvos rapidamente após acordá-los do controle de grupo."}
            ], ensure_ascii=False),
            "daevanion_priority": "Nós Laranja que reduzem o Cast Time global e garantem penetração mágica (Magic Suppression Ignore). Nós Verdes em regeneração de MP e nós Brancos focados 100% em Magic Boost e Magical Critical Hit.",
            "skill_rotation": "1. Ativar Stone Skin antes do combate -> 2. Acionar Boon of Quickness -> 3. Controlar ameaças secundárias com Curse of Tree -> 4. Disparar Glacial Shard no alvo prioritário -> 5. Finalizar com Flame Spray e magias de gelo instantâneas.",
            "image_placeholder": "sorcerer.svg"
        },
        {
            "slug": "elementalist",
            "name": "Elementalist",
            "role": "Ranged Magic DPS",
            "role_category": "Summoner & Utility DPS",
            "primary_weapon": "Tome ou Orb (Orbe Mágico)",
            "secondary_weapon": "Espíritos Elementais (Fire, Earth, Water, Wind)",
            "armor_type": "Cloth (Armadura de Tecido)",
            "difficulty": 4,
            "badge_color": "from-teal-500 to-emerald-700",
            "summary": "Invocador arcano místico (Spiritmaster) que comanda espíritos dos elementos para suporte, dano sustentado, enfraquecimento e controle de campo. Mestre absoluto de feitiços de dano contínuo (DoTs), remoção de buffs inimigos (Dispel) e o temido Fear.",
            "lore": "Conjuradores ligados às forças naturais primordiais de Atreia. Criam laços de sangue e espírito com entidades elementais, fazendo com que seus espíritos lutem em seu lugar.",
            "playstyle": "Dano sustentado constante através de maldições e espíritos invocados. Em grupos, desfaz defesas de chefes removendo seus escudos com Dispel, e espalha terror em batalhas de Strongholds através do Fear AoE.",
            "strengths": json.dumps([
                "Controle de multidão temível através do efeito de Fear (Terror)",
                "Especialista em remoção completa de buffs e escudos dos oponentes",
                "O melhor dano sustentado com feitiços de DoT (Damage over Time)",
                "Possui espíritos que podem atuar como mini-tanks em explorações solo"
            ], ensure_ascii=False),
            "weaknesses": json.dumps([
                "Dano de burst imediato menor do que o Sorcerer",
                "Dependência de gerenciar a vida e posicionamento do espírito invocado",
                "Vulnerabilidade clássica de armaduras Cloth quando atacado diretamente"
            ], ensure_ascii=False),
            "stigmas_pve": json.dumps([
                {"name": "Armor Spirit", "type": "Pet Buff", "desc": "Aumenta drasticamente o ataque e vida do espírito invocado, permitindo que tanke chefes."},
                {"name": "Ignite Aether", "type": "Dispel / Burst", "desc": "Remove até 3 buffs mágicos do inimigo e causa dano por cada efeito removido."},
                {"name": "Spirit Burn", "type": "Active AoE DoT", "desc": "Comanda o espírito para incendiar o solo em chamas contínuas sobre os monstros."},
                {"name": "Body Root", "type": "Crowd Control", "desc": "Enraíza e silencia ataques físicos do inimigo por 8 segundos."},
                {"name": "Spirit Wall of Protection", "type": "Party Buff", "desc": "O espírito projeta uma barreira protetora para todo o grupo com base no elemento ativo."},
                {"name": "Curse Cloud", "type": "Toxic Cloud", "desc": "Nuvem ácida que corrói os alvos e diminui o poder de ataque dos chefes."}
            ], ensure_ascii=False),
            "stigmas_pvp": json.dumps([
                {"name": "Fear Shriek", "type": "AoE Fear", "desc": "Habilidade temida em Aion: coloca todos os inimigos ao redor em estado de terror incontrolável."},
                {"name": "Ignite Aether", "type": "Buff Stripper", "desc": "Destrói Iron Skin de Templars e Stone Skin de Sorcerers instantaneamente."},
                {"name": "Disenchant", "type": "Cleanse / Debuff", "desc": "Anula pergaminhos e elixires consumidos pelos oponentes em combate."},
                {"name": "Stone Scour", "type": "Crowd Control", "desc": "Petrifica o oponente no lugar por 5 segundos sem poder agir."},
                {"name": "Spirit Substitution", "type": "Survival", "desc": "Transfere 100% do dano recebido pelo Elementalist diretamente para seu espírito."},
                {"name": "Erosion Curse", "type": "DoT Drain", "desc": "Drena mana e vida do alvo simultaneamente ao longo do tempo."}
            ], ensure_ascii=False),
            "daevanion_priority": "Nós Laranja que ampliam a duração de feitiços de Fear e fortalecem o escalonamento dos espíritos elementais. Nós Verdes em aceleração de DoTs e nós Brancos em Magic Boost e Magical Accuracy.",
            "skill_rotation": "1. Invocar espírito de acordo com a situação (Fire para dano, Earth para tank) -> 2. Aplicar maldições e DoTs contínuos -> 3. Usar Ignite Aether para purgar proteções do alvo -> 4. Lançar Fear Shriek para desestruturar a formação inimiga.",
            "image_placeholder": "elementalist.svg"
        },
        {
            "slug": "cleric",
            "name": "Cleric",
            "role": "Main Healer",
            "role_category": "Main Healer",
            "primary_weapon": "Mace & Shield ou Staff (Báculo)",
            "secondary_weapon": "Shield (Escudo para alta sobrevivência)",
            "armor_type": "Chain (Armadura de Malha)",
            "difficulty": 3,
            "badge_color": "from-amber-400 to-yellow-600",
            "summary": "O salvador absoluto do grupo. O Main Healer de Aion 2 possui as curas mais potentes, remoção em massa de malefícios (Cleanse), barreiras protetoras e o indispensável poder de ressurreição em combate.",
            "lore": "Devotos mais fervorosos dos deuses de Aion. Dotados de graça curativa imensa, eles canalizam a luz para curar feridas fatais e purificar a corrupção do abismo que assola Atreia.",
            "playstyle": "Monitorar a barra de vida de todos os membros da party, antecipar mecânicas pesadas de chefes com barreiras e curas de grupo, além de usar o martelo com escudo para manter alta sobrevivência.",
            "strengths": json.dumps([
                "O mais completo e confiável conjunto de curas em alvo único e em grupo",
                "Habilidades essenciais de ressurreição em combate e fora dele",
                "Capacidade de limpar debuffs e venenos de todos os aliados com facilidade",
                "Alta defesa pessoal graças ao uso conjunto de Chain Armor e Shield"
            ], ensure_ascii=False),
            "weaknesses": json.dumps([
                "Dano ofensivo modesto quando configurado com Stigmas de cura",
                "Foco prioritário imediato dos adversários em qualquer batalha de PvP",
                "Consumo elevado de Mana durante batalhas prolongadas se não for bem administrado"
            ], ensure_ascii=False),
            "stigmas_pve": json.dumps([
                {"name": "Splendor of Recovery", "type": "Burst AoE Heal", "desc": "Cura massiva instantânea que restaura 60% do HP de todos os membros do grupo."},
                {"name": "Benevolence", "type": "Passive Stigma", "desc": "Aumenta o poder de todas as curas em 30% e reduz o custo de mana dos feitiços."},
                {"name": "Ripple of Purification", "type": "Cleanse AoE", "desc": "Remove imediatamente todos os debuffs e efeitos alteradores de status do grupo."},
                {"name": "Yustiel's Light", "type": "Ultimate Regen", "desc": "Bênção divina que cura e regenera HP continuamente a cada 2s por 30s."},
                {"name": "Rebirth", "type": "Auto-Revive", "desc": "Aplica uma bênção que ressuscita automaticamente o alvo caso ele seja abatido."},
                {"name": "Flash of Recovery", "type": "Instant Emergency Heal", "desc": "Cura instantânea de emergência de altíssimo valor sem tempo de conjuração."}
            ], ensure_ascii=False),
            "stigmas_pvp": json.dumps([
                {"name": "Flash of Recovery", "type": "Emergency Heal", "desc": "Salva a si mesmo ou um companheiro prestes a sucumbir a um burst rápido."},
                {"name": "Splendor of Rebirth", "type": "Shield & Heal", "desc": "Concede barreira protetora absorvente e cura simultânea."},
                {"name": "Root", "type": "Crowd Control", "desc": "Imobiliza atacantes corpo a corpo no lugar por 10s para conseguir se reposicionar."},
                {"name": "Blind", "type": "Debuff", "desc": "Cega o oponente, fazendo com que 80% dos seus golpes físicos errem o alvo."},
                {"name": "Ripple of Purification", "type": "Group Cleanse", "desc": "Neutraliza táticas de envenenamento e silenciamento de Rangers e Assassins."},
                {"name": "Hand of Reincarnation", "type": "Self Resurrection", "desc": "Permite ressuscitar imediatamente no local com 50% de HP durante conflitos."}
            ], ensure_ascii=False),
            "daevanion_priority": "Nós Laranja focados em Healing Power Amplification e redução do tempo de recarga de Flash of Recovery. Nós Verdes em Cast Time Reduction e consumo de mana, e nós Brancos em Max HP e Magic Resist.",
            "skill_rotation": "1. Manter Benevolence ativo -> 2. Aplicar bênçãos de regeneração contínua no Tank -> 3. Usar Ripple of Purification no primeiro segundo em que o grupo sofrer debuffs -> 4. Guardar Flash of Recovery e Splendor of Recovery para picos mecânicos.",
            "image_placeholder": "cleric.svg"
        },
        {
            "slug": "chanter",
            "name": "Chanter",
            "role": "Support / Healer",
            "role_category": "Support & Utility Buffs",
            "primary_weapon": "Staff (Báculo de duas mãos)",
            "secondary_weapon": "Mace & Shield (Opção de maior defesa)",
            "armor_type": "Chain (Armadura de Malha)",
            "difficulty": 2,
            "badge_color": "from-cyan-400 to-blue-600",
            "summary": "O melhor amigo de todo grupo em Aion 2. Especialista em 'Mantras' (auras permanentes de grupo), poderosos buffs de velocidade e ataque, escudos sagrados e atordoamentos contundentes com o báculo.",
            "lore": "Guerreiros clérigos treinados tanto na fé quanto nas artes marciais de bastão. Através de canções sagradas e mantras de batalha, eles elevam o poder de seus aliados além dos limites físicos normais.",
            "playstyle": "Alterna entre desferir golpes marciais com o báculo para atordoar alvos, fornecer curas secundárias e manter simultaneamente 3 Mantras ativos que impulsionam o DPS e defesa de todos ao redor.",
            "strengths": json.dumps([
                "Os melhores buffs ofensivos e defensivos do jogo através do sistema de Mantras",
                "Habilidades icônicas que dobram o dano do grupo (Word of Wind)",
                "Excelente sobrevivência e capacidade de lutar tanto de suporte quanto solo",
                "Capacidade de estontear (Stun / Stumble) inimigos constantemente com golpes de Staff"
            ], ensure_ascii=False),
            "weaknesses": json.dumps([
                "Poder de cura pura inferior ao do Cleric em situações de dano catastrófico",
                "Requer equilíbrio entre focar no combate direto e prestar atenção nas barras de HP dos companheiros",
                "Dependência de manter a party próxima para usufruir do alcance dos Mantras"
            ], ensure_ascii=False),
            "stigmas_pve": json.dumps([
                {"name": "Word of Wind", "type": "Ultimate Group Buff", "desc": "Aumenta drasticamente a Attack Speed e Movement Speed de toda a party em 50% por 30s."},
                {"name": "Victory Mantra", "type": "Mantra Aura", "desc": "Aura permanente que aumenta o Physical Attack e Magic Boost de todos os aliados em 20m."},
                {"name": "Shield of Protection", "type": "Group Barrier", "desc": "Cria um escudo sagrado em todos os aliados que absorve 2500 de dano."},
                {"name": "Hit Mantra", "type": "Mantra Aura", "desc": "Aura passiva que eleva a taxa de Critical Hit e Accuracy de todo o esquadrão."},
                {"name": "Healing Conduit", "type": "Active Heal", "desc": "Cura instantânea em cone à frente que recupera HP e concede regeneração."},
                {"name": "Mountain Fall", "type": "Active Knockdown", "desc": "Golpe descendente com o báculo que causa dano elevado e derruba o chefe."}
            ], ensure_ascii=False),
            "stigmas_pvp": json.dumps([
                {"name": "Word of Wind", "type": "Engage Ultimate", "desc": "Acelera a tropa inteira para abater formações inimigas antes que recuem."},
                {"name": "Celerity Mantra", "type": "Mantra Aura", "desc": "Aura permanente que garante velocidade de corrida contínua no mapa aberto."},
                {"name": "Magic Mantra", "type": "Mantra Aura", "desc": "Aumenta a Magic Resist da party inteira contra feitiços de Sorcerers."},
                {"name": "Soul Crush", "type": "Stun Combo", "desc": "Sequência marcial com o bastão que atordoa o inimigo repetidamente."},
                {"name": "Protective Ward", "type": "Emergency Shield", "desc": "Gera um escudo impenetrável de emergência contra ataques de surpresa."},
                {"name": "Recovery Spell", "type": "HoT (Heal over Time)", "desc": "Cura contínua aplicada em si mesmo para aguentar trocas diretas de dano."}
            ], ensure_ascii=False),
            "daevanion_priority": "Nós Laranja que ampliam a potência dos Mantras em 25% e o alcance para 30m. Nós Verdes em redução de tempo de recarga de buffs e nós Brancos em Physical Critical Hit, Attack e Max HP.",
            "skill_rotation": "1. Ativar Victory Mantra, Hit Mantra e Celerity Mantra para a equipe -> 2. Utilizar Word of Wind na fase de dano máximo do chefe -> 3. Aplicar combos de Staff para derrubar o alvo com Mountain Fall -> 4. Fornecer curas e escudos quando o Cleric estiver ocupado.",
            "image_placeholder": "chanter.svg"
        }
    ]

    for c in classes_data:
        cursor.execute('''
            INSERT INTO classes (
                slug, name, role, role_category, primary_weapon, secondary_weapon,
                armor_type, difficulty, badge_color, summary, lore, playstyle,
                strengths, weaknesses, stigmas_pve, stigmas_pvp, daevanion_priority,
                skill_rotation, image_placeholder
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            c["slug"], c["name"], c["role"], c["role_category"], c["primary_weapon"],
            c["secondary_weapon"], c["armor_type"], c["difficulty"], c["badge_color"],
            c["summary"], c["lore"], c["playstyle"], c["strengths"], c["weaknesses"],
            c["stigmas_pve"], c["stigmas_pvp"], c["daevanion_priority"],
            c["skill_rotation"], c["image_placeholder"]
        ))

    # Notícias
    news_data = [
        {
            "title": "Aion 2: Lançamento Global Confirmado com Level Cap 45 Inicial",
            "category": "Global Launch",
            "date_published": "27 de Setembro, 2026",
            "summary": "O aguardado MMORPG da NCSoft chegará mundialmente com servidores simultâneos, gráficos na Unreal Engine 5, combate aéreo tridimensional e o nível máximo inicial estipulado em Level 45.",
            "content": "A jornada de Atreia ressurge com poder renovado. Durante o período de lançamento global, todos os jogadores disputarão a corrida até o Level 45. Este teto de nível garantirá um balanceamento refinado para as primeiras disputas de facção entre Elyos e Asmodians nas zonas de conflito de Strongholds e nas desafiadoras Sealed Dungeons.",
            "is_featured": 1
        },
        {
            "title": "Guia de Sobrevivência Econômica: Por que Guardar suas Enhancement Stones",
            "category": "Economy & Gearing",
            "date_published": "25 de Setembro, 2026",
            "summary": "Especialistas alertam: as taxas de sucesso de Enhancement são 100% de +0 a +10, mas materiais de aprimoramento e Kina devem ser estocados para armas de Level 45.",
            "content": "Não caia na armadilha comum dos novatos de gastar todas as suas Enhancement Stones em equipamentos de nível baixo. Aproveite as armas concedidas nas Regional Quests e na Main Story até o teto de nível para garantir seu arsenal mítico assim que alcançar o end-game.",
            "is_featured": 1
        },
        {
            "title": "Sistema de Montarias e Pets: Captura Através do Combate Confirmada",
            "category": "Gameplay Systems",
            "date_published": "22 de Setembro, 2026",
            "summary": "Diga adeus às compras puras de montarias: em Aion 2 você precisará enfrentar, enfraquecer e domar feras selvagens diretamente no mundo aberto de Atreia.",
            "content": "O novo sistema de captura transforma a fauna de Atreia em aliados valiosos. Ao reduzir o HP de monstros especiais para menos de 20%, o jogador poderá iniciar o minigame de domesticação para transformá-los em montarias de viagem ou pets de suporte com bônus passivos de status.",
            "is_featured": 0
        }
    ]

    for n in news_data:
        cursor.execute('''
            INSERT INTO news (title, category, date_published, summary, content, is_featured)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (n["title"], n["category"], n["date_published"], n["summary"], n["content"], n["is_featured"]))

    # Sistemas
    systems_data = [
        {
            "key": "stigmas",
            "title": "Skills & Stigmas",
            "subtitle": "Customização profunda com até 6 Stigmas equipáveis",
            "description": "O sistema de Stigmas permite que cada classe personalize seu kit de habilidades com feitiços lendários que modificam a dinâmica do combate PvE e PvP.",
            "details_json": json.dumps({
                "max_slots": 6,
                "unlock_levels": [10, 20, 30, 35, 40, 45],
                "description": "Cada personagem pode equipar até 6 Stigmas simultaneamente. Essas habilidades não pertencem à árvore básica e fornecem ferramentas decisivas como o teletransporte Shadowstep para Assassin ou as auras de Mantras para Chanter.",
                "tip": "Mantenha conjuntos pré-definidos para alternar rapidamente entre masmorras PvE e embates de facção PvP."
            }, ensure_ascii=False)
        },
        {
            "key": "daevanion",
            "title": "Daevanion Boards",
            "subtitle": "A árvore estelar de nodes de progressão de Atreia",
            "description": "O tabuleiro Daevanion substitui as antigas grades rígidas por nós de constelações que oferecem status, habilidades passivas, novos combos e efeitos especiais.",
            "details_json": json.dumps({
                "nodes": [
                    {"color": "Branco", "type": "Status Básicos", "desc": "Concede atributos brutos essenciais como Physical Attack, Magic Boost, HP, Physical Defense e Critical Hit."},
                    {"color": "Verde", "type": "Skills Passivas", "desc": "Desbloqueia melhorias passivas de combate, redução de cooldown, bônus de velocidade e mitigação de dano."},
                    {"color": "Azul", "type": "Skills Ativas", "desc": "Adiciona novas habilidades de combate ou versões aprimoradas de combos clássicos de cada classe."},
                    {"color": "Laranja", "type": "Bônus Únicos Lendários", "desc": "O ápice do poder Daevanion: efeitos transformadores de gameplay, como cura após mortes ou recarga total de recargas."}
                ]
            }, ensure_ascii=False)
        },
        {
            "key": "enhancement",
            "title": "Enhancement & Gearing",
            "subtitle": "Regras do sistema de melhoria com Enhancement Stones e proteção até +10",
            "description": "Entenda as regras matemáticas do Enhancement para não perder Kina nem quebrar itens valiosos no início do jogo.",
            "details_json": json.dumps({
                "safe_range": "+0 a +10 (100% de taxa de sucesso garantida)",
                "danger_range": "+11 a +15 (Queda drástica de chance e risco de perda de nível)",
                "resource": "Enhancement Stones e Kina",
                "golden_rule": "Economize todos os seus recursos de upgrade para o Level 45. Durante o leveling, utilize apenas o equipamento recompensado na Main Story e Regional Quests."
            }, ensure_ascii=False)
        },
        {
            "key": "inheritance",
            "title": "Sistema de Inheritance",
            "subtitle": "Transfira o nível de aprimoramento de equipamentos antigos",
            "description": "O sistema de Inheritance elimina a frustração de perder investimentos em armas anteriores ao transferir aprimoramentos para novos equipamentos de tier superior.",
            "details_json": json.dumps({
                "mechanic": "Permite transferir o nível de Enhancement (+X) de uma arma ou armadura anterior diretamente para uma nova peça obtida em Sealed Dungeons de nível superior.",
                "benefit": "Evita o desperdício de Enhancement Stones e Kina em cada troca de equipamento."
            }, ensure_ascii=False)
        },
        {
            "key": "soul_binding",
            "title": "Soul Binding & Reroll de Status",
            "subtitle": "Vincule o item à sua alma e refine os substats perfeitos",
            "description": "Ao vincular um item ao personagem com Soul Binding, desbloqueie linhas de propriedades secundárias ajustáveis para obter atributos ideais para sua classe.",
            "details_json": json.dumps({
                "features": "Permite roletar novamente substats indesejados (como trocar Defesa Mágica por Crítico Físico em um Gladiator).",
                "warning": "Uma vez realizado o Soul Binding, o equipamento torna-se intransferível e não pode ser negociado na casa de leilões por Kina."
            }, ensure_ascii=False)
        },
        {
            "key": "manastones_godstones",
            "title": "Manastones & Godstones",
            "subtitle": "Gemas de atributos e pedras divinas de efeitos de combate",
            "description": "Equipe Manastones nos soquetes de armaduras e armas para elevar atributos específicos e incruste Godstones para efeitos de batalha surpreendentes.",
            "details_json": json.dumps({
                "manastones": "Gemas engastadas em soquetes livres (slots) de armaduras e armas. Permitem acumular Critical Hit, Attack, Magic Boost, HP e Accuracy.",
                "godstones": "Pedras ancestrais lendárias equipadas na arma principal que oferecem uma chance percentual de ativar efeitos de combate por golpe, como Paralyze (paralisia), Silence (silêncio), Blind (cegueira) ou rajadas de dano elemental extra."
            }, ensure_ascii=False)
        }
    ]

    for s in systems_data:
        cursor.execute('''
            INSERT INTO systems (key, title, subtitle, description, details_json)
            VALUES (?, ?, ?, ?, ?)
        ''', (s["key"], s["title"], s["subtitle"], s["description"], s["details_json"]))

def seed_events(cursor):
    """Insere os eventos ativos in-game iniciais."""
    events_data = [
        {
            "title": "Festival de Lançamento Global: Bênção de Atreia",
            "category": "EXP & Leveling Boost",
            "status": "Ativo Agora",
            "badge_color": "border-emerald-500/40 text-emerald-300 bg-emerald-500/10",
            "period": "27 de Setembro a 15 de Outubro",
            "summary": "Durante o período de abertura dos servidores globais de Aion 2, todos os Daevas recebem +20% de EXP adicional ao completar missões da Main Story e Regional Quests até o Level 45.",
            "rewards": "+20% EXP em Quests, Poções de Voo e Pacote Inicial de Kina",
            "is_active": 1
        },
        {
            "title": "Cerco aos Abismos: Guerra em Strongholds",
            "category": "PvPvE & Facções",
            "status": "Ativo Agora",
            "badge_color": "border-rose-500/40 text-rose-300 bg-rose-500/10",
            "period": "Quintas e Domingos às 21h00 BRT",
            "summary": "Guerra territorial direta entre Elyos e Asmodians pelo domínio das primeiras fortalezas de mapa. Facções que defenderem ou conquistarem Strongholds recebem bônus territoriais globais.",
            "rewards": "Medalhas de Honra em dobro, Kina e Buffs de Facção",
            "is_active": 1
        },
        {
            "title": "Expedição Heroica: Provações em Sealed Dungeons",
            "category": "Masmorras & Loot",
            "status": "Ativo Agora",
            "badge_color": "border-amber-500/40 text-amber-300 bg-amber-500/10",
            "period": "Temporada 1 de Lançamento",
            "summary": "Complete as Sealed Dungeons diárias com sua party para receber baús bônus contendo Enhancement Stones e soquetes adicionais de Manastones para o seu arsenal.",
            "rewards": "Enhancement Stones extras e Baús Raros de Manastones",
            "is_active": 1
        }
    ]

    for ev in events_data:
        cursor.execute('''
            INSERT INTO events (title, category, status, badge_color, period, summary, rewards, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (ev["title"], ev["category"], ev["status"], ev["badge_color"], ev["period"], ev["summary"], ev["rewards"], ev["is_active"]))

if __name__ == '__main__':
    print("Inicializando banco de dados aion2_guides.db...")
    init_db()
    print("Banco de dados inicializado com sucesso!")
