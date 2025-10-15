// Funções de filtro e ordenação dos voos

// Dados dos voos (serão preenchidos dinamicamente)
let allFlights = [];
let currentFilter = 'all';

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    // Carrega todos os cartões de voos
    allFlights = Array.from(document.querySelectorAll('.flight-card'));

    // Adiciona animação de entrada
    allFlights.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
});

// Função para filtrar voos
function filterFlights(filterType) {
    currentFilter = filterType;

    // Atualiza botões ativos
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.closest('.filter-btn').classList.add('active');

    // Aplica filtro
    allFlights.forEach(card => {
        card.classList.remove('hidden');

        switch(filterType) {
            case 'direct':
                const stops = parseInt(card.dataset.stops);
                if (stops > 0) {
                    card.classList.add('hidden');
                }
                break;
            case 'cheapest':
                // Mostra apenas os 5 mais baratos
                const sortedByPrice = [...allFlights].sort((a, b) => {
                    return parseFloat(a.dataset.price) - parseFloat(b.dataset.price);
                });
                if (sortedByPrice.indexOf(card) >= 5) {
                    card.classList.add('hidden');
                }
                break;
            case 'all':
            default:
                // Mostra todos
                break;
        }
    });

    // Anima a entrada
    animateFilteredCards();
}

// Função para ordenar voos
function sortFlights(sortType) {
    // Atualiza botões ativos
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.closest('.filter-btn').classList.add('active');

    const flightsList = document.getElementById('flightsList');
    const sortedFlights = [...allFlights];

    switch(sortType) {
        case 'price':
            sortedFlights.sort((a, b) => {
                return parseFloat(a.dataset.price) - parseFloat(b.dataset.price);
            });
            break;
        case 'duration':
            sortedFlights.sort((a, b) => {
                return parseInt(a.dataset.duration) - parseInt(b.dataset.duration);
            });
            break;
    }

    // Remove todos os cartões
    flightsList.innerHTML = '';

    // Adiciona os cartões ordenados
    sortedFlights.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.05}s`;
        flightsList.appendChild(card);
    });

    allFlights = sortedFlights;
}

// Função para animar cartões filtrados
function animateFilteredCards() {
    const visibleCards = allFlights.filter(card => !card.classList.contains('hidden'));
    visibleCards.forEach((card, index) => {
        card.style.animation = 'none';
        setTimeout(() => {
            card.style.animation = `slideIn 0.5s ease-out ${index * 0.05}s both`;
        }, 10);
    });
}

// Função para formatar moeda
function formatCurrency(value, currency) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: currency || 'BRL'
    }).format(value);
}

// Função para compartilhar resultados
function shareResults() {
    const url = window.location.href;
    if (navigator.share) {
        navigator.share({
            title: 'Resultados de Busca - Flight Crawler',
            text: 'Confira os voos que encontrei!',
            url: url
        }).catch(() => {
            copyToClipboard(url);
        });
    } else {
        copyToClipboard(url);
    }
}

// Função para copiar para clipboard
function copyToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);

    // Mostra feedback
    showNotification('Link copiado para a área de transferência!');
}

// Função para mostrar notificação
function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #10b981;
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        animation: slideInRight 0.3s ease-out;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Adiciona estilos de animação para notificações
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Detecta se o usuário está em modo escuro (opcional para futuras implementações)
function detectDarkMode() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
}

// Função para imprimir resultados
function printResults() {
    window.print();
}

// Adiciona eventos de teclado para acessibilidade
document.addEventListener('keydown', function(e) {
    // Esc para resetar filtros
    if (e.key === 'Escape') {
        const allButton = document.querySelector('.filter-btn[onclick*="all"]');
        if (allButton) {
            allButton.click();
        }
    }

    // Ctrl/Cmd + P para imprimir
    if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
        e.preventDefault();
        printResults();
    }
});

// Scroll suave para o topo ao filtrar
function smoothScrollTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// Adiciona indicador de carregamento (para futuras chamadas AJAX)
function showLoading() {
    const loading = document.createElement('div');
    loading.id = 'loading';
    loading.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    `;
    loading.innerHTML = `
        <div style="background: white; padding: 30px; border-radius: 16px; text-align: center;">
            <i class="fas fa-spinner fa-spin" style="font-size: 48px; color: #2563eb; margin-bottom: 15px;"></i>
            <p style="font-size: 18px; color: #1f2937;">Carregando...</p>
        </div>
    `;
    document.body.appendChild(loading);
}

function hideLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        document.body.removeChild(loading);
    }
}

// Log de analytics (placeholder para futuras implementações)
function logAnalytics(action, data) {
    console.log('Analytics:', action, data);
    // Aqui você pode integrar com Google Analytics, Mixpanel, etc.
}

// Inicializa tooltips (se necessário)
function initTooltips() {
    const elements = document.querySelectorAll('[data-tooltip]');
    elements.forEach(el => {
        el.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.dataset.tooltip;
            document.body.appendChild(tooltip);

            const rect = this.getBoundingClientRect();
            tooltip.style.top = `${rect.top - tooltip.offsetHeight - 10}px`;
            tooltip.style.left = `${rect.left + (rect.width - tooltip.offsetWidth) / 2}px`;
        });

        el.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.tooltip');
            if (tooltip) {
                document.body.removeChild(tooltip);
            }
        });
    });
}

console.log('Flight Crawler v2.0 - Scripts carregados');

