# wsgi_crabs
Запускаем 2 воркера на 8005 порту, с функцией hot_reload при изменении кода

`
gunicorn -w 2 -b 127.0.0.1:8005 --reload crabs_project.main:app
`