# MLDataAnalysis

RTS - Project

**Title** :  Data Analysis of a Cisco Network using Machine Learning algorithms.

---

### Install Project

1. Clone the project :

```bash
git clone git@github.com:malclement/MLDataAnalysis.git
```

2. Install the requirements :

```bash
cd MLDataAnalysis &&
pip install -r requirements.txt
```

---

### Run Backend Server

```bash
uvicorn main:app
```

---

### Run Docker

```bash
docker compose -f docker-compose.yml up --build
```

### Stop Docker

```bash
docker compose -f docker-compose.yml down && docker system prune -af && docker volume prune -f
```

---

## Tools

### Pre-commit

1. Install pre-commit :

   ```bash
   pip install pre-commit
   ```

2. Run :

   ```bash
   pre-commit install
   ```

#### Note

You can skip the pre-commit validation using `-n`:

```bash
git commit -m 'my_message' -n
```

### Virtual Environment

1. Instal virtualenv :

   ```bash
   pip install virtualenv
   ```

2. Create a virutal environment :
   Locate yourself at the root of your project

   ```bash
    python<version> -m venv env
   ```

3. Activate :

   ```bash
   source env/bin/activate
   ```

---

## Usage

- Run the project using Docker using docker commands
- Run the project on your machine using :
   ```bash
   uvicorn main:app --reload
   ```

Once the project is running you can trigger the different endpoint directly using the documentation interface.

For endpoints outputing vizualisation it is recommended to directly trigger the endpoint. For exemple :
```url
http://localhost:8000/gd/histogram?file_size=Test
```

## Deployed Versions 

- Heroku : https://ml-analysis-751e2972b3a3.herokuapp.com
- AWS : http://fastapi-application-lb-1541022285.eu-west-3.elb.amazonaws.com
