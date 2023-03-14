# pyfungivisum : Identification de l'espèce d'un champignon

## Objectif

Ce projet est réalisé dans le cadre de la formation MLOps que j'ai suivie chez Datascientest du 04/10/2022 au 14/03/2023. Il a pour objectif de déployer le modèle de Deep Learning que j'ai développé avec Clement Tellier, Daniela Lazar et Laure Duboeuf pour l'identification de l'espèce d'un champignon à partir de son image.

## Modélisation
### Espèces retenues:
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

### Données

* Entrainement: 11 104 images
* Test: 2 777 images


### Approche méthodologique

* CNN from scratch : baseline
* Transfer Learning : VGG16, VGG19, ResNet50, EfficientNetB

### Meilleur modèle

* Meilleure performance : Accuracy, recall et precison de 85%
* Meilleur modèle : EfficientNetB0

## Création d'une API avec FastAPI pour exposer le modèle

L'API comporte 4 routers:
* home : pour vérifier que l'application fonctionne normalement
* user avec 4 routes:
 * /subscription : pour s'identifier afin de pouvoir utiliser l'application
 * /update : pour modifier les informations d'un utilisateur
 * /token : pour générer un token de connexion
 * /unsubscribe : pour se désinscrire 
* admin avec 3 routes:
 * /database: reset_table
 * /users/remove : pour supprimer un utilisateur
 * /users/show: pour afficher tous les utilisateurs
* predictions avec 3 routes:
 * /new_prediction : pour charger l'image d'un champignon et connaitre son espèce
 * /existing_predictions : pour affciher les prédictions déjà effectuées
 * /deletion: pour supprimer les prédictions existentes

## Création d'une base de données MySQL pour stocker les informations des utilisateurs et les prédictions du modèle

La base de données (pyfungivisum) est composée de deux tables : users et predictions.

```sql
USE pyfungivisum;
DROP TABLE IF EXISTS `predictions`;
DROP TABLE IF EXISTS `users`;

CREATE TABLE `users`(
`id` varchar(100) NOT NULL,
`username` varchar(50) NOT NULL,
`firstname` varchar(50) NOT NULL,
`lastname` varchar(50) NOT NULL,
`email` varchar(200) NOT NULL,
`is_admin` varchar(5) DEFAULT 'false',
`hashedpassword` varchar(200) NOT NULL,
PRIMARY KEY (`id`)
)engine=InnoDB  DEFAULT CHARSET=latin1;

CREATE TABLE `predictions`(
`id` varchar(100) NOT NULL,
`imagename` varchar(50) NOT NULL,
`confidence` float NOT NULL,
`predictedspecy` varchar(50) NOT NULL,
`presumedspecy` varchar(50) DEFAULT NULL,
`userid` varchar(100) NOT NULL,
 PRIMARY KEY(`id`),
 FOREIGN KEY(`userid`) REFERENCES users(`id`)
 ON DELETE CASCADE ON UPDATE CASCADE
)engine=InnoDB  DEFAULT CHARSET=latin1;

```


