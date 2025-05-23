/**
 * script.js - Language control and main functionalities
 * @version 1.5
 * @description Manages language switching and user preferences for all pages, with added debugging
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
    // or if it's the home page (empty cleanPath or 'index.html')
    if (cleanPath.endsWith(fileName + '.html') || (fileName === 'index' && (cleanPath === '' || cleanPath === 'index.html'))) {
      console.log(`DEBUG: getCurrentPageIdentifier detected: ${identifier} for cleanPath: "${cleanPath}"`);
      return identifier;
    }
  }
  console.log(`DEBUG: getCurrentPageIdentifier returning 'home' as default for cleanPath: "${cleanPath}"`);
  return 'home'; // Default to home if no match
}

/**
 * Determines the current active language based on the URL.
 * @returns {string} 'pt' or 'en'
 */
function getCurrentLanguage() {
  const currentLang = window.location.pathname.includes('/en/') ? 'en' : 'pt';
  console.log(`DEBUG: getCurrentLanguage detected: ${currentLang}`);
  return currentLang;
}

/**
 * Switches between languages and stores preference
 * @param {string} lang - Language code (pt/en)
 */
function switchLanguage(lang) {
  if (languageConfig[lang]) {
    // Store preference
    localStorage.setItem(languageConfig[lang].storageKey, lang);
    console.log(`DEBUG: Preferred language set to: ${lang} in localStorage.`);

    // Get current page identifier
    const currentPage = getCurrentPageIdentifier();
    const currentLanguage = getCurrentLanguage();

    // Only redirect if changing to a different language
    if (lang !== currentLanguage) {
      // Redirect to the selected language version
      if (languageConfig[lang].path[currentPage]) {
        const targetUrl = languageConfig[lang].path[currentPage];
        console.log(`DEBUG: Redirecting from ${currentLanguage} to ${lang} page: ${targetUrl}`);
        window.location.href = targetUrl;
      } else {
        // Fallback to home if page not found in config
        const targetUrl = languageConfig[lang].path['home'];
        console.log(`DEBUG: Page not found in config for ${lang}/${currentPage}, falling back to home: ${targetUrl}`);
        window.location.href = targetUrl;
      }
    } else {
      console.log(`DEBUG: Already on ${lang} page, no redirect needed.`);
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
  console.log(`DEBUG: applyPreferredLanguage - Preferred language from localStorage: ${preferredLanguage}`);

  if (!preferredLanguage) {
    console.log('DEBUG: No preferred language set in localStorage. Skipping redirection.');
    return; // No preferred language set
  }

  const currentLanguage = getCurrentLanguage();
  const currentPage = getCurrentPageIdentifier();

  // If preferred language is different from current page's language, redirect
  if (preferredLanguage !== currentLanguage) {
    const targetPath = languageConfig[preferredLanguage].path[currentPage] || languageConfig[preferredLanguage].path['home'];
    console.log(`DEBUG: Mismatch detected! Preferred: ${preferredLanguage}, Current: ${currentLanguage}. Redirecting to: ${targetPath}`);
    window.location.href = targetPath;
  } else {
    console.log(`DEBUG: Preferred language (${preferredLanguage}) matches current page language (${currentLanguage}). No redirection needed.`);
  }
}

/**
 * Activates the current language button
 */
function setActiveLanguageButton() {
  const currentLanguage = getCurrentLanguage();
  const languageButtons = document.querySelectorAll('.language-btn');
  console.log(`DEBUG: Setting active button for language: ${currentLanguage}`);

  languageButtons.forEach(button => {
    button.classList.remove('active');
    const buttonLang = button.textContent.trim().toLowerCase();

    if (buttonLang === currentLanguage) {
      button.classList.add('active');
      console.log(`DEBUG: Activated button for: ${buttonLang}`);
    }
  });
}

/**
 * Initializes all functionalities when DOM is ready
 */
function init() {
  try {
    console.log('DEBUG: init() called. DOMContentLoaded event fired.');
    // Apply preferred language only if not already on the correct language page
    applyPreferredLanguage();
    setActiveLanguageButton();

    // Event listeners for language buttons
    document.querySelectorAll('.language-btn').forEach(button => {
      button.addEventListener('click', function() {
        const lang = this.textContent.trim().toLowerCase();
        console.log(`DEBUG: Language button clicked: ${lang}`);
        switchLanguage(lang);
      });
    });
  } catch (error) {
    console.error('Language initialization error:', error);
  }
}

// Wait for DOM to load before initializing
document.addEventListener('DOMContentLoaded', init);
