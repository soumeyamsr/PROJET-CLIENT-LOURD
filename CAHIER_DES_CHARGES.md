Cahier des charges — RUSHIFY Admin (Client Lourd)
Projet académique EFREI Paris — 2025/2026


1. PRESENTATION DU PROJET
--------------------------

Dans le cadre du projet RUSHIFY, on a développé deux applications distinctes qui tournent sur la même base de données. Le site web gère la partie utilisateurs, et cette application bureau gère la partie administration. L'idée, c'est d'offrir aux admins un outil dédié, plus rapide à utiliser qu'une interface web, qui se connecte directement à la base sans passer par un navigateur.

RUSHIFY Admin est une application de bureau développée en Python avec tkinter. Elle est réservée aux administrateurs de la plateforme. Elle leur permet de surveiller l'activité en temps réel, gérer les comptes utilisateurs, intervenir sur les ventes flash et consulter l'historique complet des actions.

Tout ce que l'admin fait dans cette application est immédiatement visible sur le site web, parce que les deux projets partagent la même base de données MySQL.


2. POURQUOI UNE APPLICATION BUREAU
------------------------------------

Le choix d'une application bureau plutôt qu'un simple panel web s'explique par plusieurs raisons pratiques.

D'abord, ça permet de travailler en dehors du serveur web. L'admin n'a pas besoin que le serveur PHP soit démarré pour accéder aux données. Il se connecte directement à MySQL.

Ensuite, une application bureau est plus rapide et plus réactive qu'une page web pour des tâches répétitives comme la gestion de listes ou la vérification de comptes.

Enfin, c'est un outil réservé à un usage interne. Il n'est pas accessible depuis l'extérieur, ce qui réduit la surface d'attaque par rapport à un panel web exposé sur internet.


3. QUI UTILISE CETTE APPLICATION
----------------------------------

L'application est uniquement destinée aux administrateurs de la plateforme RUSHIFY. Ces personnes ont un compte dans la table admin_users de la base de données, avec un mot de passe sécurisé. Elles sont responsables de la bonne marche de la plateforme et doivent pouvoir intervenir rapidement en cas de problème.


4. CE QUE L'APPLICATION DOIT FAIRE
------------------------------------

4.1 Connexion

Au lancement, l'application affiche une fenêtre de connexion sobre avec le logo RUSHIFY, un champ identifiant, un champ mot de passe et un bouton pour se connecter. Les identifiants sont vérifiés dans la base de données. Le mot de passe est comparé avec bcrypt pour que ce soit sécurisé. Si les identifiants sont incorrects, un message d'erreur s'affiche en rouge. Si tout est bon, on passe directement au tableau de bord.

4.2 Tableau de bord

La première page après la connexion. Elle donne une vue d'ensemble rapide de ce qui se passe sur la plateforme.

En haut, quatre cartes affichent les chiffres clés du moment : le nombre total d'utilisateurs inscrits, combien de ventes flash sont actives en ce moment, le total des réservations effectuées et les revenus générés sur la plateforme. Ces données sont chargées directement depuis la base à chaque ouverture.

En dessous, deux sections côte à côte. À gauche, un tableau des meilleurs vendeurs avec leur nombre de ventes flash et leurs revenus. À droite, la liste des dernières personnes qui se sont inscrites sur la plateforme.

4.3 Gestion des utilisateurs

Cette page liste tous les comptes professionnels inscrits sur RUSHIFY. On a une barre de recherche en haut pour filtrer par nom d'entreprise, email ou numéro SIRET. Le tableau principal affiche pour chaque utilisateur son identifiant, le nom de son entreprise, son email, son SIRET, le nombre de produits en stock, le nombre de ventes flash créées, si son compte est vérifié ou non, et sa date d'inscription.

Quand on sélectionne une ligne dans le tableau, deux boutons apparaissent en bas. Le premier permet de vérifier le compte de l'utilisateur, ce qui lui donne accès à toutes les fonctionnalités du site. Le deuxième permet de supprimer le compte définitivement — une boîte de confirmation est affichée avant de faire quoi que ce soit.

4.4 Ventes flash

Cette page liste toutes les ventes flash qui existent dans la base, peu importe leur statut. Le tableau affiche l'identifiant de la vente, son titre, qui l'a publiée, le prix flash, le statut actuel et la date d'expiration.

Les statuts possibles sont : active pour une vente en cours, expired pour une vente arrivée à échéance, cancelled pour une vente annulée par un admin, et sold_out pour une vente dont le stock est épuisé.

Si on sélectionne une vente active, un bouton permet de l'annuler. Un bouton Actualiser recharge la liste pour voir les dernières ventes ajoutées depuis le site web.

