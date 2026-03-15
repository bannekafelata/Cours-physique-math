"""
╔══════════════════════════════════════════════════════════════════╗
║     PRODUIT EN CROIX — Terminal CRT Pédagogique  v2.0           ║
║     Cours scénarisé  •  IA pour aide & correction               ║
╚══════════════════════════════════════════════════════════════════╝

pip install customtkinter requests
ollama serve && ollama pull llama3
python produit_en_croix_crt.py
"""

import tkinter as tk
import customtkinter as ctk
import threading, requests, json, random

# ══════════════════════════════════════════════════════════════════
#  COULEURS / POLICES
# ══════════════════════════════════════════════════════════════════
PHOSPHOR     = "#ffb300"
PHOSPHOR_DIM = "#8a6300"
PHOSPHOR_GLO = "#ffd966"
BG_DEEP      = "#050300"
BG_CARD      = "#0d0900"
BG_PANEL     = "#0a0800"
GREEN_OK     = "#00e676"
RED_ERR      = "#ff5252"
BLUE         = "#4fc3f7"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL      = "llama3"

# ══════════════════════════════════════════════════════════════════
#  COURS SCÉNARISÉ  (liste de "slides")
#  Chaque slide = { "titre", "lignes": [(tag, texte), ...] }
# ══════════════════════════════════════════════════════════════════
COURS = [
    # ── SLIDE 0 ──────────────────────────────────────────────────
    {
        "titre": "C'est quoi une proportion ?",
        "lignes": [
            ("title", "📐  UNE PROPORTION, C'EST QUOI ?"),
            ("",      ""),
            ("prof",  "Une proportion, c'est une égalité entre deux fractions."),
            ("",      ""),
            ("prof",  "Exemple simple avec une recette :"),
            ("",      ""),
            ("schema","  2 verres d'eau   =    4 verres d'eau"),
            ("schema", " ─────────────────   ─────────────────"),
            ("schema","  1 verre de lait       2 verres de lait"),
            ("",      ""),
            ("prof",  "👉  Si tu doubles l'eau → tu doubles le lait."),
            ("prof",  "     C'est toujours le même rapport."),
            ("",      ""),
            ("dim",   "→  Voilà ce qu'on appelle une PROPORTION."),
        ],
    },
    # ── SLIDE 1 ──────────────────────────────────────────────────
    {
        "titre": "Les 4 cases",
        "lignes": [
            ("title", "📦  LES 4 CASES"),
            ("",      ""),
            ("prof",  "On écrit toujours une proportion avec 4 cases."),
            ("",      ""),
            ("schema", "    A          C    "),
            ("schema", "  ─────   =   ─────  "),
            ("schema", "    B          ?    "),
            ("",      ""),
            ("prof",  "●  A, B, C  →  on les connaît."),
            ("prof",  "●   ?       →  c'est ce qu'on cherche !"),
            ("",      ""),
            ("dim",   "Exemple avec des pizzas :"),
            ("",      ""),
            ("schema", "  300 g        ?   "),
            ("schema", " ───────  =  ─────── "),
            ("schema", "  2 pizzas   5 pizzas"),
            ("",      ""),
            ("prof",  "On connaît A=300, B=2, C=5."),
            ("prof",  "On cherche ? (la farine pour 5 pizzas)."),
        ],
    },
    # ── SLIDE 2 ──────────────────────────────────────────────────
    {
        "titre": "La croix magique",
        "lignes": [
            ("title", "✖️   LA CROIX MAGIQUE"),
            ("",      ""),
            ("prof",  "On fait une croix en diagonale :"),
            ("",      ""),
            ("schema", "    A  ╲        C    "),
            ("schema", "  ─────  ╲  =  ─────  "),
            ("schema", "    B     ╲      ?    "),
            ("",      ""),
            ("prof",  "La croix te dit QUOI multiplier :"),
            ("",      ""),
            ("ok",    "   ?  =  A  ×  C  ÷  B"),
            ("",      ""),
            ("dim",   "C'est LA formule. Retiens-la bien !"),
            ("",      ""),
            ("prof",  "Avec les pizzas :"),
            ("ok",    "   ?  =  300  ×  5  ÷  2  =  750 g"),
            ("",      ""),
            ("prof",  "🎉  Pour 5 pizzas → 750 g de farine !"),
        ],
    },
    # ── SLIDE 3 ──────────────────────────────────────────────────
    {
        "titre": "Les étapes à suivre",
        "lignes": [
            ("title", "📋  LES 3 ÉTAPES"),
            ("",      ""),
            ("prof",  "Face à un exercice, fais TOUJOURS ça :"),
            ("",      ""),
            ("ok",    "  ÉTAPE 1 ─────────────────────────"),
            ("prof",  "  Lis bien le problème."),
            ("prof",  "  Repère les 3 nombres connus."),
            ("",      ""),
            ("ok",    "  ÉTAPE 2 ─────────────────────────"),
            ("prof",  "  Écris la proportion dans les 4 cases."),
            ("",      ""),
            ("schema", "    A       C   "),
            ("schema", "  ─────  =  ─────"),
            ("schema", "    B       ?   "),
            ("",      ""),
            ("ok",    "  ÉTAPE 3 ─────────────────────────"),
            ("prof",  "  Applique la formule :"),
            ("ok",    "   ?  =  A  ×  C  ÷  B"),
            ("",      ""),
            ("dim",   "→  C'est tout ! Pas de magie, juste 3 étapes."),
        ],
    },
    # ── SLIDE 4 ──────────────────────────────────────────────────
    {
        "titre": "Exemple complet",
        "lignes": [
            ("title", "🚗  EXEMPLE COMPLET"),
            ("",      ""),
            ("prof",  "Problème :"),
            ("blue",  "  Une voiture fait 120 km en 2 heures."),
            ("blue",  "  Combien fait-elle en 5 heures ?"),
            ("",      ""),
            ("ok",    "  ÉTAPE 1 — les 3 nombres connus :"),
            ("prof",  "  A = 120 km   B = 2 h   C = 5 h"),
            ("",      ""),
            ("ok",    "  ÉTAPE 2 — la proportion :"),
            ("schema", "   120 km      ?    "),
            ("schema", "  ────────  =  ──────"),
            ("schema", "    2 h        5 h  "),
            ("",      ""),
            ("ok",    "  ÉTAPE 3 — la formule :"),
            ("prof",  "  ?  =  120  ×  5  ÷  2"),
            ("prof",  "  ?  =  600  ÷  2"),
            ("ok",    "  ?  =  300 km  ✅"),
            ("",      ""),
            ("prof",  "🎉  En 5 heures → 300 km !"),
        ],
    },
]

