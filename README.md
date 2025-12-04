# SGEA - Sistema de Gestão de Eventos Acadêmicos

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Sistema web para gerenciamento de eventos acadêmicos como seminários, palestras, workshops e cursos. Permite cadastro de usuários, inscrição em eventos, emissão de certificados e controle de auditoria.

## 📋 Funcionalidades

- **Gestão de Usuários**: Três perfis (Aluno, Professor, Organizador) com permissões distintas
- **Gestão de Eventos**: Cadastro, edição e exclusão de eventos acadêmicos
- **Inscrições**: Sistema de inscrição com controle de vagas
- **Certificados**: Emissão automática de certificados de participação
- **API REST**: Endpoints para integração com outros sistemas
- **Auditoria**: Registro de ações críticas do sistema
- **Notificações**: Envio de e-mails de confirmação

## 🚀 Guia de Instalação

### Pré-requisitos

- Python 3.10 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/Projeto_01_Web.git
   cd Projeto_01_Web
   ```

2. **Crie e ative o ambiente virtual**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute as migrações do banco de dados**
   ```bash
   python manage.py migrate
   ```

5. **Crie os usuários de teste (opcional)**
   ```bash
   python manage.py seed_users
   ```

6. **Inicie o servidor de desenvolvimento**
   ```bash
   python manage.py runserver
   ```

7. **Acesse o sistema**
   - URL: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/

## 🧪 Guia de Testes

### Usuários de Teste

Após executar `python manage.py seed_users`, os seguintes usuários estarão disponíveis:

| Perfil | Login | Senha | Descrição |
|--------|-------|-------|-----------|
| Organizador | organizador@sgea.com | Admin@123 | Pode criar/editar/excluir eventos, ver logs de auditoria |
| Aluno | aluno@sgea.com | Aluno@123 | Pode se inscrever em eventos, ver certificados |
| Professor | professor@sgea.com | Professor@123 | Pode ser responsável por eventos, se inscrever |

### Script de Teste Funcional

1. **Testar cadastro de usuário**
   - Acesse `/api/users/register/`
   - Cadastre um novo usuário e confirme o e-mail

2. **Testar criação de evento (como Organizador)**
   - Faça login como `organizador@sgea.com`
   - Acesse `/api/events/create/`
   - Cadastre um evento com data futura

3. **Testar inscrição em evento (como Aluno)**
   - Faça login como `aluno@sgea.com`
   - Acesse `/api/events/`
   - Inscreva-se em um evento existente

4. **Testar geração de certificados**
   ```bash
   # Simula a geração para eventos finalizados
   python manage.py generate_certificates --dry-run
   
   # Gera os certificados
   python manage.py generate_certificates
   ```

5. **Testar API REST**
   - Obtenha um token:
     ```bash
     curl -X POST http://127.0.0.1:8000/api/token/ \
       -H "Content-Type: application/json" \
       -d '{"username": "aluno", "password": "Aluno@123"}'
     ```
   - Use o token para acessar endpoints:
     ```bash
     curl http://127.0.0.1:8000/api/events/ \
       -H "Authorization: Token SEU_TOKEN_AQUI"
     ```

## 📡 Endpoints da API

| Método | Endpoint | Descrição | Limite |
|--------|----------|-----------|--------|
| POST | `/api/token/` | Obter token de autenticação | - |
| GET | `/api/events/` | Listar eventos | 20/dia |
| POST | `/api/events/create/` | Criar evento | - |
| GET | `/api/events/<id>/` | Detalhes do evento | - |
| POST | `/api/events/register/` | Inscrever-se em evento | 50/dia |
| GET | `/api/certificates/` | Listar certificados | - |
| GET | `/api/audit/` | Listar logs de auditoria | - |
| POST | `/api/users/register/` | Cadastrar usuário | - |
| GET | `/api/users/me/` | Dados do usuário logado | - |

## ⚙️ Configuração de E-mail

Para enviar e-mails reais, configure as variáveis em `settings.py`:

```python
EMAIL_HOST = 'smtp.seu-servidor.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seu-email@exemplo.com'
EMAIL_HOST_PASSWORD = 'sua-senha-de-app'
```

**Dica para Gmail**: Use uma [senha de app](https://support.google.com/accounts/answer/185833).

## 📁 Estrutura do Projeto

```
Projeto_01_Web/
├── apps/
│   ├── usuarios/     # Gestão de usuários
│   ├── eventos/      # Gestão de eventos e inscrições
│   ├── certificados/ # Gestão de certificados
│   └── audit/        # Logs de auditoria
├── static/
│   ├── css/          # Estilos CSS
│   ├── js/           # JavaScript
│   └── images/       # Imagens e logo
├── templates/        # Templates HTML
├── media/            # Uploads de usuários
├── Projeto_01_Web/   # Configurações Django
├── manage.py
└── requirements.txt
```

## 🎨 Identidade Visual

- **Cor Primária**: #43054E (Roxo escuro)
- **Cor Destaque**: #E71984 (Magenta)
- **Tipografia**: Inter (Google Fonts)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request
