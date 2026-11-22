# GOLDEN MONKEY

Golden Monkey is a small OSR RPG knowledge base. It was written on a Raspberry Pi Model 4 8GB using AI (VSCode and copilot).

I did it this way to help me understand the best way for me to make use of AI (everybody's workflow is different). I took what could be called a mix of Behavioural/Spec driven development and vibe coding all in one.

I started out writing a Python/Qt6 desktop app, but changed half way through to see how easily that could be converted to a web app. 

## Repo Structure

- app-react - contains the application code
- data - contains the SQLite database file
- spec - contains markdown docs explaining the requrements
- work - contains taks used to drive the AI development and logs of the work carried out
- .agents - specifies one skill I set up to implement a task, ensuring the agent reads the architecture docs and logs the output.

## Application Architecture

Architecture details are provided in the [spec](spec/README.md).

The active React frontend and modular FastAPI backend are under
[app-react/](app-react/). Both use the shared
[data/golden_monkey.db](data/golden_monkey.db) SQLite database.

## Running the App

Install backend dependencies and start the web app with:

```sh
./build.sh
./run.sh
```

For frontend development and production build instructions, see
[app-react/README.md](app-react/README.md).
