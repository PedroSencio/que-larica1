document.getElementById('button-loggin').addEventListener('click', function () {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Determina o tipo de usuário pelo background color do container
    let userType = '';
    const container = document.getElementById('main-container');
    const bgColor = container.style.backgroundColor;
    if (bgColor.includes('76, 175, 80')) userType = 'cliente';
    else if (bgColor.includes('33, 150, 243')) userType = 'restaurante';
    else if (bgColor.includes('255, 152, 0')) userType = 'entregador';

    // Envia os dados para o backend
    fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, userType })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Redireciona para a página inicial do usuário
            window.location.href = `/dashboard_${userType}`;
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error('Erro no login:', error));
});
