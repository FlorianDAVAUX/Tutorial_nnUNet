# Tutorial_nnUNet


---

# 🧰 Prérequis – Installation de nnU-Net v2

```
# Cloner le dépôt
git clone https://github.com/MIC-DKFZ/nnUNet.git
cd nnUNet

# Installer les dépendances
pip install -e .
```
---
# Étape 0️⃣ – Préparation des masques

Avant d’utiliser nnU-Net, il faut que les masques de segmentation soient bien formatés, avec les classes correctement étiquetées :  
⚠️ le label 0 correspond au background (obligatoire pour nnU-Net)  

Pour réaliser la partie background, il faut aller dans la section *Data* de 3D Slicer puis, clique droit sur le masque et cliquer sur *Export visible segments to binary label map*.    
Une fois cela fait, aller dans la section *Segment editor* et dans *Source Volume*, chargé ce nouveau masque binaire qui vient dêtre généré.     
METTRE UN EXEMPLE DE MASQUE BINAIRE  
Ensuite, utiliser l'outil *Threshold* et cliquer sur une zone qui ne contient pas de pixels appartenant au masque (une zone noire) et cliquer sur *Apply*.    
Pour finir, renommer ce nouveau segment en *background*.

---
# Étape 1️⃣ - Organisation des données
La première étape une fois que nnUNet est clôné et compilé est l'organisation des données afin de respecter le schéma souhaité par nnUNet. Il faut créer 3 dossiers :
```
3D_UNet
└── nnUNet_results/
└── nnUNet_raw/
└── nnUNet_preprocessed/  
```
- **nnUNet_results** : va contenir les résultats des entraînements (le laisser vide pour l'instant)  
- **nnUNet_preprocessed** : va contenir les images preprocessed par nnUNet (le laisser vide également)  
- **nnUNet_raw** : va contenir les données utilisées pour l'entraînement et c'est ce dossier qui va nous intéresser dans un premier temps puisque la disposition des données doit se faire de cette façon :  
```
nnUNet_raw/  
└── DatasetXXX_name/  
    ├── imagesTr/  
    │   ├── 001_0000.nrrd  # images de training   
    │   ├── 002_0000.nrrd
    │   ├── ...
    ├── labelsTr/  
    │   ├── 001.nrrd       # masques de 3D Slicer  
    │   ├── 002.nrrd
    │   ├── ...
    ├── imagesTs/  
    │   ├── 008.nrrd       # images de test  
    │   ├── 009.nrrd
    │   ├── ...
    ├── dataset.json       # fichier de configuration
```

⚠️ Le nom du couple image/masque est important. Exemple : l'image 001_0000.nrrd doit être associée au masque 001.nrrd.  
⚠️ L'extension **.nnrd** est importante. Il est possible de converitr une image DICOM en .nrrd en la chargant dans 3D SLicer et en exportant l'image, de choisir l'extension souhaitée.   
⚠️ La séparation entre images de training et images de test se fait avec un ratio de 80/20% pour maximiser les performances.

## Écriture du fichier de configuration :
### Exemple d'un fichier de configuration
```
{
    "name": "Dataset00X_name",
    "description": "Test_Segmentation",
    "tensorImageSize": "3D",
    "reference": "",
    "licence": "",
    "release": "1.0",
    "labels": {
        "background" : 0,
        "airways" : 1
    },
    "numTraining": 4,
    "numTest": 2,
    "training": [
        {"image": "./imagesTr/001_0000.nrrd", "label": "./labelsTr/001.nrrd"},
        {"image": "./imagesTr/002_0000.nrrd", "label": "./labelsTr/002.nrrd"},
        {"image": "./imagesTr/003_0000.nrrd", "label": "./labelsTr/003.nrrd"},
        {"image": "./imagesTr/004_0000.nrrd", "label": "./labelsTr/004.nrrd"},
    ],
    "test": [
        {"image": "./imagesTs/0_0000.nrrd"},
        {"image": "./imagesTs/012_0000.nrrd"}

    ],
    "channel_names": {
    "0": "CT"
    },
    "file_ending": ".nrrd"
}

```
- **name** : nom du dataset d'images (le même que celui présent dans le dossier **nnUNet_raw**)
- **description** : indication sur la tâche de segmentation (pas nécessaire)
- **tensorImageSize** : laisser 3D pour les images du SPCCT
- **labels** : laisser le *background* en 0 et ensuite, lister sans ordre d'importance les autres classes du masques (parenchyme, lobes etc)
- **numTraining** : nombre d'images de training présentes dans imagesTr
- **numTest** : nombre d'images de test présentes dans imagesTs
- **training** : liste des couples image/masque du dataset
- **test** : liste des images présentes dans imagesTs
- **channel_names** : laisser *CT* pour les images du SPCCT
- **file_ending** : laisser *.nrrd" si les images sonts exportés en *.nrrd*

---
# Étape 2️⃣ - Préparation des données
⚠️ **AVANT** de continuer, il faut **export** les chemins vers ces dossiers dans l'environement qui va executer la commande pour effectuer le preprocessing.  
```
export nnUNet_raw="path/to/nnUNet_raw"
export nnUNet_preprocessed="path/to/nnUNet_preprocessed"
export nnUNet_results="path/to/nnUNet_results"
```
Une fois que les données sont organisées de la bonne façon. Il faut executer un script **correct.py** qui permet de corriger le nom et le numéro des classes.  
Comme évoqué précédemment, background **DOIT** avoir le label 0. Ensuite, l'ordre des classes n'importe pas.

