# Projeto_01_Web - Sistema de Gestão de Eventos Acadêmicos (SGEA)

Este projeto consiste em um sistema web desenvolvido com foco em backend, utilizando o framework Django. O objetivo principal é gerenciar eventos acadêmicos, permitindo o cadastro de usuários, inscrição em eventos, emissão de certificados e prototipação de interfaces.

## Funcionalidades Principais

- Cadastro e autenticação de usuários
  - Perfis disponíveis: Aluno, Professor, Organizador
  - Campos obrigatórios: Nome completo, telefone, instituição de ensino (para alunos e professores), nome de usuário, senha e perfil
  - Autocadastro e inscrição em eventos existentes

- Criação e gerenciamento de eventos (Organizadores)
  - Tipos de evento: seminário, palestra, entre outros
  - Informações exigidas: data de início e término, horário, local, número de participantes e organizador responsável

- Inscrição em eventos (Alunos e Professores)
  - Associação do evento ao perfil do usuário

- Emissão de certificados (Organizadores)
  - Disponível apenas para usuários inscritos
  - Certificados vinculados ao evento e ao participante

## Tecnologias Utilizadas

- Python 3.x
- Django
- Banco de dados: SQLite (padrão) ou outro configurado
- HTML/CSS para prototipação de interface
- Bootstrap (opcional para estilização)

## Estrutura do Projeto

- `apps/` – Aplicações Django organizadas por domínio (ex.: usuarios, eventos, certificados)
- `models.py` – Modelagem das entidades principais
- `views.py` – Lógica de apresentação e controle
- `urls.py` – Roteamento das views
- `templates/` – Protótipos e layouts das interfaces
- `static/` – Arquivos estáticos (CSS, JavaScript, imagens)
- `requirements.txt` – Dependências do projeto

## Instruções de Execução

1. Clonar o repositório:
   git clone https://github.com/LMalaguti/Projeto_01_Web.git
   cd Projeto_01_Web

2. Criar e ativar um ambiente virtual:
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows

3. Instalar as dependências:
   pip install -r requirements.txt

4. Executar as migrações:
   python manage.py migrate

5. Criar usuário administrativo (opcional):
   python manage.py createsuperuser

6. Iniciar o servidor de desenvolvimento:
   python manage.py runserver

7. Acessar o sistema via navegador:
   http://localhost:8000

## Licença

Este projeto possui finalidade acadêmica e está disponível para uso educacional.

## Autores: 
- Lucas Malaguti
- Dimitri Ramos
- Felipe Pirangi
