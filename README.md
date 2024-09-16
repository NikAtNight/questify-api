# GETTING STARTED

1. `touch .envs/dvelopment.env`

Here are the env vars you need, change the DB URL

```
ENV_LABEL=local
DJANGO_SECRET_KEY=""

DJANGO_DEBUG=False
POSTGRES_CONN_MAX_AGE=600

DATABASE_URL=postgres://dbmaster:dbmaster@postgres:5432/DB_NAME_CHANGE_ME
REDIS_URL=redis://redis:6379
CELERY_BEAT_SCHEDULER=django_celery_beat.schedulers:DatabaseScheduler
SUPABASE_JWT_SECRET=
SUPABASE_URL=
SUPABASE_JWT_ISSUER=
SUPABASE_JWT_ALGORITHMS=HS256
```

2. In a new terminal, run `docker compose up web`

3. In a new terminal, run `docker compose exec postgres bash`

4. Feel free to change dbmaster to whatever you want. _NOTE_: You will have to update the database URL

`su postgres`
`psql`

```
create user dbmaster with password 'dbmaster';
alter role dbmaster with superuser;
create database DB_NAME_CHANGE_ME;
grant all privileges on database DB_NAME_CHANGE_ME to dbmaster;
\q

```

5. In a new terminal, run `docker compose exect web bash`

6. Run `python manage.py makemigrations`

7. Run `python manage.py migrate`

8. Stop the web service now, cancel running the service in the terminal or run `docker compose down`

9. Run `docker compose up`

TA DA app should be running on `http://localhost`
