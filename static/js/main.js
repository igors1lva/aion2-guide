/**
 * main.js - Comportamentos interativos do portal Aion 2 Guides
 * Gerencia menu responsivo, accordions, modais, abas de builds, simulador de Enhancement e Daevanion.
 */

document.addEventListener('DOMContentLoaded', () => {
    initMobileMenu();
    initAccordions();
    initTabs();
    initModals();
    initClassFilters();
    initEnhancementSimulator();
    initDaevanionExplorer();
    initBeginnerChecklist();
});

/* ----------------------------------------------------
 * 1. Menu Mobile
 * ---------------------------------------------------- */
function initMobileMenu() {
    const toggleBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (toggleBtn && mobileMenu) {
        toggleBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }
}

/* ----------------------------------------------------
 * 2. Accordions Acessíveis
 * ---------------------------------------------------- */
function initAccordions() {
    const accordionTriggers = document.querySelectorAll('.accordion-header');

    accordionTriggers.forEach(trigger => {
        trigger.addEventListener('click', () => {
            const content = trigger.nextElementSibling;
            const arrow = trigger.querySelector('.accordion-arrow');
            const isOpen = content.classList.contains('open');

            // Fechar outros no mesmo grupo se data-accordion-group estiver presente
            const group = trigger.closest('[data-accordion-group]');
            if (group) {
                group.querySelectorAll('.accordion-content').forEach(c => c.classList.remove('open'));
                group.querySelectorAll('.accordion-arrow').forEach(a => a.classList.remove('rotated'));
            }

            if (!isOpen) {
                content.classList.add('open');
                if (arrow) arrow.classList.add('rotated');
            } else if (!group) {
                content.classList.remove('open');
                if (arrow) arrow.classList.remove('rotated');
            }
        });
    });
}

/* ----------------------------------------------------
 * 3. Abas Dinâmicas (Tabs)
 * ---------------------------------------------------- */
function initTabs() {
    const tabContainers = document.querySelectorAll('[data-tabs]');

    tabContainers.forEach(container => {
        const triggers = container.querySelectorAll('[data-tab-target]');
        const panels = container.querySelectorAll('[data-tab-content]');

        triggers.forEach(btn => {
            btn.addEventListener('click', () => {
                const target = btn.getAttribute('data-tab-target');

                triggers.forEach(t => {
                    t.classList.remove('active', 'border-sky-400', 'text-sky-400', 'bg-sky-500/10');
                    t.classList.add('text-slate-400');
                });
                panels.forEach(p => p.classList.add('hidden'));

                btn.classList.add('active', 'border-sky-400', 'text-sky-400', 'bg-sky-500/10');
                btn.classList.remove('text-slate-400');

                const activePanel = container.querySelector(`[data-tab-content="${target}"]`);
                if (activePanel) {
                    activePanel.classList.remove('hidden');
                }
            });
        });
    });
}

/* ----------------------------------------------------
 * 4. Modais
 * ---------------------------------------------------- */
function initModals() {
    // Abrir modal
    document.querySelectorAll('[data-modal-open]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            const modalId = btn.getAttribute('data-modal-open');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.remove('hidden');
                modal.classList.add('flex');
                document.body.style.overflow = 'hidden';
            }
        });
    });

    // Fechar modal
    document.querySelectorAll('[data-modal-close]').forEach(btn => {
        btn.addEventListener('click', () => {
            const modal = btn.closest('.modal-container');
            if (modal) {
                modal.classList.add('hidden');
                modal.classList.remove('flex');
                document.body.style.overflow = '';
            }
        });
    });

    // Fechar ao clicar no overlay ou pressionar ESC
    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal-container')) {
            e.target.classList.add('hidden');
            e.target.classList.remove('flex');
            document.body.style.overflow = '';
        }
    });

    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-container:not(.hidden)').forEach(modal => {
                modal.classList.add('hidden');
                modal.classList.remove('flex');
                document.body.style.overflow = '';
            });
        }
    });
}

/* ----------------------------------------------------
 * 5. Filtros de Classes (Página /classes)
 * ---------------------------------------------------- */
function initClassFilters() {
    const filterBtns = document.querySelectorAll('.class-filter-btn');
    const classCards = document.querySelectorAll('.class-item-card');

    if (!filterBtns.length || !classCards.length) return;

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const filter = btn.getAttribute('data-filter');

            // Atualizar botões
            filterBtns.forEach(b => {
                b.classList.remove('bg-sky-500', 'text-white', 'shadow-lg', 'shadow-sky-500/30');
                b.classList.add('bg-slate-800', 'text-slate-300');
            });
            btn.classList.add('bg-sky-500', 'text-white', 'shadow-lg', 'shadow-sky-500/30');
            btn.classList.remove('bg-slate-800', 'text-slate-300');

            // Filtrar cards
            let countVisible = 0;
            classCards.forEach(card => {
                const category = card.getAttribute('data-category');
                if (filter === 'all' || category.includes(filter)) {
                    card.style.display = 'flex';
                    countVisible++;
                } else {
                    card.style.display = 'none';
                }
            });

            const noResultMsg = document.getElementById('no-class-results');
            if (noResultMsg) {
                noResultMsg.classList.toggle('hidden', countVisible > 0);
            }
        });
    });
}

