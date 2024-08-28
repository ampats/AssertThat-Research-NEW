# AssertThat-research

### 1. Clone down the repository:
`git clone git@github.com:ampats/AssertThat-research.git`

### 2. Create you venv environment and folder called venv:
`python -m venv venv`

### 3. Active venv
`source venv/Scripts/activate`

You should see `(venv)` if your working in the virtual environment
- As an example:
![Alt text](docs/images/venvActivated.png)

### 4. Install from requirements.txt:
`pip install -r requirements.txt`

### Optional - If updates are made to packages in venv, run the following command in the **root directory** to update requirements.txt 
`pip freeze > requirements.txt`

### 5. Create a .env file with your AssertThat and GitHub credentials

### 6. Run the following command in your terminal:
`python sync_features.py`
