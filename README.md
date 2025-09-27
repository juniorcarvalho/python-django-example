'''# python-django-example

Um projeto Django básico com um endpoint de status.

## Requisitos

- Python 3.11+
- [uv](https://github.com/astral-sh/uv)

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/juniorcarvalho/python-django-example.git
   cd python-django-example
   ```

2. Crie um ambiente virtual e instale as dependências:
   ```bash
   uv sync
   ```

## Executando o servidor de desenvolvimento

Para iniciar o servidor de desenvolvimento, execute:

```bash
uv run python manage.py runserver
```

O servidor estará disponível em `http://127.0.0.1:8000/`.

## Endpoint

O projeto expõe o seguinte endpoint:

- `GET /api/status/`

  Retorna uma resposta JSON simples:
  ```json
  {
    "message": "OK"
  }
  ```
'''
