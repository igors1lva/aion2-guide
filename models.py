"""
models.py - Camada de acesso aos dados e abstrações do banco SQLite.
"""

import json
from database import get_db_connection

def get_embed_url(url):
    """Converte automaticamente links normais do YouTube para formato iframe embed."""
    if not url:
        return None
    url = url.strip()
    if 'embed/' in url:
        return url
    if 'watch?v=' in url:
        vid = url.split('watch?v=')[1].split('&')[0]
        return f"https://www.youtube.com/embed/{vid}"
    if 'youtu.be/' in url:
        vid = url.split('youtu.be/')[1].split('?')[0]
        return f"https://www.youtube.com/embed/{vid}"
    return url


# Base de Macros Oficiais da Comunidade (.txt) para Boss, Auto-Mode e Buffs
CLASS_MACROS = {
    "gladiator": [
        {
            "id": "macro-gladiator-boss",
            "title": "Rotação de Boss & Burst DPS (Single Target)",
            "category": "boss",
            "category_label": "Boss & Dungeons",
            "badge_color": "bg-rose-500/20 text-rose-300 border-rose-500/30",
            "description": "Quebra as defesas do chefe com Armor Murder, engaja com Ferocious Strike para provocar derrubada (Knockdown) e desfere os golpes de alto dano crítico Severe Precision Cut e Draining Blow.",
            "filename": "macro_gladiator_boss.txt",
            "commands_raw": """/Select [%Target]
/Skill Armor Murder
/Delay 1.1
/Skill Ferocious Strike
/Delay 0.9
/Skill Severe Precision Cut
/Delay 1.2
/Skill Draining Blow
/Delay 1.0
/Attack"""
        },
        {
            "id": "macro-gladiator-auto",
            "title": "Auto-Mode & Missões Regionais (Limpeza AoE)",
            "category": "auto",
            "category_label": "Auto-Mode / Missões",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "description": "Mira no monstro mais próximo automaticamente, avança com investida, gira com o corte em área Whirlwind Strike e conecta combos rápidos para cumprir missões sem fadiga.",
            "filename": "macro_gladiator_auto_mode.txt",
            "commands_raw": """/AutomaticSelection
/Attack
/Skill Dauntless Charge
/Delay 1.0
/Skill Whirlwind Strike
/Delay 1.3
/Skill Ferocious Strike
/Delay 1.0
/Attack"""
        },
        {
            "id": "macro-gladiator-buff",
            "title": "Auto-Buff & Sobrevivência (Pré-Combate)",
            "category": "buff",
            "category_label": "Auto-Buff & Sobrevivência",
            "badge_color": "bg-amber-500/20 text-amber-300 border-amber-500/30",
            "description": "Ativa a postura berserker de 80% de bônus de dano físico e o buff de cura de emergência Second Wind antes de voltar a mirar no chefe.",
            "filename": "macro_gladiator_buffs.txt",
            "commands_raw": """/Select [%Self]
/Skill Berserking
/Delay 1.0
/Skill Second Wind
/Delay 0.9
/Select [%PreviousTarget]"""
        }
    ],
    "templar": [
        {
            "id": "macro-templar-boss",
            "title": "Rotação de Boss & Travamento de Aggro (Single Target)",
            "category": "boss",
            "category_label": "Boss & Dungeons",
            "badge_color": "bg-rose-500/20 text-rose-300 border-rose-500/30",
            "description": "Avanço de escudo seguido de Incite Rage para consolidar Threat absoluto, debuff de dano com Righteous Punishment e atordoamento de escudo.",
            "filename": "macro_templar_boss.txt",
            "commands_raw": """/Select [%Target]
/Skill Shield Charge
/Delay 1.0
/Skill Incite Rage
/Delay 1.1
/Skill Taunt Strike
/Delay 1.0
/Skill Righteous Punishment
/Delay 1.2
/Skill Shield Burst
/Attack"""
        },
        {
            "id": "macro-templar-auto",
            "title": "Auto-Mode & Missões Regionais (Puxão & Escudo)",
            "category": "auto",
            "category_label": "Auto-Mode / Missões",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "description": "Mira automática no mob mais próximo, puxa com corrente etérea Doom Lure a até 16m e destrói o alvo com contra-ataques de escudo.",
            "filename": "macro_templar_auto_mode.txt",
            "commands_raw": """/AutomaticSelection
/Skill Doom Lure
/Delay 1.2
/Attack
/Skill Shield Counter
/Delay 1.0
/Skill Taunt Strike
/Delay 1.0
/Attack"""
        },
        {
            "id": "macro-templar-buff",
            "title": "Muralha Sagrada de Emergência (Auto-Defesa)",
            "category": "buff",
            "category_label": "Defensivo & Sobrevivência",
            "badge_color": "bg-sky-500/20 text-sky-300 border-sky-500/30",
            "description": "Aciona redução de dano de 50% de Iron Skin somado ao bônus de 25% de vida de Empyrean Armor para segurar mecânicas brutais.",
            "filename": "macro_templar_defensivos.txt",
            "commands_raw": """/Select [%Self]
/Skill Iron Skin
/Delay 0.8
/Skill Empyrean Armor
/Delay 0.8
/Select [%PreviousTarget]"""
        }
    ],
    "assassin": [
        {
            "id": "macro-assassin-boss",
            "title": "Rotação de Boss & Detonação de Runas (Single Target)",
            "category": "boss",
            "category_label": "Boss & Dungeons",
            "badge_color": "bg-rose-500/20 text-rose-300 border-rose-500/30",
            "description": "Teleporta instantaneamente para as costas do chefe com Shadowstep (100% crítico garantido), grava runas corrosivas e detona com Rune Burst.",
            "filename": "macro_assassin_boss.txt",
            "commands_raw": """/Select [%Target]
/Skill Shadowstep
/Delay 0.7
/Skill Rune Carve
/Delay 0.8
/Skill Quickening Gloom
/Delay 0.9
/Skill Rune Burst
/Delay 1.0
/Attack"""
        },
        {
            "id": "macro-assassin-auto",
            "title": "Auto-Mode & Missões Regionais (Emboscada Rápida)",
            "category": "auto",
            "category_label": "Auto-Mode / Missões",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "description": "Localiza o monstro mais próximo da missão, inicia com atordoamento Ambush pelas costas e desfere cortes de adaga velozes.",
            "filename": "macro_assassin_auto_mode.txt",
            "commands_raw": """/AutomaticSelection
/Skill Ambush
/Delay 0.8
/Skill Rune Carve
/Delay 0.8
/Skill Rune Burst
/Delay 0.9
/Attack"""
        },
        {
            "id": "macro-assassin-buff",
            "title": "Pré-Engajamento com Flurry & Furtividade",
            "category": "buff",
            "category_label": "Auto-Buff & Preparação",
            "badge_color": "bg-purple-500/20 text-purple-300 border-purple-500/30",
            "description": "Acelera a velocidade de ataque de adagas em 25% por 30s, ativa esquiva mágica Spelldodge e entra em Shadow Walk.",
            "filename": "macro_assassin_buffs.txt",
            "commands_raw": """/Select [%Self]
/Skill Flurry
/Delay 0.8
/Skill Spelldodge
/Delay 0.8
/Skill Shadow Walk"""
        }
    ],
    "ranger": [
        {
            "id": "macro-ranger-boss",
            "title": "Rotação de Boss & Disparo Perfurante (Single Target)",
            "category": "boss",
            "category_label": "Boss & Dungeons",
            "badge_color": "bg-rose-500/20 text-rose-300 border-rose-500/30",
            "description": "Ignora 30% da armadura do chefe com Spiral Arrow, ativa a precisão de Sharpshooter Aim e dispara três flechas consecutivas de Gale Arrow.",
            "filename": "macro_ranger_boss.txt",
            "commands_raw": """/Select [%Target]
/Skill Spiral Arrow
/Delay 1.1
/Skill Sharpshooter Aim
/Delay 0.9
/Skill Gale Arrow
/Delay 1.3
/Attack"""
        },
        {
            "id": "macro-ranger-auto",
            "title": "Auto-Mode & Missões Regionais (Chuva de Flechas AoE)",
            "category": "auto",
            "category_label": "Auto-Mode / Missões",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "description": "Mira automática à distância no mob da missão, imobiliza com Entangling Shot e extermina o grupo com Arrow Deluge.",
            "filename": "macro_ranger_auto_mode.txt",
            "commands_raw": """/AutomaticSelection
/Skill Entangling Shot
/Delay 1.0
/Skill Arrow Deluge
/Delay 1.4
/Skill Gale Arrow
/Delay 1.1
/Attack"""
        },
        {
            "id": "macro-ranger-buff",
            "title": "Transformação Mau Form & Imunidade",
            "category": "buff",
            "category_label": "Auto-Buff & Mobilidade",
            "badge_color": "bg-teal-500/20 text-teal-300 border-teal-500/30",
            "description": "Entra na forma felina Mau Form aumentando mobilidade e velocidade de disparo enquanto remove quaisquer efeitos de lentidão.",
            "filename": "macro_ranger_buffs.txt",
            "commands_raw": """/Select [%Self]
/Skill Mau Form
/Delay 0.8
/Skill Nature's Resolve
/Delay 0.8
/Select [%PreviousTarget]"""
        }
    ],
    "sorcerer": [
        {
            "id": "macro-sorcerer-boss",
            "title": "Rotação de Boss & Glacial Burst (Single Target)",
            "category": "boss",
            "category_label": "Boss & Dungeons",
            "badge_color": "bg-rose-500/20 text-rose-300 border-rose-500/30",
            "description": "Reduz o tempo de conjuração pela metade com Boon of Quickness, desaba a lança Glacial Shard e executa com Flame Spray.",
            "filename": "macro_sorcerer_boss.txt",
            "commands_raw": """/Select [%Target]
/Skill Boon of Quickness
/Delay 0.8
/Skill Glacial Shard
/Delay 2.2
/Skill Flame Spray
/Delay 1.2
/Skill Aetheric Spellburst"""
        },
        {
            "id": "macro-sorcerer-auto",
            "title": "Auto-Mode & Missões Regionais (Erupção Vulcânica AoE)",
            "category": "auto",
            "category_label": "Auto-Mode / Missões",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "description": "Trava no monstro mais próximo e derrete ondas inteiras de mobs da missão com Big Magma Eruption e jatos de fogo instantâneos.",
            "filename": "macro_sorcerer_auto_mode.txt",
            "commands_raw": """/AutomaticSelection
/Skill Big Magma Eruption
/Delay 2.0
/Skill Flame Spray
/Delay 1.1
/Attack"""
        },
        {
            "id": "macro-sorcerer-buff",
            "title": "Barreira Arcana de Mana (Auto-Shield)",
            "category": "buff",
            "category_label": "Auto-Buff & Sobrevivência",
            "badge_color": "bg-amber-500/20 text-amber-300 border-amber-500/30",
            "description": "Conjura a casca de éter Stone Skin para absorver 3000 de dano e prepara o casulo refletor Frost Barrier.",
            "filename": "macro_sorcerer_buffs.txt",
            "commands_raw": """/Select [%Self]
/Skill Stone Skin
/Delay 0.8
/Skill Frost Barrier
/Delay 0.8
/Select [%PreviousTarget]"""
        }
    ],
    "elementalist": [
        {
            "id": "macro-elementalist-boss",
            "title": "Rotação de Boss & Corrosão Contínua (Single Target)",
            "category": "boss",
            "category_label": "Boss & Dungeons",
            "badge_color": "bg-rose-500/20 text-rose-300 border-rose-500/30",
            "description": "Buffa o pet elemental, expurga buffs e escudos do chefe com Ignite Aether e empilha venenos corrosivos de Curse Cloud.",
            "filename": "macro_elementalist_boss.txt",
            "commands_raw": """/Select [%Target]
/Skill Armor Spirit
/Delay 1.0
/Skill Ignite Aether
/Delay 1.2
/Skill Curse Cloud
/Delay 1.4
/Skill Erosion Curse
/Delay 1.1
/Attack"""
        },
        {
            "id": "macro-elementalist-auto",
            "title": "Auto-Mode & Missões Regionais (Controle & Dano em Área)",
            "category": "auto",
            "category_label": "Auto-Mode / Missões",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "description": "Enraíza o alvo com Body Root enquanto comanda o espírito elemental para incendiar todos os monstros com Spirit Burn.",
            "filename": "macro_elementalist_auto_mode.txt",
            "commands_raw": """/AutomaticSelection
/Skill Body Root
/Delay 1.0
/Skill Spirit Burn
/Delay 1.3
/Skill Erosion Curse
/Delay 1.1
/Attack"""
        },
        {
            "id": "macro-elementalist-buff",
            "title": "Barreira de Grupo & Substituição de Dano",
            "category": "buff",
            "category_label": "Suporte & Sobrevivência",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "description": "Projeta a muralha elemental de proteção para todo o grupo e transfere o dano do invocador para o pet com Spirit Substitution.",
            "filename": "macro_elementalist_buffs.txt",
            "commands_raw": """/Select [%Self]
/Skill Spirit Wall of Protection
/Delay 0.9
/Skill Spirit Substitution
/Delay 0.8
/Select [%PreviousTarget]"""
        }
    ],
    "cleric": [
        {
            "id": "macro-cleric-boss",
            "title": "Rotação de Cura de Emergência no Tank (Single Target)",
            "category": "boss",
            "category_label": "Boss & Dungeons (Cura)",
            "badge_color": "bg-rose-500/20 text-rose-300 border-rose-500/30",
            "description": "Foca instantaneamente o Main Tank da party para aplicar cura de emergência imediata sem cast, seguida de bênçãos de regeneração.",
            "filename": "macro_cleric_tank_heal.txt",
            "commands_raw": """/Select [%Group1]
/Skill Flash of Recovery
/Delay 0.8
/Skill Splendor of Recovery
/Delay 1.4
/Skill Yustiel's Light
/Delay 1.2
/Select [%Target]"""
        },
        {
            "id": "macro-cleric-auto",
            "title": "Auto-Mode & Missões Regionais (Leveling Solo & Purificação)",
            "category": "auto",
            "category_label": "Auto-Mode / Missões",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "description": "Trava no monstro mais próximo, imobiliza com Root, purifica debuffs do personagem e conecta ataques de punição sagrada.",
            "filename": "macro_cleric_auto_mode.txt",
            "commands_raw": """/AutomaticSelection
/Skill Root
/Delay 1.0
/Select [%Self]
/Skill Ripple of Purification
/Delay 0.9
/Select [%PreviousTarget]
/Attack"""
        },
        {
            "id": "macro-cleric-buff",
            "title": "Postura Benevolence & Auto-Ressurreição",
            "category": "buff",
            "category_label": "Auto-Buff & Bênçãos",
            "badge_color": "bg-amber-500/20 text-amber-300 border-amber-500/30",
            "description": "Ativa a postura curativa Benevolence (+30% poder de cura e menor custo de MP) e a bênção de reviver preventivo Rebirth.",
            "filename": "macro_cleric_buffs.txt",
            "commands_raw": """/Select [%Self]
/Skill Benevolence
/Delay 0.8
/Skill Rebirth
/Delay 1.0
/Select [%PreviousTarget]"""
        }
    ],
    "chanter": [
        {
            "id": "macro-chanter-boss",
            "title": "Rotação de Boss & Aceleração de Party (Burst Ofensivo)",
            "category": "boss",
            "category_label": "Boss & Dungeons (Buffs & DPS)",
            "badge_color": "bg-rose-500/20 text-rose-300 border-rose-500/30",
            "description": "Impulsiona todo o grupo com Word of Quickness e Word of Wind, travando o chefe com combos contundentes de báculo.",
            "filename": "macro_chanter_boss.txt",
            "commands_raw": """/Select [%Self]
/Skill Word of Quickness
/Delay 0.8
/Skill Word of Wind
/Delay 0.8
/Select [%Target]
/Skill Soul Strike
/Delay 1.1
/Skill Meteor Strike
/Attack"""
        },
        {
            "id": "macro-chanter-auto",
            "title": "Auto-Mode & Missões Regionais (Combos com Báculo)",
            "category": "auto",
            "category_label": "Auto-Mode / Missões",
            "badge_color": "bg-emerald-500/20 text-emerald-300 border-emerald-500/30",
            "description": "Trava no inimigo mais próximo, atordoa com Soul Strike e conecta golpes marciais contínuos para limpar missões solo.",
            "filename": "macro_chanter_auto_mode.txt",
            "commands_raw": """/AutomaticSelection
/Skill Soul Strike
/Delay 1.0
/Skill Meteor Strike
/Delay 1.2
/Attack"""
        },
        {
            "id": "macro-chanter-buff",
            "title": "Ciclo Permanente de Mantras & Escudo Sagrado",
            "category": "buff",
            "category_label": "Auras de Grupo / Mantras",
            "badge_color": "bg-cyan-500/20 text-cyan-300 border-cyan-500/30",
            "description": "Liga simultaneamente Victory Mantra (ataque), Shield Mantra (defesa) e aciona a barreira sagrada Protective Ward.",
            "filename": "macro_chanter_mantras.txt",
            "commands_raw": """/Select [%Self]
/Skill Victory Mantra
/Delay 0.8
/Skill Shield Mantra
/Delay 0.8
/Skill Protective Ward
/Delay 0.9
/Select [%PreviousTarget]"""
        }
    ]
}


