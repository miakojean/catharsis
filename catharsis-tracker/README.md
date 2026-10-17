# Catharsis Tracker

Le tracker Catharsis est un script JavaScript destiné à être installé sur un site web afin de suivre les visites et certaines interactions. Ce README décrit le parcours prévu pour un utilisateur et précise ce qui est effectivement opérationnel dans le code actuel.

## Parcours utilisateur

### 1. Créer un compte

Le nouvel utilisateur ouvre la page d’inscription de Catharsis et renseigne son adresse e-mail, un nom d’utilisateur/entreprise et un mot de passe. Le frontend envoie ces informations à `POST /account/customer/`.

### 2. Se connecter

L’utilisateur se connecte avec son adresse e-mail et son mot de passe. Après une connexion réussie, il est redirigé vers le tableau de bord.

### 3. Ajouter un site à suivre

Depuis le tableau de bord, l’utilisateur choisit **Enregistrer un site**. Une modale s’ouvre avec un formulaire pour saisir le nom du site ou de l’application web. Après validation, le frontend envoie le nom à `POST /event/`. Le backend crée le projet pour l’utilisateur connecté et génère un `site_id` unique. La confirmation affiche cet identifiant et permet de le copier.

Les sites enregistrés sont ensuite chargés dans l’espace de l’utilisateur. Le modèle backend stocke pour le moment le nom du projet, pas l’URL de son domaine.

La génération et l’enregistrement du projet sont opérationnels. L’affichage du code d’installation et la réception des événements sont des étapes distinctes qui restent à mettre en place.

### 4. Installer le script — quand le projet et l’hébergement du tracker seront prêts

Le code d’installation prendra cette forme, avec les valeurs fournies par Catharsis :

```html
<script
  src="URL_PUBLIQUE_DU_TRACKER"
  data-site-id="IDENTIFIANT_DU_SITE">
</script>
```

`URL_PUBLIQUE_DU_TRACKER` et `IDENTIFIANT_DU_SITE` sont des valeurs à remplacer : l’URL publique du script dépendra de son hébergement, et l’identifiant devra être celui généré pour le projet. Le projet du tracker compile actuellement `src/tracker.ts` dans `dist/tracker.js` avec `npm run build`; le déploiement de ce fichier sur une URL publique reste à configurer.

### 5. Consulter les données

Une fois la collecte et la réception des événements raccordées, l’utilisateur pourra retrouver les données de son site dans le tableau de bord. Tant qu’aucun événement ne remonte, celui-ci affiche un état vide.

## État actuel de la collecte

Le script lit `data-site-id` et crée un identifiant de session conservé dans `sessionStorage`. Il prépare automatiquement les événements suivants :

- `page_view` au chargement de la page ;
- `click` lors d’un clic ;
- `form_submit` lors de l’envoi d’un formulaire ;
- `scroll_bottom_reached` lorsque le visiteur arrive près du bas de la page.

Les intégrations peuvent aussi appeler l’API du navigateur :

```js
window.Catharsis?.trackEvent('inscription_terminee', {
  plan: 'standard'
})
```

**Important : le code prépare actuellement les événements mais ne les envoie pas au backend.** L’envoi réseau est encore indiqué comme TODO dans `src/tracker.ts`. Le endpoint actuel `/event/` gère les projets et ne constitue pas encore une API de réception des événements du tracker. Il faut donc implémenter et configurer cette réception avant de considérer la collecte comme active.

## Développement

Depuis le dossier `catharsis-tracker` :

```bash
npm install
npm run build
```

La compilation TypeScript génère le script dans `dist/tracker.js`. Le script de test du projet n’est pas encore configuré.