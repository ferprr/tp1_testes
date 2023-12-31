[![codecov](https://codecov.io/gh/ferprr/tp1_testes/tree/main/graph/badge.svg)](https://codecov.io/gh/ferprr/tp1_testes)

# Integrantes

- Etelvina Oliveira
- Fernanda Pereira

# Explicação do Sistema

Este projeto consiste na criação de um sistema de blog completo, que oferece diversas funcionalidades para a escrita, publicação e visualização de artigos. Além disso, inclui recursos de deleção, filtragem por categorias, busca, autenticação de usuário (login) e a capacidade de sair (logout).

## Funcionalidades Principais

O sistema oferece as seguintes funcionalidades:

- Autenticação de Usuário:
  Para realizar publicações, o usuário deve estar autenticado no sistema.
  Se o usuário não possui um login, é possível criar uma conta. Assim, os dados são salvos em um banco de dados.

- Gerenciamento de Artigos:
  Após o login, o usuário pode criar, editar e publicar artigos.
  Além disso, é possível excluir artigos de sua autoria.

- Filtragem por Categorias:
  Os artigos podem ser filtrados com base em categorias específicas, facilitando a busca por conteúdo relevante.

- Funcionalidade de Busca:
  Os usuários podem pesquisar por palavras-chave ou tópicos específicos para encontrar artigos de interesse.

## Restrições de Funcionalidades

É importante notar que algumas funcionalidades, como a criação, edição e exclusão de artigos, estão disponíveis apenas para usuários autenticados. Usuários não autenticados terão acesso apenas à visualização de artigos.

# Tecnologias utilizadas

- _Python_ com o framework _Django_
- _SQLite_ para banco de dados
- _unittest_ para criação e execução de testes unitários

# Documentação de referência

- [Django](https://www.djangoproject.com/)
- [Testando com Django](https://developer.mozilla.org/pt-BR/docs/Learn/Server-side/Django/Testing)

# Execução

    python3 manage.py makemigrations blog
    python3 manage.py migrate blog
    python3 manage.py runserver

### Interface

    localhost:8000

### Testes de Sistema 

Para executar os testes e2e, inicie o servidor

    phyton3 manage.py runserver

e execute o seguinte comando em outro terminal:

    python3 manage.py test blog/tests/e2e
