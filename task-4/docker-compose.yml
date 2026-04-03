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
