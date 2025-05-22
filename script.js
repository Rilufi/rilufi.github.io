/**
 * script.js - Language control and main functionalities
 * @version 1.3
 * @description Manages language switching and user preferences for all pages
 */

// Supported language configuration for all pages
const languageConfig = {
  'pt': {
    path: {
      'home': '../index.html',
      'petbot': '../petbot.html',
      'apod': '../apod.html',
      'covid_atual': '../covid_atual.html',
      'covid_historico': '../covid_historico.html',
      'clima': '../clima.html',
      'triand': '../triand.html'
    },
    storageKey: 'preferredLanguage'
  },
  'en': {
    path: {
      'home': 'en/index.html',
      'petbot': 'en/petbot.html',
      'apod': 'en/apod.html',
      'covid_atual': 'en/covid_atual.html',
      'covid_historico': 'en/covid_historico.html',
      'clima': 'en/clima.html',
      'triand': 'en/triand.html'
    },
    storageKey: 'preferredLanguage'
  }
};

/**
 * Gets the current page identifier based on URL
 */
function getCurrentPage() {
  const path = window.location.pathname;
  const pageMap = {
    'petbot': 'petbot',
    'apod': 'apod',
    'covid_atual': 'covid_atual',
    'covid_historico': 'covid_historico',
    'clima': 'clima',
    'triand': 'triand'
  };
  
  for (const [key, value] of Object.entries(pageMap)) {
    if (path.includes(key)) return value;
  }
  return 'home'; // Default to home if no match
}

/**
 * Switches between languages and stores preference
 * @param {string} lang - Language code (pt/en)
 */
function switchLanguage(lang) {
  if (languageConfig[lang]) {
    // Store preference
    localStorage.setItem(languageConfig[lang].storageKey, lang);
    
    // Get current page identifier
    const currentPage = getCurrentPage();
    
    // Redirect to the selected language version
    if (languageConfig[lang].path[currentPage]) {
      window.location.href = languageConfig[lang].path[currentPage];
    } else {
      // Fallback to home if page not found in config
      window.location.href = languageConfig[lang].path['home'];
    }
  }
}

/**
 * Applies user's preferred language
 */
function applyPreferredLanguage() {
  const preferredLanguage = localStorage.getItem('preferredLanguage');
  if (!preferredLanguage) return;

  const currentPath = window.location.pathname;
  const shouldRedirectToPT = preferredLanguage === 'pt' && currentPath.includes('/en/');
  const shouldRedirectToEN = preferredLanguage === 'en' && !currentPath.includes('/en/');
  
  if (shouldRedirectToPT || shouldRedirectToEN) {
    const currentPage = getCurrentPage();
    const targetLang = shouldRedirectToPT ? 'pt' : 'en';
    
    // Check if the target page exists in config
    if (languageConfig[targetLang].path[currentPage]) {
      window.location.href = languageConfig[targetLang].path[currentPage];
    } else {
      // Fallback to home if specific page not configured
      window.location.href = languageConfig[targetLang].path['home'];
    }
  }
}

/**
 * Activates the current language button
 */
function setActiveLanguageButton() {
  const currentPath = window.location.pathname;
  const languageButtons = document.querySelectorAll('.language-btn');
  const isEnglish = currentPath.includes('/en/');
  
  languageButtons.forEach(button => {
    button.classList.remove('active');
    const buttonLang = button.textContent.trim().toLowerCase();
    
    if ((isEnglish && buttonLang === 'en') || (!isEnglish && buttonLang === 'pt')) {
      button.classList.add('active');
    }
  });
}

/**
 * Initializes all functionalities when DOM is ready
 */
function init() {
  try {
    applyPreferredLanguage();
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
