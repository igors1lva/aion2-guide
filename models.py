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
CLASS_MACROS = {   'assassin': [   {   'badge_color': 'bg-rose-500/20 text-rose-300 border-rose-500/30',
                        'category': 'boss',
                        'category_label': 'Boss & Burst DPS',
                        'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                        'Classe: Assassin\n'
                                        'Preset: Preset 1 (Alt + 4) - Boss Burst DPS & Detonação de Runas\n'
                                        'Local no Jogo: Pressione K (Skills) -> Ability-Macro\n'
                                        'Tecla de Acesso: Settings -> Key Settings -> General -> Gameplay -> '
                                        'Ability-Macro\n'
                                        '\n'
                                        'SLOTS DE HABILIDADES CONFIGURADOS:\n'
                                        'Slot 1: Rune Carve (Entalhe de Runa)\n'
                                        'Slot 2: Quickening Gloom (Veneno & Empilhamento)\n'
                                        'Slot 3: Rune Burst (Detonação Crítica com 5 Runas)\n'
                                        'Slot 4: Fang Strike (Combo Rápido de Adagas)\n'
                                        '\n'
                                        'CONFIGURAÇÃO DE DELAY: 10 ms por slot\n'
                                        'MODO DE USO EM COMBATE:\n'
                                        'Posicione-se nas costas do chefe com Shadowstep e segure a tecla do '
                                        'Ability-Macro. O sistema ativará os golpes e entrelaçará cortes duplos com '
                                        'animação cancelada.',
                        'delay_ms': 10,
                        'description': 'Grava runas corrosivas em alta velocidade com Rune Carve e Quickening Gloom, '
                                       'detonando-as com Rune Burst para dano crítico colossal.',
                        'exclusions': 'Shadowstep deve ser usado manualmente para reposicionar instantaneamente nas '
                                      'costas antes de segurar o macro.',
                        'filename': 'assassin_ability_macro_preset1.txt',
                        'id': 'macro-assassin-boss',
                        'preset_name': 'Preset 1',
                        'preset_number': 1,
                        'shortcut': 'Alt + 4',
                        'skill_slots': ['Rune Carve', 'Quickening Gloom', 'Rune Burst', 'Fang Strike'],
                        'title': 'Preset 1: Boss Burst DPS & Detonação de Runas',
                        'weaving_info': 'Segure a tecla do macro posicionado nas costas do alvo. O weaving entrelaça '
                                        'ataques com adagas duplas na velocidade mais rápida do jogo, cancelando '
                                        'animações perfeitamente.'},
                    {   'badge_color': 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
                        'category': 'auto',
                        'category_label': 'AoE & Emboscada',
                        'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                        'Classe: Assassin\n'
                                        'Preset: Preset 2 (Alt + 5) - Emboscada Rápida & Limpeza\n'
                                        'Local no Jogo: Menu K -> Ability-Macro\n'
                                        '\n'
                                        'SLOTS DE HABILIDADES:\n'
                                        'Slot 1: Ambush (Stun pelas Costas)\n'
                                        'Slot 2: Rune Carve\n'
                                        'Slot 3: Rune Burst\n'
                                        '\n'
                                        'CONFIGURAÇÃO DE DELAY: 10 ms',
                        'delay_ms': 10,
                        'description': 'Engaja com atordoamento Ambush pelas costas e desfere cortes de adaga velozes '
                                       'com acúmulo imediato de dano de finalização.',
                        'exclusions': 'Não use em alvos frontais para não perder o multiplicador crítico de Backstab.',
                        'filename': 'assassin_ability_macro_preset2.txt',
                        'id': 'macro-assassin-auto',
                        'preset_name': 'Preset 2',
                        'preset_number': 2,
                        'shortcut': 'Alt + 5',
                        'skill_slots': ['Ambush', 'Rune Carve', 'Rune Burst'],
                        'title': 'Preset 2: Emboscada Rápida & Limpeza de Missões',
                        'weaving_info': 'Elimina monstros regulares antes do término do tempo de atordoamento de 2 '
                                        'segundos.'},
                    {   'badge_color': 'bg-purple-500/20 text-purple-300 border-purple-500/30',
                        'category': 'buff',
                        'category_label': 'Defensivo & PvP',
                        'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                        'Classe: Assassin\n'
                                        'Preset: Preset 3 (Alt + 6) - Evasão Tática & Contra-Golpe\n'
                                        'Local no Jogo: Menu K -> Ability-Macro\n'
                                        '\n'
                                        'SLOTS DE HABILIDADES:\n'
                                        'Slot 1: Spelldodge\n'
                                        'Slot 2: Shadowstep\n'
                                        'Slot 3: Rune Burst\n'
                                        '\n'
                                        'CONFIGURAÇÃO DE DELAY: 10 ms',
                        'delay_ms': 10,
                        'description': 'Aciona Spelldodge para anular as magias inimigas enquanto conecta '
                                       'contra-ataques após esquivas físicas bem-sucedidas.',
                        'exclusions': 'Flurry e Shadow Walk devem ser ativados antes de entrar no alcance de combate.',
                        'filename': 'assassin_ability_macro_preset3.txt',
                        'id': 'macro-assassin-buff',
                        'preset_name': 'Preset 3',
                        'preset_number': 3,
                        'shortcut': 'Alt + 6',
                        'skill_slots': ['Spelldodge', 'Shadowstep', 'Rune Burst'],
                        'title': 'Preset 3: Evasão Tática & Contra-Golpe em PvP',
                        'weaving_info': 'Garante sobrevivência contra rajadas mágicas de Sorcerers e Clerics.'}],
    'chanter': [   {   'badge_color': 'bg-rose-500/20 text-rose-300 border-rose-500/30',
                       'category': 'boss',
                       'category_label': 'Boss & Dungeons (DPS)',
                       'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                       'Classe: Chanter\n'
                                       'Preset: Preset 1 (Alt + 4) - Boss Burst Ofensivo com Báculo\n'
                                       'Local no Jogo: Pressione K (Skills) -> Ability-Macro\n'
                                       'Tecla de Acesso: Settings -> Key Settings -> General -> Gameplay -> '
                                       'Ability-Macro\n'
                                       '\n'
                                       'SLOTS DE HABILIDADES CONFIGURADOS:\n'
                                       'Slot 1: Soul Strike (Atordoamento / Stun Inicial)\n'
                                       'Slot 2: Meteor Strike (Combo Consecutivo de Bastão)\n'
                                       'Slot 3: Mountain Fall (Golpe Descendente & Knockdown)\n'
                                       'Slot 4: Healing Conduit (Cone de Cura & Dano)\n'
                                       '\n'
                                       'CONFIGURAÇÃO DE DELAY: 10 ms por slot\n'
                                       'MODO DE USO EM COMBATE:\n'
                                       'Certifique-se de que seus Mantras estão ativados previamente como auras. '
                                       'Segure a tecla do Ability-Macro para manter pressão de atordoamento contínua '
                                       'no chefe.',
                       'delay_ms': 10,
                       'description': 'Atordoa o chefe com Soul Strike, conecta a sequência devastadora de Meteor '
                                      'Strike e derruba com Mountain Fall enquanto recupera HP da equipe com Healing '
                                      'Conduit.',
                       'exclusions': 'Mantras (Victory Mantra, Hit Mantra, Celerity Mantra) são auras permanentes e '
                                     'NÃO devem ser incluídas no loop do macro; ative-as previamente.',
                       'filename': 'chanter_ability_macro_preset1.txt',
                       'id': 'macro-chanter-boss',
                       'preset_name': 'Preset 1',
                       'preset_number': 1,
                       'shortcut': 'Alt + 4',
                       'skill_slots': ['Soul Strike', 'Meteor Strike', 'Mountain Fall', 'Healing Conduit'],
                       'title': 'Preset 1: Boss Burst Ofensivo & Combos com Báculo',
                       'weaving_info': 'Segure a tecla do Ability-Macro. O báculo desfere ataques marciais contínuos '
                                       'intercalados (weaving), atordoando e derrubando inimigos frequentemente.'},
                   {   'badge_color': 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
                       'category': 'auto',
                       'category_label': 'AoE & Missões',
                       'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                       'Classe: Chanter\n'
                                       'Preset: Preset 2 (Alt + 5) - Limpeza Rápida com Báculo\n'
                                       'Local no Jogo: Menu K -> Ability-Macro\n'
                                       '\n'
                                       'SLOTS DE HABILIDADES:\n'
                                       'Slot 1: Soul Strike\n'
                                       'Slot 2: Meteor Strike\n'
                                       'Slot 3: Mountain Fall\n'
                                       '\n'
                                       'CONFIGURAÇÃO DE DELAY: 10 ms',
                       'delay_ms': 10,
                       'description': 'Conecta golpes rápidos de báculo com chance contínua de desestabilização para '
                                      'derrotar monstros sem sofrer contra-ataques.',
                       'exclusions': 'Word of Wind deve ser reservado para puxões difíceis ou chefes de área.',
                       'filename': 'chanter_ability_macro_preset2.txt',
                       'id': 'macro-chanter-auto',
                       'preset_name': 'Preset 2',
                       'preset_number': 2,
                       'shortcut': 'Alt + 5',
                       'skill_slots': ['Soul Strike', 'Meteor Strike', 'Mountain Fall'],
                       'title': 'Preset 2: Limpeza Rápida de Missões & Ataques em Arco',
                       'weaving_info': 'Maximiza o cancelamento de animação das batidas de báculo para abates '
                                       'rápidos.'},
                   {   'badge_color': 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30',
                       'category': 'buff',
                       'category_label': 'Escudo & Suporte',
                       'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                       'Classe: Chanter\n'
                                       'Preset: Preset 3 (Alt + 6) - Barreira de Grupo & Suporte\n'
                                       'Local no Jogo: Menu K -> Ability-Macro\n'
                                       '\n'
                                       'SLOTS DE HABILIDADES:\n'
                                       'Slot 1: Shield of Protection (Escudo Absorvente de Grupo)\n'
                                       'Slot 2: Healing Conduit (Cura Ativa em Cone)\n'
                                       'Slot 3: Soul Strike\n'
                                       'Slot 4: Protective Ward (Barreira de Emergência)\n'
                                       '\n'
                                       'CONFIGURAÇÃO DE DELAY: 10 ms',
                       'delay_ms': 10,
                       'description': 'Cria um escudo sagrado de absorção para toda a party com Shield of Protection e '
                                      'canaliza pulsos de cura com Healing Conduit.',
                       'exclusions': 'Não use Protective Ward desnecessariamente devido ao seu longo tempo de recarga.',
                       'filename': 'chanter_ability_macro_preset3.txt',
                       'id': 'macro-chanter-buff',
                       'preset_name': 'Preset 3',
                       'preset_number': 3,
                       'shortcut': 'Alt + 6',
                       'skill_slots': ['Shield of Protection', 'Healing Conduit', 'Soul Strike', 'Protective Ward'],
                       'title': 'Preset 3: Barreira de Proteção & Suporte de Emergência',
                       'weaving_info': 'Mitiga danos catastróficos aliviando a sobrecarga do Cleric do grupo.'}],
    'cleric': [   {   'badge_color': 'bg-rose-500/20 text-rose-300 border-rose-500/30',
                      'category': 'boss',
                      'category_label': 'Boss & Dungeons (Cura)',
                      'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                      'Classe: Cleric\n'
                                      'Preset: Preset 1 (Alt + 4) - Cura de Emergência no Tank & Grupo\n'
                                      'Local no Jogo: Pressione K (Skills) -> Ability-Macro\n'
                                      'Tecla de Acesso: Settings -> Key Settings -> General -> Gameplay -> '
                                      'Ability-Macro\n'
                                      '\n'
                                      'SLOTS DE HABILIDADES CONFIGURADOS:\n'
                                      'Slot 1: Flash of Recovery (Cura Crítica Instantânea sem Cast)\n'
                                      'Slot 2: Healing Light (Cura de Sustentação Rápida)\n'
                                      'Slot 3: Splendor of Recovery (Cura em Área Massiva para o Grupo)\n'
                                      'Slot 4: Splendor of Rebirth (Escudo Absorvente & Regeneração)\n'
                                      '\n'
                                      'CONFIGURAÇÃO DE DELAY: 15 ms por slot\n'
                                      'MODO DE USO EM COMBATE:\n'
                                      'Com o aliado em mira, segure a tecla do macro para estabilizar as barras de HP '
                                      'imediatamente sem travamento de conjuração.',
                      'delay_ms': 15,
                      'description': 'Dispara Flash of Recovery instantâneo para salvar o Tank de picos de dano, '
                                     'emendando curas de sustentação e bênçãos de regeneração contínua.',
                      'exclusions': 'A postura Benevolence deve ser mantida ativa permanentemente (não colocar no loop '
                                    'contínuo do macro).',
                      'filename': 'cleric_ability_macro_preset1.txt',
                      'id': 'macro-cleric-boss',
                      'preset_name': 'Preset 1',
                      'preset_number': 1,
                      'shortcut': 'Alt + 4',
                      'skill_slots': [   'Flash of Recovery',
                                         'Healing Light',
                                         'Splendor of Recovery',
                                         'Splendor of Rebirth'],
                      'title': 'Preset 1: Cura de Emergência no Tank & Grupo',
                      'weaving_info': 'Segure a tecla do Ability-Macro com o Main Tank na mira. O sistema prioriza as '
                                      'curas fora de recarga, intercalando bênçãos e barreiras instantâneas.'},
                  {   'badge_color': 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
                      'category': 'auto',
                      'category_label': 'Solo & Leveling',
                      'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                      'Classe: Cleric\n'
                                      'Preset: Preset 2 (Alt + 5) - Leveling Solo & Punição Sagrada\n'
                                      'Local no Jogo: Menu K -> Ability-Macro\n'
                                      '\n'
                                      'SLOTS DE HABILIDADES:\n'
                                      'Slot 1: Root (Imobilização)\n'
                                      'Slot 2: Thorny Vine (Dano Contínuo Sagrado)\n'
                                      'Slot 3: Holy Wrath (Punição Divina)\n'
                                      'Slot 4: Smite (Golpe de Maça)\n'
                                      '\n'
                                      'CONFIGURAÇÃO DE DELAY: 10 ms',
                      'delay_ms': 10,
                      'description': 'Imobiliza alvos com Root e desfere punições sagradas com martelo e magias de luz '
                                     'para cumprir missões e farmar com velocidade.',
                      'exclusions': 'Mantenha um olho na sua própria vida e mude para o Preset 1 caso sofra dano '
                                    'inesperado.',
                      'filename': 'cleric_ability_macro_preset2.txt',
                      'id': 'macro-cleric-auto',
                      'preset_name': 'Preset 2',
                      'preset_number': 2,
                      'shortcut': 'Alt + 5',
                      'skill_slots': ['Root', 'Thorny Vine', 'Holy Wrath', 'Smite'],
                      'title': 'Preset 2: Leveling Solo & Punição Sagrada Ofensiva',
                      'weaving_info': 'Entrelaça ataques corpo a corpo com a maça e escudo entre cada punição divina.'},
                  {   'badge_color': 'bg-amber-500/20 text-amber-300 border-amber-500/30',
                      'category': 'buff',
                      'category_label': 'Purificação & Suporte',
                      'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                      'Classe: Cleric\n'
                                      'Preset: Preset 3 (Alt + 6) - Purificação em Massa & Suporte\n'
                                      'Local no Jogo: Menu K -> Ability-Macro\n'
                                      '\n'
                                      'SLOTS DE HABILIDADES:\n'
                                      'Slot 1: Ripple of Purification (Cleanse em Área de Todo o Grupo)\n'
                                      'Slot 2: Flash of Recovery\n'
                                      "Slot 3: Yustiel's Light (Regeneração Sagrada Contínua)\n"
                                      '\n'
                                      'CONFIGURAÇÃO DE DELAY: 15 ms',
                      'delay_ms': 15,
                      'description': 'Limpa venenos e debuffs de todos os aliados com Ripple of Purification e aciona '
                                     "Yustiel's Light para regenerar o grupo.",
                      'exclusions': 'Rebirth e Hand of Reincarnation devem ser aplicados antes do início dos combates '
                                    'difíceis.',
                      'filename': 'cleric_ability_macro_preset3.txt',
                      'id': 'macro-cleric-buff',
                      'preset_name': 'Preset 3',
                      'preset_number': 3,
                      'shortcut': 'Alt + 6',
                      'skill_slots': ['Ripple of Purification', 'Flash of Recovery', "Yustiel's Light"],
                      'title': 'Preset 3: Purificação em Massa (Cleanse) & Suporte',
                      'weaving_info': 'Salva o esquadrão em momentos com mecânicas de veneno em área ou sangramento de '
                                      'chefes.'}],
    'elementalist': [   {   'badge_color': 'bg-rose-500/20 text-rose-300 border-rose-500/30',
                            'category': 'boss',
                            'category_label': 'Boss & Dungeons',
                            'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                            'Classe: Elementalist (Spiritmaster)\n'
                                            'Preset: Preset 1 (Alt + 4) - Boss Sustained DPS & DoTs\n'
                                            'Local no Jogo: Pressione K (Skills) -> Ability-Macro\n'
                                            'Tecla de Acesso: Settings -> Key Settings -> General -> Gameplay -> '
                                            'Ability-Macro\n'
                                            '\n'
                                            'SLOTS DE HABILIDADES CONFIGURADOS:\n'
                                            'Slot 1: Ignite Aether (Dispel & Dano por Buff)\n'
                                            'Slot 2: Curse Cloud (Nuvem Corrosiva de Alto Dano)\n'
                                            'Slot 3: Spirit Burn (Ataque de Fogo do Pet)\n'
                                            'Slot 4: Erosion Curse (Dano Contínuo & Dreno)\n'
                                            '\n'
                                            'CONFIGURAÇÃO DE DELAY: 15 ms por slot\n'
                                            'MODO DE USO EM COMBATE:\n'
                                            'Segure a tecla do Ability-Macro para manter as maldições ativas '
                                            'ininterruptamente.',
                            'delay_ms': 15,
                            'description': 'Destrói proteções com Ignite Aether, derrete o chefe com a nuvem corrosiva '
                                           'Curse Cloud e comanda o pet elemental com Spirit Burn.',
                            'exclusions': 'A invocação e o buff Armor Spirit do pet devem ser ativados antes de '
                                          'iniciar o combate.',
                            'filename': 'elementalist_ability_macro_preset1.txt',
                            'id': 'macro-elementalist-boss',
                            'preset_name': 'Preset 1',
                            'preset_number': 1,
                            'shortcut': 'Alt + 4',
                            'skill_slots': ['Ignite Aether', 'Curse Cloud', 'Spirit Burn', 'Erosion Curse'],
                            'title': 'Preset 1: Boss Sustained DPS & Queima de Éter',
                            'weaving_info': 'Segure a tecla do Ability-Macro. O invocador mantém os DoTs 100% ativos '
                                            'enquanto o espírito elemental desfere ataques corpo a corpo constantes.'},
                        {   'badge_color': 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
                            'category': 'auto',
                            'category_label': 'AoE & Controle',
                            'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                            'Classe: Elementalist (Spiritmaster)\n'
                                            'Preset: Preset 2 (Alt + 5) - Controle & AoE\n'
                                            'Local no Jogo: Menu K -> Ability-Macro\n'
                                            '\n'
                                            'SLOTS DE HABILIDADES:\n'
                                            'Slot 1: Body Root (Enraizamento de 8s)\n'
                                            'Slot 2: Spirit Burn (Ataque em Área do Espírito)\n'
                                            'Slot 3: Curse Cloud\n'
                                            'Slot 4: Erosion Curse\n'
                                            '\n'
                                            'CONFIGURAÇÃO DE DELAY: 15 ms',
                            'delay_ms': 15,
                            'description': 'Enraíza monstros com Body Root enquanto o espírito elemental incendeia a '
                                           'área com chamas contínuas.',
                            'exclusions': 'Não usar Fear Shriek em dungeons aleatórias para evitar atrair monstros '
                                          'indesejados.',
                            'filename': 'elementalist_ability_macro_preset2.txt',
                            'id': 'macro-elementalist-auto',
                            'preset_name': 'Preset 2',
                            'preset_number': 2,
                            'shortcut': 'Alt + 5',
                            'skill_slots': ['Body Root', 'Spirit Burn', 'Curse Cloud', 'Erosion Curse'],
                            'title': 'Preset 2: Controle de Campo & Queimadura em Área',
                            'weaving_info': 'Impede que os inimigos alcancem o invocador, facilitando o farm solo.'},
                        {   'badge_color': 'bg-teal-500/20 text-teal-300 border-teal-500/30',
                            'category': 'buff',
                            'category_label': 'Suporte & Sobrevivência',
                            'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                            'Classe: Elementalist (Spiritmaster)\n'
                                            'Preset: Preset 3 (Alt + 6) - Barreira & Substituição\n'
                                            'Local no Jogo: Menu K -> Ability-Macro\n'
                                            '\n'
                                            'SLOTS DE HABILIDADES:\n'
                                            'Slot 1: Spirit Wall of Protection (Barreira para o Grupo)\n'
                                            'Slot 2: Spirit Substitution (Transfere Dano para o Pet)\n'
                                            'Slot 3: Ignite Aether\n'
                                            '\n'
                                            'CONFIGURAÇÃO DE DELAY: 15 ms',
                            'delay_ms': 15,
                            'description': 'Ergue a muralha protetora para o grupo e transfere 100% do dano sofrido '
                                           'pelo conjurador para o espírito elemental.',
                            'exclusions': 'Monitore a vida do espírito para não deixá-lo morrer enquanto Substitution '
                                          'estiver ativo.',
                            'filename': 'elementalist_ability_macro_preset3.txt',
                            'id': 'macro-elementalist-buff',
                            'preset_name': 'Preset 3',
                            'preset_number': 3,
                            'shortcut': 'Alt + 6',
                            'skill_slots': ['Spirit Wall of Protection', 'Spirit Substitution', 'Ignite Aether'],
                            'title': 'Preset 3: Barreira Elemental & Proteção de Grupo',
                            'weaving_info': 'Salva o invocador de rajadas fatais através do sacrifício de vida do '
                                            'espírito.'}],
    'gladiator': [   {   'badge_color': 'bg-rose-500/20 text-rose-300 border-rose-500/30',
                         'category': 'boss',
                         'category_label': 'Boss & Masmorras',
                         'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                         'Classe: Gladiator\n'
                                         'Preset: Preset 1 (Alt + 4) - Boss Encounter & Burst DPS\n'
                                         "Local no Jogo: Pressione K (Skills) -> Clique em 'Ability-Macro' (canto "
                                         'superior direito)\n'
                                         'Tecla de Acesso: Settings -> Key Settings -> General -> Gameplay -> '
                                         'Ability-Macro\n'
                                         '\n'
                                         'SLOTS DE HABILIDADES CONFIGURADOS:\n'
                                         'Slot 1: Armor Murder (Quebra de Defesa)\n'
                                         'Slot 2: Ferocious Strike (Derrubada / Knockdown)\n'
                                         'Slot 3: Severe Precision Cut (Finalizador Crítico)\n'
                                         'Slot 4: Draining Blow (Sustain & Dano)\n'
                                         '\n'
                                         'CONFIGURAÇÃO DE DELAY: 10 ms (0.010s) por slot\n'
                                         'MODO DE USO EM COMBATE:\n'
                                         'Segure a tecla configurada do Ability-Macro. O jogo dispara as habilidades '
                                         'na ordem assim que saírem de recarga e executa o weaving de auto-ataques de '
                                         'Greatsword automaticamente para maximizar o DPS. Solte a tecla para parar '
                                         'instantaneamente.',
                         'delay_ms': 10,
                         'description': 'Quebra as defesas do chefe com Armor Murder, engaja com Ferocious Strike para '
                                        'provocar derrubada (Knockdown) e desfere os golpes de alto dano crítico '
                                        'Severe Precision Cut e Draining Blow.',
                         'exclusions': 'Não adicionar Berserking ou Dauntless Charge neste preset; ative Berserking '
                                       'manualmente antes do pull.',
                         'filename': 'gladiator_ability_macro_preset1.txt',
                         'id': 'macro-gladiator-boss',
                         'preset_name': 'Preset 1',
                         'preset_number': 1,
                         'shortcut': 'Alt + 4',
                         'skill_slots': ['Armor Murder', 'Ferocious Strike', 'Severe Precision Cut', 'Draining Blow'],
                         'title': 'Preset 1: Boss Encounter & Burst DPS (Single Target)',
                         'weaving_info': 'Segure a tecla do Ability-Macro. O jogo executa a sequência prioritária e '
                                         'intercala ataques básicos automáticos (weaving) de Greatsword com '
                                         'cancelamento de animação.'},
                     {   'badge_color': 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
                         'category': 'auto',
                         'category_label': 'AoE & Limpeza',
                         'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                         'Classe: Gladiator\n'
                                         'Preset: Preset 2 (Alt + 5) - AoE & Limpeza de Masmorras\n'
                                         'Local no Jogo: Menu K (Skills) -> Ability-Macro\n'
                                         'Tecla de Acesso: Settings -> Key Settings -> General -> Gameplay -> '
                                         'Ability-Macro\n'
                                         '\n'
                                         'SLOTS DE HABILIDADES CONFIGURADOS:\n'
                                         'Slot 1: Dauntless Charge (Aproximação & Stun)\n'
                                         'Slot 2: Whirlwind Strike (Dano em Área 360°)\n'
                                         'Slot 3: Ferocious Strike (Knockdown)\n'
                                         'Slot 4: Severe Precision Cut (Finalizador)\n'
                                         '\n'
                                         'CONFIGURAÇÃO DE DELAY: 10 ms\n'
                                         'MODO DE USO EM COMBATE:\n'
                                         'Segure a tecla do macro para avançar e girar limpando ondas de monstros '
                                         'automaticamente.',
                         'delay_ms': 10,
                         'description': 'Avança com investida, gira com o corte em área Whirlwind Strike e conecta '
                                        'combos rápidos para varrer hordas de monstros em Sealed Dungeons e tarefas '
                                        'diárias.',
                         'exclusions': 'Evite acionar em áreas de patrulha com múltiplos chefes para não puxar aggro '
                                       'indesejado.',
                         'filename': 'gladiator_ability_macro_preset2.txt',
                         'id': 'macro-gladiator-auto',
                         'preset_name': 'Preset 2',
                         'preset_number': 2,
                         'shortcut': 'Alt + 5',
                         'skill_slots': [   'Dauntless Charge',
                                            'Whirlwind Strike',
                                            'Ferocious Strike',
                                            'Severe Precision Cut'],
                         'title': 'Preset 2: Limpeza AoE de Masmorras & Expedições',
                         'weaving_info': 'Executa dano em área contínuo em 360 graus entrelaçando auto-ataques em '
                                         'arco.'},
                     {   'badge_color': 'bg-amber-500/20 text-amber-300 border-amber-500/30',
                         'category': 'buff',
                         'category_label': 'Defensivo & Sobrevivência',
                         'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                         'Classe: Gladiator\n'
                                         'Preset: Preset 3 (Alt + 6) - Sobrevivência & Off-Tank\n'
                                         'Local no Jogo: Menu K (Skills) -> Ability-Macro\n'
                                         'Tecla de Acesso: Settings -> Key Settings -> General -> Gameplay -> '
                                         'Ability-Macro\n'
                                         '\n'
                                         'SLOTS DE HABILIDADES CONFIGURADOS:\n'
                                         'Slot 1: Armor Murder\n'
                                         'Slot 2: Tendonslice (Controle & Lentidão)\n'
                                         'Slot 3: Draining Blow (Cura Vampírica)\n'
                                         'Slot 4: Ferocious Strike\n'
                                         '\n'
                                         'CONFIGURAÇÃO DE DELAY: 10 ms\n'
                                         'MODO DE USO EM COMBATE:\n'
                                         'Utilize este preset segurando a tecla quando a vida cair ou estiver '
                                         'segurando múltiplos inimigos.',
                         'delay_ms': 10,
                         'description': 'Aciona redução de velocidade no alvo com Tendonslice, conecta Draining Blow '
                                        'para recuperar pontos de vida e sustenta o combate contra elites de alto '
                                        'dano.',
                         'exclusions': 'Second Wind deve ser ativado manualmente nos momentos críticos de queda de HP.',
                         'filename': 'gladiator_ability_macro_preset3.txt',
                         'id': 'macro-gladiator-buff',
                         'preset_name': 'Preset 3',
                         'preset_number': 3,
                         'shortcut': 'Alt + 6',
                         'skill_slots': ['Armor Murder', 'Tendonslice', 'Draining Blow', 'Ferocious Strike'],
                         'title': 'Preset 3: Sobrevivência de Emergência & Off-Tank',
                         'weaving_info': 'Mantém pressão defensiva constante sem interromper a geração de vida por '
                                         'golpe.'}],
    'ranger': [   {   'badge_color': 'bg-rose-500/20 text-rose-300 border-rose-500/30',
                      'category': 'boss',
                      'category_label': 'Boss & Dungeons',
                      'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                      'Classe: Ranger\n'
                                      'Preset: Preset 1 (Alt + 4) - Boss Single Target & Disparo Perfurante\n'
                                      'Local no Jogo: Pressione K (Skills) -> Ability-Macro\n'
                                      'Tecla de Acesso: Settings -> Key Settings -> General -> Gameplay -> '
                                      'Ability-Macro\n'
                                      '\n'
                                      'SLOTS DE HABILIDADES CONFIGURADOS:\n'
                                      'Slot 1: Spiral Arrow (Perfuração de Armadura)\n'
                                      'Slot 2: Sharpshooter Aim (Precisão & Crítico)\n'
                                      'Slot 3: Gale Arrow (Rajada Rápida de 3 Flechas)\n'
                                      'Slot 4: Power Shot (Disparo Pesado)\n'
                                      '\n'
                                      'CONFIGURAÇÃO DE DELAY: 10 ms por slot\n'
                                      'MODO DE USO EM COMBATE:\n'
                                      'Segure a tecla configurada do Ability-Macro para metralhar flechas com kiting '
                                      'fluido a até 25 metros de distância do chefe.',
                      'delay_ms': 10,
                      'description': 'Ignora 30% da armadura do chefe com Spiral Arrow e metralha flechas velozes com '
                                     'Gale Arrow e Power Shot a distância segura.',
                      'exclusions': 'Mau Form deve ser ativada manualmente como buff de explosão de 45 segundos.',
                      'filename': 'ranger_ability_macro_preset1.txt',
                      'id': 'macro-ranger-boss',
                      'preset_name': 'Preset 1',
                      'preset_number': 1,
                      'shortcut': 'Alt + 4',
                      'skill_slots': ['Spiral Arrow', 'Sharpshooter Aim', 'Gale Arrow', 'Power Shot'],
                      'title': 'Preset 1: Boss Single Target & Disparo Perfurante',
                      'weaving_info': 'Segure a tecla do Ability-Macro enquanto se move lateralmente. O jogo executa '
                                      'auto-shots com o arco longo entre cada habilidade sem desacelerar o passo.'},
                  {   'badge_color': 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
                      'category': 'auto',
                      'category_label': 'AoE & Limpeza',
                      'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                      'Classe: Ranger\n'
                                      'Preset: Preset 2 (Alt + 5) - Chuva de Flechas AoE\n'
                                      'Local no Jogo: Menu K -> Ability-Macro\n'
                                      '\n'
                                      'SLOTS DE HABILIDADES:\n'
                                      'Slot 1: Arrow Deluge (Chuva de Flechas Contínua)\n'
                                      'Slot 2: Spiral Arrow\n'
                                      'Slot 3: Gale Arrow\n'
                                      '\n'
                                      'CONFIGURAÇÃO DE DELAY: 10 ms',
                      'delay_ms': 10,
                      'description': 'Despeja Arrow Deluge sobre múltiplos alvos e finaliza inimigos enfraquecidos com '
                                     'disparos perfurantes em cadeia.',
                      'exclusions': 'Não use próximo a alvos com efeitos de Sleep ativos para não quebrar o controle.',
                      'filename': 'ranger_ability_macro_preset2.txt',
                      'id': 'macro-ranger-auto',
                      'preset_name': 'Preset 2',
                      'preset_number': 2,
                      'shortcut': 'Alt + 5',
                      'skill_slots': ['Arrow Deluge', 'Spiral Arrow', 'Gale Arrow'],
                      'title': 'Preset 2: Chuva de Flechas AoE & Limpeza de Hordas',
                      'weaving_info': 'Excelente para varrer pacotes de monstros em expedições e masmorras sem sofrer '
                                      'dano corpo a corpo.'},
                  {   'badge_color': 'bg-teal-500/20 text-teal-300 border-teal-500/30',
                      'category': 'buff',
                      'category_label': 'Kiting & Sobrevivência',
                      'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                      'Classe: Ranger\n'
                                      'Preset: Preset 3 (Alt + 6) - Desengajamento Tático & Kiting\n'
                                      'Local no Jogo: Menu K -> Ability-Macro\n'
                                      '\n'
                                      'SLOTS DE HABILIDADES:\n'
                                      'Slot 1: Silence Arrow (Silêncio de 6s)\n'
                                      'Slot 2: Entangling Shot (Lentidão de 60%)\n'
                                      'Slot 3: Retreating Slash (Salto de 10m para trás)\n'
                                      'Slot 4: Gale Arrow\n'
                                      '\n'
                                      'CONFIGURAÇÃO DE DELAY: 10 ms',
                      'delay_ms': 10,
                      'description': 'Silencia conjuradores com Silence Arrow, reduz velocidade de guerreiros com '
                                     'Entangling Shot e salta para trás mantendo distância segura.',
                      'exclusions': 'Armadilhas de sono (Sleep Trap) devem ser plantadas manualmente no chão antes do '
                                    'combate.',
                      'filename': 'ranger_ability_macro_preset3.txt',
                      'id': 'macro-ranger-buff',
                      'preset_name': 'Preset 3',
                      'preset_number': 3,
                      'shortcut': 'Alt + 6',
                      'skill_slots': ['Silence Arrow', 'Entangling Shot', 'Retreating Slash', 'Gale Arrow'],
                      'title': 'Preset 3: Desengajamento Tático & Kiting em PvP',
                      'weaving_info': 'Permite disparar em movimento contínuo criando espaço contra Gladiators e '
                                      'Assassins.'}],
    'sorcerer': [   {   'badge_color': 'bg-rose-500/20 text-rose-300 border-rose-500/30',
                        'category': 'boss',
                        'category_label': 'Boss & Dungeons',
                        'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                        'Classe: Sorcerer\n'
                                        'Preset: Preset 1 (Alt + 4) - Boss Burst Elemental\n'
                                        'Local no Jogo: Pressione K (Skills) -> Ability-Macro\n'
                                        'Tecla de Acesso: Settings -> Key Settings -> General -> Gameplay -> '
                                        'Ability-Macro\n'
                                        '\n'
                                        'SLOTS DE HABILIDADES CONFIGURADOS:\n'
                                        'Slot 1: Ice Chain (Lentidão & Abertura)\n'
                                        'Slot 2: Freezing Wind (Combo Instantâneo de Gelo)\n'
                                        'Slot 3: Flame Spray (Dano Pesado de Fogo)\n'
                                        'Slot 4: Aetheric Spellburst (Recuperação de MP)\n'
                                        '\n'
                                        'CONFIGURAÇÃO DE DELAY: 15 ms por slot\n'
                                        'MODO DE USO EM COMBATE:\n'
                                        'Segure a tecla do Ability-Macro para alternar entre as magias instantâneas e '
                                        'rajadas de fogo sem perda de tempo de conjuração.',
                        'delay_ms': 15,
                        'description': 'Aplica lentidão com Ice Chain, ativa o combo veloz Freezing Wind, desfere '
                                       'Flame Spray e consome éter com Aetheric Spellburst para manter mana alta.',
                        'exclusions': 'Glacial Shard e Big Magma Eruption possuem tempos de canalização longos e devem '
                                      'ser conjurados manualmente após acionar Boon of Quickness.',
                        'filename': 'sorcerer_ability_macro_preset1.txt',
                        'id': 'macro-sorcerer-boss',
                        'preset_name': 'Preset 1',
                        'preset_number': 1,
                        'shortcut': 'Alt + 4',
                        'skill_slots': ['Ice Chain', 'Freezing Wind', 'Flame Spray', 'Aetheric Spellburst'],
                        'title': 'Preset 1: Boss Burst Elemental & Dano Mágico Pesado',
                        'weaving_info': 'Segure a tecla do Ability-Macro. O sistema gerencia as recargas mágicas '
                                        'automaticamente, disparando ataques leves de orbe entre conjurações '
                                        'instantâneas.'},
                    {   'badge_color': 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
                        'category': 'auto',
                        'category_label': 'AoE & Masmorras',
                        'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                        'Classe: Sorcerer\n'
                                        'Preset: Preset 2 (Alt + 5) - Erupção AoE de Fogo\n'
                                        'Local no Jogo: Menu K -> Ability-Macro\n'
                                        '\n'
                                        'SLOTS DE HABILIDADES:\n'
                                        'Slot 1: Flame Spray\n'
                                        'Slot 2: Big Magma Eruption (Explosão AoE)\n'
                                        'Slot 3: Ice Chain\n'
                                        'Slot 4: Freezing Wind\n'
                                        '\n'
                                        'CONFIGURAÇÃO DE DELAY: 15 ms',
                        'delay_ms': 15,
                        'description': 'Lança erupções de fogo contínuas e rajadas geladas para pulverizar grupos de '
                                       'monstros em Sealed Dungeons.',
                        'exclusions': 'Fique atento ao aggro gerado pelo dano em massa para não roubar o monstro do '
                                      'Templar.',
                        'filename': 'sorcerer_ability_macro_preset2.txt',
                        'id': 'macro-sorcerer-auto',
                        'preset_name': 'Preset 2',
                        'preset_number': 2,
                        'shortcut': 'Alt + 5',
                        'skill_slots': ['Flame Spray', 'Big Magma Eruption', 'Ice Chain', 'Freezing Wind'],
                        'title': 'Preset 2: Erupção AoE de Fogo & Limpeza em Área',
                        'weaving_info': 'Garante o maior dano por segundo em área contra múltiplos alvos.'},
                    {   'badge_color': 'bg-amber-500/20 text-amber-300 border-amber-500/30',
                        'category': 'buff',
                        'category_label': 'Defensivo & Sobrevivência',
                        'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                        'Classe: Sorcerer\n'
                                        'Preset: Preset 3 (Alt + 6) - Barreira Defensiva Arcana\n'
                                        'Local no Jogo: Menu K -> Ability-Macro\n'
                                        '\n'
                                        'SLOTS DE HABILIDADES:\n'
                                        'Slot 1: Stone Skin (Barreira de 3000 Dano)\n'
                                        'Slot 2: Frost Barrier (Reflexão & Cura)\n'
                                        'Slot 3: Ice Chain\n'
                                        'Slot 4: Flame Spray\n'
                                        '\n'
                                        'CONFIGURAÇÃO DE DELAY: 15 ms',
                        'delay_ms': 15,
                        'description': 'Aciona barreira de éter com Stone Skin e Frost Barrier para resistir a '
                                       'investidas surpresa de assassinos.',
                        'exclusions': 'Curse of Tree e Sleeping Storm devem ser disparados manualmente no alvo certo.',
                        'filename': 'sorcerer_ability_macro_preset3.txt',
                        'id': 'macro-sorcerer-buff',
                        'preset_name': 'Preset 3',
                        'preset_number': 3,
                        'shortcut': 'Alt + 6',
                        'skill_slots': ['Stone Skin', 'Frost Barrier', 'Ice Chain', 'Flame Spray'],
                        'title': 'Preset 3: Barreira Defensiva & Sobrevivência Arcana',
                        'weaving_info': 'Protege a vida frágil de tecido enquanto retalia com feitiços defensivos.'}],
    'templar': [   {   'badge_color': 'bg-rose-500/20 text-rose-300 border-rose-500/30',
                       'category': 'boss',
                       'category_label': 'Boss & Dungeons',
                       'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                       'Classe: Templar\n'
                                       'Preset: Preset 1 (Alt + 4) - Boss Tanking & Aggro Travado\n'
                                       'Local no Jogo: Pressione K (Skills) -> Ability-Macro\n'
                                       'Tecla de Acesso: Settings -> Key Settings -> General -> Gameplay -> '
                                       'Ability-Macro\n'
                                       '\n'
                                       'SLOTS DE HABILIDADES CONFIGURADOS:\n'
                                       'Slot 1: Shield Charge (Engajamento Inicial)\n'
                                       'Slot 2: Incite Rage (Taunt em Área & Aggro Máximo)\n'
                                       'Slot 3: Taunt Strike (Manutenção de Foco)\n'
                                       'Slot 4: Righteous Punishment (Debuff de Ataque Inimigo)\n'
                                       'Slot 5: Shield Burst (Atordoamento & Interrupção)\n'
                                       '\n'
                                       'CONFIGURAÇÃO DE DELAY: 10 ms por slot\n'
                                       'MODO DE USO EM COMBATE:\n'
                                       'Segure a tecla do Ability-Macro para manter o foco total do chefe no Templar, '
                                       'intercalando golpes e bloqueios de escudo automaticamente.',
                       'delay_ms': 10,
                       'description': 'Avanço de escudo seguido de Incite Rage para consolidar Threat absoluto, debuff '
                                      'de dano com Righteous Punishment e atordoamento com Shield Burst.',
                       'exclusions': 'Iron Skin e Empyrean Armor devem ser guardados para as fases de mecânicas letais '
                                     'do chefe.',
                       'filename': 'templar_ability_macro_preset1.txt',
                       'id': 'macro-templar-boss',
                       'preset_name': 'Preset 1',
                       'preset_number': 1,
                       'shortcut': 'Alt + 4',
                       'skill_slots': [   'Shield Charge',
                                          'Incite Rage',
                                          'Taunt Strike',
                                          'Righteous Punishment',
                                          'Shield Burst'],
                       'title': 'Preset 1: Boss Tanking & Travamento de Aggro Absoluto',
                       'weaving_info': 'Segure a tecla do Ability-Macro. O jogo desfere ataques de espada e escudo '
                                       'entre cada golpe, garantindo bloqueios ativos e máxima geração de threat por '
                                       'segundo.'},
                   {   'badge_color': 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30',
                       'category': 'auto',
                       'category_label': 'AoE & Puxões',
                       'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                       'Classe: Templar\n'
                                       'Preset: Preset 2 (Alt + 5) - Puxão AoE & Limpeza de Masmorras\n'
                                       'Local no Jogo: Menu K -> Ability-Macro\n'
                                       '\n'
                                       'SLOTS DE HABILIDADES:\n'
                                       'Slot 1: Doom Lure (Corrente de Puxão a 16m)\n'
                                       'Slot 2: Shield Counter (Contra-ataque de Escudo)\n'
                                       'Slot 3: Taunt Strike\n'
                                       'Slot 4: Shield Burst\n'
                                       '\n'
                                       'CONFIGURAÇÃO DE DELAY: 10 ms\n'
                                       'Segure a tecla do macro para puxar e trancar os monstros ao alcance corpo a '
                                       'corpo.',
                       'delay_ms': 10,
                       'description': 'Puxa conjuradores distantes com a corrente etérea Doom Lure a 16m e esmaga o '
                                      'grupo de monstros com contra-ataques brutais de escudo.',
                       'exclusions': 'Não usar Doom Lure em alvos com imunidade a puxões.',
                       'filename': 'templar_ability_macro_preset2.txt',
                       'id': 'macro-templar-auto',
                       'preset_name': 'Preset 2',
                       'preset_number': 2,
                       'shortcut': 'Alt + 5',
                       'skill_slots': ['Doom Lure', 'Shield Counter', 'Taunt Strike', 'Shield Burst'],
                       'title': 'Preset 2: Puxão de Grupos (Pull AoE) & Masmorras',
                       'weaving_info': 'Garante que o grupo de inimigos fique compactado facilitando o dano dos '
                                       'conjuradores aliados.'},
                   {   'badge_color': 'bg-sky-500/20 text-sky-300 border-sky-500/30',
                       'category': 'buff',
                       'category_label': 'Muralha Sagrada',
                       'commands_raw': '=== AION 2 OFFICIAL IN-GAME ABILITY-MACRO ===\n'
                                       'Classe: Templar\n'
                                       'Preset: Preset 3 (Alt + 6) - Postura de Escudo Inabalável\n'
                                       'Local no Jogo: Menu K -> Ability-Macro\n'
                                       '\n'
                                       'SLOTS DE HABILIDADES:\n'
                                       'Slot 1: Shield Counter\n'
                                       'Slot 2: Righteous Punishment\n'
                                       'Slot 3: Taunt Strike\n'
                                       '\n'
                                       'CONFIGURAÇÃO DE DELAY: 10 ms',
                       'delay_ms': 10,
                       'description': 'Prioriza contra-golpes defensivos rápidos e sustentação de vida constante com '
                                      'Taunt Strike durante rajadas de dano extremo.',
                       'exclusions': 'Ative Bodyguard e Iron Skin manualmente conforme as instruções do grupo.',
                       'filename': 'templar_ability_macro_preset3.txt',
                       'id': 'macro-templar-buff',
                       'preset_name': 'Preset 3',
                       'preset_number': 3,
                       'shortcut': 'Alt + 6',
                       'skill_slots': ['Shield Counter', 'Righteous Punishment', 'Taunt Strike'],
                       'title': 'Preset 3: Postura de Escudo Inabalável (Defesa Máxima)',
                       'weaving_info': 'Prioriza a prontidão de bloqueio com escudo para ativação instantânea de '
                                       'contra-ataques.'}]}


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
