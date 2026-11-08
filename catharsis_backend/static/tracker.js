"use strict";
(function () {
    const script = document.currentScript;
    if (!script)
        return;
    const siteId = script.getAttribute('data-site-id');
    if (!siteId) {
        console.error('Catharsis: missing data-site-id');
        return;
    }
    const config = {
        siteId,
        debug: script.getAttribute('data-debug') === 'true',
        dryRun: script.getAttribute('data-dry-run') === 'true',
    };
    function createSessionId() {
        if (window.crypto.randomUUID) {
            return window.crypto.randomUUID();
        }
        const bytes = new Uint8Array(16);
        if (window.crypto.getRandomValues) {
            window.crypto.getRandomValues(bytes);
        }
        else {
            for (let index = 0; index < bytes.length; index += 1) {
                bytes[index] = Math.floor(Math.random() * 256);
            }
        }
        bytes[6] = (bytes[6] & 0x0f) | 0x40;
        bytes[8] = (bytes[8] & 0x3f) | 0x80;
        const hex = Array.from(bytes, byte => {
            const value = byte.toString(16);
            return value.length === 1 ? `0${value}` : value;
        }).join('');
        return `${hex.slice(0, 8)}-${hex.slice(8, 12)}-${hex.slice(12, 16)}-${hex.slice(16, 20)}-${hex.slice(20)}`;
    }
    function getOrCreateSessionId() {
        let id = sessionStorage.getItem('catharsis_session_id');
        if (!id || !/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id)) {
            id = createSessionId();
            sessionStorage.setItem('catharsis_session_id', id);
        }
        return id;
    }
    const sessionId = getOrCreateSessionId();
    function sendEvent(eventType, eventData = {}) {
        const payload = {
            site_id: config.siteId,
            session_id: sessionId,
            event_type: eventType,
            client_timestamp: new Date().toISOString(),
            url: window.location.href,
            properties: eventData,
        };
        if (config.debug) {
            console.log(`[Catharsis] ${eventType}`, payload);
        }
        if (!config.dryRun) {
            const endpoint = 'http://localhost:8000/event/track-event/';
            const payloadString = JSON.stringify(payload);
            try {
                if (navigator.sendBeacon) {
                    const blob = new Blob([payloadString], { type: 'application/json' });
                    navigator.sendBeacon(endpoint, blob);
                }
                else {
                    fetch(endpoint, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: payloadString,
                        keepalive: true
                    });
                }
            }
            catch (error) {
                if (config.debug) {
                    console.error('[Catharsis] Erreur lors de l\'envoi de l\'événement:', error);
                }
            }
        }
    }
    sendEvent('page_view', { referrer: document.referrer });
    document.addEventListener('click', (e) => {
        const target = e.target;
        sendEvent('click', {
            tag: target.tagName,
            id: target.id,
            className: target.className,
        });
    });
    document.addEventListener('submit', (e) => {
        const target = e.target;
        sendEvent('form_submit', {
            tag: target.tagName,
            formId: target.id,
            className: target.className,
        });
    });
    let hasReachedBottom = false;
    document.addEventListener('scroll', () => {
        if (hasReachedBottom)
            return;
        const scrollPosition = window.innerHeight + window.scrollY;
        const pageHeight = document.body.offsetHeight;
        if (scrollPosition >= pageHeight - 50) {
            sendEvent('scroll_bottom_reached');
            hasReachedBottom = true;
        }
    });
    window.Catharsis = { trackEvent: sendEvent };
})();
