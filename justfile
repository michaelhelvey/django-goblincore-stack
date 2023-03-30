default:
	pnpm dev &
	pipenv run python manage.py runserver_plus --nopin

format:
	pipenv run black -l 100 .

migrate:
	pipenv run python ./manage.py migrate

lint:
	ruff .

static-dev:
	pnpm dev

static-prod:
	pnpm build
