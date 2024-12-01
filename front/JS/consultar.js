// Simula o banco de dados de notas fiscais
const notasFiscais = [
    { cpf: '123.456.789-00', servico: 'Desenvolvimento', valor: 'R$1000,00' },
    { cpf: '987.654.321-00', servico: 'Consultoria', valor: 'R$500,00' },
  ];
  
  // Função para preencher a lista de notas
  function carregarNotas() {
    const notasList = document.getElementById('notasList');
    notasFiscais.forEach((nota) => {
      const li = document.createElement('li');
      li.innerHTML = `
        <strong>CPF/CNPJ:</strong> ${nota.cpf} <br>
        <strong>Serviço:</strong> ${nota.servico} <br>
        <strong>Valor:</strong> ${nota.valor}
      `;
      notasList.appendChild(li);
    });
  }
  
  // Função para o botão "Voltar"
  function voltar() {
    window.location.href = 'menu.html';
  }
  
  // Chama a função para carregar as notas ao abrir a página
  carregarNotas();
  