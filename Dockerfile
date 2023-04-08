FROM python:3.11

WORKDIR /code

COPY . .

RUN pip install pipenv
RUN pipenv sync --dev

# Staticfiles
RUN apt-get update && \
    wget -qO- https://deb.nodesource.com/setup_18.x | bash -

RUN apt-get install -y nodejs
RUN npm install -g pnpm

RUN pnpm install
RUN pnpm build

RUN pipenv run python ./manage.py collectstatic --noinput

EXPOSE 8000

CMD ["pipenv", "run", "daphne", "-b", "0.0.0.0", "-p", "8000", "base_site.asgi:application"]
