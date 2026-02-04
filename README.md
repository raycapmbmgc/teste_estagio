Teste Tecnico
Este repositorio contem a solucao do teste tecnico proposto, desenvolvida em Python, com foco em processamento de dados, validacao, enriquecimento e agregacao, seguindo boas praticas e decisoes tecnicas compativeis com o nivel de estagio.

Estrutura do Projeto
projeto/
│
├── data/
│   ├── raw/            # Arquivos originais (ZIPs e cadastro da ANS)
│   ├── extracted/      # CSVs extraidos dos ZIPs
│   └── processed/      # Arquivos finais processados e Banco de Dados
│
├── backend/            # Servidor API
│   ├── main.py         # Rotas e configuracoes FastAPI
│   ├── crud.py         # Logica de banco de dados
│   └── database.py     # Conexao SQLite
│
├── scripts/
│   ├── extrair_zips.py
│   ├── transform_data.py
│   ├── enrich_data.py
│   └── setup_db.py     # Script de criacao e carga do banco
│
├── README.md
└── requirements.txt
Parte 1 – Extracao e Consolidacao dos Dados
1.1 Extracao dos arquivos ZIP
O script extrair_zips.py e responsavel por ler os arquivos .zip presentes em data/raw/, organizar a extracao para pastas temporarias e facilitar reprocessamentos futuros sem a necessidade de manipular os arquivos compactados novamente.

1.2 Transformacao e Consolidacao
O script transform_data.py realiza a leitura em chunks para otimizacao de memoria, padronizacao de colunas, filtragem de despesas (contas iniciadas com 4) e remocao de valores invalidos.

Parte 2 – Validacao, Enriquecimento e Agregacao
2.1 Validacao de Dados
Implementacao de regras para CNPJ, valores numericos e campos obrigatorios. CNPJs invalidos sao marcados, mas preservados para evitar perda de dados financeiros relevantes.

2.2 Enriquecimento com Dados da ANS
Join entre a base financeira e o cadastro de Operadoras Ativas via CNPJ, adicionando Registro ANS, Modalidade e UF. Utilizou-se a estrategia de LEFT JOIN para garantir que a base financeira permanecesse integra mesmo em casos de ausencia no cadastro.

Parte 3 – Banco de Dados e Analise SQL
Nesta etapa, os dados foram modelados em um banco SQLite para garantir a portabilidade e facilidade na execucao do teste.

3.1 – Modelagem e Criacao das Tabelas (DDL)
Optou-se pela normalizacao dos dados, separando o cadastro das operadoras das movimentacoes financeiras consolidadas e agregadas.

Justificativa:

Evita redundancia de dados cadastrais.

Facilita a manutencao e atualizacao de novos periodos financeiros.

Melhora a performance de busca por operadoras especificas.

Parte 4 – API Backend e Integracao
Foi desenvolvido um servidor utilizando o framework FastAPI para disponibilizar os dados processados para o consumo do frontend, garantindo uma interface padronizada.

4.1 – Endpoints da API
GET /api/operadoras: Listagem com paginacao (page, limit) e busca textual.

GET /api/operadoras/{cnpj}: Detalhes cadastrais de uma operadora especifica.

GET /api/operadoras/{cnpj}/despesas: Historico financeiro trimestral.

GET /api/estatisticas: Dados agregados (Total de despesas, medias e Top 5 operadoras).

Trade-offs Tecnicos - Backend
4.2.1. Escolha do Framework: FastAPI
Justificativa: Escolhido pela alta performance, suporte nativo a operacoes assincronas e geracao automatica de documentacao interativa (Swagger/OpenAPI), acelerando o desenvolvimento e testes.

4.2.2. Estrategia de Paginacao: Offset-based
Justificativa: Abordagem ideal para o volume de dados do desafio, permitindo que o usuario navegue para paginas especificas de forma intuitiva no frontend.

4.2.3. Cache vs Queries Diretas: Queries Diretas
Justificativa: Como o banco e local (SQLite) e os dados sao estaticos apos o processamento, as consultas diretas garantem consistencia total dos dados sem a complexidade de gerenciar invalidaçao de cache.

