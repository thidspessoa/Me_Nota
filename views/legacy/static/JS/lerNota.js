    // Simula um banco de dados com notas fiscais
const notasFiscais = [
    { codigo: '12345', detalhes: 'Nota Fiscal emitida para Cliente A, valor R$1000,00.' },
    { codigo: '67890', detalhes: 'Nota Fiscal emitida para Cliente B, valor R$500,00.' },
    { codigo: '11223', detalhes: 'Nota Fiscal emitida para Cliente C, valor R$750,00.' },
  ];
  
  // Função para buscar uma nota fiscal
  function buscarNotaFiscal() {
    const inputCodigo = document.getElementById('codigoNota').value.trim();
    const resultadoDiv = document.getElementById('resultadoNota');
  
    const notaEncontrada = notasFiscais.find(nota => nota.codigo === inputCodigo);
  
    if (notaEncontrada) {
      resultadoDiv.innerHTML = `
        <p><strong>Nota Fiscal Encontrada:</strong></p>
        <p>${notaEncontrada.detalhes}</p>
      `;
      resultadoDiv.style.color = 'green';
    } else {
      resultadoDiv.innerHTML = `
        <p><strong>Nota Fiscal não encontrada. Verifique o código informado.</strong></p>
      `;
      resultadoDiv.style.color = 'red';
    }
  }
  
  // Adiciona um evento ao botão "Ler Nota"
  document.getElementById('lerNotaButton').addEventListener('click', buscarNotaFiscal);
  
  // Função para o botão "Voltar"
  function voltar() {
    window.location.href = '../Telas/telaPrincipal.html'; // Substitua por window.history.back() para voltar ao histórico
  }
  