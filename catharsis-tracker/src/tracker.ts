interface Config {
  siteId: string;
  debug?: boolean;
  dryRun?: boolean;
}

interface EventPayload {
  site_id: string;
  session_id: string;
  event_type: string;
  timestamp: string;
  url: string;
  [key: string]: unknown;
}

interface Window {
  Catharsis?: {
    trackEvent: (eventType: string, eventData?: Record<string, unknown>) => void;
  };
}

(function() {

  // State

  const script = document.currentScript;
  if (!script) return;

  const siteId = script.getAttribute('data-site-id');
  if (!siteId) {
    console.error('Catharsis: missing data-site-id');
    return;
  }

  const config: Config = {
    siteId,
    debug: script.getAttribute('data-debug') === 'true',
    dryRun: script.getAttribute('data-dry-run') === 'true',
  };

  // Génération session ID
  function getOrCreateSessionId(): string {
    let id = sessionStorage.getItem('catharsis_session_id');
    if (!id) {
      id = 'sess_' + Math.random().toString(36).substring(2);
      sessionStorage.setItem('catharsis_session_id', id);
    }
    return id;
  }

  // Ensuite, dans le code principal :
  const sessionId = getOrCreateSessionId();

  function sendEvent(eventType: string, eventData: Record<string, unknown> = {}) {
    const payload: EventPayload = {
      site_id: config.siteId,
      session_id: sessionId,
      event_type: eventType,
      timestamp: new Date().toISOString(),
      url: window.location.href,
      ...eventData,
    };

    if (config.debug) {
      console.log(`[Catharsis] ${eventType}`, payload);
    }

    if (!config.dryRun) {
      // Ici tu ajouteras fetch / sendBeacon plus tard
    }
  }

  // Une fois que tout est prêt, on peut envoyer un événement de page view. On dit que la page a été vue.
  sendEvent('page_view');

  // Ici j'ajoute tous les écouteurs d'événements que je veux tracker. Par exemple, pour les doubles clics :
  document.addEventListener('dblclick', (e: MouseEvent) => {
    const target = e.target as HTMLElement;
    sendEvent('double_click', {
      tag: target.tagName,
      id: target.id,
      className: target.className,
    });
  });

  window.Catharsis = { trackEvent: sendEvent };
})();