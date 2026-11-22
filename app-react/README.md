# Golden Monkey React

This is the active web application. It keeps using the shared SQLite database at
[`data/golden_monkey.db`](../data/golden_monkey.db).

The former Python and Rust desktop implementations are archived for reference
in [`archive/app/`](../archive/app) and
[`archive/app-rust/`](../archive/app-rust).

The FastAPI backend is organized under `backend/`: Pydantic schemas define
monster, spell, and character class records, repositories own SQLite access, routers expose the
API, and `services/odt.py` builds exports. `server.py` remains the CLI entry
point.

Long-text fields in monster and spell profiles use TinyMCE and support bold and
italic text, bulleted lists, and tables. Formatting is retained in profile
details and ODT exports.

## Run in development

In one terminal, install the Python backend dependencies and start the local
FastAPI server:

```sh
python -m pip install -r app-react/requirements.txt
python app-react/server.py
```

In another terminal:

```sh
cd app-react
npm install
npm run dev
```

Open the address printed by Vite (normally `http://localhost:5173`).

## Run as a built web app

```sh
cd app-react
python -m pip install -r requirements.txt
npm install
npm run build
cd ..
python app-react/server.py
```

Open `http://127.0.0.1:8000`. The FastAPI server serves the built React app and
provides its SQLite-backed API. The server binds to localhost by default; pass
`--host` to explicitly bind to another interface.

## Run the API tests

```sh
cd app-react
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```
