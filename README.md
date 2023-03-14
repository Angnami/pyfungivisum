# pyfungivisum : Identification de l'espèce d'un champignon

## Objectif

Ce projet est réalisé dans le cadre de la formation [MLOps](https://datascientest.com/formation-ml-ops) que j'ai suivie chez [Datascientest](https://datascientest.com/) du 04/10/2022 au 14/03/2023. Il a pour objectif de déployer le modèle de Deep Learning que j'ai développé avec [Clement Tellier](https://www.linkedin.com/in/clement-tellier-365a9743/), [Daniela Lazar](https://www.linkedin.com/in/daniela-lazar-596720107/) et [Laure Duboeuf](https://www.linkedin.com/in/laure-duboeuf-16b712114/) pour la validation du parcours [Data Scientist](https://datascientest.com/formation-data-scientist). Ce modèle avait été conçu pour l'identification de l'espèce d'un champignon à partir de son image.

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

* Entrainement & Validation: 11 104 images
    * Training set : 8 883 images
    * Validation set : 2 221 images
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
* admin avec 3 routes (doits d'administrateur nécessaires!):
    * /database: pour réinitialiser une table de la base
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

## Conteneurisation de l'API et de la base de données

### API

```docker
FROM debian:latest

WORKDIR /app

COPY . .

RUN apt update && apt install python3-pip  -y  
RUN apt update && apt install python3-opencv -y libopencv-dev
RUN pip install --upgrade pip
RUN pip install tensorflow
RUN pip install -r requirements.txt

EXPOSE 9000

CMD uvicorn main:app --host 0.0.0.0 --port 9000

```
### Base de données

```docker
FROM mysql:latest

COPY ./create_db.sql /docker-entrypoint-initdb.d/
```

### Docker-compose (API & BD)

```docker
version: "3.9"
services:
  mysql:
    container_name: mysql
    image: angnami/pyfungivisum-db:latest
    env_file:
      - ./envs/.env
    ports:
      - "306:3306"
    volumes:
      - mysqldata:/var/lib/mysql
    healthcheck:
        test: ["CMD", "mysqladmin" ,"ping", "-h", "mysql"]
        timeout: 10s
        retries: 10
    networks:
      - mysqlnet
    restart: always

  pyfungivisum-app:
    image: angnami/pyfungivisum-app:latest
    container_name: pyfungivisum-app
    command: sh -c "sleep 10s; uvicorn main:app --host 0.0.0.0 --port 9000"
    depends_on:
      - mysql
    networks:
      - mysqlnet
    ports:
      - "9000:9000"
    restart: always
    env_file:
      - ./envs/.env
  adminer:
    image: adminer
    container_name: adminer
    depends_on:
    - mysql
    ports:
    - "8080:8080"
    networks:
    - mysqlnet
    restart: always

volumes:
  mysqldata:
networks:
  mysqlnet:

```

## Deploiement sur AWS avec kubernetes

### Conversion du fichier docker-compose.yml pour créer automatiquement les manifestes des objets kubernetes nécessaires après avoir installé l'outil kompose 

Les différents fichiers créés se trouvent dans le sous-dossier aws du dossier kubernetes.
```
kompose convert

```

### Connexion au compte aws après avoir installé aws cli

```
aws configure

```

###  Création du cluster après avoir installé eksctl

```
eksctl create cluster --name pyfungivisum-cluster --nodegroup-name pyfungivisum-cluster-node-group  --node-type m5.large --nodes 3 --nodes-min 3 --nodes-max 5 --managed --asg-access --zones=us-east-1a,us-east-1b

```

### Création des différents objets kubernetes

```kubernetes

kubectl apply -f api-deployment.yaml
kubectl apply -f api-service.yaml
kubectl apply -f mysql-deployment.yaml
kubectl apply -f mysql-service.yaml
kubectl apply -f mysqldata-persistentvolume.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml

```

