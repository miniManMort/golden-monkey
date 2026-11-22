# GOLDEN MONKEY

A web app to manage monster and spell profiles.

Architecture details are provided in the [spec](spec/README.md).

The active React frontend and modular FastAPI backend are under
[app-react/](app-react/). Both use the shared
[data/golden_monkey.db](data/golden_monkey.db) SQLite database.

Install backend dependencies and start the web app with:

```sh
./build.sh
./run.sh
```

For frontend development and production build instructions, see
[app-react/README.md](app-react/README.md).

The former Python and Rust desktop applications are preserved for reference
only in [archive/app](archive/app) and [archive/app-rust](archive/app-rust).