function showForm(userType) {
    const container = document.getElementById('main-container');
    const form = document.getElementById('login-form');
    const buttonChoice = document.getElementById('button-choice');
    const buttonReturn = document.getElementById('button-return');

    if (buttonChoice) {
        buttonChoice.style.display = 'none';
    }

    if (userType === 'voltar') {
        // Esconde o formulário de login e o botão de voltar
        form.style.display = 'none';
        buttonReturn.style.display = 'none';

        // Exibe novamente os botões de escolha
        buttonChoice.style.display = 'block';

        // Restaura a cor de fundo do container para o estado inicial
        container.style.backgroundColor = 'rgba(255, 255, 255, 0.8)';
        return;
    }

    // Define a cor de fundo do container com base no tipo de usuário
    if (userType === 'cliente') {
        container.style.backgroundColor = 'rgba(76, 175, 80, 0.8)';
    } else if (userType === 'restaurante') {
        container.style.backgroundColor = 'rgba(33, 150, 243, 0.8)';
    } else if (userType === 'entregador') {
        container.style.backgroundColor = 'rgba(255, 152, 0, 0.8)';
    }

    // Mostra o formulário de login
    form.style.display = 'flex';
    buttonReturn.style.display = 'flex';
    
}
