// Atualizar Pontuação e Progresso
document.addEventListener("DOMContentLoaded", () => {
    const totalPontos = 1250; // Exemplo: Puxar do backend
    const pontosParaRecompensa = 2000;
    const progresso = Math.min((totalPontos / pontosParaRecompensa) * 100, 100);
  
    document.getElementById("pontuacao").textContent = totalPontos;
    document.getElementById("pontos-faltantes").textContent = pontosParaRecompensa - totalPontos;
  
    const barraProgresso = document.querySelector(".progresso");
    barraProgresso.style.width = `${progresso}%`;
  });
  