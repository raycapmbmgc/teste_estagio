📝 Teste Técnico – Intuitive Care


Solução do teste técnico desenvolvida por Rayca Rafaelle em Python, com foco em processamento de dados, validação, enriquecimento, agregação e visualização, seguindo boas práticas e decisões técnicas compatíveis com o nível de estágio.

⸻

📂 Estrutura do Projeto

projeto/
│
├── data/
│   ├── raw/          # Arquivos originais (ZIPs e cadastro ANS)
│   ├── extracted/    # CSVs extraídos dos ZIPs
│   └── processed/    # Arquivos finais processados + DB
│
├── backend/          # Servidor API
│   ├── main.py       # Rotas e configs FastAPI
│   ├── crud.py       # Lógica de DB
│   └── database.py   # Conexão SQLite
│
├── scripts/
│   ├── extrair_zips.py
│   ├── transform_data.py
│   ├── enrich_data.py
│   └── setup_db.py   # Criação e carga do banco
│
├── frontend/         # Interface Vue.js 3
├── postman/          # Coleção Postman
│   └── collection.json
├── README.md
└── requirements.txt


⸻


<details>
<summary>1️⃣ Extração e Consolidação dos Dados</summary>


1.1 Extração
	•	Script: scripts/extrair_zips.py
	•	Lê arquivos .zip de data/raw/ e organiza a extração em pastas temporárias.

Justificativa: Permite reprocessamentos futuros sem precisar manipular novamente os arquivos compactados.

1.2 Transformação
	•	Script: scripts/transform_data.py
	•	Operações realizadas:
	•	Leitura em chunks para otimização de memória.
	•	Padronização de colunas.
	•	Filtragem de despesas (contas iniciadas com 4).
	•	Remoção de valores inválidos.

Justificativa: Garante eficiência, consistência e integridade dos dados antes do enriquecimento.

</details>


<details>
<summary>2️⃣ Validação, Enriquecimento e Agregação</summary>


Validação
	•	Verificação de campos obrigatórios, CNPJs e valores numéricos.
	•	CNPJs inválidos são marcados, mas preservados.

Justificativa: Evita perda de dados financeiros relevantes, mantendo a integridade da base.

Enriquecimento
	•	Join com cadastro de Operadoras Ativas via CNPJ.
	•	Campos adicionados: Registro ANS, Modalidade e UF.
	•	Utilização de LEFT JOIN.

Justificativa: Garante que a base financeira permaneça integra, mesmo se algumas operadoras não estiverem no cadastro.

</details>


<details>
<summary>3️⃣ Banco de Dados (SQLite)</summary>


Modelagem
	•	Dados normalizados: cadastro de operadoras separado das movimentações financeiras.

Justificativas:
	•	Evita redundância de dados cadastrais.
	•	Facilita manutenção e atualização de novos períodos financeiros.
	•	Melhora performance de buscas por operadoras específicas.

</details>


<details>
<summary>4️⃣ API Backend (FastAPI)</summary>


Endpoints

Endpoint	Descrição
GET /api/operadoras	Listagem paginada (page, limit) + busca textual
GET /api/operadoras/{cnpj}	Detalhes de uma operadora
GET /api/operadoras/{cnpj}/despesas	Histórico financeiro trimestral
GET /api/estatisticas	Dados agregados (total de despesas, médias, Top 5 operadoras)

Decisões Técnicas
	•	Framework: FastAPI
Alta performance, suporte a operações assíncronas, documentação automática Swagger.
	•	Paginação: Offset-based
Intuitiva e eficiente para o volume de dados do desafio.
	•	Cache vs Queries Diretas: Queries diretas
Banco local (SQLite) com dados estáticos, garantindo consistência sem complexidade de cache.
	•	Estrutura de Resposta: Dados + Metadados
Permite que o frontend controle a navegação e paginamento de forma dinâmica.

Justificativa: Cada decisão foi tomada visando simplicidade, performance e clareza para manutenção futura.

</details>


<details>
<summary>5️⃣ Interface Frontend (Vue.js 3)</summary>


Funcionalidades
	•	Painel de Operadoras: Lista paginada + busca em tempo real por CNPJ ou Razão Social.
	•	Dashboard de Despesas: Gráfico trimestral dinâmico (Chart.js).
	•	Visualização Analítica: Cards com detalhes cadastrais e estados visuais.
	•	Design Responsivo: CSS Grid e Flexbox.

Trade-offs Técnicos
	•	Gerenciamento de Estado: Composables
Evita complexidade desnecessária de Vuex/Pinia em escala pequena.
	•	Busca/Filtro: Híbrido
Busca inicial server-side + filtros locais client-side para UX otimizada.
	•	Performance/UX: Estados de Loading, Empty States e tratamento de erros de rede.
	•	Estilização: CSS puro (scoped)
Mantém bundle leve e controle total sobre o design.

Justificativa: Garantir clareza visual, responsividade e experiência do usuário sem sobrecarregar o projeto.

</details>


<details>
<summary>6️⃣ Documentação da API</summary>


	•	Arquivo Postman: postman/collection.json
	•	Contém:
	•	Exemplos de requisições
	•	Parâmetros de busca e paginação
	•	Respostas de sucesso e erro

Justificativa: Permite validação rápida e testes da API sem necessidade do frontend.

</details>



⸻

⚡ Como Executar

Backend

pip install -r requirements.txt
python scripts/setup_db.py
cd backend
uvicorn main:app --reload

Acesse a documentação Swagger: http://127.0.0.1:8000/docs￼

Frontend

cd frontend
npm install
npm run dev

Acesse no navegador: http://localhost:5173￼

⸻

✅ Checklist de Entrega Final
	•	Scripts de extração e normalização (Python)
	•	Banco de dados modelado e populado (SQLite/SQL)
	•	API funcional com documentação Swagger (FastAPI)
	•	Interface web responsiva e integrada (Vue.js)
	•	Coleção Postman (postman/collection.json)
	•	README com justificativas de trade-offs

⸻

🔍 Considerações Finais
	•	Pipeline modular e escalável.
	•	Tratamento de encoding (latin-1) e delimitadores (;) específicos da ANS.
	•	Decisões técnicas documentadas para clareza e manutenção.
	•	Projeto desenvolvido por Rayca Rafaelle.



