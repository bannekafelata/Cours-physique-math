"""
VELOCITY-UNIT v2.1 — Mouvement, Vitesse & Unités
Compatible Python 3.14  •  tkinter pur  •  daltonisme-safe

pip install requests
python velocity_unit.py
"""

import tkinter as tk
import threading, requests, json, random, math

# ══════════════════════════════════════════════════════════════════
#  PALETTE  daltonisme-safe  (pas de vert/rouge)
# ══════════════════════════════════════════════════════════════════
CYA = "#00e8ff"   # cyan principal
CYD = "#005f66"   # cyan sombre
CYG = "#00c8d4"   # cyan hover
ORA = "#ff8c00"   # orange  (erreur / alerte)
ORB = "#ffb84d"   # orange clair
JAU = "#ffe066"   # jaune   (succès)
BLA = "#c8d8e8"   # blanc cassé
WDI = "#7a8fa0"   # texte dim
VIO = "#d4a8ff"   # violet  IA
BG  = "#020810"
BGC = "#050f1a"
BGG = "#040d18"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL      = "llama3"

SYSTEM_AIDE = """Tu es VELOCITY-UNIT, tuteur IA pour un élève de 6e dyslexique.
Physique : mouvement, vitesse, distance, temps, unités.
Formules : v = d ÷ t  /  d = v × t  /  t = d ÷ v
Unités   : km, m, h, s, km/h, m/s  (1 km=1000 m, 1 h=3600 s)
RÈGLES : phrases courtes (max 10 mots), émojis, encourager avant corriger,
français uniquement, max 6 lignes."""

# ══════════════════════════════════════════════════════════════════
#  COURS  (8 slides)
# ══════════════════════════════════════════════════════════════════
COURS = [
    {"titre":"Le mouvement","visual":"road","lignes":[
        ("T","🚀  LE MOUVEMENT"),("",""),
        ("P","Un objet est en MOUVEMENT"),("P","quand il CHANGE DE PLACE."),("",""),
        ("B","Exemples :"),
        ("C","  🚗  voiture qui roule   →  MOUVEMENT"),
        ("C","  🏠  une maison          →  IMMOBILE"),
        ("C","  ✈️  avion qui décolle   →  MOUVEMENT"),("",""),
        ("D","Pour décrire un mouvement on a besoin de :"),("",""),
        ("F","  📏  d  =  distance"),
        ("F","  ⏱️  t  =  temps"),
        ("F","  💨  v  =  vitesse"),
    ]},
    {"titre":"Les unités de distance","visual":"units_d","lignes":[
        ("T","📏  LES UNITÉS DE DISTANCE"),("",""),
        ("P","On mesure la distance en :"),("",""),
        ("C","  km  =  kilomètre   (grande distance)"),
        ("C","  m   =  mètre       (petite distance)"),("",""),
        ("F","  1 km  =  1 000 m"),("F","  1 m   =  0,001 km"),("",""),
        ("B","Exemples :"),
        ("D","  Paris → Lyon     ≈  465 km"),
        ("D","  Longueur d'une piscine  =  50 m"),("",""),
        ("O","  ⚠️  km et m ne se mélangent PAS !"),
        ("O","  Il faut convertir AVANT de calculer."),
    ]},
    {"titre":"Les unités de temps","visual":"units_t","lignes":[
        ("T","⏱️  LES UNITÉS DE TEMPS"),("",""),
        ("P","On mesure le temps en :"),("",""),
        ("C","  h   =  heure    (durée longue)"),
        ("C","  min =  minute   (durée moyenne)"),
        ("C","  s   =  seconde  (durée courte)"),("",""),
        ("F","  1 h   =   60 min"),
        ("F","  1 min =   60 s"),
        ("F","  1 h   =  3 600 s"),("",""),
        ("O","  ⚠️  1 heure ≠ 1 seconde !"),
        ("O","  Toujours utiliser la MÊME unité."),
    ]},
    {"titre":"Les unités de vitesse","visual":"speedometer","lignes":[
        ("T","💨  LES UNITÉS DE VITESSE"),("",""),
        ("P","La vitesse dépend des unités de d et t :"),("",""),
        ("C","  km/h  →  distance en km,  temps en h"),
        ("C","  m/s   →  distance en m,   temps en s"),("",""),
        ("F","  🚶  Marcheur   ≈    5 km/h  ≈  1,4 m/s"),
        ("F","  🚗  Voiture    ≈  100 km/h  ≈   28 m/s"),
        ("F","  ✈️  Avion      ≈  900 km/h  ≈  250 m/s"),("",""),
        ("O","  ⚠️  TOUJOURS mêmes unités dans v = d ÷ t !"),
    ]},
    {"titre":"Formule  v = d ÷ t","visual":"formula_v","lignes":[
        ("T","🧮  FORMULE 1  :  v = d ÷ t"),("",""),
        ("P","Pour trouver la VITESSE :"),("",""),
        ("F","           d"),("F","   v  =  ─────"),("F","           t"),("",""),
        ("B","Exemple (km et h) :"),
        ("D","  🚗  200 km en 2 h"),("",""),
        ("F","          200 km"),("F","  v = ────────── = 100 km/h  ✔"),("F","            2 h"),("",""),
        ("O","  ⚠️  km ÷ h  →  résultat en km/h"),
        ("O","  ⚠️  m  ÷ s  →  résultat en m/s"),
    ]},
    {"titre":"Formule  d = v × t","visual":"formula_d","lignes":[
        ("T","📏  FORMULE 2  :  d = v × t"),("",""),
        ("P","Pour trouver la DISTANCE :"),("",""),
        ("F","   d  =  v  ×  t"),("",""),
        ("B","Exemple (km/h et h) :"),
        ("D","  🚴  Vélo à 20 km/h pendant 3 h"),("",""),
        ("F","  d = 20 km/h × 3 h = 60 km  ✔"),("",""),
        ("O","  ⚠️  km/h × h  →  résultat en km"),
        ("O","  ⚠️  m/s  × s  →  résultat en m"),
    ]},
    {"titre":"Formule  t = d ÷ v","visual":"formula_t","lignes":[
        ("T","⏱️  FORMULE 3  :  t = d ÷ v"),("",""),
        ("P","Pour trouver le TEMPS :"),("",""),
        ("F","           d"),("F","   t  =  ─────"),("F","           v"),("",""),
        ("B","Exemple (km et km/h) :"),
        ("D","  ✈️  Avion à 900 km/h, trajet 1800 km"),("",""),
        ("F","         1800 km"),("F","  t = ───────── = 2 h  ✔"),("F","         900 km/h"),("",""),
        ("O","  ⚠️  km ÷ km/h  →  résultat en h"),
        ("O","  ⚠️  m  ÷ m/s   →  résultat en s"),
    ]},
    {"titre":"Le triangle magique","visual":"triangle","lignes":[
        ("T","🔺  LE TRIANGLE MAGIQUE"),("",""),
        ("P","Cache la lettre cherchée → formule !"),("",""),
        ("F","        ┌─────┐"),("F","        │  d  │"),
        ("F","       ─┴─────┴─"),("F","      │ v │ × │ t │"),("F","       ───────────"),("",""),
        ("C","  Cache v  →  d ÷ t    →   v = d ÷ t"),
        ("C","  Cache d  →  v × t    →   d = v × t"),
        ("C","  Cache t  →  d ÷ v    →   t = d ÷ v"),("",""),
        ("O","  ⚠️  TOUJOURS vérifier les unités !"),
    ]},
]

