/**
 * script.js - Language control and main functionalities
 * @version 1.4
 * @description Manages language switching and user preferences for all pages
 */

// Supported language configuration for all pages
const languageConfig = {
  'pt': {
    path: {
      'home': '/index.html',
      'petbot': '/petbot.html',
      'apod': '/apod.html',
      'covid_atual': '/covid_atual.html',
      'covid_historico': '/covid_historico.html',
      'clima': '/clima.html',
      'triand': '/triand.html'
    },
    storageKey: 'preferredLanguage'
  },
  'en': {
    path: {
      'home': '/en/index.html',
      'petbot': '/en/petbot.html',
      'apod': '/en/apod.html',
      'covid_atual': '/en/covid_atual.html',
      'covid_historico': '/en/covid_historico.html',
      'clima': '/en/clima.html',
      'triand': '/en/triand.html'
    },
    storageKey: 'preferredLanguage'
  }
};

/**
 * Gets the current page identifier based on URL.
 * Improved to handle similar page names more accurately.
 */
function getCurrentPageIdentifier() {
  const path = window.location.pathname;
  // Remove leading/trailing slashes and potential '/en/' prefix
  const cleanPath = path.replace(/^\/(en\/)?|\/$/g, '');

  // Map of file names (without extension) to identifiers
  const pageMap = {
    'index': 'home',
    'petbot': 'petbot',
    'apod': 'apod',
    'covid_atual': 'covid_atual',
    'covid_historico': 'covid_historico',
    'clima': 'clima',
    'triand': 'triand'
  };

  for (const [fileName, identifier] of Object.entries(pageMap)) {
    // Check if the cleanPath ends with the fileName (e.g., 'index' for 'index.html')
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
  return window.location.pathname.includes('/en/') ? 'en' : 'pt';
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
    const currentPage = getCurrentPageIdentifier();
    const currentLanguage = getCurrentLanguage();

    // Only redirect if changing to a different language
    if (lang !== currentLanguage) {
      // Redirect to the selected language version
      if (languageConfig[lang].path[currentPage]) {
        window.location.href = languageConfig[lang].path[currentPage];
      } else {
        // Fallback to home if page not found in config
        window.location.href = languageConfig[lang].path['home'];
      }
    }
  }
}

/**
 * Applies user's preferred language on initial load.
 * This function only redirects if the current page's language
 * does not match the preferred language.
 */
function applyPreferredLanguage() {
  const preferredLanguage = localStorage.getItem('preferredLanguage');
  if (!preferredLanguage) return; // No preferred language set

  const currentLanguage = getCurrentLanguage();
  const currentPage = getCurrentPageIdentifier();

  // If preferred language is different from current page's language, redirect
  if (preferredLanguage !== currentLanguage) {
    const targetPath = languageConfig[preferredLanguage].path[currentPage] || languageConfig[preferredLanguage].path['home'];
    window.location.href = targetPath;
  }
}

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
    // Apply preferred language only if not already on the correct language page
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
