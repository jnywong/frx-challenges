# Contributing guide

Welcome! Thank you for considering contributing to this project!

- [Development installation](#development-installation)
- [Gain Admin Access](#gain-admin-access)
- [Code of Conduct](#code-of-conduct)

## Development installation

Here are the steps to get a development installation up and running.

### 1. Fork the repository

Follow the [GitHub guide](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo) for how to fork a repository, clone it, and learn about creating pull requests.

### 2. Install the dependencies

Ensure you have the necessary dependencies installed.

```bash
pip install -r requirements.txt
```

**Important:** Make sure you have a working installation of Python 3.6 or later.

**Note:** Consider installing the dependencies in a virtual environment for better isolation.

### 3. Apply the migrations

Apply the migrations to the database. Read more about Django migrations [here](https://docs.djangoproject.com/en/5.0/topics/migrations/).

```bash
python3 manage.py migrate
```

**Note:** Every time you make any changes to the models, you will need to create a new migration and apply it.

### 4. Run the development server

Start the development server to see the changes you make.

```bash
python3 manage.py runserver
```

## Gain Admin access

In order to access the admin interface at `/admin`, your user needs to be a Django superuser.

Because we use GitHub external login we cannot use the existing `manage.py createsuperuser` command, so a separate [promote command](https://github.com/2i2c-org/unnamed-thingity-thing/blob/main/comptest/web/management/commands/promote.py) was created to promote an existing user (created via GiHub login) into a superuser.

Steps to access the admin interface:

1. Go to the admin interface `http://127.0.0.1/admin` and login with your GitHub account.

2. Promote your GitHub username to a superuser by running the following command, replace `<username>` with your GitHub username:

    ```bash
    python3 manage.py promote <username>
    ```

## Code of Conduct

Please note that this project has a [Code of Conduct](https://github.com/2i2c-org/unnamed-thingity-thing?tab=coc-ov-file). By participating in this project you agree to follow it.

Thank you for your contributions!
