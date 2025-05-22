/**
 * script.js - Controle de idiomas e funcionalidades principais
 * @version 1.1
 * @description Gerencia troca de idiomas e preferências do usuário
 */

// Configuração de idiomas suportados
const languageConfig = {
  'pt': {
    path: '../index.html',
    storageKey: 'preferredLanguage'
  },
  'en': {
    path: 'en/index.html',
    storageKey: 'preferredLanguage'
  }
};

/**
 * Alterna entre idiomas e armazena preferência
 * @param {string} lang - Código do idioma (pt/en)
 */
function switchLanguage(lang) {
  if (languageConfig[lang]) {
    // Armazena preferência
    localStorage.setItem(languageConfig[lang].storageKey, lang);
    
    // Redireciona para a página no idioma selecionado
    window.location.href = languageConfig[lang].path;
  }
}

/**
 * Aplica o idioma preferido do usuário
 */
function applyPreferredLanguage() {
  const preferredLanguage = localStorage.getItem('preferredLanguage');
  const currentPath = window.location.pathname;
  
  // Verifica se precisa redirecionar
  if (preferredLanguage) {
    const shouldRedirectToPT = preferredLanguage === 'pt' && currentPath.includes('/en/');
    const shouldRedirectToEN = preferredLanguage === 'en' && !currentPath.includes('/en/');
    
    if (shouldRedirectToPT) {
      window.location.href = languageConfig.pt.path;
    } else if (shouldRedirectToEN) {
      window.location.href = languageConfig.en.path;
    }
  }
}

/**
 * Ativa o botão do idioma atual
 */
function setActiveLanguageButton() {
  const currentPath = window.location.pathname;
  const languageButtons = document.querySelectorAll('.language-btn');
  const isEnglish = currentPath.includes('/en/');
  
  languageButtons.forEach(button => {
    button.classList.remove('active');
    
    if ((isEnglish && button.textContent === 'EN') || 
        (!isEnglish && button.textContent === 'PT')) {
      button.classList.add('active');
    }
  });
}

/**
 * Inicializa todas as funcionalidades quando o DOM estiver pronto
 */
function init() {
  applyPreferredLanguage();
  setActiveLanguageButton();
  
  // Event listeners para os botões de idioma
  document.querySelectorAll('.language-btn').forEach(button => {
    button.addEventListener('click', function() {
      const lang = this.textContent.trim().toLowerCase();
      switchLanguage(lang);
    });
  });
}

// Aguarda o carregamento do DOM para iniciar
document.addEventListener('DOMContentLoaded', init);
