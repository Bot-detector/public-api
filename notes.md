kubectl
```sh
Kubectl port-forward -n kafka svc/bd-prd-kafka-service 9094:9094
```

```sh
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

```sh
.venv\Scripts\activate
pip freeze > requirements.txt
```