# ══════════════════════════════════════════════════════════════════
#  EXERCICES GUIDÉS
# ══════════════════════════════════════════════════════════════════
GUIDES = [
    {"numero":1,"emoji":"🚗","titre":"Trouver la vitesse","type":"v",
     "enonce":"Une voiture parcourt 120 km en 2 h.\nQuelle est sa vitesse ?",
     "etapes":[
        {"consigne":"ÉTAPE 1  —  Quelle formule ?",
         "aide":"On cherche v  →  v = d ÷ t",
         "question":"Tape :  1 = v=d÷t   2 = d=v×t   3 = t=d÷v","reponse":1,
         "bravo":"✔  Bonne formule !  v = d ÷ t"},
        {"consigne":"ÉTAPE 2  —  Les unités sont-elles compatibles ?",
         "aide":"d = 120 km  /  t = 2 h\nkm ÷ h  →  résultat en km/h  ✔",
         "question":"Tape 1 = oui compatibles   2 = non il faut convertir","reponse":1,
         "bravo":"✔  Oui !  km et h → km/h"},
        {"consigne":"ÉTAPE 3  —  Quelle est la valeur de d ?",
         "aide":"L'énoncé dit : 120 km",
         "question":"Tape la valeur de d (en km) :","reponse":120,
         "bravo":"✔  d = 120 km"},
        {"consigne":"ÉTAPE 4  —  Quelle est la valeur de t ?",
         "aide":"L'énoncé dit : 2 heures",
         "question":"Tape la valeur de t (en h) :","reponse":2,
         "bravo":"✔  t = 2 h"},
        {"consigne":"ÉTAPE 5  —  Calcule  v = 120 ÷ 2",
         "aide":"120 ÷ 2 = 60",
         "question":"Tape le résultat de 120 ÷ 2 :","reponse":60,
         "bravo":"✔  v = 60 km/h  🎉"},
     ],"conclusion":"La voiture roule à 60 km/h."},
    {"numero":2,"emoji":"🚴","titre":"Trouver la distance","type":"d",
     "enonce":"Un vélo roule à 15 km/h pendant 2 h.\nQuelle distance parcourt-il ?",
     "etapes":[
        {"consigne":"ÉTAPE 1  —  Quelle formule ?",
         "aide":"On cherche d  →  d = v × t",
         "question":"Tape :  1 = v=d÷t   2 = d=v×t   3 = t=d÷v","reponse":2,
         "bravo":"✔  Bonne formule !  d = v × t"},
        {"consigne":"ÉTAPE 2  —  Les unités sont-elles compatibles ?",
         "aide":"v = 15 km/h  /  t = 2 h\nkm/h × h  →  résultat en km  ✔",
         "question":"Tape 1 = oui compatibles   2 = non il faut convertir","reponse":1,
         "bravo":"✔  Oui !  km/h × h → km"},
        {"consigne":"ÉTAPE 3  —  Quelle est la valeur de v ?",
         "aide":"L'énoncé dit : 15 km/h",
         "question":"Tape la valeur de v (en km/h) :","reponse":15,
         "bravo":"✔  v = 15 km/h"},
        {"consigne":"ÉTAPE 4  —  Quelle est la valeur de t ?",
         "aide":"L'énoncé dit : 2 heures",
         "question":"Tape la valeur de t (en h) :","reponse":2,
         "bravo":"✔  t = 2 h"},
        {"consigne":"ÉTAPE 5  —  Calcule  d = 15 × 2",
         "aide":"15 × 2 = 30",
         "question":"Tape le résultat de 15 × 2 :","reponse":30,
         "bravo":"✔  d = 30 km  🎉"},
     ],"conclusion":"Le vélo a parcouru 30 km."},
]

LIBRES = [
    {"emoji":"✈️","type":"v","enonce":"Un avion fait 900 km en 3 h.\nQuelle est sa vitesse ?",
     "formule":"v = 900 ÷ 3","reponse":300,"unite":"km/h",
     "detail":"d=900 km, t=3 h  →  v = 900÷3 = 300 km/h"},
    {"emoji":"🚗","type":"d","enonce":"Une voiture roule à 90 km/h pendant 2 h.\nQuelle distance ?",
     "formule":"d = 90 × 2","reponse":180,"unite":"km",
     "detail":"v=90 km/h, t=2 h  →  d = 90×2 = 180 km"},
    {"emoji":"🚂","type":"t","enonce":"Un train à 200 km/h doit faire 600 km.\nCombien de temps ?",
     "formule":"t = 600 ÷ 200","reponse":3,"unite":"h",
     "detail":"d=600 km, v=200 km/h  →  t = 600÷200 = 3 h"},
    {"emoji":"🏃","type":"v","enonce":"Un coureur fait 100 m en 10 s.\nVitesse en m/s ?",
     "formule":"v = 100 ÷ 10","reponse":10,"unite":"m/s",
     "detail":"d=100 m, t=10 s  →  v = 100÷10 = 10 m/s"},
    {"emoji":"🚴","type":"t","enonce":"Un cycliste à 20 km/h doit faire 60 km.\nCombien de temps ?",
     "formule":"t = 60 ÷ 20","reponse":3,"unite":"h",
     "detail":"d=60 km, v=20 km/h  →  t = 60÷20 = 3 h"},
]