4.5 Réservations

L'historique complet de toutes les réservations faites sur la plateforme. Pour chaque réservation on voit : le numéro, le titre de la vente flash concernée, l'acheteur, le vendeur, la quantité réservée, le montant total, le statut et la date.

Les statuts sont pending quand la réservation attend une confirmation, confirmed quand elle est validée, completed quand tout s'est bien passé, et cancelled si elle a été annulée.

4.6 Journal d'audit

Cette page est importante pour la traçabilité. Chaque action significative effectuée par un admin dans l'application est enregistrée automatiquement dans la base de données. Le journal affiche la date et l'heure exacte, quel admin a fait l'action, le type d'action, sur quelle ressource, et une courte description.

Les actions tracées sont les connexions et déconnexions des admins, les vérifications de comptes utilisateurs, les suppressions, les annulations de ventes flash, et toutes les autres interventions importantes.


5. ARCHITECTURE TECHNIQUE
---------------------------

L'application est intentionnellement simple dans sa structure. Tout le code est dans un seul fichier app.py. Ce choix a été fait pour faciliter la maintenance et la compréhension — pas besoin de naviguer entre dix fichiers pour comprendre comment fonctionne un écran.

Le fichier contient plusieurs classes. LoginWindow gère la fenêtre de connexion. AdminApp gère la fenêtre principale avec le menu latéral et la navigation entre les écrans. Chaque écran a sa propre fonction : show_dashboard, show_users, show_flash_sales, show_reservations, show_audit. La fonction query() centralise tous les appels à la base de données — elle ouvre une connexion, exécute la requête et ferme la connexion proprement.

Pour l'interface graphique, on utilise tkinter avec les widgets ttk notamment ttk.Treeview pour les tableaux. C'est la bibliothèque graphique intégrée à Python, ce qui évite d'avoir des dépendances lourdes à installer.

La connexion à MySQL se fait avec mysql-connector-python. Les mots de passe sont gérés avec la bibliothèque bcrypt.


6. CHARTE GRAPHIQUE
--------------------

L'interface a une palette de couleurs sobre et professionnelle qui correspond à l'identité visuelle de la plateforme RUSHIFY.

Le menu latéral est en vert foncé (#1E3528). Les boutons et les éléments d'accent sont en bordeaux (#8B1A2F). Les cartes de contenu sont sur fond blanc. Le fond général de l'application est en gris clair (#F5F5F5).


7. SECURITE
------------

La connexion de l'admin est sécurisée par bcrypt. Les mots de passe ne sont jamais stockés en clair dans la base — uniquement un hash. Lors de la connexion, bcrypt compare le mot de passe entré avec le hash stocké sans jamais reconstruire le mot de passe original.

L'application ne tourne qu'en local, sur la machine de l'administrateur. Elle n'est pas exposée sur internet. L'accès physique à la machine est donc la première barrière de sécurité.

Les identifiants de connexion ne sont pas stockés dans la documentation ni dans le code. Ils sont transmis séparément à l'administrateur.


8. CONTRAINTES TECHNIQUES
---------------------------

Il faut Python 3.13 minimum et MySQL 8.4 avec la base rushify_db déjà créée. Les dépendances à installer sont mysql-connector-python et bcrypt, les deux se téléchargent avec pip.

La base de données doit être la même que celle du site web RUSHIFY pour que les deux applications soient synchronisées.

Un fichier RUSHIFY Admin.bat est disponible sur le Bureau pour lancer l'application en double-cliquant dessus, sans avoir à ouvrir un terminal.


9. STRUCTURE DES FICHIERS
---------------------------

rushify-admin-python/
    app.py           tout le code de l'application
    README.md        guide de démarrage rapide
    DOCUMENTATION.md documentation technique complète
    CAHIER_DES_CHARGES.md  ce fichier


10. LIEN AVEC LE SITE WEB
---------------------------

Le client lourd et le site web RUSHIFY sont deux projets séparés mais ils fonctionnent sur la même base de données. Quand un admin vérifie un utilisateur depuis cette application, le compte est immédiatement accessible sur le site. Quand un utilisateur publie une vente flash depuis le site, elle apparaît immédiatement dans la liste des ventes flash de cette application.

Les deux projets se complètent : le site web est l'interface pour les professionnels, et cette application est l'outil de gestion pour les administrateurs.

Dépôt GitHub du site web : https://github.com/soumeyamsr/PROJET-CLIENT-L-GER-
Dépôt GitHub de cette application : https://github.com/soumeyamsr/PROJET-CLIENT-LOURD


---------------------------------------------------------------
RUSHIFY Admin — Cahier des charges v1.0 — Projet EFREI 2025/2026
---------------------------------------------------------------
