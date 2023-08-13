### About
- here we have a demo of an nginx deployment in a kubernetes cluster
- which is scaled up to 2 replicas at 10:30 AM daily (UTC) and scaled down to 1 replica at 11:30 AM daily (UTC)
- with the help of cronjobs which also run in the same cluster and same namespace as the deployment
- these cronjobs make use of the k8s service account to communicate with the k8s API and
- use a python script which is available as a docker image on docker.io as **satyamsundaram01/scaler_script** to scale deployments

### How to run
- clone this repo

To use your own docker image, change the image name in the cronjob yaml files and build and push your image to docker.io:
```
cd scaler_script
docker build -t <your_dockerhub_username>/<your_image_name> .
docker login
docker push <your_dockerhub_username>/<your_image_name>
```

Apply the yaml files in the following order:
```
# create nginx-deployment
kubectl apply -f nginx-deployment.yaml

# create service account, role and role binding
kubectl apply -f serviceaccount.yaml
kubectl apply -f role.yaml
kubectl apply -f rolebinding.yaml

# scale up cron job, triggers at 10:30 AM daily (UTC)
kubectl apply -f scaleupcron.yaml

# scale down cron job, triggers at 11:30 AM daily (UTC)
kubectl apply -f scaledowncron.yaml

(we can trigger the cron jobs manually to test them)
```

And, there you have it, a deployment which scales up and down at a scheduled time daily.
You can modify this for your own use case.