/* ----------------------------------------------------
 * 6. Simulador Interativo de Enhancement
 * ---------------------------------------------------- */
function initEnhancementSimulator() {
    const simContainer = document.getElementById('enhancement-simulator');
    if (!simContainer) return;

    let currentLevel = 0;
    let totalKinaSpent = 0;
    let attemptsCount = 0;

    const currentLevelBadge = document.getElementById('sim-current-level');
    const successRateText = document.getElementById('sim-success-rate');
    const kinaSpentText = document.getElementById('sim-total-kina');
    const attemptsText = document.getElementById('sim-total-attempts');
    const statusLog = document.getElementById('sim-status-log');
    const enhanceBtn = document.getElementById('sim-enhance-btn');
    const resetBtn = document.getElementById('sim-reset-btn');
    const itemVisual = document.getElementById('sim-item-visual');
    const safetyBanner = document.getElementById('sim-safety-banner');

    function updateDisplay(result = null) {
        if (currentLevelBadge) currentLevelBadge.textContent = `+${currentLevel}`;
        if (kinaSpentText) kinaSpentText.textContent = totalKinaSpent.toLocaleString('pt-BR') + ' Kina';
        if (attemptsText) attemptsText.textContent = attemptsCount;

        // Taxa aproximada do próximo nível
        const rates = {
            0: 100, 1: 100, 2: 100, 3: 100, 4: 100,
            5: 100, 6: 100, 7: 100, 8: 100, 9: 100,
            10: 70, 11: 50, 12: 35, 13: 20, 14: 10
        };
        const nextRate = rates[currentLevel] !== undefined ? rates[currentLevel] : 0;
        if (successRateText) {
            successRateText.textContent = currentLevel >= 15 ? 'MAX (+15)' : `${nextRate}%`;
            successRateText.className = nextRate === 100 ? 'text-emerald-400 font-bold' : (nextRate < 40 ? 'text-red-400 font-bold' : 'text-amber-400 font-bold');
        }

        // Safety indicator
        if (safetyBanner) {
            if (currentLevel < 10) {
                safetyBanner.className = 'p-3 rounded-lg border border-emerald-500/40 bg-emerald-500/10 text-emerald-300 text-xs flex items-center gap-2';
                safetyBanner.innerHTML = '<i class="fa-solid fa-shield-halved text-emerald-400 text-base"></i> <span><strong>Zona Segura:</strong> 100% de chance garantida de +0 até +10 sem risco de quebra.</span>';
            } else if (currentLevel < 15) {
                safetyBanner.className = 'p-3 rounded-lg border border-amber-500/40 bg-amber-500/10 text-amber-300 text-xs flex items-center gap-2';
                safetyBanner.innerHTML = '<i class="fa-solid fa-triangle-exclamation text-amber-400 text-base"></i> <span><strong>Zona de Risco:</strong> A taxa decresce drasticamente e falhas podem regredir o nível. Economize para o Level 45!</span>';
            } else {
                safetyBanner.className = 'p-3 rounded-lg border border-purple-500/40 bg-purple-500/10 text-purple-300 text-xs flex items-center gap-2';
                safetyBanner.innerHTML = '<i class="fa-solid fa-crown text-purple-400 text-base"></i> <span><strong>Nível Mítico Máximo (+15) alcançado!</strong> Arma de Atreia em poder absoluto!</span>';
            }
        }

        // Estilização do visual do item conforme o nível
        if (itemVisual) {
            if (currentLevel >= 15) {
                itemVisual.className = 'w-24 h-24 mx-auto rounded-xl flex items-center justify-center text-4xl shadow-2xl transition-all duration-300 bg-gradient-to-tr from-purple-700 via-pink-600 to-amber-400 border-2 border-amber-300 shadow-purple-500/50 scale-105';
            } else if (currentLevel >= 10) {
                itemVisual.className = 'w-24 h-24 mx-auto rounded-xl flex items-center justify-center text-4xl shadow-2xl transition-all duration-300 bg-gradient-to-tr from-amber-600 to-yellow-400 border-2 border-amber-300 shadow-amber-500/50';
            } else if (currentLevel >= 5) {
                itemVisual.className = 'w-24 h-24 mx-auto rounded-xl flex items-center justify-center text-4xl shadow-xl transition-all duration-300 bg-gradient-to-tr from-sky-600 to-cyan-400 border-2 border-cyan-300 shadow-cyan-500/40';
            } else {
                itemVisual.className = 'w-24 h-24 mx-auto rounded-xl flex items-center justify-center text-4xl shadow transition-all duration-300 bg-slate-800 border border-slate-700 text-slate-300';
            }
        }

        if (result && statusLog) {
            const entry = document.createElement('div');
            entry.className = `text-xs py-1 px-2 rounded mb-1 border ${result.success ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-300' : 'border-rose-500/30 bg-rose-500/10 text-rose-300'}`;
            entry.innerHTML = `<strong>Tentativa #${attemptsCount}:</strong> ${result.message} <span class="opacity-70">(Taxa: ${result.rate}%, Sorteio: ${result.roll})</span>`;
            statusLog.prepend(entry);
            // Limitar log a 8 itens
            if (statusLog.children.length > 8) {
                statusLog.removeChild(statusLog.lastChild);
            }
        }
    }

    if (enhanceBtn) {
        enhanceBtn.addEventListener('click', async () => {
            if (currentLevel >= 15) return;

            enhanceBtn.disabled = true;
            enhanceBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-1"></i> Aprimorando...';

            try {
                const response = await fetch('/api/enhancement-simulate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ current_level: currentLevel })
                });

                const data = await response.json();
                attemptsCount++;
                totalKinaSpent += data.kina_spent || 0;
                currentLevel = data.new_level;

                updateDisplay(data);
            } catch (err) {
                console.error("Erro na simulação:", err);
            } finally {
                enhanceBtn.disabled = false;
                enhanceBtn.innerHTML = '<i class="fa-solid fa-hammer mr-2"></i> Aprimorar Equipamento com Enhancement Stone';
            }
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            currentLevel = 0;
            totalKinaSpent = 0;
            attemptsCount = 0;
            if (statusLog) statusLog.innerHTML = '<div class="text-xs text-slate-500 italic">Histórico de aprimoramentos limpo.</div>';
            updateDisplay();
        });
    }

    // Inicializar
    updateDisplay();
}

