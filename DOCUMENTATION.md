Documentation - RUSHIFY Client Lourd
Application de bureau d'administration
Version 1.0 - Python 3.13 / tkinter / MySQL


---------------------------------------------------------------
PRESENTATION DU PROJET
---------------------------------------------------------------

Le client lourd RUSHIFY Admin est une application de bureau qui permet aux administrateurs de gérer toute la plateforme RUSHIFY directement depuis leur ordinateur. Contrairement au site web, cette application se connecte directement à la base de données MySQL sans passer par un navigateur ou un serveur web.

L'idée c'est d'avoir un outil réservé aux admins, plus rapide à utiliser, qui fonctionne en local et qui permet de gérer les utilisateurs, les ventes flash et les réservations de façon simple et efficace.


---------------------------------------------------------------
INSTALLATION ET LANCEMENT
---------------------------------------------------------------

Ce qu'il faut avant de commencer :
- Python 3.13 ou plus récent installé sur la machine
- MySQL 8.4 avec la base rushify_db déjà créée et remplie

Pour installer les dépendances nécessaires, ouvrir un terminal et taper :

    pip install mysql-connector-python bcrypt

Ensuite pour lancer l'application :

    python app.py

Il y a aussi un fichier RUSHIFY Admin.bat sur le Bureau qui lance tout automatiquement en double-cliquant dessus, c'est plus pratique.

Les identifiants de connexion admin :
    Identifiant : superadmin
    Mot de passe : Admin@Rushify2025


---------------------------------------------------------------
STRUCTURE DU PROJET
---------------------------------------------------------------

Le projet est volontairement simple, tout est dans un seul fichier app.py pour faciliter la maintenance et la compréhension.

    rushify-admin-python/
        app.py           -> tout le code de l'application
        README.md        -> guide de démarrage rapide
        DOCUMENTATION.md -> ce fichier

Dans app.py on trouve plusieurs classes qui gèrent chaque partie :
- LoginWindow s'occupe de la fenêtre de connexion
- AdminApp gère la fenêtre principale avec le menu latéral
- Les fonctions show_dashboard, show_users, etc. gèrent chaque page
- La fonction query() centralise tous les appels à la base de données


---------------------------------------------------------------
LES DIFFERENTS ECRANS
---------------------------------------------------------------


ECRAN DE CONNEXION

C'est la première chose qu'on voit au lancement. L'écran est sobre avec le logo RUSHIFY, deux champs pour entrer l'identifiant et le mot de passe, et un bouton pour se connecter.

Quand on clique sur Se connecter, l'application vérifie les identifiants dans la table admin_users de la base de données. Le mot de passe est comparé avec bcrypt pour que ce soit sécurisé. Si les identifiants sont bons, on passe au tableau de bord. Sinon un message d'erreur s'affiche en rouge.

[AJOUTER SCREENSHOT : Ecran de connexion]


TABLEAU DE BORD

C'est la page principale une fois connecté. Elle donne une vue d'ensemble rapide de ce qui se passe sur la plateforme.

En haut on a quatre cartes qui montrent les chiffres clés : le nombre d'utilisateurs inscrits, combien de ventes flash sont actives en ce moment, le total des réservations et les revenus générés sur la plateforme.

En dessous on a deux sections côte à côte. À gauche un tableau qui liste les meilleurs vendeurs avec leur nombre de ventes flash et leurs revenus. À droite une liste des dernières personnes qui se sont inscrites sur la plateforme.

Toutes ces données viennent directement de la base de données, donc c'est toujours à jour.

[AJOUTER SCREENSHOT : Tableau de bord]


GESTION DES UTILISATEURS

Cette page permet de voir et gérer tous les comptes professionnels inscrits sur RUSHIFY.

Il y a une barre de recherche en haut qui permet de filtrer par nom d'entreprise, email ou numéro SIRET. En dessous un grand tableau liste tous les utilisateurs avec leurs informations : leur identifiant, le nom de leur entreprise, leur email, leur SIRET, le nombre de produits qu'ils ont en stock, le nombre de ventes flash qu'ils ont créées, si leur compte est vérifié ou non, et la date à laquelle ils se sont inscrits.

