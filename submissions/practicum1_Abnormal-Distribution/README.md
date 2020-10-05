# Art Search Engine by Abnormal Distribution

## Practicum 1


## Eduardo PEYNETTI, Jessica WIJAYA, Rohit BERI, Stuart NEILSON


## Overview
Art Search Engine comprises of three parts:
* Frontend for user input
* Backend 1 for managing the metadata search
* Backend 2 for managing the similar image search
* You can watch a short intro video [here](https://youtu.be/vchr2w84GtQ)
* A short note on the project is available [here](https://drive.google.com/file/d/1KSdzLSLOFbbH6Z0HAxVmzRVX39Ov86JU/view?usp=sharing)


## Practicum Memo
* [Link Here](https://drive.google.com/file/d/1KSdzLSLOFbbH6Z0HAxVmzRVX39Ov86JU/view?usp=sharing)


## Video Presentation
* [Link Here](https://youtu.be/vchr2w84GtQ)


## How to build and deploy the Art Search Engine

### Step 0: Clone repo
* Clone the repo to a local or a virtual machine

### Step 1: Setup ```gcloud```
* Create an account on Google Cloud
* Create a project on Google Cloud Console and take note of project id (```PROJECT_ID```)
* Install the latest Cloud SDK version
* Initialize the ```gcloud``` with the command ```gcloud init``` and follow the instructions
* Make sure to select the correct project

### Step 2: Set environment variables
* Run the following commands to set the environment and to check the ```gloud``` configuration
```
export PROJECT_ID=gothic-space-289008
gcloud config set project $PROJECT_ID
gcloud config list
gcloud auth configure-docker
```

### Step 3: Build docker images
* Execute the below commands on the shell from the following folder ```~/AC295_abnormal-distribution/submissions/practicum1_Abnormal-Distribution/```
```
docker build -t gcr.io/${PROJECT_ID}/frontend:fe -f frontend/Docker_frontend ./frontend
docker build -t gcr.io/${PROJECT_ID}/metadatabase:db -f backend_metaDataQuery/Docker_metaDataQuery ./backend_metaDataQuery
docker build -t gcr.io/${PROJECT_ID}/simidatabase:db -f backend_similarity/Docker_similarity ./backend_similarity
```

### Step 4: Push docker images to ```gcloud```
```
docker push gcr.io/${PROJECT_ID}/frontend:fe
docker push gcr.io/${PROJECT_ID}/metadatabase:db
docker push gcr.io/${PROJECT_ID}/simidatabase:db
```

### Step 5: Correctly specify project id in ```YAML``` files
* Manually replace ```gothic-space-289008``` with the value of your ```PROJECT_ID``` in the following ```YAML``` files:
```
frontend_deployment_k8s.yaml
backend_metaDataQuery_deployment_k8s.yaml
backend_similarity_deployment_k8s.yaml
```

### Step 6: Persistent disk creation and data transfer
* Follow the instructions [here](https://cloud.google.com/compute/docs/disks/add-persistent-disk) to setup persistent disks on GCE
* Create three separate disk for the following data:

    - Image Data - Transfer all original ```gap_xxxxx.jpg``` images into a folder ```gap_images``` on disk 1
    - Meta Data - Save ```metadata.csv``` on disk 2
    - Model and Latent Space Data - Save model file ```conv_encoder.h5```, latent space file ```conv_encoding.npy``` resized image folder ```bw_resize``` on disk 3
    
        - The model and latent space data files can be generated using provided jupyter notebook ```convolutional_encoder.ipynb``` and by running ```similarity.py``` on the local or virtual machine
        - The data can also be downloaded [here](https://drive.google.com/file/d/1xlZjgPPdqsmD7behiZEWvJjDBB2R7_IS/view?usp=sharing) 
* Its important to unmount the disk properly. Follow the instructions [here](https://cloud.google.com/sdk/gcloud/reference/compute/instances/detach-disk)

### Step 7: Start a cluster of 3 nodes
```
gcloud container clusters create practicum-1-cluster --num-nodes 3 --zone <zone>
```

### Step 8: Apply Secrets
* Before apply the secrets, update the username and password in ```gce_secrets_k8s.yaml```
* Username and password should be specified in ```base64``` format
* You can generate that with the command ```echo -n <username> | base64``` on the shell
```
kubectl apply -f gce_secrets_k8s.yaml
```

### Step 9: Create Persistent Volumes and Persistent Volume Claims
```
kubectl apply -f gce_pd_images_k8s.yaml
kubectl apply -f gce_pd_meta-data_k8s.yaml
kubectl apply -f gce_pd_similarity_k8s.yaml
```

### Step 10: Apply config map
```
kubectl apply -f webapp_configmap.yaml
```

### Step 11: Deploy the app - frontend and backend
```
kubectl apply -f frontend_deployment_k8s.yaml
kubectl apply -f backend_metaDataQuery_deployment_k8s.yaml
kubectl apply -f backend_similarity_deployment_k8s.yaml
```

### Step 12: Get the external IP
* Run ```kubectl get services``` to get external IP
* Use ```<external_IP:8081>``` on your browser to access the app
* The following commands can be used to determine the status of the app
```
kubectl get secrets
kubectl get pv
kubectl get pvc
kubectl get pods
kubectl get services
kubectl get all
kubectl describe <service> <service name: optional>
```


## How to stop the app and close the cluster

### Step 0: Kill the deployment
```
kubectl delete all --all
kubectl delete pvc --all
kubectl delete pv --all
kubectl delete secret --all
```

### Step 1: Stop the cluster
```
gcloud container clusters delete practicum-1-cluster --zone <zone>
y
```
