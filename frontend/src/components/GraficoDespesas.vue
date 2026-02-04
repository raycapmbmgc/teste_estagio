<template>
  <div class="wrapper">
    <div v-if="chartData.datasets[0].data.length > 0" class="chart-container">
      <Bar :data="chartData" :options="chartOptions" />
    </div>

    <div v-else-if="props.dados && props.dados.length === 0" class="no-data">
      <div class="icon">⚠️</div>
      <p>Nenhuma despesa financeira encontrada para esta operadora.</p>
    </div>

    <div v-else class="loading">
      <p>Selecione uma operadora para ver o histórico financeiro.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

const props = defineProps(['dados']);

const chartData = ref({
  labels: [],
  datasets: [{ 
    label: 'Despesas Trimestrais (R$)', 
    backgroundColor: '#42b983', 
    data: [] 
  }]
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    tooltip: {
      callbacks: {
        // Formata o valor para Real Brasileiro no tooltip
        label: (context) => {
          return 'Valor: ' + new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(context.raw);
        }
      }
    }
  }
};

watch(() => props.dados, (novosDados) => {
  // Se novosDados for nulo ou vazio, resetamos o gráfico
  if (!novosDados || novosDados.length === 0) {
    chartData.value = {
      labels: [],
      datasets: [{ label: 'Despesas (R$)', backgroundColor: '#42b983', data: [] }]
    };
    return;
  }

  // Se houver dados, monta o gráfico
  const ordenados = [...novosDados].sort((a, b) => a.ano - b.ano || a.trimestre - b.trimestre);
  
  chartData.value = {
    labels: ordenados.map(d => `${d.trimestre}T/${d.ano}`),
    datasets: [{
      label: 'Despesas (R$)',
      backgroundColor: '#42b983',
      data: ordenados.map(d => d.valor_despesas)
    }]
  };
}, { immediate: true, deep: true });
</script>

<style scoped>
.chart-card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 16px;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  padding: 20px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #334155;
}

.card-header h3 {
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #f8fafc;
  margin: 0;
}

.badge {
  font-size: 0.7rem;
  background: #0f172a;
  color: #38bdf8;
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid #334155;
}

.card-content {
  flex: 1;
  padding: 24px;
  display: flex;
  flex-direction: column;
}

.chart-container {
  flex: 1;
  width: 100%;
  min-height: 300px;
}

/* Estados de Status */
.status-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px;
}

.status-icon {
  font-size: 3rem;
  margin-bottom: 15px;
  opacity: 0.5;
}

.status-view h4 {
  color: #f8fafc;
  margin-bottom: 8px;
  font-weight: 600;
}

.status-view p {
  color: #94a3b8;
  font-size: 0.9rem;
  max-width: 220px;
}

.waiting { background: rgba(255, 255, 255, 0.01); border-radius: 12px; }
.empty { background: rgba(239, 68, 68, 0.05); border-radius: 12px; }

/* Animações */
.pulse { animation: pulse 2s infinite; }
@keyframes pulse {
  0% { transform: scale(1); opacity: 0.5; }
  50% { transform: scale(1.1); opacity: 0.8; }
  100% { transform: scale(1); opacity: 0.5; }
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 768px) {
  .chart-container { min-height: 250px; }
  .card-header { padding: 15px; }
}
</style>