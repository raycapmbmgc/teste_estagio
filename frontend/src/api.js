import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api'
});

export const operadoraService = {
  // Rota de listagem (Parte 4.1)
  getOperadoras: (page = 1) => api.get(`/operadoras?page=${page}`),
  
  // Rota de detalhes (Parte 4.2)
  getDetalhes: (cnpj) => api.get(`/operadoras/${cnpj}`),
  
  // Rota de despesas para o Gráfico (O que acabamos de consertar!)
  getDespesas: (cnpj) => api.get(`/operadoras/${cnpj}/despesas`),
  
  // Rota de estatísticas para o Dashboard
  getEstatisticas: () => api.get('/estatisticas')
};