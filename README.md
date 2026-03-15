# 🎓 Programmes Pédagogiques Interactifs

Applications éducatives pour élèves de 6e avec difficultés d’apprentissage.  
Style terminal rétro • Compatible Python 3.14 • IA locale via Ollama

-----

## 📦 Programmes inclus

|Fichier                  |Matière      |Sujet                                      |
|-------------------------|-------------|-------------------------------------------|
|`velocity_unit.py`       |Physique     |Mouvement, vitesse, distance, temps, unités|
|`produit_en_croix_crt.py`|Mathématiques|Le produit en croix                        |

-----

## ✅ Prérequis

- **Python 3.8 ou supérieur** → [python.org](https://www.python.org/downloads/)
- **Ollama** (IA locale) → [ollama.com](https://ollama.com)

-----

## 🚀 Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/TON_USERNAME/NOM_DU_REPO.git
cd NOM_DU_REPO
```

### 2. Installer la dépendance Python

```bash
pip install requests
```

### 3. Installer et démarrer Ollama

```bash
# Télécharger Ollama sur https://ollama.com puis :
ollama serve
ollama pull llama3
```

> Ollama doit tourner en arrière-plan avant de lancer les programmes.

-----

## ▶️ Lancement

### Physique — Mouvement & Vitesse

```bash
python velocity_unit.py
```

### Mathématiques — Produit en Croix

```bash
python produit_en_croix_crt.py
```

-----

## 🎯 Fonctionnalités

### Les deux programmes partagent :

- Interface style **terminal CRT rétro** animé
- Navigation par **boutons cliquables** (pas de clavier)
- **Pavé numérique** pour les réponses aux exercices
- **IA locale** (Ollama) qui intervient uniquement si l’élève ne comprend pas ou fait une erreur
- Adapté **dyslexie** : phrases courtes, une idée à la fois
- Adapté **daltonisme** : palette cyan / orange / jaune (pas de vert/rouge)

### VELOCITY-UNIT (Physique)

- 8 leçons scénarisées : mouvement → unités → 3 formules → triangle magique
- Visuels animés : voiture sur route, compteur de vitesse, formules HUD
- Notion d’unités : km/h vs m/s, conversions km↔m et h↔s
- 2 exercices **entièrement guidés** étape par étape
- 5 exercices libres avec correction IA

### PRODUIT EN CROIX (Maths)

- 5 leçons scénarisées
- Schéma de proportion toujours visible
- Exercices avec pavé numérique
- Correction et encouragements via IA

-----

## 🗂️ Structure du projet

```
.
├── velocity_unit.py          # Programme physique
├── produit_en_croix_crt.py   # Programme maths
└── README.md
```

-----

## 🔧 Changer de modèle IA

Par défaut les programmes utilisent `llama3`.  
Pour utiliser un autre modèle, modifie la ligne en haut de chaque fichier :

```python
MODEL = "llama3"   # ← remplace par : mistral, gemma3, qwen2.5, etc.
```

Puis télécharge le modèle choisi :

```bash
ollama pull mistral
```

-----

## 📝 Notes techniques

- Aucune connexion internet requise (IA 100% locale)
- Pas de `customtkinter` : tkinter standard uniquement
- Testé sur macOS avec Python 3.14
- La dépendance `requests` sert uniquement à communiquer avec Ollama en local

-----

## 👨‍💻 Auteur

Jonathan Zerbib — Audioprothésiste & développeur de outils pédagogiques  
Cabinet **Ouïe Audition** — Fontenay-sous-Bois
