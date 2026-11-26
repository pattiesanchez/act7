<h1 align="center">ACT7 Confeitaria</h1>

<p align="center"><strong>Confeitaria feita em casa</strong></p>
<p align="center">Encontre receitas de bolos, doces e sobremesas e compartilhe suas criações com a comunidade.</p>
<p align="center">
  <img src="frontend/public/img/bg-img/act7-bolo-framboesa.jpg" width="240" alt="Fatia de bolo red velvet">
</p>
<p align="center">Vue 3 · JavaScript · Pinia · Vite · Django REST Framework · MySQL</p>

## O que você pode fazer

- Explorar o catálogo, buscar receitas por nome ou categoria e consultar o modo de preparo
- Criar uma conta com ativação por e-mail e gerenciar suas receitas em um painel com envio e prévia de fotos
- Enviar dúvidas e sugestões pelo formulário de contato
- Navegar em uma interface responsiva

## Rodar localmente

Use Node.js 24.12 ou superior, Python 3.12 e um banco MySQL já criado. Os comandos abaixo usam PowerShell e partem da raiz do repositório.

**API** · Crie `backend/.env` com as configurações do seu ambiente de desenvolvimento.

```dotenv
DEBUG=True
DATABASE_BD=act7
DATABASE_USER=seu_usuario
DATABASE_PASSWORD=sua_senha
DATABASE_SERVER=127.0.0.1
DATABASE_PORT=3306
BASE_URL=http://127.0.0.1:8000
BASE_URL_FRONTEND=http://127.0.0.1:5173
```

```powershell
python -m venv ../act7-venv
& ..\act7-venv\Scripts\Activate.ps1
cd backend
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Para ativação de contas e envio de e-mails pelo contato, configure também `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` e `SMTP_FROM` no `backend/.env`. Com a API rodando, abra a [documentação Swagger](http://127.0.0.1:8000/documentacao).

**Interface** · Adicione `VITE_API_URL=http://127.0.0.1:8000/api/v1/` ao `frontend/.env`. Em outro terminal, rode os comandos da raiz.

```powershell
cd frontend
npm ci
npm run dev
```

Abra a [ACT7 Confeitaria no navegador](http://127.0.0.1:5173/).

## Integração contínua

O GitHub Actions executa o lint e o build do frontend e os testes Django com SQLite em memória em pull requests para `main` e em pushes nessa branch. [Ver workflow](.github/workflows/ci.yml)
