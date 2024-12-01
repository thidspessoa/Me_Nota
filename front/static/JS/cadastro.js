document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('formCadastro');
  
    form.addEventListener('submit', (event) => {
      event.preventDefault(); // Impede o envio padrão do formulário
  
      const email = document.getElementById('email').value;
      const senha = document.getElementById('senha').value;
  
      // Verifica se os campos foram preenchidos
      if (email === '' || senha === '') {
        alert('Por favor, preencha todos os campos.');
        return;
      }
  
      // Simulação de resposta do servidor
      setTimeout(() => {
        const simulatedResponse = { success: true, message: 'Cadastro realizado com sucesso!' };
  
        if (simulatedResponse.success) {
          alert(simulatedResponse.message);
          
          // Certifique-se de que o caminho para a página de login está correto
          window.location.href = 'http://127.0.0.1:5501/MeNota-main/Me%20Nota/Telas/login.html'; // Redireciona para login.html
        } else {
          alert(simulatedResponse.message || 'Erro ao realizar o cadastro.');
        }
      }, 1000); // Simula um atraso de 1 segundo
    });
  });
  

  // QUANDO BANCO FOR INTEGRADO:


/*const form = document.getElementById('formCadastro');
form.addEventListener('submit', (event) => {
  event.preventDefault(); // Impede o envio padrão do formulário

  const email = document.getElementById('email').value;
  const senha = document.getElementById('senha').value;

  // Validação básica
  if (email === '' || senha === '') {
    alert('Por favor, preencha todos os campos.');
    return;
  }



  // Envio dos dados para o servidor quando este estiver conectado (exemplo com fetch)
  fetch('/seu-endpoint', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, senha })
  })
    .then(response => {
      if (response.ok) {
        alert('Cadastro realizado com sucesso!');
        // Redirecionar para a tela de login
        window.location.href = '../Telas/login.html'; // Caminho para a tela de login
      } else {
        alert('Erro ao realizar o cadastro.');
      }
    })
    .catch(error => {
      console.error('Erro:', error);
    });
});*/