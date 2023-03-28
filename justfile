default:
	pipenv run python manage.py runserver_plus

format:
	pipenv run black -l 100 .

migrate:
	pipenv run python ./manage.py migrate
