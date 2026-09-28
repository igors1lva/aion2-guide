/**
 * planner.js - Mecânica interativa do Planejador de Builds de Aion 2
 * Baseado no Daevanion Planner com dados comunitários.
 */

document.addEventListener('DOMContentLoaded', () => {
    initBuildPlanner();
});

function initBuildPlanner() {
    // Dados completos das 8 classes, nós de Daevanion e catálogo de Stigmas
    const plannerDatabase = {
        gladiator: {
            name: "Gladiator",
            role: "Tank / Melee DPS",
            roleDetail: "Melee DPS & Off-Tank (Greatsword)",
            nodes: [
                { id: "g1", tier: 1, name: "Força Bruta I", color: "white", cost: 3, stats: { attack: 35, hp: 180, crit: 10, def: 15 }, desc: "+35 Physical Attack, +180 Max HP" },
                { id: "g2", tier: 1, name: "Resistência de Placas", color: "white", cost: 3, stats: { attack: 0, hp: 320, crit: 0, def: 45 }, desc: "+320 Max HP, +45 Physical Defense" },
                { id: "g3", tier: 1, name: "Passo Pesado", color: "green", cost: 4, stats: { attack: 15, hp: 0, crit: 15, def: 0 }, perk: "Redução de 6% no recuo sofrido por atordoamentos", desc: "Passiva de estabilidade contra controle de grupo" },
                { id: "g4", tier: 2, name: "Golpe Dilacerante", color: "blue", cost: 5, stats: { attack: 45, hp: 0, crit: 25, def: 0 }, perk: "Novo combo de ataque cruzado após aparar golpes", desc: "Skill Ativa: Retaliação de Espadão" },
                { id: "g5", tier: 2, name: "Foco Destrutivo", color: "white", cost: 4, stats: { attack: 55, hp: 200, crit: 30, def: 0 }, desc: "+55 Physical Attack, +30 Physical Crit" },
                { id: "g6", tier: 2, name: "Fúria Sanguinária", color: "green", cost: 4, stats: { attack: 20, hp: 0, crit: 20, def: 0 }, perk: "+8% Attack Speed ao atingir alvos sangrando", desc: "Aceleração contínua de golpes" },
                { id: "g7", tier: 3, name: "Mestria em Derrubada", color: "blue", cost: 6, stats: { attack: 60, hp: 150, crit: 35, def: 0 }, perk: "+25% de dano bônus em alvos sob Knockdown", desc: "Amplificação de finalizações aéreas e solo" },
                { id: "g8", tier: 3, name: "Couraça Empírea", color: "white", cost: 5, stats: { attack: 0, hp: 450, crit: 0, def: 70 }, desc: "+450 Max HP, +70 Physical Defense" },
                { id: "g9", tier: 4, name: "Impacto Cataclísmico", color: "orange", cost: 8, stats: { attack: 90, hp: 400, crit: 50, def: 30 }, perk: "Severe Precision Cut reseta 50% do cooldown ao abater um inimigo", desc: "Nó Mítico Lendário: Dominância em área" },
                { id: "g10", tier: 4, name: "Fúria do Berzerker Imortal", color: "orange", cost: 8, stats: { attack: 110, hp: 250, crit: 60, def: 0 }, perk: "Ao ficar com menos de 25% de HP, ganha 30% de dano e 20% de roubo de vida por 10s", desc: "Nó Mítico Lendário: Sobrevivência explosiva" }
            ],
            stigmas: [
                { id: "st-g1", name: "Severe Precision Cut", type: "Active Burst", desc: "Golpe descendente massivo que causa dano crítico dobrado em alvos derrubados." },
                { id: "st-g2", name: "Whirlwind Strike", type: "Active AoE", desc: "Giro contínuo de 360° atingindo todos os alvos num raio de 7m com alto Aggro." },
                { id: "st-g3", name: "Ankle Snare", type: "Crowd Control", desc: "Prende os pés do alvo na terra, impedindo qualquer movimento por 8s." },
                { id: "st-g4", name: "Berserking", type: "Buff", desc: "Aumenta o Physical Attack em 80% ao custo de 20% das defesas." },
                { id: "st-g5", name: "Draining Blow", type: "Sustain", desc: "Causa dano físico e cura o Gladiator em 30% do valor infligido." },
                { id: "st-g6", name: "Armor Murder", type: "Debuff", desc: "Reduz a Physical Defense do alvo em 35% por 15 segundos." },
                { id: "st-g7", name: "Lockdown", type: "Crowd Control", desc: "Silencia habilidades físicas do adversário em combates diretos." },
                { id: "st-g8", name: "Dauntless Charge", type: "Mobility", desc: "Investida instantânea que atordoa o alvo por 1.5s e quebra escudos." },
                { id: "st-g9", name: "Second Wind", type: "Survival", desc: "Recuperação de emergência de 35% do HP total e aumento da resistência a Stun." }
            ],
            presets: {
                pve: { nodes: ["g1", "g2", "g4", "g5", "g7", "g9"], stigmas: ["st-g1", "st-g2", "st-g4", "st-g5", "st-g6", "st-g3"] },
                pvp: { nodes: ["g1", "g3", "g5", "g6", "g7", "g10"], stigmas: ["st-g1", "st-g4", "st-g7", "st-g8", "st-g9", "st-g6"] }
            }
        },
        templar: {
            name: "Templar",
            role: "Main Tank",
            roleDetail: "Main Tank (Sword & Shield)",
            nodes: [
                { id: "t1", tier: 1, name: "Bastião Sagrado I", color: "white", cost: 3, stats: { attack: 15, hp: 350, crit: 0, def: 50 }, desc: "+350 Max HP, +50 Physical Defense" },
                { id: "t2", tier: 1, name: "Postura de Bloqueio", color: "green", cost: 4, stats: { attack: 0, hp: 200, crit: 0, def: 30 }, perk: "+12% de chance de Shield Block bem-sucedido", desc: "Mitigação contínua de golpes frontais" },
                { id: "t3", tier: 2, name: "Golpe Provocador", color: "blue", cost: 5, stats: { attack: 25, hp: 250, crit: 10, def: 40 }, perk: "Ataque com o escudo que gera 150% mais Threat/Aggro", desc: "Consolidação de foco em chefes" },
                { id: "t4", tier: 2, name: "Aura Protetora", color: "white", cost: 4, stats: { attack: 0, hp: 450, crit: 0, def: 60 }, desc: "+450 Max HP, +60 Physical Defense" },
                { id: "t5", tier: 3, name: "Vontade Inabalável", color: "green", cost: 5, stats: { attack: 10, hp: 300, crit: 0, def: 40 }, perk: "Reduz em 20% o dano de ataques mágicos e em área", desc: "Resistência elementar ampliada" },
                { id: "t6", tier: 4, name: "Fortaleza Divina de Aion", color: "orange", cost: 8, stats: { attack: 40, hp: 800, crit: 0, def: 120 }, perk: "Ao ativar Iron Skin, concede 25% de barreira protetora para todos os aliados próximos", desc: "Nó Mítico Lendário: Escudo para o grupo inteiro" }
            ],
            stigmas: [
                { id: "st-t1", name: "Iron Skin", type: "Defensive", desc: "Reduz todo o dano recebido em 50% e confere imunidade total a controles por 15s." },
                { id: "st-t2", name: "Incite Rage", type: "Taunt AoE", desc: "Provoca monstros em área forçando o foco imediato no Templar." },
                { id: "st-t3", name: "Empyrean Armor", type: "Buff", desc: "Aumenta Max HP em 25% e regenera vida a cada ataque bloqueado." },
                { id: "st-t4", name: "Bodyguard", type: "Party Protect", desc: "Redireciona 70% do dano de um aliado para si mesmo durante 20s." },
                { id: "st-t5", name: "Shield Burst", type: "Active Stun", desc: "Pancada com o escudo que atordoa o chefe e cancela conjurações perigosas." },
                { id: "st-t6", name: "Righteous Punishment", type: "Debuff", desc: "Causa dano divino e reduz o poder de ataque do inimigo em 20%." },
                { id: "st-t7", name: "Doom Lure", type: "Pull CC", desc: "Puxa o inimigo com corrente mágica a até 16m de distância." },
                { id: "st-t8", name: "Shield of Faith", type: "Sustain", desc: "Cria barreira sagrada equivalente a 40% do HP por 12s." }
            ],
            presets: {
                pve: { nodes: ["t1", "t2", "t3", "t4", "t6"], stigmas: ["st-t1", "st-t2", "st-t3", "st-t4", "st-t5", "st-t6"] },
                pvp: { nodes: ["t1", "t2", "t4", "t5", "t6"], stigmas: ["st-t1", "st-t7", "st-t8", "st-t2", "st-t4", "st-t5"] }
            }
        },
        assassin: {
            name: "Assassin",
            role: "Melee DPS",
            roleDetail: "Melee DPS (Daggers & Swords)",
            nodes: [
                { id: "a1", tier: 1, name: "Precisão Silenciosa", color: "white", cost: 3, stats: { attack: 40, hp: 120, crit: 30, def: 10 }, desc: "+40 Physical Attack, +30 Critical Hit" },
                { id: "a2", tier: 1, name: "Passos Evasivos", color: "green", cost: 4, stats: { attack: 10, hp: 80, crit: 15, def: 0 }, perk: "+10% de Evasão física e velocidade em Stealth", desc: "Agilidade aprimorada nas sombras" },
                { id: "a3", tier: 2, name: "Entalhe Rúnico Veloz", color: "blue", cost: 5, stats: { attack: 55, hp: 100, crit: 35, def: 0 }, perk: "Gera 2 cargas de runas ao conectar acertos críticos", desc: "Aceleração do combo de detonação" },
                { id: "a4", tier: 2, name: "Veneno Concentrado", color: "white", cost: 4, stats: { attack: 65, hp: 0, crit: 40, def: 0 }, desc: "+65 Physical Attack, +40 Critical Hit" },
                { id: "a5", tier: 3, name: "Golpe Fatal nas Costas", color: "green", cost: 5, stats: { attack: 30, hp: 0, crit: 45, def: 0 }, perk: "+30% de Dano Crítico ao atacar alvos pelas costas (Backstab)", desc: "Amplificação de dano cirúrgico" },
                { id: "a6", tier: 4, name: "Reinício das Sombras", color: "orange", cost: 8, stats: { attack: 120, hp: 150, crit: 70, def: 15 }, perk: "Abater um inimigo reseta instantaneamente o cooldown de Shadowstep e Ambush", desc: "Nó Mítico Lendário: Eliminações em cadeia" }
            ],
            stigmas: [
                { id: "st-a1", name: "Shadowstep", type: "Gap Closer", desc: "Teleporta imediatamente atrás do alvo, garantindo 100% de crítico no próximo ataque." },
                { id: "st-a2", name: "Flurry", type: "Buff", desc: "Aumenta a velocidade de ataque em 25% por 30s acelerando os combos de adaga." },
                { id: "st-a3", name: "Quickening Gloom", type: "Burst", desc: "Aplica veneno corrosivo que explode ao acumular 5 cargas de runas." },
                { id: "st-a4", name: "Spelldodge", type: "Defensive", desc: "Esquiva com 100% de certeza das próximas 2 magias recebidas." },
                { id: "st-a5", name: "Rune Carve", type: "Active Combo", desc: "Entalha runas no corpo da vítima para preparar a explosão." },
                { id: "st-a6", name: "Rune Burst", type: "Finisher", desc: "Detona as runas causando dano massivo e atordoamento de 2s." },
                { id: "st-a7", name: "Ambush", type: "Crowd Control", desc: "Ataque furtivo que causa Stun imediato pelas costas." },
                { id: "st-a8", name: "Smoke Screen", type: "Disruption", desc: "Cega todos os inimigos em 6m por 5 segundos." }
            ],
            presets: {
                pve: { nodes: ["a1", "a3", "a4", "a5", "a6"], stigmas: ["st-a1", "st-a2", "st-a3", "st-a4", "st-a5", "st-a6"] },
                pvp: { nodes: ["a1", "a2", "a4", "a5", "a6"], stigmas: ["st-a1", "st-a7", "st-a6", "st-a4", "st-a2", "st-a8"] }
            }
        },
        ranger: {
            name: "Ranger",
            role: "Ranged DPS",
            roleDetail: "Ranged DPS (Bow & Traps)",
            nodes: [
                { id: "r1", tier: 1, name: "Olho de Águia I", color: "white", cost: 3, stats: { attack: 40, hp: 120, crit: 25, def: 10 }, desc: "+40 Physical Attack, +25 Critical Hit" },
                { id: "r2", tier: 1, name: "Kiting Ágil", color: "green", cost: 4, stats: { attack: 15, hp: 100, crit: 15, def: 0 }, perk: "+12% de velocidade de movimento ao atirar recuando", desc: "Mobilidade e posicionamento contínuos" },
                { id: "r3", tier: 2, name: "Disparo Penetrante", color: "blue", cost: 5, stats: { attack: 55, hp: 0, crit: 30, def: 0 }, perk: "Flechada perfurante que ignora 20% da armadura do chefe", desc: "Penetração de armadura avançada" },
                { id: "r4", tier: 2, name: "Aljava Rápida", color: "white", cost: 4, stats: { attack: 60, hp: 150, crit: 35, def: 0 }, desc: "+60 Physical Attack, +35 Critical Hit" },
                { id: "r5", tier: 3, name: "Engenharia de Armadilhas", color: "green", cost: 5, stats: { attack: 20, hp: 0, crit: 25, def: 0 }, perk: "Reduz o tempo de recarga de todas as Traps em 25%", desc: "Controle territorial intensificado" },
                { id: "r6", tier: 4, name: "Atirador de Elite Mítico", color: "orange", cost: 8, stats: { attack: 115, hp: 200, crit: 65, def: 15 }, perk: "Aumenta o alcance de disparo em +4 metros e concede +30% de dano crítico acima de 18m", desc: "Nó Mítico Lendário: Franco-atirador supremo" }
            ],
            stigmas: [
                { id: "st-r1", name: "Arrow Deluge", type: "AoE Burst", desc: "Chuva de flechas contínua sobre uma área concentrada." },
                { id: "st-r2", name: "Spiral Arrow", type: "Piercing", desc: "Disparo que perfura armaduras e reduz a defesa do alvo." },
                { id: "st-r3", name: "Mau Form", type: "Transformation", desc: "Transfiguração que aumenta a velocidade de ataque e dano físico." },
                { id: "st-r4", name: "Sharpshooter Aim", type: "Buff", desc: "Aumenta o dano crítico físico e a precisão dos disparos." },
                { id: "st-r5", name: "Gale Arrow", type: "Burst Knockback", desc: "Sequência de 3 flechas velozes que repelem o alvo para trás." },
                { id: "st-r6", name: "Nature's Resolve", type: "Cleanse", desc: "Remove lentidões e imobilizações garantindo fuga segura." },
                { id: "st-r7", name: "Sleep Trap", type: "Crowd Control", desc: "Armadilha no solo que coloca o inimigo em sono profundo por 10s." },
                { id: "st-r8", name: "Silence Arrow", type: "Interrupt", desc: "Silencia o oponente impedindo conjurações de magias por 6s." }
            ],
            presets: {
                pve: { nodes: ["r1", "r3", "r4", "r6"], stigmas: ["st-r1", "st-r2", "st-r3", "st-r4", "st-r5", "st-r6"] },
                pvp: { nodes: ["r1", "r2", "r4", "r5", "r6"], stigmas: ["st-r7", "st-r8", "st-r3", "st-r5", "st-r6", "st-r2"] }
            }
        },
        sorcerer: {
            name: "Sorcerer",
            role: "Ranged Magic DPS",
            roleDetail: "Ranged Magic DPS (Orb / Spellbook)",
            nodes: [
                { id: "s1", tier: 1, name: "Harmonia Elemental", color: "white", cost: 3, stats: { attack: 45, hp: 100, crit: 20, def: 10 }, desc: "+45 Magic Boost, +100 Max HP" },
                { id: "s2", tier: 1, name: "Fluxo de Mana", color: "green", cost: 4, stats: { attack: 15, hp: 80, crit: 15, def: 0 }, perk: "Reduz o consumo de Mana em 15% e aumenta regeneração", desc: "Sustentação contínua de feitiços" },
                { id: "s3", tier: 2, name: "Chama Concentrada", color: "blue", cost: 5, stats: { attack: 65, hp: 0, crit: 30, def: 0 }, perk: "Feitiços de fogo aplicam queimadura cumulativa", desc: "Dano elemental potencializado" },
                { id: "s4", tier: 2, name: "Aceleração Arcana", color: "white", cost: 4, stats: { attack: 70, hp: 120, crit: 35, def: 0 }, desc: "+70 Magic Boost, +35 Magical Crit" },
                { id: "s5", tier: 3, name: "Gelo Profundo", color: "green", cost: 5, stats: { attack: 25, hp: 0, crit: 20, def: 20 }, perk: "Magias gélidas reduzem velocidade do alvo em 40%", desc: "Controle de terreno impenetrável" },
                { id: "s6", tier: 4, name: "Meteoro Apocalíptico", color: "orange", cost: 8, stats: { attack: 135, hp: 180, crit: 75, def: 10 }, perk: "Reduz o tempo de conjuração de Glacial Shard e Big Magma Eruption em 50%", desc: "Nó Mítico Lendário: Glass Cannon Absoluto" }
            ],
            stigmas: [
                { id: "st-s1", name: "Flame Spray", type: "Active Burst", desc: "Jatos vulcânicos que causam dano estrondoso de fogo." },
                { id: "st-s2", name: "Glacial Shard", type: "Heavy Burst", desc: "Lança colossal de gelo com o maior dano único de Atreia." },
                { id: "st-s3", name: "Big Magma Eruption", type: "Ultimate AoE", desc: "Erupção magmática que aniquila grupos de monstros." },
                { id: "st-s4", name: "Stone Skin", type: "Defensive Shield", desc: "Carapaça de éter que absorve até 3000 de dano." },
                { id: "st-s5", name: "Boon of Quickness", type: "Buff", desc: "Reduz tempos de conjuração pela metade por 15s." },
                { id: "st-s6", name: "Aetheric Spellburst", type: "Finisher", desc: "Explosão de éter que recupera 20% do MP." },
                { id: "st-s7", name: "Curse of Tree", type: "Hard CC", desc: "Transforma o inimigo em árvore imóvel por 15s." },
                { id: "st-s8", name: "Sleeping Storm", type: "AoE Sleep", desc: "Adormece múltiplos inimigos na área." }
            ],
            presets: {
                pve: { nodes: ["s1", "s3", "s4", "s6"], stigmas: ["st-s1", "st-s2", "st-s3", "st-s4", "st-s5", "st-s6"] },
                pvp: { nodes: ["s1", "s2", "s4", "s5", "s6"], stigmas: ["st-s7", "st-s8", "st-s4", "st-s5", "st-s1", "st-s2"] }
            }
        },
        elementalist: {
            name: "Elementalist",
            role: "Ranged Magic DPS",
            roleDetail: "Summoner & Utility (Tome / Orb)",
            nodes: [
                { id: "e1", tier: 1, name: "Pacto Elemental", color: "white", cost: 3, stats: { attack: 40, hp: 150, crit: 20, def: 20 }, desc: "+40 Magic Boost, +150 Max HP" },
                { id: "e2", tier: 1, name: "Corrosão Contínua", color: "green", cost: 4, stats: { attack: 20, hp: 0, crit: 15, def: 0 }, perk: "Aumenta a velocidade de dano por segundo de DoTs em 20%", desc: "Erosão acelerada de vida" },
                { id: "e3", tier: 2, name: "Vínculo de Sangue", color: "blue", cost: 5, stats: { attack: 50, hp: 200, crit: 25, def: 25 }, perk: "O espírito absorve 15% de todo dano sofrido pelo invocador", desc: "Sobrevivência compartilhada" },
                { id: "e4", tier: 3, name: "Terror Ancestral", color: "green", cost: 5, stats: { attack: 15, hp: 0, crit: 15, def: 0 }, perk: "Aumenta a duração do Fear Shriek em +2 segundos", desc: "Pânico coletivo prolongado" },
                { id: "e5", tier: 4, name: "Avatar dos Quatro Elementos", color: "orange", cost: 8, stats: { attack: 125, hp: 300, crit: 60, def: 40 }, perk: "Ignite Aether causa 100% de dano bônus e remove todos os buffs do alvo", desc: "Nó Mítico Lendário: Purgador implacável" }
            ],
            stigmas: [
                { id: "st-e1", name: "Armor Spirit", type: "Pet Buff", desc: "Aumenta atributos do espírito permitindo que tanke chefes." },
                { id: "st-e2", name: "Ignite Aether", type: "Dispel Burst", desc: "Remove 3 buffs mágicos do inimigo e causa dano por cada um." },
                { id: "st-e3", name: "Spirit Burn", type: "AoE DoT", desc: "Comanda o espírito para incendiar o solo em chamas contínuas." },
                { id: "st-e4", name: "Body Root", type: "Crowd Control", desc: "Enraíza e silencia ataques físicos do alvo por 8s." },
                { id: "st-e5", name: "Spirit Wall of Protection", type: "Party Buff", desc: "Barreira protetora para o grupo inteiro com base no elemento." },
                { id: "st-e6", name: "Curse Cloud", type: "Toxic Cloud", desc: "Nuvem ácida que enfraquece o ataque de chefes de masmorra." },
                { id: "st-e7", name: "Fear Shriek", type: "AoE Fear", desc: "Aterroriza todos os adversários na área fazendo-os fugir sem controle." },
                { id: "st-e8", name: "Spirit Substitution", type: "Survival", desc: "Transfere 100% do dano para o espírito invocado." }
            ],
            presets: {
                pve: { nodes: ["e1", "e2", "e3", "e5"], stigmas: ["st-e1", "st-e2", "st-e3", "st-e4", "st-e5", "st-e6"] },
                pvp: { nodes: ["e1", "e2", "e4", "e5"], stigmas: ["st-e7", "st-e2", "st-e8", "st-e4", "st-e1", "st-e3"] }
            }
        },
        cleric: {
            name: "Cleric",
            role: "Main Healer",
            roleDetail: "Main Healer (Mace & Shield / Staff)",
            nodes: [
                { id: "c1", tier: 1, name: "Graça Divina I", color: "white", cost: 3, stats: { attack: 25, hp: 300, crit: 0, def: 35 }, desc: "+25 Magic Boost, +300 Max HP, +35 Def" },
                { id: "c2", tier: 1, name: "Rezar Acelerado", color: "green", cost: 4, stats: { attack: 0, hp: 150, crit: 0, def: 20 }, perk: "Reduz o tempo de conjuração de curas diretas em 15%", desc: "Curas velozes de emergência" },
                { id: "c3", tier: 2, name: "Onda de Purificação", color: "blue", cost: 5, stats: { attack: 35, hp: 250, crit: 15, def: 30 }, perk: "Curas em área também removem 1 veneno ou lentidão", desc: "Purificação contínua do esquadrão" },
                { id: "c4", tier: 3, name: "Fé Inquebrantável", color: "green", cost: 5, stats: { attack: 0, hp: 400, crit: 0, def: 50 }, perk: "+25% de poder curativo total em alvos com menos de 30% de HP", desc: "Salvamento de tanques em perigo" },
                { id: "c5", tier: 4, name: "Luz Sagrada de Yustiel", color: "orange", cost: 8, stats: { attack: 50, hp: 750, crit: 20, def: 80 }, perk: "Ao ressuscitar um aliado, concede barreira de invulnerabilidade de 5s para ele", desc: "Nó Mítico Lendário: Ressurreição heroica" }
            ],
            stigmas: [
                { id: "st-c1", name: "Splendor of Recovery", type: "AoE Burst Heal", desc: "Restaura 60% do HP de todo o grupo instantaneamente." },
                { id: "st-c2", name: "Benevolence", type: "Passive Buff", desc: "Eleva o poder curativo em 30% e reduz custos de MP." },
                { id: "st-c3", name: "Ripple of Purification", type: "Cleanse AoE", desc: "Purifica todos os debuffs e efeitos alteradores da equipe." },
                { id: "st-c4", name: "Yustiel's Light", type: "Regen AoE", desc: "Regenera vida continuamente a cada 2s por 30 segundos." },
                { id: "st-c5", name: "Rebirth", type: "Auto-Revive", desc: "Aplica bênção que ressuscita o alvo automaticamente se cair." },
                { id: "st-c6", name: "Flash of Recovery", type: "Instant Heal", desc: "Cura de emergência instantânea sem tempo de cast." },
                { id: "st-c7", name: "Root", type: "Crowd Control", desc: "Imobiliza alvos no solo por 10s para reposicionamento seguro." },
                { id: "st-c8", name: "Hand of Reincarnation", type: "Self Revive", desc: "Permite ressuscitar a si mesmo durante o combate." }
            ],
            presets: {
                pve: { nodes: ["c1", "c2", "c3", "c4", "c5"], stigmas: ["st-c1", "st-c2", "st-c3", "st-c4", "st-c5", "st-c6"] },
                pvp: { nodes: ["c1", "c2", "c4", "c5"], stigmas: ["st-c6", "st-c3", "st-c7", "st-c8", "st-c1", "st-c2"] }
            }
        },
        chanter: {
            name: "Chanter",
            role: "Support / Healer",
            roleDetail: "Support & Buffs (Staff / Mace & Shield)",
            nodes: [
                { id: "ch1", tier: 1, name: "Cântico de Guerra I", color: "white", cost: 3, stats: { attack: 35, hp: 200, crit: 15, def: 25 }, desc: "+35 Attack, +200 Max HP, +25 Def" },
                { id: "ch2", tier: 1, name: "Ressoar de Mantras", color: "green", cost: 4, stats: { attack: 15, hp: 150, crit: 10, def: 0 }, perk: "Aumenta o alcance de todos os Mantras de 20m para 30m", desc: "Alcance total do grupo" },
                { id: "ch3", tier: 2, name: "Quebra de Postura", color: "blue", cost: 5, stats: { attack: 45, hp: 180, crit: 25, def: 15 }, perk: "Golpes de bastão possuem +15% de chance de atordoar (Stun)", desc: "Controle marcial contundente" },
                { id: "ch4", tier: 3, name: "Harmonia de Batalha", color: "green", cost: 5, stats: { attack: 25, hp: 250, crit: 20, def: 30 }, perk: "Aumenta o bônus de dano de Victory Mantra em +20%", desc: "Potencialização do DPS dos aliados" },
                { id: "ch5", tier: 4, name: "Palavra do Vento Celestial", color: "orange", cost: 8, stats: { attack: 85, hp: 500, crit: 45, def: 60 }, perk: "Word of Wind concede imunidade a atordoamentos e lentidões para toda a party", desc: "Nó Mítico Lendário: Investida incontrolável" }
            ],
            stigmas: [
                { id: "st-ch1", name: "Word of Wind", type: "Ultimate Buff", desc: "Eleva a velocidade de ataque e corrida do grupo em 50% por 30s." },
                { id: "st-ch2", name: "Victory Mantra", type: "Aura Mantra", desc: "Aumenta o Physical Attack e Magic Boost de todos os aliados em 20m." },
                { id: "st-ch3", name: "Shield of Protection", type: "Group Shield", desc: "Cria barreira sagrada em toda a equipe que absorve 2500 de dano." },
                { id: "st-ch4", name: "Hit Mantra", type: "Aura Mantra", desc: "Eleva a taxa de Critical Hit e Precisão de todo o esquadrão." },
                { id: "st-ch5", name: "Healing Conduit", type: "Active Heal", desc: "Cura em cone à frente que regenera vida continuamente." },
                { id: "st-ch6", name: "Mountain Fall", type: "Knockdown", desc: "Golpe descendente com o báculo que derruba o alvo no chão." },
                { id: "st-ch7", name: "Celerity Mantra", type: "Aura Mantra", desc: "Garante velocidade de corrida permanente no mapa aberto." },
                { id: "st-ch8", name: "Soul Crush", type: "Stun Combo", desc: "Sequência marcial veloz que atordoa o adversário repetidamente." }
            ],
            presets: {
                pve: { nodes: ["ch1", "ch2", "ch3", "ch4", "ch5"], stigmas: ["st-ch1", "st-ch2", "st-ch3", "st-ch4", "st-ch5", "st-ch6"] },
                pvp: { nodes: ["ch1", "ch2", "ch3", "ch4", "ch5"], stigmas: ["st-ch1", "st-ch7", "st-ch4", "st-ch8", "st-ch3", "st-ch6"] }
            }
        }
    };

    // Estado da Build Atual
    let currentClass = "gladiator";
    let allocatedNodeIds = new Set();
    let equippedStigmaIds = [];
    const MAX_POINTS = 50;
    const MAX_STIGMAS = 6;

    // Elementos DOM
    const classSelector = document.getElementById('planner-class-selector');
    const classTitle = document.getElementById('active-class-title');
    const classRole = document.getElementById('active-class-role');
    const pointsSpentEl = document.getElementById('stat-points-spent');
    const pointsRemainingEl = document.getElementById('stat-points-remaining');
    const stigmasEquippedEl = document.getElementById('stat-stigmas-equipped');
    const daevanionTreeContainer = document.getElementById('daevanion-tree-container');
    const equippedStigmasGrid = document.getElementById('equipped-stigmas-grid');
    const availableStigmasList = document.getElementById('available-stigmas-list');
    const stigmasSlotIndicator = document.getElementById('stigmas-slot-indicator');
    
    // Stats Summary Elements
    const statAttackEl = document.getElementById('stat-sum-attack');
    const statHpEl = document.getElementById('stat-sum-hp');
    const statCritEl = document.getElementById('stat-sum-crit');
    const statDefEl = document.getElementById('stat-sum-defense');
    const perksListEl = document.getElementById('build-perks-list');

    // Botões
    const btnPresetPve = document.getElementById('planner-btn-preset-pve');
    const btnPresetPvp = document.getElementById('planner-btn-preset-pvp');
    const btnReset = document.getElementById('planner-btn-reset');
    const btnShare = document.getElementById('planner-btn-share');
    const shareToast = document.getElementById('share-toast');

    function calculateTotalPointsSpent() {
        const clsData = plannerDatabase[currentClass];
        let total = 0;
        allocatedNodeIds.forEach(id => {
            const node = clsData.nodes.find(n => n.id === id);
            if (node) total += node.cost;
        });
        return total;
    }

    function updateStatsSummary() {
        const clsData = plannerDatabase[currentClass];
        let totalAttack = 0;
        let totalHp = 0;
        let totalCrit = 0;
        let totalDef = 0;
        let perks = [];

        allocatedNodeIds.forEach(id => {
            const node = clsData.nodes.find(n => n.id === id);
            if (node) {
                totalAttack += node.stats.attack || 0;
                totalHp += node.stats.hp || 0;
                totalCrit += node.stats.crit || 0;
                totalDef += node.stats.def || 0;
                if (node.perk) perks.push(node.perk);
            }
        });

        if (statAttackEl) statAttackEl.textContent = `+${totalAttack}`;
        if (statHpEl) statHpEl.textContent = `+${totalHp}`;
        if (statCritEl) statCritEl.textContent = `+${totalCrit}`;
        if (statDefEl) statDefEl.textContent = `+${totalDef}`;

        if (perksListEl) {
            if (perks.length === 0) {
                perksListEl.innerHTML = '<li class="text-slate-500 italic">Nenhum nó passivo ou mítico alocado ainda.</li>';
            } else {
                perksListEl.innerHTML = perks.map(p => `
                    <li class="flex items-start gap-1.5 text-xs text-amber-300">
                        <i class="fa-solid fa-sparkles text-amber-400 mt-0.5 flex-shrink-0"></i>
                        <span>${p}</span>
                    </li>
                `).join('');
            }
        }

        const spent = calculateTotalPointsSpent();
        const remaining = MAX_POINTS - spent;
        if (pointsSpentEl) pointsSpentEl.textContent = spent;
        if (pointsRemainingEl) {
            pointsRemainingEl.textContent = remaining;
            pointsRemainingEl.className = remaining < 0 ? 'text-red-400 font-bold font-mono' : 'text-amber-400 font-bold font-mono';
        }

        if (stigmasEquippedEl) stigmasEquippedEl.textContent = equippedStigmaIds.length;
        if (stigmasSlotIndicator) stigmasSlotIndicator.textContent = `${equippedStigmaIds.length}/${MAX_STIGMAS} Slots`;
    }

    function renderDaevanionTree() {
        if (!daevanionTreeContainer) return;
        const clsData = plannerDatabase[currentClass];
        daevanionTreeContainer.innerHTML = '';

        // Agrupar nós por Tier
        const tiers = [1, 2, 3, 4];
        const tierNames = {
            1: "Tier 1: Despertar de Éter (Nível 10-25)",
            2: "Tier 2: Especialização de Atreia (Nível 25-35)",
            3: "Tier 3: Mestria Ancestral (Nível 35-44)",
            4: "Tier 4: Poder Mítico Supremo (Level 45)"
        };

        tiers.forEach(tier => {
            const tierNodes = clsData.nodes.filter(n => n.tier === tier);
            if (tierNodes.length === 0) return;

            const tierWrapper = document.createElement('div');
            tierWrapper.className = 'p-4 rounded-2xl bg-dark-950/70 border border-slate-800/80 space-y-3';

            const tierHeader = document.createElement('div');
            tierHeader.className = 'flex items-center justify-between text-xs border-b border-slate-800/80 pb-2';
            tierHeader.innerHTML = `
                <span class="font-fantasy font-bold text-slate-300">${tierNames[tier]}</span>
                <span class="text-[10px] uppercase font-bold text-slate-500">${tierNodes.length} Nós Disponíveis</span>
            `;
            tierWrapper.appendChild(tierHeader);

            const grid = document.createElement('div');
            grid.className = 'grid grid-cols-1 sm:grid-cols-2 gap-2.5';

            tierNodes.forEach(node => {
                const isAllocated = allocatedNodeIds.has(node.id);
                const nodeCard = document.createElement('div');
                
                // Cores de nós
                let badgeClass = "bg-slate-200 text-slate-900";
                let activeBorderClass = "border-white bg-white/10 text-white shadow-lg shadow-white/10";
                if (node.color === 'green') {
                    badgeClass = "bg-emerald-500 text-slate-950";
                    activeBorderClass = "border-emerald-400 bg-emerald-500/15 text-emerald-300 shadow-lg shadow-emerald-500/20";
                } else if (node.color === 'blue') {
                    badgeClass = "bg-sky-500 text-slate-950";
                    activeBorderClass = "border-sky-400 bg-sky-500/15 text-sky-300 shadow-lg shadow-sky-500/20";
                } else if (node.color === 'orange') {
                    badgeClass = "bg-amber-400 text-slate-950";
                    activeBorderClass = "border-amber-400 bg-amber-500/20 text-amber-300 shadow-xl shadow-amber-500/25";
                }

                nodeCard.className = `p-3 rounded-xl border transition-all cursor-pointer select-none flex flex-col justify-between ${isAllocated ? activeBorderClass : 'border-slate-800 bg-slate-900/60 text-slate-300 hover:border-slate-700'}`;
                
                nodeCard.innerHTML = `
                    <div>
                        <div class="flex items-center justify-between mb-1.5">
                            <span class="text-[9px] font-bold px-2 py-0.5 rounded-full uppercase ${badgeClass}">${node.color}</span>
                            <span class="text-[11px] font-bold font-mono ${isAllocated ? 'text-cyan-300' : 'text-slate-500'}">${node.cost} Pts</span>
                        </div>
                        <h5 class="text-xs font-bold font-fantasy text-white mb-1 flex items-center justify-between">
                            ${node.name}
                            ${isAllocated ? '<i class="fa-solid fa-circle-check text-cyan-400 text-xs"></i>' : ''}
                        </h5>
                        <p class="text-[11px] text-slate-400 leading-snug">${node.desc}</p>
                        ${node.perk ? `<div class="mt-2 text-[10px] font-semibold text-amber-400/90"><i class="fa-solid fa-bolt mr-1"></i>${node.perk}</div>` : ''}
                    </div>
                `;

                nodeCard.addEventListener('click', () => {
                    if (allocatedNodeIds.has(node.id)) {
                        allocatedNodeIds.delete(node.id);
                    } else {
                        const currentSpent = calculateTotalPointsSpent();
                        if (currentSpent + node.cost > MAX_POINTS) {
                            alert(`Você não tem pontos de Daevanion suficientes! Limite: ${MAX_POINTS} pontos.`);
                            return;
                        }
                        allocatedNodeIds.add(node.id);
                    }
                    renderDaevanionTree();
                    updateStatsSummary();
                });

                grid.appendChild(nodeCard);
            });

            tierWrapper.appendChild(grid);
            daevanionTreeContainer.appendChild(tierWrapper);
        });
    }

    function renderStigmas() {
        if (!equippedStigmasGrid || !availableStigmasList) return;
        const clsData = plannerDatabase[currentClass];

        // 1. Renderizar os 6 Slots Equipados
        equippedStigmasGrid.innerHTML = '';
        for (let i = 0; i < MAX_STIGMAS; i++) {
            const stigmaId = equippedStigmaIds[i];
            const slotEl = document.createElement('div');

            if (stigmaId) {
                const st = clsData.stigmas.find(s => s.id === stigmaId);
                slotEl.className = 'p-2 rounded-xl border border-purple-500/60 bg-purple-500/15 min-h-[64px] flex flex-col items-center justify-center text-center cursor-pointer hover:border-red-400 group transition-all relative';
                slotEl.title = "Clique para desequipar esta Stigma";
                slotEl.innerHTML = `
                    <span class="text-[9px] font-bold text-purple-300 uppercase tracking-tighter truncate w-full">${st.name}</span>
                    <span class="text-[8px] text-slate-400">${st.type}</span>
                    <div class="absolute inset-0 bg-red-950/80 rounded-xl opacity-0 group-hover:opacity-100 flex items-center justify-center text-red-300 text-xs font-bold transition-opacity">
                        <i class="fa-solid fa-trash-can mr-1"></i> Tirar
                    </div>
                `;
                slotEl.addEventListener('click', () => {
                    equippedStigmaIds.splice(i, 1);
                    renderStigmas();
                    updateStatsSummary();
                });
            } else {
                slotEl.className = 'p-2 rounded-xl border border-dashed border-slate-800 bg-dark-950/60 min-h-[64px] flex flex-col items-center justify-center text-center text-[10px] text-slate-500';
                slotEl.innerHTML = `
                    <i class="fa-solid fa-plus text-xs mb-1 opacity-40"></i>
                    <span>Slot 0${i + 1}</span>
                `;
            }
            equippedStigmasGrid.appendChild(slotEl);
        }

        // 2. Renderizar Lista de Stigmas Disponíveis
        availableStigmasList.innerHTML = '';
        clsData.stigmas.forEach(st => {
            const isEquipped = equippedStigmaIds.includes(st.id);
            const item = document.createElement('div');
            item.className = `p-2.5 rounded-xl border transition-all flex items-center justify-between text-xs cursor-pointer ${isEquipped ? 'border-purple-500/40 bg-purple-950/20 opacity-60' : 'border-slate-800 bg-dark-950 hover:border-purple-400'}`;
            
            item.innerHTML = `
                <div class="pr-2">
                    <div class="flex items-center gap-2">
                        <strong class="text-white font-fantasy text-xs">${st.name}</strong>
                        <span class="text-[9px] font-bold px-1.5 py-0.2 rounded bg-purple-500/20 text-purple-300 border border-purple-500/30">${st.type}</span>
                    </div>
                    <p class="text-[10px] text-slate-400 leading-snug mt-0.5">${st.desc}</p>
                </div>
                <button class="px-2.5 py-1 rounded-lg text-[10px] font-bold transition-all flex-shrink-0 ${isEquipped ? 'bg-slate-800 text-slate-400' : 'bg-purple-600 hover:bg-purple-500 text-white shadow-md'}">
                    ${isEquipped ? 'Equipada' : '+ Equipar'}
                </button>
            `;

            item.addEventListener('click', () => {
                if (isEquipped) {
                    equippedStigmaIds = equippedStigmaIds.filter(id => id !== st.id);
                } else {
                    if (equippedStigmaIds.length >= MAX_STIGMAS) {
                        alert("Todos os 6 slots de Stigmas já estão ocupados! Desequipe uma Stigma primeiro.");
                        return;
                    }
                    equippedStigmaIds.push(st.id);
                }
                renderStigmas();
                updateStatsSummary();
            });

            availableStigmasList.appendChild(item);
        });
    }

    function switchClass(newSlug) {
        if (!plannerDatabase[newSlug]) return;
        currentClass = newSlug;
        allocatedNodeIds.clear();
        equippedStigmaIds = [];

        // Atualizar Seletor Visual
        document.querySelectorAll('.planner-class-btn').forEach(btn => {
            const slug = btn.getAttribute('data-slug');
            if (slug === currentClass) {
                btn.className = 'planner-class-btn p-2.5 rounded-xl border text-center transition-all flex flex-col items-center justify-center gap-1 bg-cyan-500/20 border-cyan-400 text-cyan-300 shadow-lg shadow-cyan-500/20 active';
            } else {
                btn.className = 'planner-class-btn p-2.5 rounded-xl border text-center transition-all flex flex-col items-center justify-center gap-1 bg-dark-950/70 border-slate-800 text-slate-300 hover:border-slate-700 hover:text-white';
            }
        });

        const clsData = plannerDatabase[currentClass];
        if (classTitle) classTitle.textContent = clsData.name;
        if (classRole) classRole.textContent = clsData.roleDetail;

        // Auto-carregar preset PvE ao trocar de classe
        loadPreset('pve');
    }

    function loadPreset(type) {
        const clsData = plannerDatabase[currentClass];
        const preset = clsData.presets[type];
        if (!preset) return;

        allocatedNodeIds = new Set(preset.nodes);
        equippedStigmaIds = [...preset.stigmas];

        renderDaevanionTree();
        renderStigmas();
        updateStatsSummary();
    }

    // Eventos dos botões de classe
    if (classSelector) {
        classSelector.querySelectorAll('.planner-class-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                const slug = btn.getAttribute('data-slug');
                switchClass(slug);
            });
        });
    }

    // Botões de Presets e Ações
    if (btnPresetPve) {
        btnPresetPve.addEventListener('click', () => loadPreset('pve'));
    }

    if (btnPresetPvp) {
        btnPresetPvp.addEventListener('click', () => loadPreset('pvp'));
    }

    if (btnReset) {
        btnReset.addEventListener('click', () => {
            allocatedNodeIds.clear();
            equippedStigmaIds = [];
            renderDaevanionTree();
            renderStigmas();
            updateStatsSummary();
        });
    }

    if (btnShare) {
        btnShare.addEventListener('click', () => {
            const url = new URL(window.location.href);
            url.searchParams.set('class', currentClass);
            url.searchParams.set('nodes', Array.from(allocatedNodeIds).join(','));
            url.searchParams.set('stigmas', equippedStigmaIds.join(','));

            navigator.clipboard.writeText(url.toString()).then(() => {
                if (shareToast) {
                    shareToast.classList.remove('hidden');
                    setTimeout(() => {
                        shareToast.classList.add('hidden');
                    }, 3500);
                }
            }).catch(() => {
                alert(`Link da Build copiado: ${url.toString()}`);
            });
        });
    }

    // Inicialização da classe inicial
    switchClass("gladiator");
}
