# Documentation – RUSHIFY Client Lourd

**Application de bureau d'administration RUSHIFY**  
Version 1.0 | Technologies : Python 3.13 · tkinter · MySQL

---

## Sommaire

1. [Présentation](#1-présentation)
2. [Installation et lancement](#2-installation)
3. [Structure du projet](#3-structure)
4. [Écrans et fonctionnalités](#4-écrans)
5. [Architecture technique](#5-architecture)

---

## 1. Présentation

Le **client lourd RUSHIFY Admin** est une application de bureau native permettant aux administrateurs de gérer la plateforme RUSHIFY directement depuis leur machine, sans passer par un navigateur web.

**Avantages d'un client lourd :**
- Fonctionne sans serveur web intermédiaire
- Connexion directe à la base de données MySQL
- Interface native Windows
- Démarrage rapide

---

## 2. Installation

### Prérequis
- Python 3.13+
- MySQL 8.4 avec la base `rushify_db`

### Installation des dépendances

```bash
pip install mysql-connector-python bcrypt
```

### Lancement

```bash
python app.py
```

Ou double-cliquer sur **`RUSHIFY Admin.bat`** sur le Bureau.

### Identifiants

| Champ | Valeur |
|---|---|
| Identifiant | `superadmin` |
| Mot de passe | `Admin@Rushify2025` |

---

## 3. Structure du projet

```
rushify-admin-python/
├── app.py           → Application complète (point d'entrée)
├── README.md        → Guide rapide
└── DOCUMENTATION.md → Documentation complète
```

L'application est contenue dans un seul fichier `app.py` organisé en classes :

| Classe | Rôle |
|---|---|
| `LoginWindow` | Fenêtre de connexion |
| `AdminApp` | Fenêtre principale avec sidebar |
| Fonctions `show_*` | Affichage de chaque page |
| `query()` | Fonction utilitaire requêtes SQL |

---

## 4. Écrans

### 4.1 Écran de connexion

La fenêtre s'ouvre au lancement de l'application.

**Composants :**
- Logo RUSHIFY (éclair bordeaux + texte)
- Champ **Identifiant**
- Champ **Mot de passe** (masqué)
- Bouton **Se connecter** (bordeaux)
- Message d'erreur si identifiants incorrects

**Authentification :**
- Requête SQL sur la table `admin_users`
- Vérification du mot de passe avec **bcrypt**
- Mise à jour de `last_login_at` à chaque connexion

📸 *[Screenshot : Écran de connexion]*

---

### 4.2 Tableau de bord

Première page après connexion. Affiche une vue d'ensemble de RUSHIFY.

**Composants :**
- **4 cartes KPI** (fond coloré) :
  - 👥 Nombre total d'utilisateurs
  - ⚡ Ventes flash actives / total
  - 🛒 Nombre de réservations
  - 💶 Revenus totaux en €
- **Tableau "Top vendeurs"** : entreprise, nombre de flash sales, revenus
- **Liste "Dernières inscriptions"** : nom + email + date

**Source de données :** Vue SQL `vw_dashboard_stats` + requêtes dédiées.

📸 *[Screenshot : Tableau de bord]*

---

### 4.3 Gestion des utilisateurs

Liste paginée de tous les comptes professionnels inscrits.

**Composants :**
- **Barre de recherche** : filtre par nom, email ou SIRET
- **Tableau interactif** (ttk.Treeview) avec colonnes :
  - ID, Entreprise, Email, SIRET, Nb produits, Nb ventes, Vérifié, Inscription
- **Boutons d'action** sur la sélection :
  - ✅ **Vérifier** : marque le compte comme vérifié (`is_verified=1`)
  - 🗑️ **Supprimer** : supprime définitivement le compte (avec confirmation)

📸 *[Screenshot : Gestion utilisateurs]*

---

### 4.4 Ventes Flash

Liste de toutes les ventes flash avec gestion.

**Composants :**
- **Tableau** avec : ID, Titre, Vendeur, Prix flash, Statut, Date d'expiration
- **Boutons d'action** :
  - 🚫 **Annuler** : passe le statut à `cancelled` (si la vente est active)
  - ↻ **Actualiser** : recharge les données en temps réel

**Statuts gérés :**
- `active` : en cours
- `expired` : expirée naturellement
- `cancelled` : annulée par l'admin
- `sold_out` : épuisée

📸 *[Screenshot : Ventes Flash]*

---

### 4.5 Réservations

Historique complet de toutes les réservations de la plateforme.

**Colonnes affichées :**
- ID, Titre de la vente, Acheteur, Vendeur, Quantité, Total (€), Statut, Date

**Statuts :**
- `pending` : en attente de confirmation
- `confirmed` : confirmée
- `completed` : finalisée
- `cancelled` : annulée

📸 *[Screenshot : Réservations]*

---

### 4.6 Journal d'audit

Traçabilité de toutes les actions effectuées par les administrateurs.

**Colonnes :**
- Date/Heure, Admin, Action, Ressource, Description

**Types d'actions enregistrées :**
| Action | Description |
|---|---|
| `LOGIN` | Connexion d'un admin |
| `LOGOUT` | Déconnexion |
| `UPDATE` | Modification d'une ressource |
| `DELETE` | Suppression |
| `CREATE` | Création |

📸 *[Screenshot : Journal d'audit]*

---

## 5. Architecture technique

### Connexion à la base de données

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'rushify_db',
    'charset': 'utf8mb4'
}
```

Chaque requête ouvre et ferme une connexion (pool simple) via la fonction `query()` :

```python
def query(sql, params=None, fetch=True):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, params or ())
    if fetch:
        result = cur.fetchall()
    else:
        conn.commit()
    conn.close()
    return result
```

### Authentification

```python
import bcrypt
ok = bcrypt.checkpw(
    password.encode('utf-8'),
    admin['password_hash'].encode('utf-8')
)
```

### Interface graphique (tkinter)

- **`tk.Tk()`** : fenêtre principale
- **`ttk.Treeview`** : tableaux de données interactifs
- **`tk.Frame`** : organisation en sections
- **`ttk.Style`** : personnalisation des couleurs et polices

### Palette de couleurs

| Variable | Valeur | Usage |
|---|---|---|
| `BORDEAUX` | `#8B1A2F` | Boutons, accents |
| `BG` | `#1E3528` | Fond sidebar |
| `CARD` | `#FFFFFF` | Fond des cartes |
| `CARD_BG` | `#F5F5F5` | Fond de l'application |

---

## Lien avec le client léger

Le client lourd et le client léger **partagent la même base de données** `rushify_db`.

Toute action faite dans le client lourd (vérifier un utilisateur, annuler une vente) est **immédiatement reflétée** sur le site web, et vice-versa.

→ **Client léger** : https://github.com/soumeyamsr/PROJET-CLIENT-L-GER-

---

*Documentation RUSHIFY Client Lourd v1.0 — Projet académique EFREI*
