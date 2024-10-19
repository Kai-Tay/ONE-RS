<template>
  <div>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { Chart, registerables } from 'chart.js';

// Register Chart.js components
Chart.register(...registerables);

// Define props with TypeScript
const props = defineProps<{
  data: { [key: string]: any }[]; // Adjust this type based on your actual data structure
  index: string;
  categories: string[];
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
let chartInstance: Chart | null = null;

onMounted(() => {
  console.log('Props Data:', props.data);
  console.log('Chart Categories:', props.categories);

  const chartData = {
    labels: props.data.map(item => item[props.index]),
    datasets: props.categories.map(category => ({
      label: category,
      data: props.data.map(item => item[category]),
      fill: true,
      borderColor: category === 'total' ? 'blue' : 'orange',
      backgroundColor: category === 'total' ? 'rgba(0, 0, 255, 0.2)' : 'rgba(255, 165, 0, 0.2)',
    })),
  };

  chartInstance = new Chart(chartCanvas.value!, {
    type: 'line',
    data: chartData,
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Area Chart Example',
        },
      },
    },
  });
});

// Cleanup on component unmount
onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy(); // Clean up the chart instance
  }
});
</script>

<style scoped>
canvas {
  max-width: 100%;
}
</style>