# ══════════════════════════════════════════════════════════════════
#  OLLAMA
# ══════════════════════════════════════════════════════════════════
def ask_ollama(messages, on_token, on_done, on_error):
    def run():
        try:
            prompt = ""
            for m in messages:
                prompt += (f"\n[ÉLÈVE]: {m['content']}\n" if m["role"]=="user"
                           else f"\n[VELOCITY-UNIT]: {m['content']}\n")
            prompt += "\n[VELOCITY-UNIT]: "
            r = requests.post(OLLAMA_URL,
                json={"model":MODEL,"system":SYSTEM_AIDE,"prompt":prompt,"stream":True},
                stream=True, timeout=60)
            r.raise_for_status()
            full = ""
            for line in r.iter_lines():
                if line:
                    d=json.loads(line); tok=d.get("response","")
                    full+=tok; on_token(tok)
                    if d.get("done"): break
            on_done(full)
        except requests.exceptions.ConnectionError:
            on_error("❌ Ollama non démarré !\nollama serve  puis  ollama pull llama3")
        except Exception as e:
            on_error(f"❌ Erreur : {e}")
    threading.Thread(target=run, daemon=True).start()

# ══════════════════════════════════════════════════════════════════
#  CANVAS VISUELS
# ══════════════════════════════════════════════════════════════════
class Visual(tk.Canvas):
    def __init__(self, parent, **kw):
        super().__init__(parent, bg=BGC, highlightthickness=0, **kw)
        self._mode=None; self._tick=0; self._job=None
        self.bind("<Configure>", lambda e: self._draw())

    def set_mode(self, mode):
        self._mode=mode; self._tick=0
        if self._job: self.after_cancel(self._job)
        self._loop()

    def _loop(self):
        self._tick+=1; self._draw()
        self._job=self.after(50,self._loop)

    def _draw(self):
        self.delete("all")
        W=self.winfo_width(); H=self.winfo_height()
        if W<10 or H<10 or not self._mode: return
        # grille
        s=30; off=(self._tick*2)%s
        for x in range(-s+off,W+s,s):
            self.create_line(x,0,x,H,fill=CYD,width=1,dash=(1,7))
        for y in range(0,H+s,s):
            self.create_line(0,y,W,y,fill=CYD,width=1,dash=(1,7))
        fn = {"road":self._road,"speedometer":self._speedo,
              "units_d":self._units_d,"units_t":self._units_t,
              "formula_v":lambda w,h:self._hud(w,h,"v = d ÷ t","d=km  t=h","→ km/h","200÷2=100",CYA),
              "formula_d":lambda w,h:self._hud(w,h,"d = v × t","v=km/h  t=h","→ km","20×3=60",JAU),
              "formula_t":lambda w,h:self._hud(w,h,"t = d ÷ v","d=km  v=km/h","→ h","600÷200=3",ORB),
              "triangle":self._triangle}.get(self._mode)
        if fn: fn(W,H)

    def _road(self,W,H):
        r1,r2=int(H*.55),int(H*.85)
        self.create_rectangle(0,r1,W,r2,fill="#111122",outline="")
        dw,gap=32,18; off=(self._tick*5)%(dw+gap)
        for x in range(-dw+off,W+dw,dw+gap):
            m=r1+(r2-r1)//2
            self.create_rectangle(x,m-3,x+dw,m+3,fill=JAU,outline="")
        cx=20+(self._tick*4)%max(1,W-100); cy=r1-8
        for i in range(1,9):
            self.create_line(cx-i*9,cy+18,cx-i*9+6,cy+18,fill=CYD,width=max(1,4-i//2))
        self.create_rectangle(cx,cy+6,cx+72,cy+28,fill=CYA,outline=CYG,width=2)
        self.create_rectangle(cx+13,cy-8,cx+56,cy+8,fill=CYG,outline=CYA)
        for wx in [cx+10,cx+52]:
            self.create_oval(wx,cy+22,wx+18,cy+36,fill="#1a1a2e",outline=BLA,width=2)
            self.create_oval(wx+4,cy+26,wx+14,cy+33,fill=BLA,outline="")
        self.create_rectangle(cx+66,cy+10,cx+74,cy+18,fill=JAU,outline="")
        self.create_text(cx+36,cy-18,text="??? km/h",fill=CYA,font=("Courier",9,"bold"))
        self.create_text(W//2,H-6,text="mouvement = changement de place",fill=WDI,font=("Courier",9))

    def _speedo(self,W,H):
        r=min(W,H)//2-18; cx,cy=W//2,H//2+8
        self.create_arc(cx-r,cy-r,cx+r,cy+r,start=210,extent=-240,outline=CYD,width=4,style="arc")
        for s,e,col in [(0,80,CYD),(80,160,CYA),(160,200,JAU),(200,240,ORA)]:
            self.create_arc(cx-r+5,cy-r+5,cx+r-5,cy+r-5,start=210-s,extent=-(e-s),outline=col,width=7,style="arc")
        for i in range(0,241,40):
            a=math.radians(210-i)
            self.create_line(cx+(r-8)*math.cos(a),cy-(r-8)*math.sin(a),
                             cx+(r-18)*math.cos(a),cy-(r-18)*math.sin(a),fill=CYA,width=2)
            self.create_text(cx+(r-30)*math.cos(a),cy-(r-30)*math.sin(a),
                             text=str(i*900//240),fill=WDI,font=("Courier",7))
        ang=120+90*math.sin(self._tick*0.04)
        na=math.radians(210-ang)
        self.create_line(cx,cy,cx+(r-22)*math.cos(na),cy-(r-22)*math.sin(na),fill=ORA,width=3)
        self.create_oval(cx-7,cy-7,cx+7,cy+7,fill=ORA,outline=JAU)
        self.create_text(cx,cy+r//2+4,text=f"{int(ang*900/240)} km/h",fill=CYA,font=("Courier",13,"bold"))

    def _bloc(self,cx,cy,lbl,sub,col):
        self.create_rectangle(cx-44,cy-22,cx+44,cy+22,outline=col,width=2,fill=BG)
        self.create_text(cx,cy-5,text=lbl,fill=col,font=("Courier",15,"bold"))
        self.create_text(cx,cy+13,text=sub,fill=WDI,font=("Courier",8))

    def _units_d(self,W,H):
        self.create_text(W//2,14,text="UNITÉS DE DISTANCE",fill=CYA,font=("Courier",12,"bold"))
        cx=W//2
        self._bloc(cx-120,H//2,"km","kilomètre",CYA)
        self._bloc(cx+120,H//2,"m","mètre",JAU)
        self.create_line(cx-60,H//2,cx+60,H//2,fill=ORB,width=2,arrow="both")
        self.create_text(cx,H//2-14,text="÷ 1000",fill=ORB,font=("Courier",10,"bold"))
        self.create_text(cx,H//2+14,text="× 1000",fill=ORB,font=("Courier",10,"bold"))
        self.create_text(cx,H-8,text="1 km = 1 000 m",fill=WDI,font=("Courier",10,"bold"))

    def _units_t(self,W,H):
        self.create_text(W//2,14,text="UNITÉS DE TEMPS",fill=CYA,font=("Courier",12,"bold"))
        q=W//4
        self._bloc(q,H//2,"h","heure",CYA)
        self._bloc(2*q,H//2,"min","minute",JAU)
        self._bloc(3*q,H//2,"s","seconde",ORB)
        for x1,x2,lbl in [(q+46,2*q-46,"×60 / ÷60"),(2*q+46,3*q-46,"×60 / ÷60")]:
            self.create_line(x1,H//2,x2,H//2,fill=ORA,width=2,arrow="both")
            self.create_text((x1+x2)//2,H//2-12,text=lbl,fill=ORA,font=("Courier",8,"bold"))
        self.create_text(W//2,H-8,text="1 h = 60 min = 3 600 s",fill=WDI,font=("Courier",10,"bold"))

    def _hud(self,W,H,formula,sl,sr,ex,col):
        p=2+int(abs(math.sin(self._tick*0.06))*4)
        cx,cy=W//2,H//2-8; fw,fh=min(W-40,300),46
        self.create_rectangle(cx-fw//2-p,cy-fh//2-p,cx+fw//2+p,cy+fh//2+p,outline=col,width=2,fill=BG)
        for dx,dy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
            bx=cx+dx*(fw//2+p); by=cy+dy*(fh//2+p)
            self.create_line(bx,by,bx+dx*14,by,fill=col,width=2)
            self.create_line(bx,by,bx,by+dy*14,fill=col,width=2)
        self.create_text(cx,cy,text=formula,fill=col,font=("Courier",19,"bold"))
        self.create_text(W//4,H-26,text=sl,fill=WDI,font=("Courier",9))
        self.create_text(3*W//4,H-26,text=sr,fill=WDI,font=("Courier",9))
        self.create_text(cx,H-8,text=ex,fill=JAU,font=("Courier",10,"bold"))
        sy=(self._tick*3)%H
        self.create_line(0,sy,W,sy,fill=col,width=1,dash=(2,10))

    def _triangle(self,W,H):
        cx,cy=W//2-30,H//2+5; r=min(W,H)//2-20
        pts=[(cx,cy-r),(cx-r,cy+r//2),(cx+r,cy+r//2)]
        p=abs(math.sin(self._tick*0.05))
        self.create_polygon(*[c for pt in pts for c in pt],outline=CYA,width=int(1+p*3),fill=BGC)
        self.create_line(pts[1][0],pts[1][1],pts[2][0],pts[2][1],fill=JAU,width=3)
        self.create_line(cx,pts[1][1]-4,cx,pts[2][1]+4,fill=WDI,width=2)
        self.create_text(cx,cy-r+4,text="d",fill=CYA,font=("Courier",22,"bold"))
        self.create_text(cx-r+14,cy+r//2-4,text="v",fill=JAU,font=("Courier",22,"bold"))
        self.create_text(cx+r-14,cy+r//2-4,text="t",fill=ORB,font=("Courier",22,"bold"))
        rx=cx+r+18
        for i,(col,txt) in enumerate([(JAU,"v = d ÷ t"),(CYA,"d = v × t"),(ORB,"t = d ÷ v")]):
            self.create_text(rx,cy-28+i*34,text=txt,fill=col,font=("Courier",12,"bold"),anchor="w")

# ══════════════════════════════════════════════════════════════════
#  BOUTON TKINTER PUR
# ══════════════════════════════════════════════════════════════════
def mkbtn(parent, text, bg, fg, cmd, w=224, h=48, fs=13):
    c=tk.Canvas(parent,width=w,height=h,bg=BGG,highlightthickness=0,cursor="hand2")
    def draw(hov=False):
        c.delete("all")
        bc=CYG if hov else bg
        c.create_rectangle(1,1,w-2,h-2,outline=bc,width=2,fill=BGC if hov else bg)
        c.create_text(w//2,h//2,text=text,fill=bc if hov else fg,font=("Courier",fs,"bold"))
    draw()
    c.bind("<Enter>",    lambda e: draw(True))
    c.bind("<Leave>",    lambda e: draw(False))
    c.bind("<Button-1>", lambda e: cmd())
    return c

def mklbl(parent,text,fg=WDI,fs=11,bold=False):
    return tk.Label(parent,text=text,fg=fg,bg=BGG,
                    font=("Courier",fs,"bold" if bold else "normal"),
                    wraplength=220,justify="center")

# ══════════════════════════════════════════════════════════════════
#  APPLICATION  — PAS D'HÉRITAGE tk.Tk  (fix Python 3.14)
# ══════════════════════════════════════════════════════════════════
class VelocityApp:
    def __init__(self):
        # ── Fenêtre racine créée PUIS passée à l'app ──
        self.root = tk.Tk()
        self.root.title("VELOCITY-UNIT v2.1 — Mouvement & Vitesse")
        self.root.geometry("1100x800")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        # État
        self.slide_idx    = 0
        self.conversation = []
        self.waiting_ai   = False
        self.score        = 0
        self.guide_idx    = 0
        self.etape_idx    = 0
        self.en_guide     = False
        self.etape_obj    = None
        self.libres       = list(LIBRES); random.shuffle(self.libres)
        self.ex_courant   = None
        self.saisie_num   = ""

        self._build_ui()
        self._show_accueil()

    def run(self):
        self.root.mainloop()

    # ── raccourci after
    def after(self, ms, fn=None, *a):
        return self.root.after(ms, fn, *a) if fn else self.root.after(ms)

    # ══════════════════════════════════════
    #  UI
    # ══════════════════════════════════════
    def _build_ui(self):
        root = self.root

        # Header canvas
        self._hc = tk.Canvas(root,bg=BGC,height=52,highlightthickness=0)
        self._hc.pack(fill="x")
        self._hc.bind("<Configure>",lambda e:self._dh())

        # Visual animé
        self.visual = Visual(root, height=140)
        self.visual.pack(fill="x")
        tk.Canvas(root,height=2,bg=CYD,highlightthickness=0).pack(fill="x")

        # Corps
        body=tk.Frame(root,bg=BG)
        body.pack(fill="both",expand=True)

        # Terminal
        tw=tk.Frame(body,bg=BGC)
        tw.pack(side="left",fill="both",expand=True)
        thc=tk.Canvas(tw,bg=BGG,height=22,highlightthickness=0)
        thc.pack(fill="x")
        thc.bind("<Configure>",lambda e,c=thc:self._dth(c))

        self.txt=tk.Text(tw,wrap="word",bg=BGC,fg=CYA,font=("Courier",15),
                         relief="flat",padx=16,pady=10,spacing1=5,spacing3=5,
                         state="disabled",cursor="arrow",
                         insertbackground=CYA,selectbackground=CYD)
        sc=tk.Scrollbar(tw,command=self.txt.yview,bg=BGG,troughcolor=BGC,activebackground=CYA)
        self.txt.configure(yscrollcommand=sc.set)
        sc.pack(side="right",fill="y")
        self.txt.pack(fill="both",expand=True)

        for tag,col,sz,bold in [
            ("T",CYA,18,True),("P",BLA,15,False),("F",JAU,16,True),
            ("C",ORB,15,False),("B",BLA,15,True),("D",WDI,14,False),
            ("O",ORA,14,True),("ai",VIO,15,False),("ok",JAU,16,True),
            ("er",ORA,16,True),("",BGC,5,False),
        ]:
            self.txt.tag_config(tag,foreground=col,
                                font=("Courier",sz,"bold" if bold else "normal"))

        tk.Canvas(body,width=2,bg=CYD,highlightthickness=0).pack(side="left",fill="y")

        # Panneau droit
        self._pw=tk.Frame(body,bg=BGG,width=258)
        self._pw.pack(side="left",fill="y")
        self._pw.pack_propagate(False)
        phc=tk.Canvas(self._pw,bg=BGG,height=22,highlightthickness=0)
        phc.pack(fill="x")
        phc.bind("<Configure>",lambda e,c=phc:self._dph(c))
        self.panel=tk.Frame(self._pw,bg=BGG)
        self.panel.pack(fill="both",expand=True)

        # Status
        self._sc=tk.Canvas(root,bg=BGG,height=22,highlightthickness=0)
        self._sc.pack(fill="x",side="bottom")
        self._st="PRÊT"; self._scol=CYD
        self._sc.bind("<Configure>",lambda e:self._ds())

    # ── Barres décoratives
    def _dh(self):
        c=self._hc; c.delete("all"); W=c.winfo_width()
        c.create_rectangle(0,0,W,52,fill=BGC,outline="")
        c.create_line(0,51,W,51,fill=CYD); c.create_line(0,49,W,49,fill=CYA,dash=(4,6))
        c.create_text(16,18,text="◈",fill=CYA,font=("Courier",18,"bold"),anchor="w")
        c.create_text(40,18,text="VELOCITY-UNIT  v2.1",fill=CYA,font=("Courier",15,"bold"),anchor="w")
        c.create_text(40,38,text="PHYSIQUE  ›  MOUVEMENT  •  VITESSE  •  UNITÉS",fill=CYD,font=("Courier",9),anchor="w")
        c.create_text(W-16,18,text=f"⭐ {self.score} pts",fill=JAU,font=("Courier",13,"bold"),anchor="e")
        c.create_text(16,38,text="◤",fill=CYD,font=("Courier",12),anchor="w")
        c.create_text(W-16,38,text="◥",fill=CYD,font=("Courier",12),anchor="e")

    def _dth(self,c):
        c.delete("all"); W=c.winfo_width()
        c.create_rectangle(0,0,W,22,fill=BGG,outline="")
        c.create_line(0,21,W,21,fill=CYD)
        c.create_text(12,11,text="[ TERMINAL ]",fill=CYD,font=("Courier",9),anchor="w")
        for i,col in enumerate([ORA,JAU,CYA]):
            c.create_oval(W-52+i*18,5,W-38+i*18,17,fill=col,outline="")

    def _dph(self,c):
        c.delete("all"); W=c.winfo_width()
        c.create_rectangle(0,0,W,22,fill=BGG,outline="")
        c.create_line(0,21,W,21,fill=CYD)
        c.create_text(12,11,text="[ CONTRÔLES ]",fill=CYD,font=("Courier",9),anchor="w")

    def _ds(self):
        c=self._sc; c.delete("all"); W=c.winfo_width()
        c.create_line(0,0,W,0,fill=CYD)
        c.create_text(12,11,text=f"◆  {self._st}",fill=self._scol,font=("Courier",9),anchor="w")

    def _ss(self,t,col=None): self._st=t; self._scol=col or CYD; self._ds()
    def _rs(self): self._dh()

    # ══════════════════════════════════════
    #  PANNEAUX
    # ══════════════════════════════════════
    def _cp(self):
        for w in self.panel.winfo_children(): w.destroy()

    def _pk(self,w,py=5): w.pack(pady=py,padx=12)
    def _sep(self): self._pk(tk.Canvas(self.panel,height=1,bg=CYD,highlightthickness=0,width=220),6)

    def _pan_accueil(self):
        self._cp()
        self._pk(mklbl(self.panel,"Prêt à décoller ?",CYA,13,True),20)
        self._sep()
        self._pk(mkbtn(self.panel,"▶  DÉMARRER !",CYA,BG,self._start,h=60,fs=16),10)

    def _pan_cours(self):
        self._cp()
        total=len(COURS); idx=self.slide_idx
        pc=tk.Canvas(self.panel,width=228,height=26,bg=BGG,highlightthickness=0)
        pc.pack(pady=(12,4),padx=12)
        def dp(e=None):
            pc.delete("all"); W=pc.winfo_width() or 228
            pc.create_rectangle(0,6,W,20,fill=BGC,outline=CYD)
            pc.create_rectangle(0,6,max(4,int(W*(idx+1)/total)),20,fill=CYA,outline="")
            pc.create_text(W//2,13,text=f"LEÇON {idx+1}/{total}",fill=BG,font=("Courier",9,"bold"))
        pc.bind("<Configure>",dp); self.after(10,dp)
        self._sep()
        if idx<total-1:
            self._pk(mkbtn(self.panel,"SUIVANT  ▶",CYA,BG,self._next,h=56,fs=15),8)
        else:
            self._pk(mkbtn(self.panel,"✅  J'AI COMPRIS",JAU,BG,self._compris,h=52,fs=13),8)
            self._pk(mklbl(self.panel,"— ou —"),2)
            self._pk(mkbtn(self.panel,"❓  PAS COMPRIS",ORA,BG,self._pascompris,h=46,fs=12),4)
        self._sep()
        if idx>0:
            self._pk(mkbtn(self.panel,"◀  PRÉCÉDENT",BGG,WDI,self._prev,h=38,fs=11),4)

    def _pan_aide(self):
        self._cp()
        self._pk(mklbl(self.panel,"🤖  IA explique...",VIO,13,True),16)
        self._sep()
        self._pk(mklbl(self.panel,"Quand l'IA a fini :"),8)
        self._pk(mkbtn(self.panel,"✅  J'AI COMPRIS",JAU,BG,self._compris,h=52,fs=13),8)
        self._pk(mkbtn(self.panel,"▶  SUITE DU COURS",CYA,BG,self._next,h=44,fs=12),4)

    def _pan_transition(self):
        self._cp()
        self._pk(mklbl(self.panel,"Cours terminé ! 🎉",JAU,13,True),20)
        self._sep()
        self._pk(mkbtn(self.panel,"🎯  1er EXERCICE !",CYA,BG,self._lancer_guides,h=62,fs=15),12)

    def _pan_guide_pave(self):
        self._cp()
        self._pk(mklbl(self.panel,"Tape ta réponse :",CYA,12,True),14)
        self._build_pave()

    def _pan_apres_libre(self,correct):
        self._cp()
        msg="✔  CORRECT !" if correct else "🤖  IA explique..."
        self._pk(mklbl(self.panel,msg,JAU if correct else VIO,14,True),16)
        self._sep()
        lbl="🎯  Exercice suivant" if self.libres else "🏆  Voir mon score"
        cmd=self._lancer_libre if self.libres else self._fin
        self._pk(mkbtn(self.panel,lbl,CYA,BG,cmd,h=56,fs=13),10)

    def _pan_fin(self):
        self._cp()
        self._pk(mklbl(self.panel,f"🏆  SCORE FINAL\n\n{self.score} pts",JAU,14,True),24)
        self._sep()
        self._pk(mkbtn(self.panel,"🔄  Recommencer",CYD,BG,self._restart,h=46,fs=12),12)

    # ── Pavé numérique
    def _build_pave(self):
        self.saisie_num=""
        dc=tk.Canvas(self.panel,width=228,height=54,bg=BGC,highlightthickness=0)
        dc.pack(pady=(6,4),padx=12)
        self._disp_c=dc
        def dd(e=None):
            dc.delete("all"); W=dc.winfo_width() or 228
            dc.create_rectangle(2,2,W-2,52,outline=CYA,width=2,fill=BG)
            for dx,dy in [(-1,-1),(1,-1),(-1,1),(1,1)]:
                bx=(W//2)+dx*(W//2-4); by=28+dy*24
                dc.create_line(bx,by,bx+dx*10,by,fill=CYA,width=2)
                dc.create_line(bx,by,bx,by+dy*10,fill=CYA,width=2)
            dc.create_text(W//2,28,text=self.saisie_num or "?",
                           fill=JAU,font=("Courier",24,"bold"))
        dc.bind("<Configure>",dd); self._draw_disp=dd; self.after(10,dd)
        g=tk.Frame(self.panel,bg=BGG); g.pack(pady=3)
        for i,v in enumerate([7,8,9,4,5,6,1,2,3,None,0,None]):
            r,c=divmod(i,3)
            if v is None:
                tk.Label(g,text="",width=4,bg=BGG).grid(row=r,column=c,padx=2,pady=2)
            else:
                mkbtn(g,str(v),BGC,CYA,lambda n=v:self._num(n),w=56,h=42,fs=16
                      ).grid(row=r,column=c,padx=2,pady=2)
        act=tk.Frame(self.panel,bg=BGG); act.pack(pady=(2,6))
        mkbtn(act,"⌫",BGC,ORA,self._suppr,w=56,h=40,fs=15).pack(side="left",padx=2)
        mkbtn(act,"✔  OK",CYA,BG,self._valider,w=148,h=40,fs=13).pack(side="left",padx=2)

    # ══════════════════════════════════════
    #  TERMINAL
    # ══════════════════════════════════════
    def _w(self,text,tag="P"):
        self.txt.configure(state="normal")
        self.txt.insert("end",text,tag)
        self.txt.see("end")
        self.txt.configure(state="disabled")

    def _clr(self):
        self.txt.configure(state="normal"); self.txt.delete("1.0","end")
        self.txt.configure(state="disabled")

    def _slide(self,s):
        self._clr()
        for tag,txt in s["lignes"]: self._w(txt+"\n",tag if tag else "")
        self._w("\n","")

    # ══════════════════════════════════════
    #  ACCUEIL
    # ══════════════════════════════════════
    def _show_accueil(self):
        self.visual.set_mode("road"); self._clr()
        for tag,txt in [
            ("T","╔══════════════════════════════════════════╗"),
            ("T","║  VELOCITY-UNIT v2.1  —  DÉMARRAGE...    ║"),
            ("T","╚══════════════════════════════════════════╝"),("",""),
            ("D","▸ Mouvement & Vitesse .......... CHARGÉ"),
            ("D","▸ Unités km/h, m/s, h, s ....... ACTIF"),
            ("D","▸ Exercices guidés ............. PRÊTS"),
            ("D","▸ Mode dyslexie ................ ON"),("",""),
            ("P","🚀  Salut ! Je suis VELOCITY-UNIT."),("",""),
            ("P","Je vais t'apprendre :"),
            ("C","  ●  v = d ÷ t"),("C","  ●  d = v × t"),("C","  ●  t = d ÷ v"),("",""),
            ("O","  ●  Pourquoi les UNITÉS sont importantes !"),("",""),
            ("D","  8 leçons  +  2 exercices guidés  +  5 exercices."),("",""),
            ("F","  Clique sur DÉMARRER →"),
        ]:
            self._w(txt+"\n",tag if tag else "")
        self._pan_accueil(); self._rs(); self._ss("SYSTÈME PRÊT")

    # ══════════════════════════════════════
    #  COURS
    # ══════════════════════════════════════
    def _start(self): self.slide_idx=0; self._show_slide()

    def _show_slide(self):
        s=COURS[self.slide_idx]; self._slide(s)
        self.visual.set_mode(s["visual"])
        self._ss(f"LEÇON {self.slide_idx+1}/{len(COURS)}  —  {s['titre'].upper()}")
        self._pan_cours()

    def _next(self):
        if self.slide_idx<len(COURS)-1: self.slide_idx+=1; self._show_slide()
        else: self._transition()

    def _prev(self):
        if self.slide_idx>0: self.slide_idx-=1; self._show_slide()

    def _compris(self): self._next()

    def _pascompris(self):
        self._pan_aide(); self._ss("IA EN LIGNE...",JAU)
        s=COURS[self.slide_idx]
        contenu="\n".join(t for _,t in s["lignes"] if t.strip())
        msg=f"L'élève n'a pas compris : « {s['titre']} ».\nContenu :\n{contenu}\n\nRé-explique plus simplement. Nouvel exemple. Max 6 lignes."
        self.conversation=[{"role":"user","content":msg}]
        self._w("\n"+"─"*40+"\n","D"); self._w("🤖  VELOCITY-UNIT ré-explique :\n\n","ai")
        def ok(tok): self.after(0,lambda t=tok:self._w(t,"ai"))
        def done(f):
            self.conversation.append({"role":"assistant","content":f})
            self.after(0,lambda:self._w("\n","ai")); self.after(0,lambda:self._ss("EN ATTENTE"))
        def err(e):
            self.after(0,lambda:self._w(f"\n{e}\n","er")); self.after(0,lambda:self._ss("ERREUR",ORA))
        ask_ollama(self.conversation,ok,done,err)

    # ══════════════════════════════════════
    #  TRANSITION
    # ══════════════════════════════════════
    def _transition(self):
        self.visual.set_mode("triangle"); self._ss("MODE EXERCICES"); self._clr()
        self._w("─"*42+"\n","D"); self._w("🎯  EXERCICES — À TOI DE JOUER !\n\n","T")
        self._w("Les 2 premiers sont GUIDÉS étape par étape.\n\n","P")
        self._w("  v = d ÷ t\n  d = v × t\n  t = d ÷ v\n\n","F")
        self._pan_transition()

    # ══════════════════════════════════════
    #  EXERCICES GUIDÉS
    # ══════════════════════════════════════
    def _lancer_guides(self):
        self.en_guide=True; self.guide_idx=0; self._show_guide()

    def _show_guide(self):
        ex=GUIDES[self.guide_idx]
        self.visual.set_mode({"v":"formula_v","d":"formula_d","t":"formula_t"}[ex["type"]])
        self._clr()
        self._w("─"*42+"\n","D")
        self._w(f"{ex['emoji']}  EXERCICE GUIDÉ {ex['numero']}/2  —  {ex['titre']}\n\n","T")
        self._w(ex["enonce"]+"\n\n","P")
        self._w("On résout ça ENSEMBLE, étape par étape.\n\n","D")
        self._ss(f"EXERCICE GUIDÉ {ex['numero']}/2")
        self.etape_idx=0; self._show_etape()

    def _show_etape(self):
        ex=GUIDES[self.guide_idx]
        if self.etape_idx>=len(ex["etapes"]):
            self._fin_guide(); return
        e=ex["etapes"][self.etape_idx]; self.etape_obj=e
        self._w("─"*30+"\n","D")
        self._w(f"{e['consigne']}\n\n","B")
        self._w(f"💡  {e['aide']}\n\n","D")
        self._w(f"▶  {e['question']}\n\n","C")
        self._pan_guide_pave()

    def _fin_guide(self):
        ex=GUIDES[self.guide_idx]
        self._w("─"*30+"\n","D")
        self._w("🎉  EXERCICE TERMINÉ !\n\n","ok")
        self._w(f"✔  {ex['conclusion']}\n\n","F")
        self.score+=20; self._rs(); self._ss(f"EXERCICE GUIDÉ {ex['numero']} TERMINÉ !",JAU)
        self._cp()
        if self.guide_idx<len(GUIDES)-1:
            self._pk(mklbl(self.panel,"Super ! 🎉",JAU,14,True),20)
            self._sep()
            self._pk(mkbtn(self.panel,"▶  Exercice guidé 2",CYA,BG,self._next_guide,h=54,fs=13),10)
        else:
            self._pk(mklbl(self.panel,"Tu es prêt ! 🚀",JAU,14,True),20)
            self._sep()
            self._pk(mkbtn(self.panel,"🎯  Exercices libres !",CYA,BG,self._lancer_libre,h=54,fs=13),10)

    def _next_guide(self):
        self.guide_idx+=1; self.etape_idx=0; self._show_guide()

    # ══════════════════════════════════════
    #  PAVÉ
    # ══════════════════════════════════════
    def _num(self,n):
        if len(self.saisie_num)<5:
            self.saisie_num+=str(n)
            if hasattr(self,"_draw_disp"): self._draw_disp()

    def _suppr(self):
        self.saisie_num=self.saisie_num[:-1]
        if hasattr(self,"_draw_disp"): self._draw_disp()

    def _valider(self):
        if not self.saisie_num: return
        rep=int(self.saisie_num); self.saisie_num=""
        if self.en_guide: self._verif_etape(rep)
        else: self._verif_libre(rep)

    def _verif_etape(self,rep):
        e=self.etape_obj; bonne=e["reponse"]
        if rep==bonne:
            self._w(f"    ✔  {e['bravo']}\n\n","ok")
            self.etape_idx+=1; self.after(400,self._show_etape)
        else:
            self._w(f"    ✘  Tu as tapé {rep}.  Attendu : {bonne}\n","er")
            self._w(f"    💡  {e['aide']}\n\n","D")
            msg=(f"L'élève a répondu {rep}, la bonne réponse est {bonne}.\n"
                 f"Question : {e['question']}\nIndice : {e['aide']}\n"
                 f"Explique gentiment pourquoi. Max 4 lignes.")
            self.conversation=[{"role":"user","content":msg}]
            self._w("🤖  VELOCITY-UNIT :\n\n","ai")
            def ok(tok): self.after(0,lambda t=tok:self._w(t,"ai"))
            def done(f):
                self.conversation.append({"role":"assistant","content":f})
                self.after(0,lambda:self._w("\n\n","ai"))
                self.after(600,self._show_etape)
            def err(e2):
                self.after(0,lambda:self._w(f"\n{e2}\n","er"))
                self.after(600,self._show_etape)
            ask_ollama(self.conversation,ok,done,err)

    # ══════════════════════════════════════
    #  EXERCICES LIBRES
    # ══════════════════════════════════════
    def _lancer_libre(self):
        self.en_guide=False
        if not self.libres: self._fin(); return
        ex=self.libres.pop(0); self.ex_courant=ex
        self.visual.set_mode({"v":"formula_v","d":"formula_d","t":"formula_t"}[ex["type"]])
        n=len(LIBRES)-len(self.libres)
        self._clr()
        self._w("─"*42+"\n","D")
        self._w(f"{ex['emoji']}  EXERCICE LIBRE {n}/{len(LIBRES)}\n\n","T")
        self._w(ex["enonce"]+"\n\n","P")
        self._w(f"   Formule : {ex['formule']} = ?\n\n","F")
        self._ss(f"EXERCICE LIBRE {n}  —  TAPE TA RÉPONSE")
        self._cp()
        self._pk(mklbl(self.panel,"Tape ta réponse :",CYA,12,True),14)
        self._build_pave()

    def _verif_libre(self,rep):
        ex=self.ex_courant; self.ex_courant=None; bonne=ex["reponse"]
        if rep==bonne:
            self.score+=10; self._rs()
            self._w(f"\n✔  CORRECT !  {bonne} {ex['unite']}\n","ok")
            self._w(f"   {ex['detail']}\n","D")
            self._pan_apres_libre(True)
        else:
            self._w(f"\n✘  Tu as mis {rep}  →  attendu : {bonne} {ex['unite']}\n","er")
            self._w(f"   {ex['detail']}\n\n","D")
            self._pan_apres_libre(False)
            msg=(f"L'élève a répondu {rep} au lieu de {bonne} {ex['unite']}.\n"
                 f"Exercice : {ex['enonce']}\nSolution : {ex['detail']}\n"
                 f"Explique doucement. Étape par étape. Encourage. Max 5 lignes.")
            self.conversation=[{"role":"user","content":msg}]
            self._ss("IA ANALYSE...",JAU)
            self._w("\n🤖  VELOCITY-UNIT explique :\n\n","ai")
            def ok(tok): self.after(0,lambda t=tok:self._w(t,"ai"))
            def done(f):
                self.conversation.append({"role":"assistant","content":f})
                self.after(0,lambda:self._w("\n\n","ai")); self.after(0,lambda:self._ss("EN ATTENTE"))
            def err(e):
                self.after(0,lambda:self._w(f"\n{e}\n","er")); self.after(0,lambda:self._ss("ERREUR",ORA))
            ask_ollama(self.conversation,ok,done,err)

    # ══════════════════════════════════════
    #  FIN
    # ══════════════════════════════════════
    def _fin(self):
        self.visual.set_mode("speedometer"); self._ss("MISSION ACCOMPLIE !",JAU); self._clr()
        self._w("─"*42+"\n","D"); self._w("🏆  MISSION ACCOMPLIE !\n\n","T")
        self._w("Tu maîtrises :\n","P")
        self._w("  v = d ÷ t\n  d = v × t\n  t = d ÷ v\n\n","F")
        self._w("  + Les unités  km/h  m/s  h  s  km  m\n\n","C")
        self._w(f"Score final : {self.score} points ⭐\n","ok")
        self._pan_fin()

    def _restart(self):
        self.score=0; self.slide_idx=0; self.guide_idx=0; self.etape_idx=0
        self.en_guide=False; self.libres=list(LIBRES); random.shuffle(self.libres)
        self.conversation=[]; self._show_accueil()

# ══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = VelocityApp()
    app.run()
