/**
 * script.js - Language control and main functionalities
 * @version 1.7
 * @description Manages language switching for all pages (without preference storage)
 */

// Supported language configuration for all pages
const languageConfig = {
  'pt': {
    path: {
      'home': '/index.html',
      'petbot': '/pt/petbot.html',
      'apod': '/pt/apod.html',
      'covid_atual': '/pt/covid_atual.html',
      'covid_historico': '/pt/covid_historico.html',
      'clima': '/pt/clima.html',
      'triand': '/pt/triand.html',
      'wow': '/pt/wow.html'
    },
    // storageKey: 'preferredLanguage' // Removido
  },
  'en': {
    path: {
      'home': '/en/index.html',
      'petbot': '/en/petbot.html',
      'apod': '/en/apod.html',
      'covid_atual': '/en/covid_atual.html',
      'covid_historico': '/en/covid_historico.html',
      'clima': '/en/clima.html',
      'triand': '/en/triand.html',
      'wow': '/en/wow.html'
    },
    // storageKey: 'preferredLanguage' // Removido
  }
};

/**
 * Gets the current page identifier based on URL.
 * Improved to handle similar page names more accurately.
 */
function getCurrentPageIdentifier() {
  const path = window.location.pathname;
  const cleanPath = path.replace(/^\/(en\/)?|\/$/g, '');

  const pageMap = {
    'index': 'home',
    'petbot': 'petbot',
    'apod': 'apod',
    'covid_atual': 'covid_atual',
    'covid_historico': 'covid_historico',
    'clima': 'clima',
    'triand': 'triand',
    'wow': 'wow'
  };

  for (const [fileName, identifier] of Object.entries(pageMap)) {
    if (cleanPath.endsWith(fileName + '.html') || (fileName === 'index' && (cleanPath === '' || cleanPath === 'index.html'))) {
      return identifier;
    }
  }
  return 'home'; // Default to home if no match
}

/**
 * Determines the current active language based on the URL.
 * @returns {string} 'pt' or 'en'
 */
function getCurrentLanguage() {
  const currentLang = window.location.pathname.includes('/en/') ? 'en' : 'pt';
  return currentLang;
}

/**
 * Switches between languages
 * @param {string} lang - Language code (pt/en)
 */
function switchLanguage(lang) {
  if (languageConfig[lang]) {
    // A linha 'localStorage.setItem()' foi removida daqui!
    
    const currentPage = getCurrentPageIdentifier();
    const currentLanguage = getCurrentLanguage();

    // Only redirect if changing to a different language
    if (lang !== currentLanguage) {
      if (languageConfig[lang].path[currentPage]) {
        window.location.href = languageConfig[lang].path[currentPage];
      } else {
        window.location.href = languageConfig[lang].path['home'];
      }
    }
  }
}

// A função applyPreferredLanguage() foi completamente removida!

/**
 * Activates the current language button
 */
function setActiveLanguageButton() {
  const currentLanguage = getCurrentLanguage();
  const languageButtons = document.querySelectorAll('.language-btn');

  languageButtons.forEach(button => {
    button.classList.remove('active');
    const buttonLang = button.textContent.trim().toLowerCase();

    if (buttonLang === currentLanguage) {
      button.classList.add('active');
    }
  });
}

/**
 * Initializes all functionalities when DOM is ready
 */
function init() {
  try {
    // applyPreferredLanguage() foi removido daqui!
    setActiveLanguageButton();
    
    // Event listeners for language buttons
    document.querySelectorAll('.language-btn').forEach(button => {
      button.addEventListener('click', function() {
        const lang = this.textContent.trim().toLowerCase();
        switchLanguage(lang);
      });
    });
  } catch (error) {
    console.error('Language initialization error:', error);
  }
}

// Wait for DOM to load before initializing
document.addEventListener('DOMContentLoaded', init);
