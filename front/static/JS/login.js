const formLogin = document.getElementById('formLogin');

formLogin.addEventListener('submit', (event) => {
  event.preventDefault(); // Impede o envio padrão do formulário

  const email = document.getElementById('email').value;
  const senha = document.getElementById('senha').value;

  // Validação básica
  if (!email || !senha) {
    alert('Por favor, preencha todos os campos.');
    return;
  }

  // Envio dos dados para o servidor
  fetch('/seu-endpoint-login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, senha })
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      alert('Login realizado com sucesso!');

      // Redireciona de acordo com o tipo de usuário
      if (data.tipo === 'admin') {
        window.location.href = 'admin.html';
      } else {
        window.location.href = 'telaPrincipal.html';
      }
    } else {
      alert('E-mail ou senha incorretos.');
    }
  })
  .catch(error => {
    console.error('Erro:', error);
  });
});


/* _modelo ideal: uso de token para autenticação_

  try {
    const response = await fetch('/seu-endpoint-login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, senha })
    });

    if (response.ok) {
      const data = await response.json();

      if (data.success) {
        // Armazena o token e tipo de usuário
        localStorage.setItem('token', data.token);
        localStorage.setItem('tipo_usuario', data.tipo_usuario);

        // Redireciona com base no tipo
        if (data.tipo_usuario === 'admin') {
          window.location.href = '/admin-dashboard.html';
        } else if (data.tipo_usuario === 'cidadao') {
          window.location.href = '/cidadao-dashboard.html';
        }
      } else {
        showError(data.message || 'Erro no login.');
      }
    } else {
      showError('Email ou senha incorretos.');
    }
  } catch (error) {
    console.error('Erro:', error);
    showError('Erro ao fazer login. Tente novamente.');
  }
});

// Função para exibir mensagens de erro na interface
function showError(message) {
  const errorContainer = document.getElementById('error-message');
  errorContainer.textContent = message;
  errorContainer.style.display = 'block';
}*/ 