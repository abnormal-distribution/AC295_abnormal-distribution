Practicum 1 - Art Search Engine
==============================

Abnormal Distribution

Local build
------------
    
docker build -t simple_query:frontend -f Docker_simple_query_frontend .

docker build -t database:db -f Docker_maindb .   

docker-compose up -d

docker-compose down

Minikube
------------

minikube start

eval $(minikube docker-env)

docker build -t simple_query:frontend -f Docker_simple_query_frontend .

docker build -t database:db -f Docker_maindb .   

kubectl apply -f webapp_configmap.yaml

kubectl apply -f webapp_db_deployment_k8s.yaml

kubectl apply -f simple_query_deployment_k8s.yaml

minikube service webapp-simplequery-service


minikube delete

eval $(minikube -u minikube docker-env)
