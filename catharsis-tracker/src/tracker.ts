// ==========================================
// DÉFINITION DES TYPES (TypeScript)
// ==========================================

// Définit la structure de la configuration de notre tracker
interface Config {
  siteId: string;
  debug?: boolean;
  dryRun?: boolean;
}

// Définit la structure des données envoyées lors d'un événement (le payload)
interface EventPayload {
  site_id: string;
  session_id: string;
  event_type: string;
  timestamp: string; // Heure exacte au format ISO
  url: string;       // Page sur laquelle l'événement s'est produit
  [key: string]: unknown; // Permet d'ajouter n'importe quelle autre donnée dynamique (tag, id, etc.)
}

// Étend l'objet global "Window" du navigateur pour y déclarer notre tracker
// Cela permet à TypeScript de savoir que window.Catharsis existe et est valide
interface Window {
  Catharsis?: {
    trackEvent: (eventType: string, eventData?: Record<string, unknown>) => void;
  };
}

// ==========================================
// LOGIQUE PRINCIPALE DU TRACKER
// ==========================================

// IIFE (Immediately Invoked Function Expression)
// On encapsule tout le code dans une fonction anonyme qui s'exécute immédiatement.
// Cela évite de polluer l'espace global du navigateur avec nos variables.
(function() {

  // --- 1. INITIALISATION ET CONFIGURATION ---

  // Récupère la balise <script> qui est en train d'exécuter ce code
  const script = document.currentScript;
  if (!script) return; // Sécurité : si on ne trouve pas le script, on arrête tout

  // Récupère l'ID du site défini dans l'attribut data-site-id="..." du HTML
  const siteId = script.getAttribute('data-site-id');
  if (!siteId) {
    // Le siteId est obligatoire, on lève une erreur s'il est absent
    console.error('Catharsis: missing data-site-id');
    return;
  }

  // Construit l'objet de configuration en lisant les attributs de la balise script
  const config: Config = {
    siteId,
    // On convertit les chaînes de caractères "true" en vrais booléens
    debug: script.getAttribute('data-debug') === 'true',
    dryRun: script.getAttribute('data-dry-run') === 'true',
  };


  // --- 2. GESTION DE LA SESSION ---

  // Fonction pour récupérer ou créer un identifiant de session unique
  function getOrCreateSessionId(): string {
    // On cherche un ID existant dans le stockage de session du navigateur
    let id = sessionStorage.getItem('catharsis_session_id');

    if (!id) {
      // S'il n'existe pas, on en génère un aléatoire (ex: sess_a1b2c3d4)
      id = 'sess_' + Math.random().toString(36).substring(2);
      // Et on le sauvegarde pour la durée de la session
      sessionStorage.setItem('catharsis_session_id', id);
    }
    return id;
  }

  // Initialisation de l'identifiant de session pour ce visiteur
  const sessionId = getOrCreateSessionId();


  // --- 3. MOTEUR D'ENVOI D'ÉVÉNEMENTS ---

  // Fonction centrale pour préparer et expédier un événement
  function sendEvent(eventType: string, eventData: Record<string, unknown> = {}) {

    // Construction du paquet de données (payload)
    const payload: EventPayload = {
      site_id: config.siteId,
      session_id: sessionId,
      event_type: eventType,
      timestamp: new Date().toISOString(), // Horodatage précis
      url: window.location.href,           // URL active au moment de l'événement
      ...eventData,                        // Fusionne les données supplémentaires passées en paramètre
    };

    // Si le mode debug est activé (data-debug="true"), on affiche l'action dans la console
    if (config.debug) {
      console.log(`[Catharsis] ${eventType}`, payload);
    }

    // Si le mode dryRun n'est PAS activé, on procède à l'envoi réel
    if (!config.dryRun) {
      // TODO: Ici tu ajouteras fetch() ou navigator.sendBeacon() plus tard
      // pour envoyer 'payload' vers ton serveur de base de données.
    }
  }


  // --- 4. SUIVI AUTOMATIQUE (AUTO-TRACKING) ---

  // Une fois que tout est prêt, on envoie automatiquement un événement "page_view"
  // pour indiquer que l'utilisateur vient d'afficher ou recharger la page
  sendEvent('page_view');

  // Ajout d'écouteurs d'événements globaux pour traquer les actions des utilisateurs.
  // Exemple : on écoute tous les clics sur la page entière.
  document.addEventListener('click', (e: MouseEvent) => {
    const target = e.target as HTMLElement; // L'élément précis qui a été cliqué

    // On envoie un événement "double_click" avec des détails sur l'élément cliqué
    sendEvent('click', {
      tag: target.tagName,
      id: target.id,
      className: target.className,
    });
  });

  // Tracker les soumissions de formulaires
  document.addEventListener('submit', (e: SubmitEvent) => {
    const target = e.target as HTMLFormElement;
    sendEvent('form_submit', {
      tag: target.tagName,
      formId: target.id,
      className: target.className,
    });
  });

  // NOUVEAU : Détection du défilement jusqu'au bas de la page
  let hasReachedBottom = false; // Drapeau pour éviter d'envoyer l'événement en boucle

  document.addEventListener('scroll', () => {
    // Si l'événement a déjà été envoyé pour cette lecture, on arrête l'exécution
    if (hasReachedBottom) return;

    // On calcule la position actuelle par rapport à la hauteur totale du document
    const scrollPosition = window.innerHeight + window.scrollY;
    const pageHeight = document.body.offsetHeight;

    // Si l'utilisateur est à 50 pixels ou moins du bas de page
    if (scrollPosition >= pageHeight - 50) {
      sendEvent('scroll_bottom_reached');
      hasReachedBottom = true; // Verrouille l'envoi
    }
  });


  // --- 5. EXPOSITION PUBLIQUE (API) ---

  // On attache notre fonction sendEvent à l'objet global window.Catharsis
  // Cela permet à d'autres scripts (comme ton main.js) d'appeler manuellement :
  // window.Catharsis.trackEvent('mon_action_personnalisée');
  window.Catharsis = { trackEvent: sendEvent };

})();
