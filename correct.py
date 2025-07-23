import os
import re
import nrrd
import numpy as np
import SimpleITK as sitk
import argparse

# labels_dir = '/home/davaux/Documents/Rats/3DUNet_Rats/nnUNet_raw/Dataset001_rats/labelsTr'
# images_dir = '/home/davaux/Documents/Rats/3DUNet_Rats/nnUNet_raw/Dataset001_rats/imagesTr'

# label_mapping = {
#     "background" : 0,
#     "kidneys" : 1,
#     "liver" : 2,
#     "spleen" : 3,
#     "lungs" : 4,
#     "heart" : 5,
#     "parenchyma" : 6,
#     "airways" : 7
# }

# # def main(args) :
# for label_file in os.listdir(labels_dir):
#     if label_file.endswith('.nrrd'):
#         label_path = os.path.join(labels_dir, label_file)

#         # Charger le fichier NRRD
#         data, header = nrrd.read(label_path)

#         # Copier les données et le header
#         new_data = np.copy(data)
#         new_header = header.copy()

#         print(f"Traitement de {label_file}...")

#         # Modifier les valeurs dans new_data en fonction du mapping
#         for key in header.keys():
#             match = re.match(r"Segment(\d+)_Name$", key)
#             if match:
#                 segment_index = match.group(1)
#                 segment_name = header[key].lower()
                
#                 if segment_name in label_mapping:
#                     old_value = int(header[f"Segment{segment_index}_LabelValue"])
#                     new_value = label_mapping[segment_name]

#                     print(f"Segment{segment_index}_Name: {segment_name} -> {new_value}")

#                     # Modifier les valeurs de `new_data`
#                     new_data[data == old_value] = new_value

#                     # Mettre à jour le header
#                     new_header[f"Segment{segment_index}_LabelValue"] = str(new_value)

#                 else:
#                     print(f"⚠️ Warning: '{segment_name}' non trouvé dans label_mapping !")

#         # Sauvegarder la segmentation modifiée
#         new_label_path = label_path.replace(".nrrd", "_modified.nrrd")

#         # Sauvegarde
#         nrrd.write(new_label_path, data=new_data, header=new_header)


#         # Chercher l'image correspondante
#         image_file = label_file.replace('.nrrd', '_0000.nrrd')
#         image_path = os.path.join(images_dir, image_file)

#         if os.path.exists(image_path):
#             # Charger l'image et la segmentation modifiée
#             image = sitk.ReadImage(image_path)
#             seg = sitk.ReadImage(new_label_path)

#             # Resampling avec interpolation nearest neighbor (préserve les valeurs des labels)
#             resampler = sitk.ResampleImageFilter()
#             resampler.SetReferenceImage(image)
#             resampler.SetInterpolator(sitk.sitkNearestNeighbor)
#             seg_resampled = resampler.Execute(seg)

#             # Corriger l'origine et la direction
#             seg_resampled.SetDirection(image.GetDirection())
#             seg_resampled.SetOrigin(image.GetOrigin())

#             # Sauvegarder la segmentation redimensionnée
#             resampled_label_path = os.path.join(labels_dir, label_file.replace('.nrrd', '_resampled.nrrd'))
#             sitk.WriteImage(seg_resampled, resampled_label_path)

#             print(f"✅ Segmentation {label_file} redimensionnée et sauvegardée.")
#         else:
#             print(f"⚠️ Image {image_file} non trouvée.")

# print("\nTous les fichiers ont été traités.")

import os
import re
import nrrd
import numpy as np
import SimpleITK as sitk
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Remappe les labels et redimensionne les segmentations.")
    parser.add_argument('--images_dir', required=True, help='Chemin vers le dossier des images')
    parser.add_argument('--labels_dir', required=True, help='Chemin vers le dossier des labels')
    parser.add_argument('--classes', nargs='+', required=True, help='Liste des classes utilisées dans le mapping')
    return parser.parse_args()

def main(images_dir, labels_dir, classes):
    label_mapping = {name: idx for idx, name in enumerate(['background'] + classes)}

    for label_file in os.listdir(labels_dir):
        if label_file.endswith('.nrrd'):
            label_path = os.path.join(labels_dir, label_file)

            data, header = nrrd.read(label_path)
            new_data = np.copy(data)
            new_header = header.copy()

            print(f"🔄 Traitement de {label_file}...")

            for key in header.keys():
                match = re.match(r"Segment(\d+)_Name$", key)
                if match:
                    segment_index = match.group(1)
                    segment_name = header[key].lower()

                    if segment_name in label_mapping:
                        old_value = int(header[f"Segment{segment_index}_LabelValue"])
                        new_value = label_mapping[segment_name]

                        print(f"  ➤ {segment_name}: {old_value} -> {new_value}")

                        new_data[data == old_value] = new_value
                        new_header[f"Segment{segment_index}_LabelValue"] = str(new_value)
                    else:
                        print(f"⚠️  Warning: '{segment_name}' non trouvé dans le label_mapping !")

            new_label_path = label_path.replace(".nrrd", "_modified.nrrd")
            nrrd.write(new_label_path, data=new_data, header=new_header)

            image_file = label_file.replace('.nrrd', '_0000.nrrd')
            image_path = os.path.join(images_dir, image_file)

            if os.path.exists(image_path):
                image = sitk.ReadImage(image_path)
                seg = sitk.ReadImage(new_label_path)

                resampler = sitk.ResampleImageFilter()
                resampler.SetReferenceImage(image)
                resampler.SetInterpolator(sitk.sitkNearestNeighbor)
                seg_resampled = resampler.Execute(seg)

                seg_resampled.SetDirection(image.GetDirection())
                seg_resampled.SetOrigin(image.GetOrigin())

                resampled_label_path = os.path.join(labels_dir, label_file.replace('.nrrd', '_resampled.nrrd'))
                sitk.WriteImage(seg_resampled, resampled_label_path)

                print(f"✅ Sauvegardé : {resampled_label_path}")
            else:
                print(f"❌ Image {image_file} introuvable.")

    print("\n🧹 Nettoyage des fichiers temporaires...")

    for file_name in os.listdir(labels_dir):
        file_path = os.path.join(labels_dir, file_name)

        # Supprimer les anciens fichiers .nrrd originaux (non "_resampled", non "_modified")
        if file_name.endswith('.nrrd') and not ('_resampled' in file_name or '_modified' in file_name):
            os.remove(file_path)
            print(f"🗑️ Supprimé original : {file_name}")

        # Supprimer les fichiers "_modified"
        elif '_modified.nrrd' in file_name:
            os.remove(file_path)
            print(f"🗑️ Supprimé modifié : {file_name}")

        # Renommer les fichiers "_resampled" -> version finale sans suffixe
        elif '_resampled.nrrd' in file_name:
            new_name = file_name.replace('_resampled.nrrd', '.nrrd')
            new_path = os.path.join(labels_dir, new_name)
            os.rename(file_path, new_path)
            print(f"📛 Renommé : {file_name} → {new_name}")

    print("\n🎉 Tous les fichiers ont été traités et nettoyés.")

if __name__ == "__main__":
    args = parse_arguments()
    main(args.images_dir, args.labels_dir, args.classes)
