# Contributing guide

Welcome! Thank you for considering contributing to this project! Here are the steps to get a development installation up and running.

## Getting started

### Fork the repository

Follow the [GitHub guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo
) for how to fork a repository, clone it, and learn about creating pull requests.

### Install dependencies

Ensure you have the necessary dependencies installed. 

  ```bash
  pip install -r requirements.txt
  ```

**Important:** Make sure you have a working installation of Python 3.6 or later.

**Note:** Consider installing the dependencies in a virtual environment for better isolation.

### Apply migrations

Apply the migrations to the database. Read more about Django migrations [here](https://docs.djangoproject.com/en/5.0/topics/migrations/).

```bash
python3 manage.py migrate
```

**Note:** Every time you make any changes to the models, you will need to create a new migration and apply it.

### Run the development server

Start the development server to see the changes you make.

```bash
python3 manage.py runserver
```

## Code of Conduct

Please note that this project has a [Code of Conduct](https://github.com/2i2c-org/unnamed-thingity-thing?tab=coc-ov-file). By participating in this project you agree to follow it.

Thank you for your contributions!