Quand on sélectionne un utilisateur dans le tableau, deux boutons apparaissent en bas. Le premier permet de marquer le compte comme vérifié, ce qui lui donne accès à toutes les fonctionnalités. Le deuxième permet de supprimer le compte définitivement, mais une confirmation est demandée avant de faire ça.

[AJOUTER SCREENSHOT : Gestion des utilisateurs]


VENTES FLASH

Cette page liste toutes les ventes flash qui existent sur la plateforme, peu importe leur statut.

Le tableau affiche pour chaque vente : son identifiant, son titre, qui l'a publiée, le prix flash, le statut actuel et la date d'expiration.

Les statuts possibles sont active pour une vente en cours, expired pour une vente qui a atteint sa date limite, cancelled pour une vente annulée par un admin, et sold_out pour une vente dont le stock est épuisé.

Si on sélectionne une vente active, on peut l'annuler avec le bouton prévu. Un bouton Actualiser permet de recharger la liste pour voir les dernières ventes ajoutées.

[AJOUTER SCREENSHOT : Ventes Flash]


RESERVATIONS

Cette page donne accès à l'historique complet de toutes les réservations faites sur la plateforme.

Pour chaque réservation on voit : le numéro de la réservation, le titre de la vente flash concernée, le nom de l'acheteur, le nom du vendeur, la quantité réservée, le montant total payé, le statut et la date.

Les statuts sont pending quand la réservation attend une confirmation, confirmed quand elle est validée, completed quand tout s'est bien passé, et cancelled quand elle a été annulée.

[AJOUTER SCREENSHOT : Reservations]


JOURNAL D'AUDIT

Cette page est là pour garder une trace de tout ce que font les admins sur l'application. C'est important pour savoir qui a fait quoi et quand.

Chaque ligne du tableau montre la date et l'heure exacte de l'action, quel admin l'a faite, le type d'action (connexion, modification, suppression, création), sur quelle ressource ça a été fait, et une courte description.

Toutes les actions importantes sont enregistrées automatiquement : les connexions et déconnexions des admins, les vérifications ou suppressions de comptes utilisateurs, les annulations de ventes flash, etc.

[AJOUTER SCREENSHOT : Journal d'audit]


---------------------------------------------------------------
COMMENT CA MARCHE TECHNIQUEMENT
---------------------------------------------------------------

La connexion à la base de données se fait avec mysql-connector-python. Chaque fois qu'on a besoin de données, la fonction query() ouvre une connexion, fait la requête et referme la connexion. C'est simple et ça évite de garder des connexions ouvertes inutilement.

Pour les mots de passe, on utilise la bibliothèque bcrypt qui est le standard pour stocker des mots de passe de façon sécurisée. Quand l'admin se connecte, bcrypt compare le mot de passe entré avec le hash stocké en base sans jamais stocker le vrai mot de passe en clair.

L'interface graphique est faite avec tkinter qui est la bibliothèque graphique intégrée à Python. Les tableaux utilisent ttk.Treeview qui permet d'afficher des données en lignes et colonnes avec la possibilité de sélectionner et d'interagir avec les éléments.

La palette de couleurs choisie : vert foncé (#1E3528) pour le menu latéral, bordeaux (#8B1A2F) pour les boutons et accents, blanc pour les cartes de contenu et gris clair (#F5F5F5) pour le fond général.


---------------------------------------------------------------
LIEN AVEC LE SITE WEB
---------------------------------------------------------------

Le client lourd et le site web RUSHIFY utilisent exactement la même base de données. Donc tout ce qu'un admin fait dans cette application (vérifier un utilisateur, annuler une vente flash) est visible immédiatement sur le site web, et inversement.

Les deux projets sont complémentaires : le site web est l'interface pour les utilisateurs, et cette application est l'outil de gestion pour les administrateurs.

Site web (client léger) : https://github.com/soumeyamsr/PROJET-CLIENT-L-GER-


---------------------------------------------------------------
Documentation RUSHIFY Client Lourd v1.0 - Projet académique EFREI
---------------------------------------------------------------
