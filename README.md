# Enterprise Asynchronous To-Do Ecosystem 🚀

A highly responsive, production-ready full-stack To-Do application engineered with a modern distributed architecture. This ecosystem showcases a decoupled React client interacting with an asynchronous Python API gateway, backed by a persistent relational database container.

---

## 🛠️ Complete Technology Stack Matrix

This project leverages industry-standard tools divided into specialized layers to ensure high throughput, security, and developer velocity:

### ⚛️ Frontend Tier

- **React (JavaScript):** Component-driven interface layer rendering a highly responsive, real-time user workspace.
- **Vite Engine (Development):** Serves as a lightning-fast local development server utilizing Native ESM to provide near-instant Hot Module Replacement (HMR).
- **Nginx Server (Production):** A high-performance, reverse-proxy web server used in production to host and deliver compiled, minified static React bundles with minimal memory overhead.

### 🐍 Backend API Gateway

- **FastAPI Framework:** High-performance Python framework leveraging native asynchronous concurrency (`async/await`) for near-zero network latency.
- **Uvicorn:** A lightning-fast ASGI web server implementation used to run and reload the FastAPI application.
- **Slowapi Middleware:** Advanced token-bucket rate limiting applied directly to endpoint decorators, protecting backend routes from algorithmic spam and DDoS vectors.

### 🗄️ Persistence & Infrastructure

- **PostgreSQL 16:** Industrial-grade relational database running an isolated Alpine Linux instance to maintain transactional data integrity.
- **Docker & Docker Compose:** Multi-service application isolation layers enforcing absolute environment parity across your local machine and cloud servers.

---

## 🔒 Security & Decoupled Secret Architecture

To ensure project code satisfies strict security metrics, all private database passwords and admin keys are abstracted away from configuration manifests.

A root-level `.env` file serves as the singular source of truth. At container runtime, the Docker engine safely references this file to inject credential values directly into the target environments' temporary system memory (RAM). This prevents private passwords from leaking to version control platforms or public GitHub repositories.

---

## 🏁 Complete Lifecycle Setup Guide

Follow these steps in chronological order to initialize your codebases, generate automated blueprints, and orchestrate the full-stack container environment.

### Step 1: Bootstrap Application Folders & Blueprints

Before launching Docker, we must generate the initial application folders, the JavaScript dependency blueprint (`package.json`), and the Python requirement file (`requirements.txt`).

1. Open your native machine terminal in your empty root project directory (`my-project/`).
2. Execute the initialization script to automatically create your frontend folder, baseline React scripts, and your **`package.json`** file all at once using Vite:
   ```bash
   npm create vite@latest frontend -- --template react
   ```
3. Generate your backend subfolder framework:
   ```bash
   mkdir backend
   ```
4. Create a plain text file named precisely **`requirements.txt`** inside that new `/backend` folder, and populate it with your core Python libraries:
   ```text
   fastapi==0.115.0
   uvicorn==0.30.6
   slowapi==0.1.9
   psycopg2-binary==2.9.9
   ```

### Step 2: Configure Infrastructure Secrets

Create a file named exactly **`.env`** in the root of your main project directory to store your structural database configurations:

```ini
# --- PostgreSQL Initial Database Secrets ---
DB_USER=todo_admin
DB_PASSWORD=secure_dev_password_2026
DB_NAME=todo_app_db
```

_(Make sure to add `.env` to a root `.gitignore` file immediately so these credentials never hit GitHub)._

---

### Step 3: Execution & Orchestration Targets

#### Target A: Build and Run the Full Stack via Docker (Recommended)

This path ensures absolute environment parity. The whole platform compiles and runs inside clean virtual networks without polluting your physical host operating system.

1.  **Boot with Hot-Reloading (Development Mode - Vite + Uvicorn)**
    Maps your local workspace directories live. Making code edits on your laptop will instantly trigger file-watchers to update your application live:

    ```bash
    docker compose up --build
    ```

    - **React Frontend (Vite Dev Server):** `http://localhost:5173`
    - **FastAPI OpenAPI Playground docs:** `http://localhost:8000/docs`

2.  **Boot in Frozen Production Simulation Mode (Nginx + Clean Uvicorn)**
    Compiles optimized React assets into raw static directories, discards the Node runtime entirely, and serves the files through Nginx on the standard web channel:
    ```bash
    docker compose -f docker-compose.prod.yml up --build
    ```

    - **React Frontend (Served by Nginx):** `http://localhost` (Port 80)
    - **FastAPI API Gateway:** `http://localhost:8000`

#### Target B: Run the Stack Locally (Native Host Development)

If you prefer running application code servers natively on your machine's hardware while keeping external infrastructure running cleanly in the background:

1.  **Launch PostgreSQL Infrastructure via Docker:**

    ```bash
    docker compose up db -d
    ```

    _(The `-d` flag runs the database detached silently in the background)._

2.  **Spin Up the FastAPI Backend Gateway:**
    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    pip install -r requirements.txt
    export DATABASE_URL=postgresql://todo_admin:secure_dev_password_2026@localhost:5432/todo_app_db
    uvicorn main:app --reload
    ```
3.  **Spin Up the React Frontend App:**
    Open a new terminal tab and execute:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
