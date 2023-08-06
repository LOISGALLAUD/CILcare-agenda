# **CILpink-agenda**

<img src="https://www.cilcare.com/wp-content/uploads/2014/10/logo-cilcare-20141.jpg" width=200 align="right">

Cette application est un agenda pour l'organisation interne de Cilcare. Elle permet de gérer les études, les opérateurs, les équipements et les salles d'étude.

## **Installation**

Un Dockerfile est présent à la racine du projet, il suffit donc de construire l'image Docker et de la lancer.

```bash
docker build -t cilcare-agenda .
docker run cilcare-agenda
```
