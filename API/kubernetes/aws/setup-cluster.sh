eksctl create cluster --name pyfungivisum-cluster --nodegroup-name pyfungivisum-cluster-node-group  --node-type m5.large --nodes 3 --nodes-min 3 --nodes-max 5 --managed --asg-access --zones=us-east-1a,us-east-1b
kubectl apply -f api-deployment.yaml
kubectl apply -f api-service.yaml
kubectl apply -f mysql-deployment.yaml
kubectl apply -f mysql-service.yaml
kubectl apply -f mysqldata-persistentvolume.yaml
kubectl apply -f configmap.yaml
kubectl apply -f secret.yaml
  