class ClassModel:
    @staticmethod
    def _format_row(row):
        if not row:
            return None
        data = dict(row)
        data['strengths_list'] = json.loads(data['strengths']) if data.get('strengths') else []
        data['weaknesses_list'] = json.loads(data['weaknesses']) if data.get('weaknesses') else []
        data['stigmas_pve_list'] = json.loads(data['stigmas_pve']) if data.get('stigmas_pve') else []
        data['stigmas_pvp_list'] = json.loads(data['stigmas_pvp']) if data.get('stigmas_pvp') else []

        # Gerar URL de embed caso não esteja explícita mas video_url exista
        if data.get('video_url') and not data.get('video_embed_url'):
            data['video_embed_url'] = get_embed_url(data['video_url'])

        # Injetar os macros da classe correspondente
        data['macros'] = CLASS_MACROS.get(data.get('slug'), [])

        return data

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM classes ORDER BY id ASC')
        rows = cursor.fetchall()
        conn.close()
        return [cls._format_row(r) for r in rows]

    @classmethod
    def get_by_slug(cls, slug):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM classes WHERE slug = ?', (slug,))
        row = cursor.fetchone()
        conn.close()
        return cls._format_row(row)

    @classmethod
    def update_video(cls, slug, video_url, video_title=None, video_credits=None, video_author_url=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        embed_url = get_embed_url(video_url)
        cursor.execute('''
            UPDATE classes 
            SET video_url = ?, video_embed_url = ?, video_title = ?, video_credits = ?, video_author_url = ?
            WHERE slug = ?
        ''', (video_url, embed_url, video_title, video_credits, video_author_url, slug))
        conn.commit()
        conn.close()
        return True

    @classmethod
    def get_macros_by_slug(cls, slug):
        return CLASS_MACROS.get(slug, [])


class NewsModel:
    @staticmethod
    def get_featured():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM news WHERE is_featured = 1 ORDER BY id DESC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_all(limit=10):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM news ORDER BY id DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

class EventModel:
    @staticmethod
    def get_active():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events WHERE is_active = 1 ORDER BY id ASC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events ORDER BY id ASC')
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

class SystemModel:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM systems ORDER BY id ASC')
        rows = cursor.fetchall()
        conn.close()
        result = []
        for r in rows:
            item = dict(r)
            item['details'] = json.loads(item['details_json']) if item.get('details_json') else {}
            result.append(item)
        return result

    @staticmethod
    def get_by_key(key):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM systems WHERE key = ?', (key,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            return None
        item = dict(row)
        item['details'] = json.loads(item['details_json']) if item.get('details_json') else {}
        return item
