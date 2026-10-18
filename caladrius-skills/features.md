### Comment faire une feature!

#### On passe par uv et bun comme runtime python et Node.

- Vérifie dans le backend si la feature a déjà été implémentée. Quand elle est faite tu passes au frontend sinon tu proposes un plan détaillé pour implémenter la feature côté backend.

- Ensuite on passe par l'implémentation côté front. Tu vérifie s'il existe un store relatif à la feature, sinon tu le crées comme suit:

```js

    import defineStore from "pinia"

    export const featureStore = DefineStore('featureID',()=>{

        // Ux-ui

        // states

        // Getters

        // Actions

        return{
            
            // Ux-ui

            // states

            // Getters

            // Actions
        }
    })

```
Tu fais le proprement le crud dans le store puis tu l'utilises dans les composants, Jamais dans Pages.

- Pour les composants tu vérifies s'il y a des composants déjà créés, si oui tu les utilises sinon tu crées un module dans component dans lequel tu vas ajouter le composant créé.

- Pour l'ux/ui tu es expert webdesigner; nous avons une palette de couleurs déjà implémenté dans le fichier main.css tu les utilises en fonction des besoins relatifs au features. N'hésites pas à utiliser les composants dans tools pour faire 