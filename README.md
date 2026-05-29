# RUSHIFY – Client Lourd (Back-Office Admin)

Application de bureau pour l'administration de la plateforme RUSHIFY.
Développée en **Python 3.13 + tkinter + MySQL**.

## Fonctionnalités

- 📊 **Tableau de bord** — KPIs en temps réel, top vendeurs, dernières inscriptions
- 👥 **Gestion utilisateurs** — Recherche, vérification SIRET, suspension, suppression
- ⚡ **Ventes Flash** — Liste complète, annulation
- 🛒 **Réservations** — Historique de toutes les réservations
- 📋 **Journal d'audit** — Traçabilité de toutes les actions admin

## Prérequis

- Python 3.13+
- MySQL 8.4 avec la base `rushify_db`
- Dépendances Python : `mysql-connector-python`, `bcrypt`

## Installation

```bash
pip install mysql-connector-python bcrypt
```

## Lancement

```bash
python app.py
```

## Connexion

Les identifiants de connexion sont transmis séparément à l'administrateur pour des raisons de sécurité.

## Technologies

| Technologie | Rôle |
|---|---|
| Python 3.13 | Langage principal |
| tkinter | Interface graphique desktop |
| mysql-connector-python | Connexion base de données |
| bcrypt | Hashage / vérification des mots de passe |

## Lien avec le client léger

Ce client lourd se connecte à la base `rushify_db` partagée avec le site web RUSHIFY.

→ **Client léger** : https://github.com/soumeyamsr/PROJET-CLIENT-L-GER-
