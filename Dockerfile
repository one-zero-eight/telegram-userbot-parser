FROM python:3.12-slim


RUN apt-get update && apt-get install -y curl

# Installing Poetry using curl
RUN curl -sS https://install.python-poetry.org | python3 -

#Adding Poetry to the PATH
ENV PATH="/root/.local/bin:$PATH"


COPY pyproject.toml poetry.lock /app/

#We give full access rights to the /app directory.
RUN chmod 777 /app

WORKDIR /app

#we install the dependencies specified in py project.toml, excluding dev dependencies.
RUN poetry install --no-interaction

COPY . /app

CMD ["poetry", "run", "python", "-u", "pyrogram_parser.py"]
