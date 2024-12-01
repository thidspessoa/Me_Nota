/*function navigateTo(section) {
    if (section === 'emitir') {
      location.href = 'Telas/emitir.html';
    } else if (section === 'consultar') {
      location.href = 'Telas/consultar.html';
    }
  }
  // Navegar para a tela anterior
function navigateBack() {
    // Redireciona para o menu inicial
    window.location.href = "../Telas/menu.html"; // Caminho para o menu
  }*/

  // Função para navegar para diferentes seções
function navigateTo(section) {
  if (section === 'emitir') {
      location.href = 'Telas/emitir.html'; // Redireciona para a página de emitir
  } else if (section === 'consultar') {
      location.href = 'Telas/consultar.html'; // Redireciona para a página de consultar
  } else if (section === 'validar') {
      location.href = 'Telas/validar.html'; // Redireciona para a nova página de validar
  } else if (section === 'menu') {
      location.href = 'Telas/menu.html'; // Redireciona para o menu principal
  }
}

// Função para voltar à tela anterior
function navigateBack() {
  // Redireciona para o menu inicial
  window.location.href = "http://127.0.0.1:5501/MeNota-main/Me%20Nota/Telas/telaPrincipal.html?email=mwaoao%40llkds.com&senha=111111111111"; // Caminho relativo para o menu principal
}
