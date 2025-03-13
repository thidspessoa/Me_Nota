// Função para voltar ao menu principal
function voltar() {
    window.location.href = "../Telas/telaPrincipal.html"; // Caminho relativo para o menu principal
}

// Função para validar o arquivo
function validateFile() {
    const fileInput = document.getElementById("uploadInput");
    const feedback = document.getElementById("feedback");

    if (fileInput.files.length === 0) {
        feedback.textContent = "Por favor, selecione um arquivo!";
        feedback.style.color = "red";
        return;
    }

    const file = fileInput.files[0];
    const allowedTypes = ["application/pdf", "image/jpeg", "image/png"];

    if (allowedTypes.includes(file.type)) {
        feedback.textContent = `Arquivo "${file.name}" carregado com sucesso!`;
        feedback.style.color = "green";
        
        // Envia o formulário após a validação bem-sucedida
        document.getElementById("uploadForm").submit();
    } else {
        feedback.textContent = "Formato não suportado. Envie um arquivo PDF ou imagem.";
        feedback.style.color = "red";
    }
}