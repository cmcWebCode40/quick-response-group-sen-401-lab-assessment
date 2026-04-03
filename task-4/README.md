# Lab 4: Re-Engineering & Migration — Report

## Quick Response Group | SEN 401 Lab Assessment

---

## 1. Reverse Engineering

### Original Architecture (Labs 2 & 3)

Both Lab 2 (`task-2/`) and Lab 3 (`task-3/`) share the same pattern:

```
app.py          → imports data + utils, prints a console report
students.py     → hardcoded list of Pydantic objects (Lab 2)
inventory.py    → hardcoded list of Pydantic objects (Lab 3)
helpers/utils.py → pure functions that accept lists and return results
```

### Dependency Diagram

```
┌────────────┐       ┌──────────────┐       ┌──────────────────┐
│   app.py   │──────▶│ students.py  │──────▶│  models (inline) │
│ (display)  │       │ / inventory  │       │  Pydantic class  │
└─────┬──────┘       └──────────────┘       └──────────────────┘
      │
      ▼
┌──────────────────┐
│ helpers/utils.py │
│  (analysis fns)  │
└──────────────────┘
```

### Issues Identified

| Issue | Description |
|---|---|
| **Tight coupling to hardcoded data** | Data lives in Python files — no external storage, no CRUD |
| **No API layer** | Results are only available via console — cannot be consumed by other systems |
| **Model + data in same file** | `inventory.py` defines both the Pydantic class and the data list |
| **No persistence** | Restarting the app resets everything |

---

## 2. Refactor & Modularize

### New Structure (Task 4)

```
task-4/
├── main.py              FastAPI app with REST endpoints
├── seed.py              Migrates hardcoded data into SQLite
├── requirements.txt     Dependencies
├── Dockerfile           Container image definition
├── docker-compose.yml   Container orchestration
├── .dockerignore        Files excluded from Docker build
├── app/
│   ├── __init__.py
│   ├── models.py        SQLAlchemy ORM model
│   ├── schemas.py       Pydantic request/response schemas
│   └── database.py      Engine and session configuration
└── db/
    └── inventory.db     SQLite database (created at runtime)
```

### What Changed

| Before (Lab 3) | After (Task 4) | Why |
|---|---|---|
| Pydantic model + data in one file | `app/models.py` (ORM) + `app/schemas.py` (validation) | Separation of concerns |
| Hardcoded list in Python | SQLite database via `seed.py` | Persistent, queryable storage |
| Console-only output | FastAPI REST endpoints | Accessible by any client |
| Analysis functions in `utils/` | SQL queries + `/stats` endpoint | Database handles aggregation |
| No deployment config | Dockerfile + docker-compose.yml | Reproducible deployment |

---

## 3. Migrate Data/API

### Data Migration: Hardcoded → SQLite

The `seed.py` script migrates the 10 inventory items from the original hardcoded list into a SQLite database:

```bash
python seed.py
# Output: Seeded 10 items.
```

The SQLite file is created at `db/inventory.db`. The seed only runs if the table is empty (idempotent).

### API Migration: Console → FastAPI

| Endpoint | Method | Description |
|---|---|---|
| `/items` | GET | List all inventory items |
| `/items/{id}` | GET | Get a single item by ID |
| `/items` | POST | Create a new item |
| `/items/{id}` | PUT | Update an existing item |
| `/items/{id}` | DELETE | Delete an item |
| `/stats` | GET | Summary statistics (total items, units, value, avg price) |
| `/docs` | GET | Auto-generated Swagger UI documentation |

### Testing the API

```bash
# Start the server
uvicorn main:api --port 8000

# List all items
curl http://localhost:8000/items

# Get stats
curl http://localhost:8000/stats

# Create a new item
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"item_name": "USB Cable", "quantity": 200, "price": 5.99}'

# Swagger docs
open http://localhost:8000/docs
```

**Sample `/stats` response:**

```json
{
  "total_items": 10,
  "total_units": 1580,
  "total_value": 33655.70,
  "average_price": 36.77
}
```

**Sample `/items/1` response:**

```json
{
  "id": 1,
  "item_name": "Wireless Mouse",
  "quantity": 150,
  "price": 12.99,
  "stock_value": 1948.50
}
```

---

## 4. Docker Compose Deployment

### Dockerfile

```dockerfile
FROM python:3.12-slim
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /code/db
EXPOSE 8000
CMD ["uvicorn", "main:api", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - db-data:/code/db
    environment:
      - DATABASE_URL=sqlite:///./db/inventory.db

volumes:
  db-data:
```

### Build & Run

```bash
cd task-4
docker-compose up --build
```

### Verify

```bash
# In a separate terminal
curl http://localhost:8000/items
curl http://localhost:8000/stats
```

> 📸 **[Screenshot Placeholder: `curl` responses from running container]**

### Stop

```bash
docker-compose down
```

---

## 5. Version Control

### Branch

```bash
git checkout -b dev-task-4-reengineering-migration
```

### Commits

| # | Message | Scope |
|---|---|---|
| 1 | `feat: add SQLAlchemy models, Pydantic schemas, and database config` | Models + DB |
| 2 | `feat: add FastAPI REST API and seed script` | API + Migration |
| 3 | `feat: add Dockerfile and docker-compose for deployment` | Docker |
| 4 | `docs: add Lab 4 re-engineering and migration report` | Documentation |

### Merge & Tag

```bash
git checkout main
git merge dev-task-4-reengineering-migration
git tag -a v1.3 -m "Release v1.3 — Lab 4: Re-Engineering & Migration Complete"
git push origin main --tags
```

>
> ```bash
> git log --oneline --graph dev-task-4-reengineering-migration
> ```

---

## 6. Results & Observations

| Aspect | Before (Labs 2–3) | After (Task 4) |
|---|---|---|
| Data storage | Hardcoded Python lists | SQLite database |
| Interface | Console output only | REST API (6 endpoints) |
| Validation | Pydantic on data load | Pydantic on every request |
| Deployment | `python app.py` | `docker-compose up` |
| Persistence | None | SQLite file in Docker volume |
| Documentation | README | Swagger UI auto-generated |

---

## 7. Conclusion

1. **Reverse engineering** the existing codebase revealed tight coupling between data and presentation — hardcoded lists with no external storage.
2. **Refactoring** into `models.py`, `schemas.py`, `database.py`, and `main.py` follows separation of concerns and makes each component independently testable.
3. **Migrating to SQLite** provides persistent, queryable storage. The `seed.py` script handles the one-time data migration.
4. **FastAPI** replaces console output with a full CRUD REST API, including auto-generated Swagger documentation.
5. **Docker Compose** packages everything into a reproducible, single-command deployment.