4.2.4. Estrutura de Resposta: Dados + Metadados
Justificativa: A API retorna a lista de registros junto com o total de registros e metadados de paginacao, permitindo que o frontend controle dinamicamente os componentes de navegacao.

Como Executar o Projeto
Instale as dependencias: pip install -r requirements.txt

Prepare os dados e o banco: python scripts/setup_db.py

Inicie o servidor: cd backend && uvicorn main:app --reload

Acesse a documentaçao: http://127.0.0.1:8000/docs

Consideracoes Finais
Pipeline construido de forma modular e escalavel.

Tratamento de encoding e delimitadores especificos dos arquivos da ANS (latin-1 e ponto e virgula).

Decisoes tecnicas documentadas visando clareza e manutençao do codigo.

Desenvolvido por: Rayca Rafaelle

Parte 5 – Interface Frontend (Vue.js 3)
A interface foi desenvolvida para oferecer uma visualização clara e intuitiva dos dados financeiros, permitindo que o usuário identifique tendências e analise operadoras específicas com facilidade.

5.1 – Funcionalidades da Interface
Painel de Operadoras: Lista paginada com busca em tempo real por CNPJ ou Razão Social.

Dashboard de Despesas: Gráfico de barras dinâmico (Chart.js) que projeta o histórico financeiro trimestral.

Visualização Analítica: Cards com detalhes cadastrais e estados visuais para dados vazios ou carregamento.

Design Responsivo: Layout adaptável para diferentes resoluções utilizando CSS Grid e Flexbox.

Trade-offs Técnicos - Frontend
5.2.1. Gerenciamento de Estado: Composables (Vue 3)
Justificativa: Para a escala deste projeto, o uso de Pinia ou Vuex traria uma complexidade desnecessária. Utilizei Composables para encapsular a lógica de busca e paginação, mantendo o código limpo, reutilizável e fácil de testar, conforme as recomendações modernas do Vue 3.

5.2.2. Estratégia de Busca/Filtro: Híbrido
Justificativa: A busca inicial é realizada no servidor (Server-side) para garantir que possamos filtrar toda a base de dados. Uma vez que os dados da página atual são carregados, filtros menores de interface são processados no cliente, otimizando a experiência do usuário (UX).

5.2.3. Performance e UX: Tratamento de Estados
Justificativa: Foram implementados estados de Loading (animações de pulso), Empty States (mensagens amigáveis para buscas sem resultado) e tratamento de erros de rede. Isso evita que o usuário fique confuso caso a API demore a responder ou o CNPJ não possua dados cadastrados.

5.2.4. Estilização: CSS Puro (Scoped)
Justificativa: Optei por não utilizar frameworks CSS pesados (como Tailwind ou Bootstrap) para demonstrar domínio sobre fundamentos de CSS3, variáveis de ambiente (Custom Properties) e design responsivo, mantendo o bundle final leve.

Parte 6 – Documentação da API (Postman)
Para facilitar a validação das rotas, uma coleção completa do Postman foi incluída no repositório.

Arquivo: docs/Intuitive_Care_ANS.postman_collection.json

Conteúdo: Exemplos de requisições, parâmetros de busca, paginação e exemplos de respostas esperadas (Success/Error).

Como Executar o Frontend
Navegue até a pasta do frontend: cd frontend

Instale as dependências: npm install

Inicie o servidor de desenvolvimento: npm run dev

Acesse no navegador: http://localhost:5173 (ou a porta indicada no terminal)

Checklist de Entrega Final ✅
[x] Scripts de extração e normalização (Python).

[x] Banco de Dados modelado e populado (SQLite/SQL).

[x] API funcional com documentação Swagger (FastAPI).

[x] Interface Web responsiva e integrada (Vue.js).

[x] Coleção Postman para testes.

[x] README com justificativas de Trade-offs.

Desenvolvido por: Rayca Rafaelle