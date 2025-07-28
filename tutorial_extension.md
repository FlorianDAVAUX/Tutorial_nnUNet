# Tutorial installation extension
---

## 📚 Sommaire

- [Étape 0️⃣ – Telechargement du depot](#étape-0️⃣--téléchargement-du-depôt)
- [Étape 1️⃣ - Intégration dans 3D Slicer](#étape-1️⃣---intégration-dans-3d-slicer)
- [Étape 2️⃣ - Ouverture dans 3D Slicer](#étape-2️⃣---ouverture-dans-3d-slicer)

---

# Étape 0️⃣ – Téléchargement du depôt

Premièrement il faut télécharger ce dépot : [LungSegmentation](https://github.com/FlorianDAVAUX/SlicerLungSegmentation)
```
git clone https://github.com/FlorianDAVAUX/SlicerLungSegmentation.git
```
---

# Étape 1️⃣ - Intégration dans 3D Slicer

Une fois que l'extension est téléchargée il faut l'intégrer dans 3D Slicer :
- Ouvrir **3D SLicer**
- Ouvrir **Edit**
- Ouvrir **Application settings**
- Cliquer sur **Module** et observer l'élément **Additional module paths:** de cet onglet
- Ajouter dans module le chemin vers **LungSegmentation**  
⚠️ Il faut ajouter le chemin vers le dossier **LungSegmentation**, pas le chemin vers l'extension complète **SlicerLungSegmentation**.
- Relancer **3D Slicer**

---

# Étape 2️⃣ - Ouverture dans 3D Slicer

Une fois que vous relancez 3D Slicer, vous pouver ouvrir le menu **Modules** puis dans **Segmentation** vous devriez avoir l'extension **LungSegmentation**.  
Une fois l'extension disponible, la documentation pour l'utilisation est disponible dans le README.md de [LungSegmentation](https://github.com/FlorianDAVAUX/SlicerLungSegmentation).  
