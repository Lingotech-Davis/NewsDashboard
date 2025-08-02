# FastAPI + Postgres backend

---

### Structure

This is a docker project, that has two _containers_, the FastAPI container (api) and the pgvector Postgres container (db).

- I have some intro to docker links below if curious

- The code for the FastAPI container is within the src folder, and nested from there depending on function
  - test_main.py: has some minimal testing functions to make sure fundamental things are working. Run with pytest test_main.py (-vv for verbose, -s to allow print output)
    - Make sure to have required python packages installed.
  - db/ has db operations
  - router/ has route info (like posts/ etc.)
  - app/ has the main FastAPI code
  - utils/ has long functions that I don't want cluttering the API code

### Usage

Before running, make sure to define a .env file in your root

```
GEMINI_API_KEY=
NEWS_API_KEY=
DB_USER=
DB_PASSWORD=
DB_NAME=
```

When you want to run the project locally, first set up docker on your machine

- I had some issues with this :(

Once everything is set up, in the root of the folder you can run some docker commands to get things working

```bash
docker-compose down -v                             # Takes down the running containers (allowing refreshing)
docker-compose up --build -d                       # Runs containers, initializing them
docker-compose logs {name of container (api / db)} # Debugging purposes
```

### Docker Info

Docker lets you run containers, which are kind of like little VMs running on your machine independently. This means that if set up correctly, they run the same everywhere (made to fix the 'it works on my machine issue')

- This means you don't even need to install postgres or anything like that, just code to develop

Projects that have different moving parts often involve multiple containers working together. To run these, we use `docker-compose` to orchestrate them

Different docker files:

- Dockerfile: Used to orchestrate the building of individual containers
- .dockerignore: Same as .gitignore, allows the exclusion of files from docker containers (like node_modules). Can be useful to reduce build times
- docker-compose.yml: Like a dockerfile for docker compose. Orchestrates the interaction and deployment of multiple docker files.

Here's some [other small notes](https://dtyner-vault.vercel.app/Coding/Docker) I wrote.

### Testing

I'm slowly writing some test cases to make sure it actually... works.
To run (assuming curdir=backend/) : `pytest src/test_main.py`

- You will need to have installed the packages necessary to run this

Additionally, when running and rerunning code, you can shortcut things by using my restart.sh file.

- To execute this (which tears down containers, then restarts them), give it exec perms `chmod +x ./restart.sh` then run it
