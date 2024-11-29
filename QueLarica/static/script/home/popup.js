document.addEventListener('DOMContentLoaded', function () {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Após 4 segundos, a mensagem desaparece
        setTimeout(() => {
            alert.classList.add('hide');
        }, 2500); // Tempo em milissegundos (4 segundos)
    });
});
