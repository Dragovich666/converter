// Script para a página inicial - Home Page
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('searchForm');
    const loading = document.getElementById('loading');
    const errorMessage = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');
    const tripTypeRadios = document.querySelectorAll('input[name="tripType"]');
    const dataVoltaGroup = document.getElementById('dataVoltaGroup');
    const dataVoltaInput = document.getElementById('data_volta');

    // Define data mínima como hoje
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('data_ida').setAttribute('min', today);
    document.getElementById('data_volta').setAttribute('min', today);

    // Controla exibição da data de volta baseado no tipo de viagem
    tripTypeRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'oneway') {
                dataVoltaGroup.style.display = 'none';
                dataVoltaInput.removeAttribute('required');
                dataVoltaInput.value = '';
            } else {
                dataVoltaGroup.style.display = 'block';
                dataVoltaInput.setAttribute('required', 'required');
            }
        });
    });

    // Converte inputs de origem e destino para maiúsculas
    const origemInput = document.getElementById('origem');
    const destinoInput = document.getElementById('destino');

    origemInput.addEventListener('input', function() {
        this.value = this.value.toUpperCase();
    });

    destinoInput.addEventListener('input', function() {
        this.value = this.value.toUpperCase();
    });

    // Atualiza data mínima de volta quando data de ida muda
    document.getElementById('data_ida').addEventListener('change', function() {
        document.getElementById('data_volta').setAttribute('min', this.value);
    });

    // Submit do formulário
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Esconde mensagens anteriores
        errorMessage.classList.add('hidden');
        loading.classList.remove('hidden');

        // Coleta dados do formulário
        const formData = {
            origem: document.getElementById('origem').value.toUpperCase(),
            destino: document.getElementById('destino').value.toUpperCase(),
            data_ida: document.getElementById('data_ida').value,
            data_volta: document.getElementById('data_volta').value || null,
            passageiros: parseInt(document.getElementById('passageiros').value),
            criancas: parseInt(document.getElementById('criancas').value),
            classe: document.getElementById('classe').value,
            moeda: document.getElementById('moeda').value
        };

        // Validações adicionais
        if (formData.origem === formData.destino) {
            showError('Origem e destino não podem ser iguais');
            loading.classList.add('hidden');
            return;
        }

        if (formData.origem.length !== 3 || formData.destino.length !== 3) {
            showError('Códigos de aeroporto devem ter 3 letras (ex: GRU, GIG, SLZ)');
            loading.classList.add('hidden');
            return;
        }

        if (formData.data_volta && formData.data_volta <= formData.data_ida) {
            showError('Data de volta deve ser posterior à data de ida');
            loading.classList.add('hidden');
            return;
        }

        try {
            // Faz requisição para a API
            const response = await fetch('/consulta?format=html', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                // Se retornou HTML, redireciona para a página de resultados
                const html = await response.text();
                document.open();
                document.write(html);
                document.close();
            } else {
                // Trata erros
                const error = await response.json();
                showError(error.mensagem || 'Erro ao buscar voos. Tente novamente.');
                loading.classList.add('hidden');
            }
        } catch (error) {
            console.error('Erro:', error);
            showError('Erro de conexão. Verifique sua internet e tente novamente.');
            loading.classList.add('hidden');
        }
    });
});

// Função para preencher rota popular
function fillRoute(origem, destino) {
    document.getElementById('origem').value = origem;
    document.getElementById('destino').value = destino;

    // Define datas padrão (30 dias a partir de hoje, volta 7 dias depois)
    const hoje = new Date();
    const dataIda = new Date(hoje);
    dataIda.setDate(hoje.getDate() + 30);

    const dataVolta = new Date(dataIda);
    dataVolta.setDate(dataIda.getDate() + 7);

    document.getElementById('data_ida').value = dataIda.toISOString().split('T')[0];
    document.getElementById('data_volta').value = dataVolta.toISOString().split('T')[0];

    // Scroll suave até o formulário
    document.getElementById('searchForm').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });

    // Destaca o formulário
    const searchContainer = document.querySelector('.search-container');
    searchContainer.style.animation = 'none';
    setTimeout(() => {
        searchContainer.style.animation = 'pulse 0.5s ease-in-out';
    }, 10);

    // Foca no campo de passageiros
    setTimeout(() => {
        document.getElementById('passageiros').focus();
    }, 800);
}

// Função para mostrar erro
function showError(message) {
    const errorMessage = document.getElementById('errorMessage');
    const errorText = document.getElementById('errorText');

    errorText.textContent = message;
    errorMessage.classList.remove('hidden');

    // Scroll até o erro
    errorMessage.scrollIntoView({
        behavior: 'smooth',
        block: 'center'
    });
}

// Adiciona animação de pulse ao CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
`;
document.head.appendChild(style);

// Validação em tempo real dos códigos de aeroporto
const airportCodes = ['GRU', 'GIG', 'SLZ', 'BSB', 'FOR', 'SSA', 'REC', 'MAO', 'BEL', 'CWB',
                     'POA', 'FLN', 'VCP', 'CGH', 'SDU', 'CNF', 'NAT', 'MCZ', 'THE', 'VIX',
                     'JFK', 'LAX', 'MIA', 'ORD', 'LHR', 'CDG', 'FCO', 'MAD', 'LIS'];

function validateAirportCode(input) {
    const value = input.value.toUpperCase();
    if (value.length === 3) {
        if (airportCodes.includes(value)) {
            input.style.borderColor = 'var(--secondary-color)';
            input.style.background = '#ecfdf5';
        } else {
            input.style.borderColor = 'var(--warning-color)';
            input.style.background = '#fffbeb';
        }
    } else {
        input.style.borderColor = '';
        input.style.background = '';
    }
}

document.getElementById('origem').addEventListener('input', function() {
    validateAirportCode(this);
});

document.getElementById('destino').addEventListener('input', function() {
    validateAirportCode(this);
});

// Atalhos de teclado
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K para focar no campo de origem
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        document.getElementById('origem').focus();
    }
});

// Detecta se há parâmetros na URL (para voltar de uma busca)
const urlParams = new URLSearchParams(window.location.search);
if (urlParams.has('from_results')) {
    showNotification('Nova busca iniciada', 'info');
}

// Função para mostrar notificação
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? 'var(--secondary-color)' : 'var(--primary-color)'};
        color: white;
        padding: 15px 25px;
        border-radius: 12px;
        box-shadow: var(--shadow-xl);
        z-index: 1000;
        animation: slideInRight 0.3s ease-out;
    `;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'info-circle'}"></i>
        ${message}
    `;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Adiciona estilos de animação para notificações
const notificationStyle = document.createElement('style');
notificationStyle.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }

    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(notificationStyle);

console.log('Flight Crawler v2.0 - Home Page Loaded');

