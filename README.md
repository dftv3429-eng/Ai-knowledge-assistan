# AI Knowledge Assistant - Bootstrap API

Primer incremento funcional del proyecto (Módulo 0 - Ingeniería de Sistemas de IA).
API asíncrona con **FastAPI**, validada con **Pydantic**, probada con **pytest** y versionada con **Git/GitHub**.

> **Importante:** este incremento **no integra ningún LLM**. Las respuestas las genera un servicio local de bootstrap, identificado con `provider = "bootstrap-local"`.

## Requisitos

- Python **3.12 o superior**
- Git
- (Opcional) Una cuenta de GitHub para publicar el repositorio

## Instalación

```bash
git clone <URL-DEL-REPOSITORIO>
cd ai-knowledge-assistant

# 1. Crear el entorno virtual
python -m venv .venv

# 2. Activar el entorno
#    Linux / macOS:
source .venv/bin/activate
#    Windows (PowerShell):
.venv\Scripts\Activate.ps1
#    Windows (CMD):
.venv\Scripts\activate.bat

# 3. Instalar dependencias (declaradas en pyproject.toml), incluyendo las de desarrollo
pip install -e ".[dev]"
```

## Ejecutar la API

```bash
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Documentación Swagger (OpenAPI): http://127.0.0.1:8000/docs

## Endpoints

| Método | Ruta            | Descripción                                   |
|--------|-----------------|-----------------------------------------------|
| GET    | `/health`       | Estado de salud de la API                     |
| POST   | `/api/v1/chat`  | Recibe una pregunta y devuelve una respuesta  |
| GET    | `/api/v1/info`  | Información básica del proyecto               |

### Ejemplos

```bash
# Health
curl http://127.0.0.1:8000/health

# Chat con entrada válida
curl -X POST http://127.0.0.1:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Qué es FastAPI?"}'
# -> {"answer": "...", "provider": "bootstrap-local"}

# Chat con entrada inválida (menos de 3 caracteres) -> HTTP 422
curl -i -X POST http://127.0.0.1:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "ab"}'

# Info
curl http://127.0.0.1:8000/api/v1/info
# -> {"name":"AI Knowledge Assistant","version":"0.1.0","environment":"development","llm_enabled":false}
```

**Validación:** `question` debe tener entre **3 y 2000 caracteres**. Si no se cumple, Pydantic rechaza la petición y FastAPI responde **HTTP 422 Unprocessable Entity** con el detalle del error, sin llegar a ejecutar el servicio.

## Ejecutar las pruebas

```bash
python -m pytest -q
```

La suite incluye:

- **Unitarias** (`tests/unit/`): prueban el servicio del asistente de forma aislada (T-01).
- **Integración** (`tests/integration/`): invocan la app FastAPI con `httpx.AsyncClient` + `ASGITransport`, **sin servidor externo** (T-02 a T-05, más casos de borde y `/docs`).

## Demo de AsyncIO + HTTPX

```bash
python scripts/async_demo.py
```

Lanza 5 peticiones **concurrentes** con `asyncio.gather` y `httpx.AsyncClient` contra la propia app (sin servidor). También se puede apuntar a un servidor en ejecución:

```bash
python scripts/async_demo.py --url http://127.0.0.1:8000
```

## Arquitectura

```
Cliente → FastAPI (router) → Pydantic (schemas) → Servicio → Respuesta
```

```
ai-knowledge-assistant/
├── app/
│   ├── main.py              # Fábrica de la app y registro de routers
│   ├── api/routes/          # Capa HTTP: health, chat, info
│   ├── schemas/             # Modelos Pydantic de entrada/salida
│   └── services/            # Lógica del asistente (AssistantService)
├── scripts/async_demo.py    # Demostración AsyncIO + HTTPX
├── tests/
│   ├── unit/
│   └── integration/
├── .gitignore
├── pyproject.toml
└── README.md
```

El router **no contiene lógica**: valida con Pydantic, delega en `AssistantService` (inyectado con `Depends`) y arma la respuesta. Así, en el próximo módulo se podrá reemplazar el servicio local por un proveedor LLM sin cambiar los contratos HTTP.

## Flujo de Git

```bash
git checkout -b feat/bootstrap-api      # rama de funcionalidad
# ... commits pequeños y coherentes (chore:, feat:, test:, docs:) ...
git remote add origin <URL-DEL-REPOSITORIO>
git push -u origin main
git push -u origin feat/bootstrap-api
# Luego crear el Pull Request feat/bootstrap-api -> main en GitHub
```

## Seguridad

El repositorio no contiene secretos, tokens ni credenciales. `.env`, `.venv` y cachés están excluidos mediante `.gitignore`.
