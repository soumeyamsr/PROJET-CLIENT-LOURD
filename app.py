"""
RUSHIFY Admin – Client Lourd
Interface d'administration desktop développée en Python + tkinter
"""
import tkinter as tk
from tkinter import ttk, messagebox, font
import mysql.connector
import hashlib
import threading
from datetime import datetime

# ── Connexion BDD ──────────────────────────────────────────────
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'rushify_db',
    'charset': 'utf8mb4'
}

session = {'admin': None}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def query(sql, params=None, fetch=True):
    try:
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute(sql, params or ())
        if fetch:
            result = cur.fetchall()
            conn.close()
            return result
        else:
            conn.commit()
            conn.close()
            return True
    except Exception as e:
        print(f"DB Error: {e}")
        return [] if fetch else False

# ── Couleurs & Styles ──────────────────────────────────────────
BG       = '#1E3528'
BG2      = '#162A1E'
SIDEBAR  = '#111E17'
CARD     = '#FFFFFF'
CARD_BG  = '#F5F5F5'
BORDEAUX = '#8B1A2F'
BORDEAUX2= '#7A1526'
GREEN    = '#2EA043'
TEXT     = '#111111'
MUTED    = '#666666'
WHITE    = '#FFFFFF'

# ── FENÊTRE LOGIN ──────────────────────────────────────────────
class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title('RUSHIFY Admin – Connexion')
        self.root.geometry('420x520')
        self.root.configure(bg=BG)
        self.root.resizable(False, False)
        # Centrer la fenêtre
        self.root.update_idletasks()
        w, h = 420, 520
        x = (self.root.winfo_screenwidth()  - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        self.root.geometry(f'{w}x{h}+{x}+{y}')
        self.build()

    def build(self):
        # Logo
        frame = tk.Frame(self.root, bg=BG, pady=40)
        frame.pack(fill='x')
        tk.Label(frame, text='⚡', font=('Segoe UI', 36), bg=BG, fg=BORDEAUX).pack()
        tk.Label(frame, text='RUSHIFY', font=('Segoe UI', 22, 'bold'), bg=BG, fg=WHITE).pack()
        tk.Label(frame, text='Administration Back-Office', font=('Segoe UI', 11), bg=BG, fg='#8A9E90').pack(pady=4)

        # Card
        card = tk.Frame(self.root, bg=CARD, padx=32, pady=28)
        card.pack(fill='both', expand=True, padx=24, pady=(0,24))

        self.error_lbl = tk.Label(card, text='', fg=BORDEAUX, bg=CARD, font=('Segoe UI', 10), wraplength=320)
        self.error_lbl.pack(pady=(0,8))

        # Identifiant
        tk.Label(card, text='Identifiant', font=('Segoe UI', 10, 'bold'), bg=CARD, fg=TEXT, anchor='w').pack(fill='x')
        self.user_entry = tk.Entry(card, font=('Segoe UI', 12), bd=1, relief='solid', fg=TEXT, insertbackground=TEXT)
        self.user_entry.pack(fill='x', ipady=8, pady=(4,16))
        self.user_entry.insert(0, 'superadmin')

        # Mot de passe
        tk.Label(card, text='Mot de passe', font=('Segoe UI', 10, 'bold'), bg=CARD, fg=TEXT, anchor='w').pack(fill='x')
        self.pass_entry = tk.Entry(card, show='•', font=('Segoe UI', 12), bd=1, relief='solid', fg=TEXT, insertbackground=TEXT)
        self.pass_entry.pack(fill='x', ipady=8, pady=(4,20))
        self.pass_entry.bind('<Return>', lambda e: self.login())

        # Bouton
        btn = tk.Button(card, text='Se connecter', font=('Segoe UI', 12, 'bold'),
                        bg=BORDEAUX, fg=WHITE, relief='flat', cursor='hand2',
                        activebackground=BORDEAUX2, activeforeground=WHITE,
                        command=self.login)
        btn.pack(fill='x', ipady=10)

        footer = tk.Label(card, text='RUSHIFY Admin v1.0 – Accès restreint',
                          font=('Segoe UI', 9), bg=CARD, fg=MUTED)
        footer.pack(pady=(16,0))

    def login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get()
        if not username or not password:
            self.error_lbl.config(text='Veuillez remplir tous les champs.')
            return
        rows = query(
            'SELECT au.*, ar.name role_name FROM admin_users au JOIN admin_roles ar ON au.role_id=ar.id WHERE au.username=%s AND au.is_active=1 LIMIT 1',
            (username,)
        )
        if rows:
            admin = rows[0]
            try:
                import bcrypt
                pwd_hash = admin['password_hash']
                if isinstance(pwd_hash, str):
                    pwd_hash = pwd_hash.encode('utf-8')
                ok = bcrypt.checkpw(password.encode('utf-8'), pwd_hash)
            except Exception as e:
                print(f"bcrypt error: {e}")
                ok = False
            if ok:
                session['admin'] = admin
                query('UPDATE admin_users SET last_login_at=NOW() WHERE id=%s', (admin['id'],), fetch=False)
                self.on_success()
                return
        self.error_lbl.config(text='Identifiants incorrects.')


# ── FENÊTRE PRINCIPALE ─────────────────────────────────────────
class AdminApp:
    def __init__(self, root):
        self.root = root
        self.root.title('RUSHIFY Admin – Tableau de bord')
        self.root.geometry('1200x750')
        self.root.configure(bg=CARD_BG)
        self.root.state('zoomed')
        self.current_page = None
        self.build()
        self.show_dashboard()

    def build(self):
        # Layout principal
        self.paned = tk.PanedWindow(self.root, orient='horizontal', sashwidth=0, bg=CARD_BG)
        self.paned.pack(fill='both', expand=True)

        # Sidebar
        self.sidebar = tk.Frame(self.paned, bg=SIDEBAR, width=220)
        self.paned.add(self.sidebar, minsize=220)

        # Logo
        logo_frame = tk.Frame(self.sidebar, bg=SIDEBAR, pady=16)
        logo_frame.pack(fill='x', padx=0)
        tk.Label(logo_frame, text='⚡  RUSHIFY Admin', font=('Segoe UI', 13, 'bold'),
                 bg=SIDEBAR, fg=WHITE, padx=18).pack(anchor='w')
        tk.Frame(self.sidebar, bg='#1F3A2A', height=1).pack(fill='x')

        # User info
        admin = session['admin']
        user_frame = tk.Frame(self.sidebar, bg=SIDEBAR, pady=12, padx=18)
        user_frame.pack(fill='x')
        tk.Label(user_frame, text=f"👤  {admin['full_name']}", font=('Segoe UI', 10, 'bold'),
                 bg=SIDEBAR, fg=WHITE).pack(anchor='w')
        tk.Label(user_frame, text=admin['role_name'], font=('Segoe UI', 9),
                 bg=SIDEBAR, fg='#7A9E82').pack(anchor='w')
        tk.Frame(self.sidebar, bg='#1F3A2A', height=1).pack(fill='x')

        # Navigation
        nav_items = [
            ('📊  Tableau de bord', self.show_dashboard),
            ('👥  Utilisateurs',    self.show_users),
            ('⚡  Ventes Flash',    self.show_flash),
            ('🛒  Réservations',    self.show_reservations),
            ('📋  Journal d\'audit', self.show_audit),
        ]
        tk.Label(self.sidebar, text='NAVIGATION', font=('Segoe UI', 8, 'bold'),
                 bg=SIDEBAR, fg='#5A7A62', padx=18, pady=10).pack(anchor='w')

        self.nav_buttons = {}
        for label, cmd in nav_items:
            btn = tk.Button(self.sidebar, text=label, font=('Segoe UI', 10),
                           bg=SIDEBAR, fg='#A0C0A8', relief='flat', anchor='w',
                           padx=18, pady=8, cursor='hand2',
                           activebackground='#1F3A2A', activeforeground=WHITE,
                           command=cmd)
            btn.pack(fill='x')
            self.nav_buttons[label] = btn

        # Déconnexion
        tk.Frame(self.sidebar, bg='#1F3A2A', height=1).pack(fill='x', side='bottom', pady=0)
        tk.Button(self.sidebar, text='🚪  Déconnexion', font=('Segoe UI', 10),
                  bg=SIDEBAR, fg='#C05070', relief='flat', anchor='w',
                  padx=18, pady=10, cursor='hand2',
                  command=self.logout).pack(fill='x', side='bottom')

        # Zone contenu
        self.content = tk.Frame(self.paned, bg=CARD_BG)
        self.paned.add(self.content)

    def set_active_nav(self, label):
        for lbl, btn in self.nav_buttons.items():
            if lbl == label:
                btn.config(bg='#2A4A35', fg=WHITE, font=('Segoe UI', 10, 'bold'))
            else:
                btn.config(bg=SIDEBAR, fg='#A0C0A8', font=('Segoe UI', 10))

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def make_header(self, title, subtitle=''):
        h = tk.Frame(self.content, bg=CARD_BG, pady=16, padx=28)
        h.pack(fill='x')
        tk.Label(h, text=title, font=('Segoe UI', 18, 'bold'), bg=CARD_BG, fg=TEXT).pack(anchor='w')
        if subtitle:
            tk.Label(h, text=subtitle, font=('Segoe UI', 10), bg=CARD_BG, fg=MUTED).pack(anchor='w')
        tk.Frame(self.content, bg='#E0E0E0', height=1).pack(fill='x', padx=28)

    def make_card(self, parent, **kwargs):
        c = tk.Frame(parent, bg=CARD, relief='flat', bd=1, **kwargs)
        return c

    # ── DASHBOARD ────────────────────────────────────────────
    def show_dashboard(self):
        self.clear_content()
        self.set_active_nav('📊  Tableau de bord')
        self.make_header('📊 Tableau de bord', 'Vue d\'ensemble en temps réel')

        scroll = tk.Frame(self.content, bg=CARD_BG)
        scroll.pack(fill='both', expand=True, padx=28, pady=16)

        # Charger les stats
        stats_row = query('SELECT * FROM vw_dashboard_stats')
        s = stats_row[0] if stats_row else {}

        # KPI Cards
        kpi_frame = tk.Frame(scroll, bg=CARD_BG)
        kpi_frame.pack(fill='x', pady=(0,16))

        kpis = [
            ('👥 Utilisateurs',      str(s.get('total_users',0)),      f"+{s.get('new_users_today',0)} aujourd'hui", '#1E7820'),
            ('⚡ Ventes Flash',      str(s.get('active_flash_sales',0)), f"{s.get('total_flash_sales',0)} au total",   BORDEAUX),
            ('🛒 Réservations',      str(s.get('total_reservations',0)),'',                                            '#1a5fc8'),
            ('💶 Revenus',           f"{float(s.get('total_revenue',0)):.2f} €",'',                                   '#8a6e00'),
        ]
        for i, (label, val, sub, color) in enumerate(kpis):
            card = tk.Frame(kpi_frame, bg=CARD, relief='flat', padx=18, pady=16)
            card.grid(row=0, column=i, padx=(0,12) if i<3 else 0, sticky='ew')
            kpi_frame.columnconfigure(i, weight=1)
            tk.Label(card, text=label, font=('Segoe UI', 10), bg=CARD, fg=MUTED).pack(anchor='w')
            tk.Label(card, text=val, font=('Segoe UI', 22, 'bold'), bg=CARD, fg=color).pack(anchor='w')
            if sub:
                tk.Label(card, text=sub, font=('Segoe UI', 9), bg=CARD, fg=MUTED).pack(anchor='w')

        # Top vendeurs
        cols_frame = tk.Frame(scroll, bg=CARD_BG)
        cols_frame.pack(fill='both', expand=True)
        cols_frame.columnconfigure(0, weight=2)
        cols_frame.columnconfigure(1, weight=1)

        # Tableau top vendeurs
        sellers_card = tk.Frame(cols_frame, bg=CARD, padx=18, pady=14)
        sellers_card.grid(row=0, column=0, padx=(0,12), sticky='nsew')
        tk.Label(sellers_card, text='Top vendeurs', font=('Segoe UI', 12, 'bold'), bg=CARD, fg=TEXT).pack(anchor='w', pady=(0,10))
        sellers = query("""SELECT u.company_name, COUNT(DISTINCT fs.id) flash,
            ROUND(COALESCE(SUM(r.total_price),0),2) rev
            FROM users u LEFT JOIN flash_sales fs ON fs.seller_id=u.id
            LEFT JOIN reservations r ON r.flash_sale_id=fs.id AND r.status!='cancelled'
            GROUP BY u.id ORDER BY rev DESC LIMIT 8""")
        tree = ttk.Treeview(sellers_card, columns=('company','flash','rev'), show='headings', height=8)
        tree.heading('company', text='Entreprise')
        tree.heading('flash',   text='Flash sales')
        tree.heading('rev',     text='Revenus (€)')
        tree.column('company', width=200)
        tree.column('flash',   width=80,  anchor='center')
        tree.column('rev',     width=100, anchor='right')
        for s in sellers:
            tree.insert('', 'end', values=(s['company_name'], s['flash'], f"{s['rev']:.2f} €"))
        tree.pack(fill='both', expand=True)

        # Dernières inscriptions
        users_card = tk.Frame(cols_frame, bg=CARD, padx=18, pady=14)
        users_card.grid(row=0, column=1, sticky='nsew')
        tk.Label(users_card, text='Dernières inscriptions', font=('Segoe UI', 12, 'bold'), bg=CARD, fg=TEXT).pack(anchor='w', pady=(0,10))
        recent = query("SELECT company_name, email, DATE(created_at) dt FROM users ORDER BY created_at DESC LIMIT 8")
        for u in recent:
            f = tk.Frame(users_card, bg=CARD)
            f.pack(fill='x', pady=3)
            tk.Label(f, text='🏪', bg=CARD, font=('Segoe UI', 12)).pack(side='left')
            tk.Label(f, text=u['company_name'][:22], font=('Segoe UI', 9, 'bold'), bg=CARD, fg=TEXT).pack(side='left', padx=6)
            tk.Label(f, text=str(u['dt']), font=('Segoe UI', 9), bg=CARD, fg=MUTED).pack(side='right')

    # ── UTILISATEURS ─────────────────────────────────────────
    def show_users(self):
        self.clear_content()
        self.set_active_nav('👥  Utilisateurs')
        total = query('SELECT COUNT(*) n FROM users')[0]['n']
        self.make_header(f'👥 Utilisateurs  ({total})', 'Gérer les comptes professionnels')

        toolbar = tk.Frame(self.content, bg=CARD_BG, padx=28, pady=10)
        toolbar.pack(fill='x')
        tk.Label(toolbar, text='Recherche :', bg=CARD_BG, font=('Segoe UI', 10)).pack(side='left')
        search_var = tk.StringVar()
        search_e = tk.Entry(toolbar, textvariable=search_var, font=('Segoe UI', 10), width=28)
        search_e.pack(side='left', padx=8, ipady=5)
        def do_search():
            q = search_var.get().strip()
            load_users(q)
        tk.Button(toolbar, text='🔍 Chercher', bg=BORDEAUX, fg=WHITE, relief='flat',
                  font=('Segoe UI', 10), padx=12, pady=4, cursor='hand2', command=do_search).pack(side='left')
        tk.Button(toolbar, text='↻ Actualiser', bg=CARD_BG, fg=TEXT, relief='flat',
                  font=('Segoe UI', 10), padx=12, pady=4, cursor='hand2', command=lambda: load_users('')).pack(side='left', padx=4)

        # Tableau
        table_frame = tk.Frame(self.content, bg=CARD_BG, padx=28)
        table_frame.pack(fill='both', expand=True, pady=8)
        cols = ('ID','Entreprise','Email','SIRET','Vérifié','Inscription')
        tree = ttk.Treeview(table_frame, columns=cols, show='headings', height=20)
        for c in cols:
            tree.heading(c, text=c)
        tree.column('ID',          width=50,  anchor='center')
        tree.column('Entreprise',  width=200)
        tree.column('Email',       width=220)
        tree.column('SIRET',       width=130, anchor='center')
        tree.column('Vérifié',     width=80,  anchor='center')
        tree.column('Inscription', width=100, anchor='center')
        sb = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side='left', fill='both', expand=True)
        sb.pack(side='right', fill='y')

        def load_users(search=''):
            for item in tree.get_children():
                tree.delete(item)
            sql = "SELECT id,company_name,email,siret,is_verified,DATE(created_at) dt FROM users"
            params = []
            if search:
                sql += " WHERE company_name LIKE %s OR email LIKE %s OR siret LIKE %s"
                params = [f'%{search}%']*3
            sql += " ORDER BY created_at DESC LIMIT 50"
            rows = query(sql, params if params else None)
            for r in rows:
                v = '✅ Oui' if r['is_verified'] else '❌ Non'
                tree.insert('', 'end', values=(r['id'], r['company_name'], r['email'], r['siret'], v, str(r['dt'])))

        load_users()

        # Actions sur sélection
        action_frame = tk.Frame(self.content, bg=CARD_BG, padx=28, pady=8)
        action_frame.pack(fill='x')
        def verify_user():
            sel = tree.selection()
            if not sel: return
            uid = tree.item(sel[0])['values'][0]
            query('UPDATE users SET is_verified=1 WHERE id=%s', (uid,), fetch=False)
            messagebox.showinfo('Succès', 'Compte vérifié ✅')
            load_users()
        def delete_user():
            sel = tree.selection()
            if not sel: return
            uid = tree.item(sel[0])['values'][0]
            name = tree.item(sel[0])['values'][1]
            if messagebox.askyesno('Confirmer', f'Supprimer "{name}" ?'):
                query('DELETE FROM users WHERE id=%s', (uid,), fetch=False)
                load_users()
        tk.Button(action_frame, text='✅ Vérifier', bg='#1E7820', fg=WHITE, relief='flat',
                  font=('Segoe UI', 10), padx=14, pady=5, cursor='hand2', command=verify_user).pack(side='left', padx=(0,8))
        tk.Button(action_frame, text='🗑️ Supprimer', bg=BORDEAUX, fg=WHITE, relief='flat',
                  font=('Segoe UI', 10), padx=14, pady=5, cursor='hand2', command=delete_user).pack(side='left')

    # ── VENTES FLASH ─────────────────────────────────────────
    def show_flash(self):
        self.clear_content()
        self.set_active_nav('⚡  Ventes Flash')
        total = query("SELECT COUNT(*) n FROM flash_sales")[0]['n']
        self.make_header(f'⚡ Ventes Flash  ({total})', 'Gérer les ventes flash')
        frame = tk.Frame(self.content, bg=CARD_BG, padx=28, pady=10)
        frame.pack(fill='both', expand=True)
        cols = ('ID','Titre','Vendeur','Prix Flash','Statut','Expire')
        tree = ttk.Treeview(frame, columns=cols, show='headings', height=22)
        for c in cols:
            tree.heading(c, text=c)
        tree.column('ID',       width=50,  anchor='center')
        tree.column('Titre',    width=220)
        tree.column('Vendeur',  width=160)
        tree.column('Prix Flash',width=100, anchor='right')
        tree.column('Statut',   width=90,  anchor='center')
        tree.column('Expire',   width=130, anchor='center')
        sb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side='left', fill='both', expand=True)
        sb.pack(side='right', fill='y')
        rows = query("""SELECT fs.id,fs.title,u.company_name seller,fs.flash_price,fs.unit,fs.status,
            DATE_FORMAT(fs.expires_at,'%d/%m/%Y %H:%i') exp
            FROM flash_sales fs JOIN users u ON fs.seller_id=u.id
            ORDER BY fs.created_at DESC LIMIT 100""")
        for r in rows:
            tree.insert('', 'end', values=(
                r['id'], r['title'], r['seller'],
                f"{r['flash_price']:.2f} €/{r['unit']}",
                r['status'], r['exp']
            ))
        # Actions
        af = tk.Frame(self.content, bg=CARD_BG, padx=28, pady=8)
        af.pack(fill='x')
        def cancel_flash():
            sel = tree.selection()
            if not sel: return
            fid = tree.item(sel[0])['values'][0]
            if messagebox.askyesno('Confirmer', 'Annuler cette vente flash ?'):
                query("UPDATE flash_sales SET status='cancelled' WHERE id=%s", (fid,), fetch=False)
                self.show_flash()
        tk.Button(af, text='🚫 Annuler', bg='#D29922', fg=WHITE, relief='flat',
                  font=('Segoe UI', 10), padx=14, pady=5, cursor='hand2', command=cancel_flash).pack(side='left', padx=(0,8))
        tk.Button(af, text='↻ Actualiser', bg=CARD_BG, fg=TEXT, relief='flat',
                  font=('Segoe UI', 10), padx=14, pady=5, cursor='hand2', command=self.show_flash).pack(side='left')

    # ── RÉSERVATIONS ─────────────────────────────────────────
    def show_reservations(self):
        self.clear_content()
        self.set_active_nav('🛒  Réservations')
        total = query("SELECT COUNT(*) n FROM reservations")[0]['n']
        self.make_header(f'🛒 Réservations  ({total})', '')
        frame = tk.Frame(self.content, bg=CARD_BG, padx=28, pady=10)
        frame.pack(fill='both', expand=True)
        cols = ('ID','Vente','Acheteur','Vendeur','Qté','Total','Statut','Date')
        tree = ttk.Treeview(frame, columns=cols, show='headings', height=22)
        for c in cols:
            tree.heading(c, text=c)
        tree.column('ID',      width=50,  anchor='center')
        tree.column('Vente',   width=180)
        tree.column('Acheteur',width=140)
        tree.column('Vendeur', width=140)
        tree.column('Qté',     width=60,  anchor='center')
        tree.column('Total',   width=90,  anchor='right')
        tree.column('Statut',  width=90,  anchor='center')
        tree.column('Date',    width=120, anchor='center')
        sb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side='left', fill='both', expand=True)
        sb.pack(side='right', fill='y')
        rows = query("""SELECT r.id,fs.title,a.company_name acheteur,v.company_name vendeur,
            r.quantity,fs.unit,r.total_price,r.status,DATE_FORMAT(r.created_at,'%d/%m %H:%i') dt
            FROM reservations r JOIN flash_sales fs ON r.flash_sale_id=fs.id
            JOIN users a ON r.buyer_id=a.id JOIN users v ON fs.seller_id=v.id
            ORDER BY r.created_at DESC LIMIT 100""")
        for r in rows:
            tree.insert('', 'end', values=(
                r['id'], r['title'][:30], r['acheteur'][:20], r['vendeur'][:20],
                f"{r['quantity']} {r['unit']}", f"{r['total_price']:.2f} €",
                r['status'], r['dt']
            ))

    # ── AUDIT ─────────────────────────────────────────────────
    def show_audit(self):
        self.clear_content()
        self.set_active_nav('📋  Journal d\'audit')
        total = query("SELECT COUNT(*) n FROM admin_audit_log")[0]['n']
        self.make_header(f"📋 Journal d'audit  ({total})", 'Historique de toutes les actions admin')
        frame = tk.Frame(self.content, bg=CARD_BG, padx=28, pady=10)
        frame.pack(fill='both', expand=True)
        cols = ('Date','Admin','Action','Ressource','Description')
        tree = ttk.Treeview(frame, columns=cols, show='headings', height=22)
        for c in cols:
            tree.heading(c, text=c)
        tree.column('Date',        width=130, anchor='center')
        tree.column('Admin',       width=100)
        tree.column('Action',      width=80,  anchor='center')
        tree.column('Ressource',   width=100)
        tree.column('Description', width=300)
        sb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=sb.set)
        tree.pack(side='left', fill='both', expand=True)
        sb.pack(side='right', fill='y')
        rows = query("""SELECT al.*,au.username FROM admin_audit_log al
            JOIN admin_users au ON al.admin_id=au.id
            ORDER BY al.created_at DESC LIMIT 100""")
        for r in rows:
            tree.insert('', 'end', values=(
                str(r['created_at'])[:16], r['username'],
                r['action'], r['resource'], r.get('description','') or ''
            ))

    def logout(self):
        if messagebox.askyesno('Déconnexion', 'Se déconnecter ?'):
            session['admin'] = None
            self.root.destroy()
            main()


# ── POINT D'ENTRÉE ─────────────────────────────────────────────
def main():
    login_root = tk.Tk()

    def on_login_success():
        login_root.destroy()
        app_root = tk.Tk()
        style = ttk.Style(app_root)
        style.theme_use('clam')
        style.configure('Treeview', font=('Segoe UI', 10), rowheight=26, background='white', fieldbackground='white')
        style.configure('Treeview.Heading', font=('Segoe UI', 9, 'bold'), background='#F0F0F0')
        style.map('Treeview', background=[('selected', BORDEAUX)], foreground=[('selected', WHITE)])
        AdminApp(app_root)
        app_root.mainloop()

    LoginWindow(login_root, on_login_success)
    login_root.mainloop()

if __name__ == '__main__':
    main()