/* ----------------------------------------------------
 * 7. Explorador de Constelação Daevanion
 * ---------------------------------------------------- */
function initDaevanionExplorer() {
    const nodes = document.querySelectorAll('.daevanion-node-btn');
    const infoPanel = document.getElementById('daevanion-node-info');
    if (!nodes.length || !infoPanel) return;

    const nodeData = {
        'white': {
            title: 'Nós Brancos (White Nodes)',
            subtitle: 'Atributos Básicos Primários',
            badge: 'Status Bruto',
            badgeClass: 'bg-slate-200 text-slate-900',
            desc: 'Conferem incrementos diretos às estatísticas fundamentais de combate do seu personagem. Essenciais para garantir sobrevivência e poder contínuo de ataque.',
            examples: ['+45 Physical Attack / Magic Boost', '+350 Max HP', '+25 Physical / Magical Defense', '+15 Physical Critical Hit']
        },
        'green': {
            title: 'Nós Verdes (Green Nodes)',
            subtitle: 'Passivas e Otimizações de Combate',
            badge: 'Habilidades Passivas',
            badgeClass: 'bg-emerald-500 text-slate-950 font-bold',
            desc: 'Aprimoram a fluidez da sua rotação e reduzem tempos mortos. Não exigem ativação manual e funcionam silenciosamente fortalecendo suas mecânicas.',
            examples: ['-8% Tempo de Recarga (Cooldown Reduction)', '+15% Velocidade de Movimento ao planar', '+10% Eficiência de Recuperação de Mana', 'Chance de evitar Stun e Knockdown']
        },
        'blue': {
            title: 'Nós Azuis (Blue Nodes)',
            subtitle: 'Skills Ativas e Desbloqueio de Combos',
            badge: 'Habilidades Ativas',
            badgeClass: 'bg-sky-500 text-slate-950 font-bold',
            desc: 'Destravam variações exclusivas de habilidades e novos golpes de finalização que transformam combos normais em cadeias devastadoras de dano e controle.',
            examples: ['Golpe Adicional em cadeia após Knockdown', 'Barreira de absorção com contra-ataque refletido', 'Avanço com cancelamento de animação e atordoamento']
        },
        'orange': {
            title: 'Nós Laranja (Orange Nodes)',
            subtitle: 'Bônus Lendários e Poderes Ancestrais',
            badge: 'Transformador de Gameplay',
            badgeClass: 'bg-amber-400 text-slate-950 font-bold',
            desc: 'O ápice da Daevanion Board. Cada classe possui de 2 a 3 nós laranja por árvore estelar que redefinem completamente a forma de jogar e a dominância no campo de batalha.',
            examples: ['Restauração total do cooldown do Shadowstep ao eliminar um inimigo', 'Imunidade a controles de grupo ao ativar Word of Wind', 'Aumento de 40% do dano ao atingir alvos imobilizados']
        }
    };

    nodes.forEach(btn => {
        btn.addEventListener('click', () => {
            const nodeType = btn.getAttribute('data-node-type');
            const data = nodeData[nodeType];
            if (!data) return;

            // Highlight no botão ativo
            nodes.forEach(b => b.classList.remove('ring-4', 'ring-white', 'scale-110'));
            btn.classList.add('ring-4', 'ring-white', 'scale-110');

            infoPanel.innerHTML = `
                <div class="animate-fadeIn">
                    <div class="flex items-center justify-between mb-3">
                        <span class="px-2.5 py-1 text-xs rounded-full uppercase tracking-wider ${data.badgeClass}">${data.badge}</span>
                        <span class="text-xs text-slate-400">Daevanion Node</span>
                    </div>
                    <h4 class="text-xl font-bold font-fantasy text-white mb-1">${data.title}</h4>
                    <p class="text-xs text-sky-400 mb-3">${data.subtitle}</p>
                    <p class="text-slate-300 text-sm mb-4 leading-relaxed">${data.desc}</p>
                    <div class="border-t border-slate-700/60 pt-3">
                        <span class="text-xs uppercase font-semibold text-slate-400 tracking-wider block mb-2">Exemplos de Atributos:</span>
                        <ul class="space-y-1.5 text-xs text-slate-300">
                            ${data.examples.map(ex => `<li class="flex items-center gap-2"><i class="fa-solid fa-sparkles text-amber-400"></i> ${ex}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            `;
        });
    });
}

/* ----------------------------------------------------
 * 8. Checklist Interativo de Leveling (Iniciantes)
 * ---------------------------------------------------- */
function initBeginnerChecklist() {
    const checklistItems = document.querySelectorAll('.checklist-checkbox');
    if (!checklistItems.length) return;

    const storageKey = 'aion2_beginner_checklist_v1';
    let savedState = {};

    try {
        savedState = JSON.parse(localStorage.getItem(storageKey) || '{}');
    } catch (e) {
        savedState = {};
    }

    const progressBar = document.getElementById('checklist-progress-bar');
    const progressText = document.getElementById('checklist-progress-text');

    function updateProgress() {
        const total = checklistItems.length;
        let checked = 0;

        checklistItems.forEach(item => {
            const id = item.getAttribute('data-check-id');
            if (item.checked) {
                checked++;
                item.closest('label').classList.add('line-through', 'opacity-60');
            } else {
                item.closest('label').classList.remove('line-through', 'opacity-60');
            }
        });

        const percent = Math.round((checked / total) * 100);
        if (progressBar) progressBar.style.width = `${percent}%`;
        if (progressText) progressText.textContent = `${checked}/${total} Concluídos (${percent}%)`;
    }

    checklistItems.forEach(item => {
        const id = item.getAttribute('data-check-id');
        if (savedState[id]) {
            item.checked = true;
        }

        item.addEventListener('change', () => {
            savedState[id] = item.checked;
            try {
                localStorage.setItem(storageKey, JSON.stringify(savedState));
            } catch (e) {}
            updateProgress();
        });
    });

    updateProgress();
}

/* ----------------------------------------------------
 * 11. Sistema de Cópia de Macros In-Game (.txt)
 * ---------------------------------------------------- */
function copyMacroText(elementId, btn) {
    const codeEl = document.getElementById(elementId);
    if (!codeEl) return;
    const text = codeEl.innerText.trim();
    
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            handleCopySuccess(btn);
        }).catch(() => {
            fallbackCopyText(text, btn);
        });
    } else {
        fallbackCopyText(text, btn);
    }
}

function handleCopySuccess(btn) {
    if (!btn) return;
    const originalHtml = btn.innerHTML;
    btn.classList.remove('bg-cyan-500/10', 'text-cyan-300', 'border-cyan-500/30');
    btn.classList.add('bg-emerald-600', 'text-white', 'border-emerald-500');
    btn.innerHTML = '<i class="fa-solid fa-check mr-1"></i> <span>Copiado!</span>';
    
    setTimeout(() => {
        btn.innerHTML = originalHtml;
        btn.classList.remove('bg-emerald-600', 'text-white', 'border-emerald-500');
        btn.classList.add('bg-cyan-500/10', 'text-cyan-300', 'border-cyan-500/30');
    }, 2200);
}

function fallbackCopyText(text, btn) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.top = "-9999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
        document.execCommand('copy');
        handleCopySuccess(btn);
    } catch (err) {
        console.error('Falha no fallback de cópia:', err);
    }
    document.body.removeChild(textArea);
}
