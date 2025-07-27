#  Quotes API

A simple Quotes API built with FastAPI

## Features

- Clean FastAPI architecture
- Rate limiting with Redis
- Logging with Python’s `logging` module
- Metrics via Prometheus
- Visualization & Dashboards in Grafana
- Fully Dockerized for Dev Container

---

## Dev Container Setup

### Prerequisites

- [Docker](https://www.docker.com/)
- [Visual Studio Code](https://code.visualstudio.com/)
- [Remote - Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Getting Started

1. **Clone the repository**

```bash
git clone https://github.com/mauranpavan/QuotesAPI.git
cd QuotesAPI
```

2. **Open in VS Code**

> Use the `Remote - Containers: Open Folder in Container` command.

3. **Dev Container will automatically:**

- Install dependencies from `requirements.txt`
- Start `uvicorn` FastAPI app
- Start Redis, Prometheus, and Grafana services
- Make your API available at `http://localhost:8000`

---

## Project Structure

```
.
├── .devcontainer/           # Dev container config
│   └── devcontainer.json
├── app/
│   ├── main.py              # FastAPI app
│   ├── routes.py            # API endpoints
│   ├── utils.py             # Utilities
│   └── logger.py            # Logging setup
├── data/
│   └── quotes.csv           # Quotes dataset
├── docker-compose.yml       # All services
├── prometheus.yml           # Prometheus config
├── requirements.txt
└── README.md
```

---

## API Docs

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

### Example Endpoints

| Endpoint           | Description              |
|-------------------|--------------------------|
| `/quotes/random`  | Get a random quote       |
| `/quotes?author=...` | Filter by author     |
| `/metrics`         | Prometheus metrics       |
| `/docs`            | Swagger UI               |
| `/redoc`           | ReDoc documentation      |

---

## Monitoring & Observability

### Prometheus

- Collects metrics from `/metrics`
- Configured via `prometheus.yml`

### Grafana

- Available at `http://localhost:3000`
- Added Prometheus as data source: `http://localhost:9090/`

---

## 🪵 Logging

Using Python's `logging` module to log key events:

```python
import logging
logger = logging.getLogger(__name__)
logger.info("App started")
```

## Dependencies

Installed via `requirements.txt`:

```text
fastapi
uvicorn
pandas
slowapi[redis]
redis
prometheus-fastapi-instrumentator
```


## Dev Container Notes

Your `.devcontainer/devcontainer.json` might look like this:

```json
{
  "name": "FastAPI Dev Container",
  "dockerComposeFile": "docker-compose.yml",
  "service": "api",
  "workspaceFolder": "/workspace",
  "extensions": [
    "ms-python.python",
    "ms-azuretools.vscode-docker"
  ],
  "postCreateCommand": "pip install -r requirements.txt"
}
```
## License

MIT License

---
