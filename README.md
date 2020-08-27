# Django-general
Create a full django backend API

The modules will be separeted so you can get the module you need and just paste it on your project

<h2>To-do list:</h2>

- [x] login
- [ ] payments
- [x] sample api
- [ ] chat

<h2>SETUP</h2>
- Intale os requisitos em requirements.txt
```sh
pip install -r requirements.txt
```
- Crie o banco de dados

```sh
python manage.py makemigrations
python manage.py migrate
```

- Crie um superuser
```sh
python manage.py createsuperuser
```


# Insomnia
Para ver o funcionamento da API, faça o download do InsomniaCore (https://insomnia.rest/ )

Importe o arquivo insomnia-file.json

Execute o django server e rode os testes da API