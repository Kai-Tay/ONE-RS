<template>
  <AreaChart
    v-if="chartData.length > 0" 
    :data="chartData"
    index="interval"
    :categories="['InventoryLevel']"
    :lineOptions="lineOptions"
  />
</template>

<script setup>
import { db } from '../firebase.js';
import { doc, getDoc } from "firebase/firestore";
import { AreaChart } from '@/components/ui/areaChart';
import { ref, onMounted } from 'vue';

const chartData = ref([]);  // Declare only once here

const lineOptions = {
    yAxis: { title: 'Inventory Level' },
    xAxis: {
        title: 'Year-Month-Interval',
        plotLines: [], // Existing plot lines
    },
    series: {
        InventoryLevel: { borderColor: 'green' },
    },
};

// Fetch inventory data
async function fetchInventoryData(restaurantId) {
    const inventoryCollection = doc(db, 'inventoryLevels', restaurantId);
    const inventorySnapshot = await getDoc(inventoryCollection);

    if (!inventorySnapshot.exists()) {
        console.log("Restaurant not found");
        return null;
    }

    const inventoryData = inventorySnapshot.data();
    console.log(inventoryData.pastInventoryLevels);
    return inventoryData;
}

// Process and transform data for the chart
function transformDataForChart(inventoryData) {
    const chartDataArray = [];

    // Check if pastInventoryLevel exists
    if (inventoryData.pastInventoryLevels) {
        // Process past inventory levels
        for (const [interval, categories] of Object.entries(inventoryData.pastInventoryLevels)) {
            console.log(`Processing interval: ${interval}`);
            console.log(`Categories for interval ${interval}:`, categories);

            // Ensure "beef" data exists in "meat" category
            const beefExists = categories['meat']?.['beef'];

            // Get values for beforeOrder and afterOrder
            const beforeOrderLevel = categories.beforeOrder?.['meat']?.['beef'] || null;
            const afterOrderLevel = categories.afterOrder?.['meat']?.['beef'] || null;

            if (interval.endsWith("-5")) {
                // Check if beforeOrderLevel exists
                if (beforeOrderLevel !== null) {
                    // Add InventoryLevel for beforeOrder (renamed)
                    chartDataArray.push({
                        interval: `${interval}-1`, // New interval for beforeOrder
                        category: 'meat',
                        itemType: 'beef',
                        InventoryLevel: beforeOrderLevel, // Use InventoryLevel to display beforeOrder
                    });
                } else {
                    console.log(`No beforeOrder level for interval ${interval}`);
                }

                // Check if afterOrderLevel exists
                if (afterOrderLevel !== null) {
                    // Add InventoryLevel for afterOrder (renamed)
                    chartDataArray.push({
                        interval: `${interval}-2`, // New interval for afterOrder
                        category: 'meat',
                        itemType: 'beef',
                        InventoryLevel: afterOrderLevel, // Use InventoryLevel to display afterOrder
                    });
                } else {
                    console.log(`No afterOrder level for interval ${interval}`);
                }
            } else {
                // Single inventory level for other intervals
                if (beefExists) {
                    const singleInventoryLevel = categories['meat']['beef'];
                    chartDataArray.push({
                        interval,
                        category: 'meat',
                        itemType: 'beef',
                        InventoryLevel: singleInventoryLevel,
                    });
                } else {
                    console.log(`No beef data for interval ${interval}`);
                }
            }
        }
    } else {
        console.log("No pastInventoryLevel data found");
    }

    // Check if currentInventoryLevel exists and includes "meat" and "beef" data
    const currentInv = inventoryData.currentInventoryLevel;
    // Ensure "beef" data exists in "meat" category
    if (currentInv) {
    const interval = Object.keys(currentInv)[0]; // Get the single key
    if (interval.endsWith("-5")) {
        console.log("ebdjwbdken", currentInv[interval].beforeOrder);

        console.log(`Interval ${interval} ends with -5`);
        // Add further processing here if needed
        const currentBeforeOrderLevel = currentInv[interval].beforeOrder?.['meat']?.['beef'] || null;
        const currentAfterOrderLevel = currentInv[interval].afterOrder?.['meat']?.['beef'] || null;
        if (currentBeforeOrderLevel !== null) {
                    // Add InventoryLevel for beforeOrder (renamed)
                    chartDataArray.push({
                        interval: `${interval}-1`, // New interval for beforeOrder
                        category: 'meat',
                        itemType: 'beef',
                        InventoryLevel: currentBeforeOrderLevel, // Use InventoryLevel to display beforeOrder
                    });
                } else {
                    console.log(`No beforeOrder level for interval ${interval}`);
                }

                // Check if afterOrderLevel exists
                if ( currentAfterOrderLevel !== null) {
                    // Add InventoryLevel for afterOrder (renamed)
                    chartDataArray.push({
                        interval: `${interval}-2`, // New interval for afterOrder
                        category: 'meat',
                        itemType: 'beef',
                        InventoryLevel:  currentAfterOrderLevel, // Use InventoryLevel to display afterOrder
                    });
                } else {
                    console.log(`No afterOrder level for interval ${interval}`);
                }



    } else {
        const currentBeefExists = currentInv[interval]['meat']?.['beef'] || null;
        if (currentBeefExists) {
                    const singleInventoryLevel = categories['meat']['beef'];
                    chartDataArray.push({
                        interval,
                        category: 'meat',
                        itemType: 'beef',
                        InventoryLevel: singleInventoryLevel,
                    });
        }
    }


} else {
    console.log("No current inventory level data found");
}


    console.log("happy:", inventoryData.currentInventoryLevel);

    chartDataArray.sort((a, b) => (a.interval > b.interval ? 1 : -1));
    console.log("Final Chart Data Array:", chartDataArray);
    return chartDataArray;
}


onMounted(async () => {
    const inventoryData = await fetchInventoryData("GYFKVpkDpI74zYTzzsfY");

    if (inventoryData) {
        chartData.value = transformDataForChart(inventoryData);  // Assign to the existing chartData ref
        console.log(chartData.value); // Check to ensure data is correct
    }
});
</script>
