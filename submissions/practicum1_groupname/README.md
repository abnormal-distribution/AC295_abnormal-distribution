Practicum 1 - Art Search Engine
==============================

Abnormal Distribution

Local build
------------
    
docker build -t frontend:fe -f Docker_frontend .

docker build -t simidatabase:db -f Docker_similarity .

docker build -t metadatabase:db -f Docker_metaDataQuery .  

docker-compose up -d

docker-compose down

Minikube
------------

minikube start

eval $(minikube docker-env)

docker build -t frontend:fe -fDocker_frontend .

docker build -t simidatabase:db -f Docker_similarity .

docker build -t metadatabase:db -f Docker_metaDataQuery .

kubectl apply -f webapp_configmap.yaml

kubectl apply -f backend_metaDataQuery_deployment_k8s.yaml

kubectl apply -f backend_similarity_deployment_k8s.yaml

kubectl apply -f frontend_deployment_k8s.yaml

minikube service webapp-frontend-service


minikube delete

eval $(minikube -u minikube docker-env)
