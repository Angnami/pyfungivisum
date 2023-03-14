# pyfungivisum : Identification de l'espèce d'un champignon
[Présentation du projet](#Présentation)


Ce projet est réalisé dans le cadre de la formation MLOps que j'ai suivie chez Datascientest du 04/10/2022 au 14/03/2023. Il a pour objectif de déployer le modèle de Deep Learning que j'ai développé avec Clement Tellier, Daniela Lazar et Laure Duboeuf pour l'identification de l'espèce d'un champignon à partir de son image.


[Description sommaire de la modélisation](#Modélisation)

## Espèces retenues:
* Amanita flavoconia
* Amanita muscaria
* Baorangia bicolor
* Boletus edulis
* Coprinus comatus
* Galerina marginata
* Ganoderma applanatum
* Hypholoma fasciculare
* Laetiporus sulphureus
* Phaeolus schweinitzii
* Pleurotus ostreatus
* Pluteus cervinus
* Psathyrella candolleana
* Psilocybe cyanescens
* Psilocybe zapotecorum

## Données

* Entrainement: 11 104 images
* Test: 2 777 images


## Approche méthodologique

* CNN from scratch : baseline
* Transfer Learning : VGG16, VGG19, ResNet50, EfficientNetB

## Meilleur modèle

* Meilleure performance : Accuracy, recall et precison de 85%
* Meilleur modèle : EfficientNetB0



