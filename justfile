default:
	pnpm dev &
	pipenv run python manage.py runserver_plus --nopin

format:
	pipenv run black -l 100 .

alias mm := makemigrations
makemigrations:
	pipenv run python ./manage.py makemigrations

migrate:
	pipenv run python ./manage.py migrate

alias t := test
test:
	pipenv run pytest

test_watch:
	pipenv run pytest-watch

lint:
	pipenv run ruff .

fixtures:
	pipenv run python ./manage.py loaddata base

alias s := shell
shell:
	pipenv run python ./manage.py shell_plus --ipython

static-dev:
	pnpm dev

static-prod:
	pnpm build
	pipenv run python ./manage.py collectstatic

urls:
	pipenv run python ./manage.py show_urls
