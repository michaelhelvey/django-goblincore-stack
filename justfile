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

test:
	pipenv run pytest

lint:
	pipenv run ruff .

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
