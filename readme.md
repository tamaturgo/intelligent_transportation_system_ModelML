# ITS - Intelligent Transportation System

## Descrição do Projeto

O **ITS - Intelligent Transportation System** é uma aplicação desenvolvida para monitoramento e análise de tráfego urbano utilizando técnicas de visão computacional e aprendizado de máquina. Este sistema foi projetado para identificar veículos, rastrear suas movimentações e gerar alertas em situações específicas, como veículos parados em áreas proibidas por longos períodos. O projeto foi desenvolvido como Trabalho de Conclusão de Curso (TCC) e demonstra a aplicação prática de tecnologias avançadas para resolver problemas reais de transporte.

## Funcionalidades

- **Detecção e Rastreamento de Veículos**: Utiliza o modelo YOLO para identificar e rastrear veículos em tempo real.
- **Geração de Alertas**: Detecta veículos parados em áreas proibidas por mais de 15 segundos e gera alertas com informações detalhadas.
- **Processamento de Vídeos**: Processa vídeos para análise de tráfego e geração de relatórios.
- **Gerenciamento de Áreas e Regras**: Permite a configuração de áreas específicas e regras associadas para monitoramento.
- **API RESTful**: Disponibiliza endpoints para integração com outros sistemas.

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:

```
├── CONST.py                # Configurações globais do sistema
├── controllers.py          # Lógica de rastreamento e geração de alertas
├── main.py                 # Inicialização do servidor Flask
├── migrate.py              # Script para criação e migração do banco de dados SQLite
├── routes.py               # Definição das rotas da API
├── Tracker.py              # Implementação do rastreador de veículos
├── VideoReader.py          # Leitura e processamento de vídeos
├── datasets/               # Conjunto de dados para treinamento e validação
├── job/                    # Scripts para processamento de vídeos
├── models/                 # Modelos treinados e arquivos auxiliares
├── results/                # Resultados gerados pelo sistema
├── services/               # Serviços auxiliares para manipulação de imagens, vídeos e regras
```

## Tecnologias Utilizadas

- **Linguagem de Programação**: Python
- **Framework Web**: Flask
- **Modelo de Detecção de Objetos**: YOLO (You Only Look Once)
- **Banco de Dados**: SQLite
- **Bibliotecas**:
  - OpenCV
  - NumPy
  - MoviePy
  - Flask-CORS
  - VidGear

## Configuração e Execução

### Pré-requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes do Python)

### Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/tamaturgo/intelligent_transportation_system_ModelML.git
   cd intelligent_transportation_system_ModelML
   ```

2. Instale as dependências:
   ```bash
   pip install -r requeriments.txt
   ```

3. Configure o banco de dados:
   ```bash
   python migrate.py
   ```

### Execução

1. Inicie o servidor Flask:
   ```bash
   python main.py
   ```

2. Acesse a aplicação em `http://127.0.0.1:5000`.

## Endpoints da API

### Imagens
- `POST /image`: Envia uma imagem para o sistema.
- `GET /image`: Obtém a última imagem processada.

### Vídeos
- `POST /video`: Envia um vídeo para o sistema.
- `GET /video/process`: Obtém o último vídeo processado.
- `GET /video/to/process`: Lista os vídeos disponíveis para processamento.

### Áreas
- `POST /area`: Adiciona uma nova área para monitoramento.
- `GET /area`: Lista todas as áreas configuradas.
- `GET /area/<id>/info`: Obtém informações de uma área específica.
- `DELETE /area/<id>`: Remove uma área.

### Regras
- `POST /rule`: Adiciona uma nova regra.
- `GET /rule`: Lista todas as regras configuradas.
- `DELETE /rule/<id>`: Remove uma regra.
- `POST /rule/associate`: Associa uma regra a uma área.
- `POST /rule/desassociate`: Desassocia uma regra de uma área.

## Resultados

Os resultados gerados pelo sistema, como matrizes de confusão e curvas F1, estão disponíveis na pasta `results/`.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

---

**Autor**: Diógeles Tamaturgo
**Data de Conclusão**: Dezembro de 2023