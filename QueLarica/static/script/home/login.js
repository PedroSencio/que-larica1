function showForm(userType) {
    const container = document.getElementById('main-container');
    const form = document.getElementById('login-form');
    const buttonChoice = document.getElementById('button-choice');
    const buttonReturn = document.getElementById('button-return');
    const buttonLogin = document.getElementById('button-loggin');
    const buttonCadastro = document.getElementById('button-cadastro');

    if (buttonChoice) {
        buttonChoice.style.display = 'none';
    }

    if (userType === 'voltar') {
        form.style.display = 'none';
        buttonReturn.style.display = 'none';

        buttonChoice.style.display = 'block';

        container.style.backgroundColor = 'rgba(255, 255, 255, 0.2)';
        return;
    }

    // Define a cor de fundo do container com base no tipo de usuário
    if (userType === 'cliente') {
        container.style.backgroundColor = 'rgba(76, 175, 80, 0.2)';
        buttonLogin.style.backgroundColor = 'rgba(76, 175, 80)';
        buttonCadastro.style.backgroundColor = 'rgba(76, 175, 80)';
        buttonCadastro.addEventListener('click', function() {
            window.location.href = 'cadastro_cliente'; 
        });
    } else if (userType === 'restaurante') {
        container.style.backgroundColor = 'rgba(33, 150, 243, 0.2)';
        buttonLogin.style.backgroundColor = 'rgba(33, 150, 243)';
        buttonCadastro.style.backgroundColor = 'rgba(33, 150, 243)';
        buttonCadastro.addEventListener('click', function() {
            window.location.href = 'cadastro_restaurante'; 
        });
    } else if (userType === 'entregador') {
        container.style.backgroundColor = 'rgba(255, 152, 0, 0.2)';
        buttonLogin.style.backgroundColor = 'rgba(255, 152, 0)';
        buttonCadastro.style.backgroundColor = 'rgba(255, 152, 0)';
        buttonCadastro.addEventListener('click', function() {
            window.location.href = 'cadastro_entregador'; 
        });
    }

    // Mostra o formulário de login
    form.style.display = 'flex';
    buttonReturn.style.display = 'flex';
    
}