# ══════════════════════════════════════════════════════════════════
#  EXERCICES
# ══════════════════════════════════════════════════════════════════
EXERCICES = [
    {"emoji":"🍕","enonce":"Pour 2 pizzas → 300 g de farine.\nCombien pour 5 pizzas ?",
     "A":300,"B":2,"C":5,"reponse":750,"unite":"g","calcul":"300 × 5 ÷ 2"},
    {"emoji":"🚗","enonce":"120 km en 2 h.\nCombien en 3 h ?",
     "A":120,"B":2,"C":3,"reponse":180,"unite":"km","calcul":"120 × 3 ÷ 2"},
    {"emoji":"🍊","enonce":"4 oranges = 2 €.\nCombien coûtent 6 oranges ?",
     "A":2,"B":4,"C":6,"reponse":3,"unite":"€","calcul":"2 × 6 ÷ 4"},
    {"emoji":"🖨️","enonce":"8 pages en 4 min.\nCombien en 10 min ?",
     "A":8,"B":4,"C":10,"reponse":20,"unite":"pages","calcul":"8 × 10 ÷ 4"},
    {"emoji":"🌱","enonce":"6 L pour 3 plantes.\nCombien pour 7 plantes ?",
     "A":6,"B":3,"C":7,"reponse":14,"unite":"L","calcul":"6 × 7 ÷ 3"},
    {"emoji":"🍫","enonce":"5 tablettes = 10 €.\nCombien pour 3 tablettes ?",
     "A":10,"B":5,"C":3,"reponse":6,"unite":"€","calcul":"10 × 3 ÷ 5"},
    {"emoji":"🏃","enonce":"En 5 min il court 1 km.\nCombien en 20 min ?",
     "A":1,"B":5,"C":20,"reponse":4,"unite":"km","calcul":"1 × 20 ÷ 5"},
]

