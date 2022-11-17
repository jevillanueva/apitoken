# apitoken
To Startup configure .env using .env.production

```py
uvicorn app.main:app --host 0.0.0.0  --reload
```
## To execute using vscode
To Run project using uvicorn run:
- Python: Uvicorn -> Ctrl + F5

To Run project using uvicorn Run And Debug:
- Python: Uvicorn -> F5

In the TAB Run and Debug "Ctrl + Shift + D" can select, run all project or run single file

For Single File 
To Run project using uvicorn run:
- Python: Run Single File -> Ctrl + F5

To Run project using uvicorn Run And Debug:
- Python: Run Single File -> F5

> In both Cases, the file .vscode/launch.json load file .env to environment variables

## To test in Container Docker use
```sh
docker-compose -f docker-compose.dev.yaml up -d --build
```
## To test in Kubernetes 
First build image one form is using docker-compose
```sh
docker-compose -f docker-compose.dev.yaml build
```
Create a secret with the .env file
```sh
kubectl create secret generic apitoken --from-env-file=.env 
```
Run  de files in k8s deployment 
```sh
kubectl create -f ./k8s/deploy.yaml
```
### 1. To test in local using Port Forward
To test the service use port-forward in new terminal and **"don't close"**
```sh
kubectl port-forward deploy/apitoken 8000:8000
```
Use curl o browser to test localhost:8000

### 2. To test in local using Expose
To expose in Nodeport service use
```sh
kubectl create -f ./k8s/expose.yaml
```
Expose the endpoint using a port 30007, Kubernetes use a range in ports (30000-32767)
Use curl o browser to test localhost:3007
