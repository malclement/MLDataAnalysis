# MLDataAnalysis
RTS - Project

**Title** :  Data Analysis of a Cisco Network using Machine Learning algorithms.

**Students** :
- Aliénor d'Irumberry de Salaberry
- Clément Malige

**TODO** :
- [x] Check Database
- [x] Tryout predefined functions
- [x] First implementation of Girvain Newman Alg.
- [ ] Dev Backend structure
- [ ] Use Docker
- [ ] Deploy to AWS using terraform
- [ ] Implement Louvain Alg.
- [ ] Implement Label Propagation Alg.
- [ ] Tryout Clustering
- [ ] Review all alg.

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
## Tools

### Pre-commit

1. Install pre-commit :
   ```bash
   pip install pre-commit
   ```
2. Run :
   ```bash
   pre-commit instal
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
