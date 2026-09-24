# Nook — AI-Powered E-Commerce

A Django storefront based on the supplied SRS. The interface uses server-rendered HTML, CSS, and vanilla JavaScript; Django handles authentication, catalog, cart, checkout, order history, and recommendations. PostgreSQL is supported, with SQLite as the zero-configuration local development default.

## Features

- Customer registration, sign-in, and sign-out using Django auth.
- Search and category filtering for active products.
- Django admin for categories, products, orders, and order status.
- User-owned shopping carts with quantity and stock validation.
- Atomic demo checkout that records orders and adjusts stock. It does not collect payment details.
- Recommendations from purchase category interests and aggregate product popularity. Each result explains its reason; the logic is deterministic and can be replaced by a trained recommender later.
- JSON endpoint: `GET /api/recommendations/`.
- Responsive storefront with a hand-drawn CSS hero illustration and local demo catalog.

## Run locally

Requires Python 3.10+ and PostgreSQL only if using the PostgreSQL configuration. From this folder:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
```

By default, Django uses SQLite. To use PostgreSQL, create a database and export the values from `.env.example` in your shell (Django does not read `.env` automatically):

```powershell
$env:DB_NAME='shop_db'
$env:DB_USER='postgres'
$env:DB_PASSWORD='your-local-password'
$env:DB_HOST='localhost'
$env:DB_PORT='5432'
```

Then initialize and run:

```bash
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Admin: `/admin/`. For PostgreSQL configuration, set `DB_NAME`; if it is unset, SQLite is used.

## API notes

- `GET /api/recommendations/` — returns `{"recommendations":[{"id":1,"name":"...","reason":"..."}]}`. Anonymous visitors get trending/catalog picks; signed-in users get category-affinity picks based on prior orders.
- `POST /cart/add/<product_id>/` — authenticated JSON body: `{"quantity":1}`. Django CSRF protection applies. Returns the updated quantity.

The browser UI uses session-authenticated Django views for cart updates, checkout, and order history.

## ER diagram

See [docs/erd.md](docs/erd.md).

## Repository notes

The project contains no real payment integration or external AI API key. Demo checkout simply creates an order. Set a unique `SECRET_KEY`, `DEBUG=False`, and production `ALLOWED_HOSTS` before deployment. The recommendation assistant currently uses transparent rules over order history and aggregate purchases, so no customer data leaves the application.
