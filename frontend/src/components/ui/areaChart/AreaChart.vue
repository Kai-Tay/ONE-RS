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

// Define a color mapping for categories
const colorMapping: { [key: string]: { borderColor: string; backgroundColor: string } } = {
  total: {
    borderColor: 'blue',
    // backgroundColor: 'rgba(0, 0, 255, 0.2)',
  },
  oul: {
    borderColor: 'orange',
    // backgroundColor: 'rgba(255, 165, 0, 0.2)',
  },
  safetystock: {
    borderColor: 'green',
    // backgroundColor: 'rgba(0, 255, 0, 0.2)',
  },
  // Add more categories as needed
};

onMounted(() => {
  console.log('Props Data:', props.data);
  console.log('Chart Categories:', props.categories);

  const chartData = {
    labels: props.data.map(item => item[props.index]),
    datasets: props.categories.map(category => {
      const colors = colorMapping[category.toLowerCase()] || {
        borderColor: 'grey', // Default color if category not found
        // backgroundColor: 'rgba(128, 128, 128, 0.2)',
      };

      return {
        label: category,
        data: props.data.map(item => item[category]),
        fill: false,
        borderColor: colors.borderColor,
        backgroundColor: colors.backgroundColor,
      };
    }),
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
          text: 'Order Level based on Service Level',
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
