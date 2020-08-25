# Skin.io
skin.io is a web application that tracks a user's personalized skincare routine and skin health goals.

## `skin_app`

The `skin_app` is a dockerized `django` service that uses `poetry` for dependency management.

### `product_search`
`product_search` is an ETL pipeline querying data from [skincareAPI](https://github.com/LauraRobertson/skincareAPI) and [Google's Custom Search JSON API](https://developers.google.com/custom-search/v1/overview).

The `product_search` app also exposes a view that allows users to fuzzy-search skincare brands, products, and ingredients.

## Quickstart
`skin_app` uses docker-compose to control the services locally.

Bring up the web application and database:
```
docker-compose up
```

Migrate and load fixtures into local database:
```
make migrate
make load_db
```

Verify the containers are running locally with `docker ps`:
```
CONTAINER ID        IMAGE                  COMMAND                  CREATED             STATUS              PORTS                    NAMES
91c0da49fc9c        dev/skin-app:v2        "gunicorn --bind :80…"   6 minutes ago       Up 6 minutes        0.0.0.0:8000->8000/tcp   skin-app_skin-app_1
8b41ee349bf6        postgres               "docker-entrypoint.s…"   6 minutes ago       Up 6 minutes        5432/tcp                 skin-app_skin-db_1

```
Navigate to `localhost:8000/product_search/` to view local server.