# ══════════════════════════════════════════════════════════════════
#  SYSTEM PROMPT OLLAMA  (pour aide & correction seulement)
# ══════════════════════════════════════════════════════════════════
SYSTEM_AIDE = """Tu es PROF-UNIT. Tu aides un élève de 6e DYSLEXIQUE qui apprend le produit en croix.

RÈGLES STRICTES :
- Phrases TRÈS COURTES (max 10 mots par ligne).
- Une seule idée par ligne.
- Émojis pour aérer.
- Toujours encourager avant de corriger.
- FRANÇAIS uniquement.
- La formule est toujours : ? = A × C ÷ B
- Max 5 lignes de réponse.
"""

# ══════════════════════════════════════════════════════════════════
#  OLLAMA
# ══════════════════════════════════════════════════════════════════
def ask_ollama(messages, on_token, on_done, on_error):
    def run():
        try:
            prompt = ""
            for m in messages:
                prompt += (f"\n[ÉLÈVE]: {m['content']}\n" if m["role"] == "user"
                           else f"\n[PROF-UNIT]: {m['content']}\n")
            prompt += "\n[PROF-UNIT]: "
            resp = requests.post(OLLAMA_URL,
                json={"model": MODEL, "system": SYSTEM_AIDE,
                      "prompt": prompt, "stream": True},
                stream=True, timeout=60)
            resp.raise_for_status()
            full = ""
            for line in resp.iter_lines():
                if line:
                    d = json.loads(line)
                    tok = d.get("response", "")
                    full += tok
                    on_token(tok)
                    if d.get("done"):
                        break
            on_done(full)
        except requests.exceptions.ConnectionError:
            on_error("❌ Ollama non démarré !\nollama serve  puis  ollama pull llama3")
        except Exception as e:
            on_error(f"❌ Erreur : {e}")
    threading.Thread(target=run, daemon=True).start()

