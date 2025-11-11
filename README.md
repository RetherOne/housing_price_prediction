# Disclaimer

Although in answer to my email about the Python version, you recommended that I leave the project on version 3.9, I still decided to rework the application to version 3.12. This required retraining the model, but since all the functions were already ready, it was easy, and as I said, the prediction results differ from those before retraining, but not much. 
Also, with the transition to version 3.12, I replaced the library versions with the latest available ones.


# Task

I completed the task in full, with no problems. I implemented REST API together with token-based authentication and rate limiting. I also prepared the project for deployment using Dockerfile and tests. I implemented CI/CD using GitHub Actions, without final deployment, of course, since I don't have my own server :)

I would also like to note that I structured the entire project based on articles from the internet about how to properly create FastAPI applications. I hope it turned out to be intuitive and that there will be no problems with it.


# Description of the structure
```
.github/workflows/
├── CI_CD.yml                # GitHub Actions workflow for running CI/CD
│
app/
├── api/
│   └── endpoints.py         # FastAPI endpoints for the application
├── core/
│   ├── config.py            # Application configuration settings
│   ├── logger.py            # Centralized logging setup
│   └── security.py          # Security utilities, e.g., JWT handling
├── data/
│   ├── housing.csv          # Sample dataset
│   └── model.joblib         # Pre-trained ML model
├── schemas/
│   └── param.py             # Pydantic request schemas
├── utils/
│   └──predict.py            # Prediction logic functions
├── tests/
│   ├── __init__.py          # Makes `tests` a Python package
│   ├── E2E_test.py          # End-to-end tests
│   └── integration_test.py  # Integration tests
├── __init__.py              # Makes `app` a Python package
└── main.py                  # Entry point of the FastAPI application
.env
.gitignore
Dockerfile
.dockerignore
requirements.txt
README.md
```


# Running and other stuff

## Create venv
```bash
python -3.12 -m venv .venv

# Activate venv
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

## Running FastAPI Application
```bash
pip install -r requirements.txt
cd app
fastapi dev main.py
```
After that, you can go to `http://127.0.0.1:8000/docs` in your browser, and Swagger will open with the available endpoints.

## Running Tests with Pytest
```bash
pip install -r requirements.txt
cd app
pytest -v
```

## Building and Running Docker Container
```bash
docker build -t prod-backend .
docker run --rm -p 80:80 -e MODEL_PATH="data/model.joblib" prod-backend
```
After that, you can go to `http://127.0.0.1/docs` in your browser, and Swagger will open with the available endpoints(without port `:8000`).


# Description of endpoints `app/api/endpoints.py`

It's all pretty simple and clear from the name.
---
```
/predict
```
- This endpoint requires a JSON web token and is used to return the result of the predict function from the `predict.py` file.
---

```
/get_token
```
- This endpoint serves to ensure that before receiving a prediction, the user receives a token with which they can access the `/predict` endpoint.
