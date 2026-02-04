<template>
  <div class="app-layout">
    <header class="top-bar">
      <div class="brand">
        <div class="accent-line"></div>
        <h1>DATA<span>ANS</span></h1>
      </div>
      <div class="status-badge">SISTEMA ATUALIZADO 2026</div>
    </header>

    <main class="dashboard-grid">
      
      <section class="side-panel">
        <div class="panel-header">
          <h2>Operadoras Ativas</h2>
          <span class="count">{{ operadoras.length }} encontradas</span>
        </div>

        <div class="scroll-area">
          <div 
            v-for="op in operadoras" 
            :key="op.cnpj" 
            class="operator-card"
            :class="{ 'is-selected': cnpjAtivo === op.cnpj }"
            @click="carregarDespesas(op.cnpj)"
          >
            <div class="op-info">
              <span class="op-name" :title="op.razao_social">{{ op.razao_social }}</span>
              <span class="op-cnpj">{{ op.cnpj }}</span>
            </div>
            <div class="op-indicator"></div>
          </div>
        </div>
      </section>

      <section class="main-panel">
        <GraficoDespesas :dados="historicoFinanceiro" />
      </section>

    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { operadoraService } from './api';
import GraficoDespesas from './components/GraficoDespesas.vue';

const operadoras = ref([]);
const historicoFinanceiro = ref([]);
const cnpjAtivo = ref(null);

onMounted(async () => {
  try {
    const res = await operadoraService.getOperadoras(1);
    operadoras.value = res.data.data;
  } catch (error) {
    console.error("Erro ao carregar operadoras");
  }
});

const carregarDespesas = async (cnpj) => {
  cnpjAtivo.value = cnpj;
  try {
    const res = await operadoraService.getDespesas(cnpj);
    historicoFinanceiro.value = res.data;
  } catch (error) {
    console.error("Erro ao buscar histórico");
  }
};
</script>

<style scoped>
/* RESET & VARS */
:root {
  --bg-deep: #0b1120;
  --bg-surface: #1e293b;
  --accent: #38bdf8;
  --text-primary: #f8fafc;
  --text-muted: #94a3b8;
  --border: #334155;
}

.app-layout {
  background-color: #0b1120;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  color: #f8fafc;
  font-family: 'Inter', system-ui, sans-serif;
  overflow: hidden;
}

/* HEADER */
.top-bar {
  height: 60px;
  padding: 0 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #334155;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(10px);
}

.brand { display: flex; align-items: center; gap: 12px; }
.accent-line { width: 3px; height: 18px; background: #38bdf8; border-radius: 4px; }
.brand h1 { font-size: 0.9rem; letter-spacing: 2px; font-weight: 300; margin: 0; }
.brand h1 span { color: #38bdf8; font-weight: 800; }

.status-badge {
  font-size: 0.65rem;
  background: #1e293b;
  border: 1px solid #334155;
  padding: 4px 10px;
  border-radius: 4px;
  color: #94a3b8;
}

/* DASHBOARD GRID */
.dashboard-grid {
  flex: 1;
  display: grid;
  grid-template-columns: 380px 1fr;
  padding: 24px;
  gap: 24px;
  overflow: hidden;
}

/* PAINEL LISTAGEM */
.side-panel {
  background: #1e293b;
  border-radius: 16px;
  border: 1px solid #334155;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  padding: 20px;
  border-bottom: 1px solid #334155;
}

.panel-header h2 { font-size: 1rem; margin: 0; }
.count { font-size: 0.75rem; color: #94a3b8; }

.scroll-area {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

/* CARD DA OPERADORA */
.operator-card {
  padding: 16px;
  margin-bottom: 10px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid transparent;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.2s ease;
}

.operator-card:hover { background: rgba(255, 255, 255, 0.05); }

.operator-card.is-selected {
  background: #0ea5e9;
  border-color: #38bdf8;
}

.op-info { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
.op-name {
  font-size: 0.85rem;
  font-weight: 600;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.op-cnpj { font-size: 0.7rem; color: #94a3b8; font-family: monospace; }
.is-selected .op-cnpj { color: #bae6fd; }

.op-indicator {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #334155;
}
.is-selected .op-indicator { background: #fff; box-shadow: 0 0 8px #fff; }

/* PAINEL PRINCIPAL */
.main-panel { min-width: 0; }

/* SCROLLBAR */
.scroll-area::-webkit-scrollbar { width: 5px; }
.scroll-area::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }

/* RESPONSIVIDADE */
@media (max-width: 1024px) {
  .dashboard-grid { 
    grid-template-columns: 1fr;
    overflow-y: auto;
  }
  .side-panel { height: 400px; }
  .app-layout { overflow-y: auto; }
}
</style>