# ══════════════════════════════════════════════════════════════════
#  APPLICATION
# ══════════════════════════════════════════════════════════════════
class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("PROF-UNIT — Produit en Croix  v2.0")
        self.geometry("1060x760")
        self.configure(fg_color=BG_DEEP)
        self.resizable(True, True)

        # État
        self.slide_idx      = 0          # slide de cours actuelle
        self.mode           = "accueil"  # accueil / cours / aide / exercices
        self.conversation   = []
        self.waiting_ai     = False
        self.score          = 0
        self.ex_courant     = None
        self.saisie_num     = ""
        self.ex_restants    = list(EXERCICES)
        random.shuffle(self.ex_restants)

        self._build_ui()
        self._show_accueil()

    # ══════════════════════════════════════════
    #  UI
    # ══════════════════════════════════════════
    def _build_ui(self):
        # En-tête
        hdr = ctk.CTkFrame(self, fg_color=BG_DEEP, height=48)
        hdr.pack(fill="x", padx=20, pady=(12, 0))
        ctk.CTkLabel(hdr, text="▶ PROF-UNIT  v2.0",
                     font=("Courier", 19, "bold"),
                     text_color=PHOSPHOR).pack(side="left")
        self.lbl_score = ctk.CTkLabel(hdr, text="⭐ 0 pts",
                                       font=("Courier", 14),
                                       text_color=PHOSPHOR_DIM)
        self.lbl_score.pack(side="right", padx=12)
        self.lbl_mode = ctk.CTkLabel(hdr, text="",
                                      font=("Courier", 13),
                                      text_color=PHOSPHOR_DIM)
        self.lbl_mode.pack(side="right", padx=18)

        # Schéma permanent
        sf = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=8)
        sf.pack(fill="x", padx=20, pady=4)
        self.lbl_schema = ctk.CTkLabel(sf,
            text=self._fmt_schema("A","B","C","?"),
            font=("Courier", 14), text_color=PHOSPHOR_DIM, justify="center")
        self.lbl_schema.pack(side="left", padx=24, pady=6)
        self.lbl_formule = ctk.CTkLabel(sf,
            text="💡  ? = A × C ÷ B",
            font=("Courier", 14), text_color=PHOSPHOR_DIM, justify="left")
        self.lbl_formule.pack(side="left", padx=28, pady=6)

        # Corps
        body = ctk.CTkFrame(self, fg_color=BG_DEEP)
        body.pack(fill="both", expand=True, padx=20, pady=4)
        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)

        self.txt = tk.Text(body, wrap="word",
            bg=BG_DEEP, fg=PHOSPHOR, font=("Courier", 16),
            relief="flat", padx=16, pady=10,
            spacing1=6, spacing3=6,
            state="disabled", cursor="arrow")
        self.txt.grid(row=0, column=0, sticky="nsew")

        sb = ctk.CTkScrollbar(body, command=self.txt.yview)
        sb.grid(row=0, column=1, sticky="ns", padx=(0,4))
        self.txt.configure(yscrollcommand=sb.set)

        self.txt.tag_config("title",  foreground=PHOSPHOR_GLO, font=("Courier",18,"bold"))
        self.txt.tag_config("prof",   foreground=PHOSPHOR,     font=("Courier",16))
        self.txt.tag_config("schema", foreground="#e0a800",    font=("Courier",16))
        self.txt.tag_config("dim",    foreground=PHOSPHOR_DIM, font=("Courier",14))
        self.txt.tag_config("ok",     foreground=GREEN_OK,     font=("Courier",16,"bold"))
        self.txt.tag_config("err",    foreground=RED_ERR,      font=("Courier",16,"bold"))
        self.txt.tag_config("blue",   foreground=BLUE,         font=("Courier",16))
        self.txt.tag_config("ai",     foreground="#ce93d8",    font=("Courier",16))
        self.txt.tag_config("",       foreground=PHOSPHOR,     font=("Courier",8))

        # Panneau droit
        self.panel = ctk.CTkFrame(body, fg_color=BG_PANEL,
                                   corner_radius=10, width=250)
        self.panel.grid(row=0, column=2, sticky="nsew", padx=(10,0))
        self.panel.grid_propagate(False)

        # Barre statut
        self.lbl_status = ctk.CTkLabel(self, text="",
            font=("Courier",12), text_color=PHOSPHOR_DIM)
        self.lbl_status.pack(pady=(2,8))

    # ══════════════════════════════════════════
    #  PANNEAUX DROITS
    # ══════════════════════════════════════════
    def _clear_panel(self):
        for w in self.panel.winfo_children():
            w.destroy()

    def _sep_panel(self):
        ctk.CTkFrame(self.panel, fg_color=PHOSPHOR_DIM, height=1).pack(
            fill="x", padx=12, pady=6)

    # ─── Accueil
    def _panel_accueil(self):
        self._clear_panel()
        ctk.CTkLabel(self.panel, text="Prêt à apprendre ?",
                     font=("Courier",15), text_color=PHOSPHOR_DIM,
                     wraplength=210, justify="center").pack(pady=(50,16))
        self._btn(self.panel, "▶  COMMENCER !", PHOSPHOR, BG_DEEP,
                  self._demarrer_cours, w=210, h=68, big=True)

    # ─── Navigation cours (flèches)
    def _panel_cours(self):
        self._clear_panel()
        total = len(COURS)
        idx   = self.slide_idx

        # Barre de progression
        ctk.CTkLabel(self.panel,
            text=f"LEÇON  {idx+1} / {total}",
            font=("Courier",13), text_color=PHOSPHOR_DIM).pack(pady=(16,4))

        pct = (idx + 1) / total
        ctk.CTkProgressBar(self.panel, width=210, height=10,
            fg_color=BG_DEEP, progress_color=PHOSPHOR).pack(pady=(0,12))
        # on recrée la barre avec la bonne valeur
        self.panel.winfo_children()[-1].set(pct)

        self._sep_panel()

        # Flèche SUIVANT
        if idx < total - 1:
            self._btn(self.panel, "SUIVANT  ▶", PHOSPHOR, BG_DEEP,
                      self._slide_suivant, w=210, h=58, big=True)
        else:
            # Dernière slide → bouton "J'ai compris ?"
            self._btn(self.panel, "✅  J'ai compris !", GREEN_OK, BG_DEEP,
                      self._compris, w=210, h=58, big=True)
            ctk.CTkLabel(self.panel, text="  ou", font=("Courier",13),
                         text_color=PHOSPHOR_DIM).pack(pady=2)
            self._btn(self.panel, "❓  Pas compris", RED_ERR, BG_DEEP,
                      self._pas_compris, w=210, h=52)

        self._sep_panel()

        # Flèche PRÉCÉDENT
        if idx > 0:
            self._btn(self.panel, "◀  PRÉCÉDENT", BG_DEEP, PHOSPHOR_DIM,
                      self._slide_precedent, w=210, h=44, border=True)

    # ─── Aide IA (pas compris)
    def _panel_aide(self):
        self._clear_panel()
        ctk.CTkLabel(self.panel, text="Le prof t'aide !",
                     font=("Courier",14,"bold"), text_color="#ce93d8").pack(pady=(20,8))
        self._sep_panel()
        ctk.CTkLabel(self.panel, text="Quand il a fini :",
                     font=("Courier",13), text_color=PHOSPHOR_DIM).pack(pady=(10,6))
        self._btn(self.panel, "✅  J'ai compris !", GREEN_OK, BG_DEEP,
                  self._compris, w=210, h=54, big=True)
        self._btn(self.panel, "▶  Continuer", PHOSPHOR, BG_DEEP,
                  self._slide_suivant, w=210, h=48)

    # ─── Transition vers exercices
    def _panel_transition(self):
        self._clear_panel()
        ctk.CTkLabel(self.panel, text="Cours terminé !\nPlace aux exercices.",
                     font=("Courier",14), text_color=PHOSPHOR_DIM,
                     justify="center").pack(pady=(30,16))
        self._btn(self.panel, "🎯  1er EXERCICE !", PHOSPHOR, BG_DEEP,
                  self._lancer_exercice, w=210, h=68, big=True)

    # ─── Exercice : pavé numérique
    def _panel_pave(self):
        self._clear_panel()
        self.saisie_num = ""

        self.lbl_display = ctk.CTkLabel(self.panel,
            text="?", font=("Courier",48,"bold"), text_color=PHOSPHOR)
        self.lbl_display.pack(pady=(18,2))
        ctk.CTkLabel(self.panel, text="tape ta réponse",
                     font=("Courier",11), text_color=PHOSPHOR_DIM).pack()

        g = ctk.CTkFrame(self.panel, fg_color="transparent")
        g.pack(pady=8)
        layout = [7,8,9, 4,5,6, 1,2,3, None,0,None]
        for i, v in enumerate(layout):
            r, c = divmod(i, 3)
            if v is None:
                ctk.CTkLabel(g, text="", width=62).grid(row=r,column=c,padx=3,pady=3)
                continue
            ctk.CTkButton(g, text=str(v),
                font=("Courier",20,"bold"),
                fg_color=BG_DEEP, hover_color="#1e1400",
                text_color=PHOSPHOR,
                border_color=PHOSPHOR_DIM, border_width=1,
                width=62, height=52, corner_radius=6,
                command=lambda n=v: self._num(n),
            ).grid(row=r, column=c, padx=3, pady=3)

        act = ctk.CTkFrame(self.panel, fg_color="transparent")
        act.pack(pady=(0,8))
        ctk.CTkButton(act, text="⌫",
            font=("Courier",20,"bold"),
            fg_color=BG_DEEP, hover_color="#2a0a00",
            text_color=RED_ERR, border_color=RED_ERR, border_width=1,
            width=60, height=50, corner_radius=6,
            command=self._suppr,
        ).pack(side="left", padx=3)
        ctk.CTkButton(act, text="✔  OK",
            font=("Courier",17,"bold"),
            fg_color=PHOSPHOR, hover_color=PHOSPHOR_GLO,
            text_color=BG_DEEP,
            width=130, height=50, corner_radius=6,
            command=self._valider,
        ).pack(side="left", padx=3)

    # ─── Après exercice (correct ou non)
    def _panel_apres_ex(self, correct: bool):
        self._clear_panel()
        if correct:
            ctk.CTkLabel(self.panel, text="🎉 BRAVO !",
                         font=("Courier",18,"bold"), text_color=GREEN_OK).pack(pady=(24,8))
        else:
            ctk.CTkLabel(self.panel, text="💡 Le prof explique...",
                         font=("Courier",14), text_color="#ce93d8").pack(pady=(24,8))
        self._sep_panel()
        ctk.CTkLabel(self.panel, text="Ensuite :",
                     font=("Courier",13), text_color=PHOSPHOR_DIM).pack(pady=(8,4))
        self._btn(self.panel, "🎯  Exercice suivant", PHOSPHOR, BG_DEEP,
                  self._lancer_exercice, w=210, h=56, big=True)

    # ─── Fin des exercices
    def _panel_fin(self):
        self._clear_panel()
        ctk.CTkLabel(self.panel,
            text=f"🏆  SCORE FINAL\n\n  {self.score} pts",
            font=("Courier",18,"bold"), text_color=PHOSPHOR_GLO,
            justify="center").pack(pady=(40,20))
        self._btn(self.panel, "🔄  Recommencer", PHOSPHOR_DIM, BG_DEEP,
                  self._restart, w=210, h=52)

    # ─── Bouton utilitaire
    def _btn(self, parent, text, fg, text_color, cmd,
             w=210, h=52, big=False, border=False):
        ctk.CTkButton(parent, text=text,
            font=("Courier", 16 if big else 14, "bold"),
            fg_color=fg, hover_color=PHOSPHOR_GLO if fg == PHOSPHOR else "#1a1200",
            text_color=text_color,
            border_color=PHOSPHOR_DIM if border else fg,
            border_width=1 if border else 0,
            width=w, height=h, corner_radius=8,
            command=cmd,
        ).pack(pady=5, padx=10)

    # ══════════════════════════════════════════
    #  ÉCRITURE DANS LE TERMINAL
    # ══════════════════════════════════════════
    def _write(self, text, tag="prof"):
        self.txt.configure(state="normal")
        self.txt.insert("end", text, tag)
        self.txt.see("end")
        self.txt.configure(state="disabled")

    def _clear_txt(self):
        self.txt.configure(state="normal")
        self.txt.delete("1.0", "end")
        self.txt.configure(state="disabled")

    def _render_slide(self, slide):
        """Affiche une slide de cours dans le terminal."""
        self._clear_txt()
        for tag, texte in slide["lignes"]:
            self._write(texte + "\n", tag if tag else "")
        self._write("\n", "")

    # ══════════════════════════════════════════
    #  ACCUEIL
    # ══════════════════════════════════════════
    def _show_accueil(self):
        self.mode = "accueil"
        self.lbl_mode.configure(text="")
        self._clear_txt()
        lines = [
            ("title", "╔══════════════════════════════════════╗"),
            ("title", "║   PROF-UNIT v2.0  —  PRÊT !          ║"),
            ("title", "╚══════════════════════════════════════╝"),
            ("",      ""),
            ("prof",  "👋  Salut ! Je suis PROF-UNIT."),
            ("prof",  ""),
            ("prof",  "Je vais t'apprendre le PRODUIT EN CROIX."),
            ("prof",  ""),
            ("dim",   "Le cours est en 5 leçons."),
            ("dim",   "Tu cliques sur les flèches pour avancer."),
            ("dim",   ""),
            ("dim",   "Quand tu ne comprends pas → dis-le !"),
            ("dim",   "Je t'explique autrement."),
            ("",      ""),
            ("ok",    "  Prêt ?  Clique sur COMMENCER →"),
        ]
        for tag, txt in lines:
            self._write(txt + "\n", tag if tag else "")
        self._panel_accueil()

    # ══════════════════════════════════════════
    #  NAVIGATION COURS
    # ══════════════════════════════════════════
    def _demarrer_cours(self):
        self.mode = "cours"
        self.slide_idx = 0
        self._afficher_slide()

    def _afficher_slide(self):
        slide = COURS[self.slide_idx]
        self.lbl_mode.configure(text=f"📚  {slide['titre']}")
        self._render_slide(slide)
        self._panel_cours()

    def _slide_suivant(self):
        if self.slide_idx < len(COURS) - 1:
            self.slide_idx += 1
            self._afficher_slide()
        else:
            self._transition_exercices()

    def _slide_precedent(self):
        if self.slide_idx > 0:
            self.slide_idx -= 1
            self._afficher_slide()

    # ══════════════════════════════════════════
    #  COMPRIS / PAS COMPRIS
    # ══════════════════════════════════════════
    def _compris(self):
        """L'élève a compris → on passe à la suite ou aux exercices."""
        if self.slide_idx < len(COURS) - 1:
            self._slide_suivant()
        else:
            self._transition_exercices()

    def _pas_compris(self):
        """L'élève n'a pas compris → l'IA entre en jeu."""
        self.mode = "aide"
        slide = COURS[self.slide_idx]
        self.lbl_mode.configure(text="🤖  Aide en cours...")
        self._panel_aide()

        # Prépare le contexte de la slide pour l'IA
        contenu_slide = "\n".join(t for _, t in slide["lignes"] if t)
        msg = (f"L'élève n'a pas compris cette leçon : « {slide['titre']} ».\n"
               f"Contenu vu :\n{contenu_slide}\n\n"
               f"Ré-explique avec des mots encore plus simples. "
               f"Utilise un nouvel exemple concret de la vie quotidienne. "
               f"Max 6 lignes courtes.")

        self.conversation = []   # reset contexte aide
        self.conversation.append({"role": "user", "content": msg})
        self.waiting_ai = True
        self.lbl_status.configure(text="● PROF-UNIT réfléchit...", text_color=PHOSPHOR)

        self._write("\n" + "─"*42 + "\n", "dim")
        self._write("🤖  PROF-UNIT ré-explique :\n\n", "ai")

        def on_tok(tok):
            self.after(0, lambda t=tok: self._write(t, "ai"))

        def on_done(full):
            self.conversation.append({"role": "assistant", "content": full})
            self.waiting_ai = False
            self.after(0, lambda: self._write("\n", "ai"))
            self.after(0, lambda: self.lbl_status.configure(
                text="", text_color=PHOSPHOR_DIM))

        def on_err(err):
            self.waiting_ai = False
            self.after(0, lambda: self._write(f"\n{err}\n", "err"))
            self.after(0, lambda: self.lbl_status.configure(text=""))

        ask_ollama(self.conversation, on_tok, on_done, on_err)

    # ══════════════════════════════════════════
    #  TRANSITION → EXERCICES
    # ══════════════════════════════════════════
    def _transition_exercices(self):
        self.mode = "exercices"
        self.lbl_mode.configure(text="🎯  Exercices")
        self._clear_txt()
        self._write("─"*42 + "\n", "dim")
        self._write("🎯  EXERCICES\n\n", "title")
        self._write("Tu as bien vu le cours !\n", "prof")
        self._write("Maintenant on s'entraîne.\n", "prof")
        self._write("Clique sur le bouton pour commencer →\n", "dim")
        self._panel_transition()

    # ══════════════════════════════════════════
    #  EXERCICES
    # ══════════════════════════════════════════
    def _lancer_exercice(self):
        if not self.ex_restants:
            self._fin_exercices()
            return

        ex = self.ex_restants.pop(0)
        self.ex_courant = ex

        # Mise à jour schéma
        self.lbl_schema.configure(
            text=self._fmt_schema(ex["A"], ex["B"], ex["C"], "?"))
        self.lbl_formule.configure(
            text=f"💡  ? = ({ex['A']} × {ex['C']}) ÷ {ex['B']}   [{ex['unite']}]")

        self._clear_txt()
        self._write("─"*42 + "\n", "dim")
        self._write(f"{ex['emoji']}  EXERCICE\n\n", "title")
        self._write(ex["enonce"] + "\n\n", "prof")

        # Rappel schéma dans le texte
        self._write(f"  {ex['A']}       ?\n", "schema")
        self._write(f" ─────  =  ─────\n", "schema")
        self._write(f"  {ex['B']}       {ex['C']}\n\n", "schema")

        self._write(f"  Formule : {ex['calcul']} = ?\n\n", "dim")

        self._panel_pave()

    def _fin_exercices(self):
        self.lbl_mode.configure(text="🏆  Terminé !")
        self._clear_txt()
        self._write("─"*42 + "\n", "dim")
        self._write("🏆  FÉLICITATIONS !\n\n", "title")
        self._write("Tu as fini tous les exercices !\n", "ok")
        self._write(f"Score final : {self.score} points\n\n", "ok")
        self._write("Tu maîtrises le produit en croix. 🎉\n", "prof")
        self._panel_fin()

    # ── Pavé numérique
    def _num(self, n):
        if len(self.saisie_num) < 6:
            self.saisie_num += str(n)
            self.lbl_display.configure(text=self.saisie_num or "?")

    def _suppr(self):
        self.saisie_num = self.saisie_num[:-1]
        self.lbl_display.configure(text=self.saisie_num or "?")

    def _valider(self):
        if not self.saisie_num:
            return
        rep = int(self.saisie_num)
        self._verifier(rep)

    def _verifier(self, rep: int):
        ex = self.ex_courant
        self.ex_courant = None
        bonne = ex["reponse"]
        correct = (rep == bonne)

        if correct:
            self.score += 10
            self.lbl_score.configure(text=f"⭐ {self.score} pts")
            self._write(f"\n✅  BRAVO !  Réponse : {bonne} {ex['unite']} !\n", "ok")
            self._write(f"   {ex['calcul']} = {bonne}\n", "dim")
            self._panel_apres_ex(True)
            # Pas d'IA si correct
        else:
            self._write(f"\n🔄  Réponse : {rep} — pas tout à fait...\n", "err")
            self._write(f"   Bonne réponse : {bonne} {ex['unite']}\n", "err")
            self._write(f"   {ex['calcul']} = {bonne}\n\n", "dim")
            self._panel_apres_ex(False)
            # IA explique l'erreur
            self._ia_correction(ex, rep, bonne)

    def _ia_correction(self, ex, rep_eleve, bonne):
        msg = (f"L'élève a répondu {rep_eleve} au lieu de {bonne} {ex['unite']}.\n"
               f"Exercice : {ex['enonce']}\n"
               f"Formule : {ex['calcul']} = {bonne}\n"
               f"Explique son erreur doucement. Montre le calcul étape par étape. "
               f"Encourage-le. Max 5 lignes très courtes.")

        self.conversation = []
        self.conversation.append({"role": "user", "content": msg})
        self.waiting_ai = True
        self.lbl_status.configure(text="● PROF-UNIT analyse...", text_color=PHOSPHOR)

        self._write("\n🤖  PROF-UNIT explique :\n\n", "ai")

        def on_tok(tok):
            self.after(0, lambda t=tok: self._write(t, "ai"))

        def on_done(full):
            self.conversation.append({"role": "assistant", "content": full})
            self.waiting_ai = False
            self.after(0, lambda: self._write("\n\n", "ai"))
            self.after(0, lambda: self.lbl_status.configure(text=""))

        def on_err(err):
            self.waiting_ai = False
            self.after(0, lambda: self._write(f"\n{err}\n", "err"))
            self.after(0, lambda: self.lbl_status.configure(text=""))

        ask_ollama(self.conversation, on_tok, on_done, on_err)

    # ══════════════════════════════════════════
    #  RESTART
    # ══════════════════════════════════════════
    def _restart(self):
        self.score       = 0
        self.slide_idx   = 0
        self.ex_restants = list(EXERCICES)
        random.shuffle(self.ex_restants)
        self.conversation = []
        self.lbl_score.configure(text="⭐ 0 pts")
        self._show_accueil()

    # ══════════════════════════════════════════
    #  UTILITAIRES
    # ══════════════════════════════════════════
    def _fmt_schema(self, a, b, c, d):
        return (f"  {str(a):^8}  {str(c):^8}\n"
                f" ────────  =  ────────\n"
                f"  {str(b):^8}  {str(d):^8}")


# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
