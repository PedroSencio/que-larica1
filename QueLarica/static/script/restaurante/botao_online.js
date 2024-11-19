document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.getElementById("status-toggle");
    const statusText = document.getElementById("status-text");

    toggle.addEventListener("change", function () {
        const novoStatus = toggle.checked;

        fetch("/configuracoes/status", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ status: novoStatus }),
        })
        .then((response) => response.json())
        .then((data) => {
            if (data.success) {
                statusText.textContent = data.status;
            } else {
                alert("Erro ao atualizar status: " + data.error);
            }
        })
        .catch((error) => {
            alert("Erro ao conectar com o servidor.");
            console.error(error);
        });
    });
});
