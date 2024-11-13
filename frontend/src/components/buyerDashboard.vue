<template>
    <div class="p-8 bg-gray-100 min-h-screen">
        <h1 class="text-3xl font-semibold text-gray-800 mb-6">Inventory Management</h1>

        <!-- Category Select -->
        <div class="mb-6">
            <label for="categorySelect" class="block text-gray-700 font-medium mb-2">Select Category:</label>
            <select id="categorySelect" v-model="selectedCategory" @change="onCategoryChange"
                :disabled="!inventoryDataLoaded"
                class="block w-full bg-white border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 px-4 py-2">
                <option v-for="(items, category) in inventoryData" :key="category" :value="category">
                    {{ category }}
                </option>
            </select>
        </div>

        <!-- Item Select -->
        <div class="mb-6">
            <label for="itemSelect" class="block text-gray-700 font-medium mb-2">Select Item:</label>
            <select id="itemSelect" v-model="selectedItem" :disabled="!selectedCategory"
                class="block w-full bg-white border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 px-4 py-2">
                <option v-for="(quantity, item) in filteredItems" :key="item" :value="item">
                    {{ item }}
                </option>
            </select>
        </div>

        <!-- Service Level Input -->
        <div class="mb-6">
            <label for="serviceLevel" class="block text-gray-700 font-medium mb-2">Service Level (%):</label>
            <input type="number" id="serviceLevel" v-model="serviceLevel" min="0" max="100"
                @input="updateDependentValues" placeholder="96"
                class="block w-full bg-white border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 px-4 py-2" />
            <div v-if="serviceLevelWarning" class="text-red-500 text-sm mt-1">{{ serviceLevelWarning }}</div>
        </div>


        <div class="bg-gray-100 overflow-x-auto">
            <Card>
                <CardContent>
                    <LineChart :key="updateCounter" :data="filteredChartData" index="interval"
                        :categories="['InventoryLevel', 'OUL', 'SafetyStock']" class="w-full h-full"
                        :colors="['orange', 'blue', 'green']" />
                </CardContent>
            </Card>
        </div>

        <!-- Divider -->
        <div class="border-t border-gray-300 my-8"></div>

        <!-- Inventory Levels Table -->
        <div>
            <h2 class="text-2xl font-semibold text-gray-800 mb-4">Inventory Levels</h2>

            <!-- Loading indicator -->
            <div v-if="loadingTable" class="text-center text-gray-600">Loading...</div>

            <!-- Table -->
            <div v-else class="overflow-x-auto">
                <table class="min-w-full bg-white border border-gray-200 rounded-lg shadow-md">
                    <thead>
                        <tr class="bg-gray-200 text-gray-700 text-left text-sm font-semibold">
                            <th class="px-4 py-3 w-1/4">Category</th>
                            <th class="px-4 py-3 w-1/4">Item</th>
                            <th class="px-4 py-3 w-1/4">Current Level ({{ currentIntervalDisplay }})</th>
                            <th class="px-4 py-3 w-1/4">Update Level ({{ nextIntervalDisplay }})</th>
                        </tr>
                    </thead>
                    <tbody>
                        <template v-for="(items, category) in currentInventoryLevels" :key="category">
                            <tr v-for="(level, item, index) in items" :key="item" class="border-b border-gray-200">
                                <td v-if="index === 0" :rowspan="Object.keys(items).length"
                                    class="px-4 py-3 font-medium text-gray-800 bg-gray-100">
                                    {{ category }}
                                </td>
                                <td class="px-4 py-3 text-gray-700">{{ item }}</td>
                                <td class="px-4 py-3 text-gray-700">{{ level }}</td>
                                <td class="px-4 py-3">
                                    <input type="number" v-model.number="updatedLevels[category][item]"
                                        class="w-full bg-gray-50 border border-gray-300 rounded-md shadow-sm px-4 py-2 focus:ring-blue-500 focus:border-blue-500" />
                                </td>
                            </tr>
                        </template>
                    </tbody>
                </table>
            </div>

            <!-- Submit Button -->
            <Button @click="submitUpdatedLevels"
                class="mt-6 bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-6 rounded-md transition duration-150 ease-in-out">
                Submit
            </Button>
        </div>
    </div>

    <Dialog :open="showDialog">
        <DialogContent>
            <DialogHeader>
                <DialogTitle class="tw-text-xl">{{ status }}</DialogTitle>
            </DialogHeader>
            <DialogDescription>
                {{ description }}
            </DialogDescription>
            <DialogFooter class="sm:justify-start">
                <DialogClose as-child>
                    <Button type="button" variant="secondary" @click="closeDialog">
                        Close
                    </Button>
                </DialogClose>
            </DialogFooter>
        </DialogContent>
    </Dialog>
    
</template>


<script setup>
import { db } from '../firebase.js';
import { collection, doc, getDoc, getDocs, updateDoc } from "firebase/firestore";
import { Card, CardContent } from './ui/card/index.js';
import { LineChart } from '@/components/ui/chart-line';
import { ref, watch, computed, onMounted } from 'vue';
import { Dialog, DialogHeader, DialogContent, DialogTitle, DialogDescription, DialogClose, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';

const selectedCategory = ref(null);
const selectedItem = ref(null);
const serviceLevel = ref(96); // Initialize service level
const serviceLevelWarning = ref('');
let storedOULResults = {};
const loading = ref(true);
const inventoryDataLoaded = ref(false);
const inventoryData = ref({});
const chartData = ref([]);
const updateCounter = ref(0);

const calculatedResults = ref(null);
const filteredChartData = computed(() => {
    // Use slice to return the last 5 months of data (for example)
    return chartData.value.slice(-20);
});



// Add new refs for inventory table
const loadingTable = ref(true);
const currentInventoryLevels = ref({});
const updatedLevels = ref({});
const selectedInterval = ref("");

// Define reactive dialog control
const showDialog = ref(false);
const status = ref('');
const description = ref('');

// Function to open dialog
function openDialog(header, desc) {
    status.value = header;
    description.value = desc;
    showDialog.value = true;
    // console.log.log("Dialog opened with:", header, desc);
}

// Function to close dialog
function closeDialog() {
    showDialog.value = false;
}



// Add computed properties for interval display
const currentIntervalDisplay = computed(() => selectedInterval.value);
const nextIntervalDisplay = computed(() => {
    if (!selectedInterval.value) return ''; // Add null check

    const [year, month, interval] = selectedInterval.value.split('-').map(Number);
    if (interval === 5) {
        const nextMonth = month === 12 ? 1 : month + 1;
        const nextYear = month === 12 ? year + 1 : year;
        return `${nextYear}-${nextMonth}-1`;
    }
    return `${year}-${month}-${interval + 1}`;
});

async function fetchInventoryData(restaurantId) {
    const inventoryCollection = doc(db, 'inventoryLevels', restaurantId);
    const inventorySnapshot = await getDoc(inventoryCollection);

    if (!inventorySnapshot.exists()) {
        // console.log.log("Restaurant not found");
        return null;
    }

    const inventoryData = inventorySnapshot.data();
    return inventoryData;
}

// Process and transform data for the chart
function transformDataForChart(inventoryData, item) {
    const chartDataArray = [];

    // Check if pastInventoryLevel exists
    if (inventoryData.pastInventoryLevels) {
        // Process past inventory levels
        for (const [interval, categories] of Object.entries(inventoryData.pastInventoryLevels)) {


            const pastInv = inventoryData.pastInventoryLevels;

            let selectedCategory = null;

            if (interval.endsWith("-5")) {
                // Different logic for intervals ending with '-5'
                // Add your alternate logic here to set selectedCategory when interval ends with '-5'
                
                for (const category in pastInv[interval].beforeOrder) {
                    if (pastInv[interval].beforeOrder[category]) {
                        
                        selectedCategory = category;
                        break; // Found the category, exit the loop
                    }
                }
            } else {
                // Default logic for intervals not ending with '-5'
                for (const category in categories) {
                    if (categories[category][item]) {
                        selectedCategory = category;
                        break; // Found the category, exit the loop
                    }
                }
            }

            // Ensure "beef" data exists in "meat" category
            const beefExists = categories[selectedCategory]?.[item];

            // Get values for beforeOrder and afterOrder
            const beforeOrderLevel = pastInv[interval].beforeOrder?.[selectedCategory]?.[item] || null;
            const afterOrderLevel = pastInv[interval].afterOrder?.[selectedCategory]?.[item] || null;
            


            if (interval.endsWith("-5")) {
                // Check if beforeOrderLevel exists
                if (beforeOrderLevel !== null) {
                    // Add InventoryLevel for beforeOrder (renamed)
                    chartDataArray.push({
                        interval: `${interval}-1`, // New interval for beforeOrder
                        category: selectedCategory,
                        itemType: item,
                        InventoryLevel: beforeOrderLevel, // Use InventoryLevel to display beforeOrder
                        OUL: storedOULResults[item]?.OUL || 0, // Add OUL for beef
                        SafetyStock: storedOULResults[item]?.safetyStock || 0, // Add Safety Stock for beef
                    });
                } else {
                    // console.log.log(`No beforeOrder level for interval ${interval}`);
                }

                // Check if afterOrderLevel exists
                if (afterOrderLevel !== null) {
                    // Add InventoryLevel for afterOrder (renamed)
                    chartDataArray.push({
                        interval: `${interval}-2`, // New interval for afterOrder
                        category: selectedCategory,
                        itemType: item,
                        InventoryLevel: afterOrderLevel, // Use InventoryLevel to display afterOrder
                        OUL: storedOULResults[item]?.OUL || 0, // Add OUL for beef
                        SafetyStock: storedOULResults[item]?.safetyStock || 0, // Add Safety Stock for beef
                    });
                } else {
                    // console.log.log(`No afterOrder level for interval ${interval}`);
                }
            } else {
                // Single inventory level for other intervals
                if (beefExists) {
                    const singleInventoryLevel = categories[selectedCategory][item];
                    chartDataArray.push({
                        interval,
                        category: selectedCategory,
                        itemType: item,
                        InventoryLevel: singleInventoryLevel,
                        OUL: storedOULResults[item]?.OUL || 0, // Add OUL for beef
                        SafetyStock: storedOULResults[item]?.safetyStock || 0, // Add Safety Stock for beef
                    });
                } else {
                    // console.log.log(`No beef data for interval ${interval}`);
                }
            }
        }
    } else {
        // console.log.log("No pastInventoryLevel data found");
    }

    // Check if currentInventoryLevel exists and includes "meat" and "beef" data
    const currentInv = inventoryData.currentInventoryLevel;
    // Ensure "beef" data exists in "meat" category
    if (currentInv) {
        const interval = Object.keys(currentInv)[0]; // Get the single key

        if (interval.endsWith("-5")) {



            // Add further processing here if needed
            let selectedCategory = null;
            for (const category in currentInv[interval].beforeOrder) {
                if (currentInv[interval].beforeOrder[category][item]) {
                    selectedCategory = category;
                    break; // Found the category, exit the loop

                }
            }

            const currentBeforeOrderLevel = currentInv[interval].beforeOrder?.[selectedCategory]?.[item] || null;
            const currentAfterOrderLevel = currentInv[interval].afterOrder?.[selectedCategory]?.[item] || null;
            
            if (currentBeforeOrderLevel !== null) {
                // Add InventoryLevel for beforeOrder (renamed)
                chartDataArray.push({
                    interval: `${interval}-1`, // New interval for beforeOrder
                    category: selectedCategory,
                    itemType: item,
                    InventoryLevel: currentBeforeOrderLevel, // Use InventoryLevel to display beforeOrder
                    OUL: storedOULResults[item]?.OUL || 0, // Add OUL for beef
                    SafetyStock: storedOULResults[item]?.safetyStock || 0, // Add Safety Stock for beef
                });
            } else {
                // console.log.log(`No beforeOrder level for interval ${interval}`);
            }

            // Check if afterOrderLevel exists
            if (currentAfterOrderLevel !== null) {
                // Add InventoryLevel for afterOrder (renamed)
                chartDataArray.push({
                    interval: `${interval}-2`, // New interval for afterOrder
                    category: selectedCategory,
                    itemType: item,
                    InventoryLevel: currentAfterOrderLevel, // Use InventoryLevel to display afterOrder
                    OUL: storedOULResults[item]?.OUL || 0, // Add OUL for beef
                    SafetyStock: storedOULResults[item]?.safetyStock || 0, // Add Safety Stock for beef
                });
            } else {
                // console.log.log(`No afterOrder level for interval ${interval}`);
            }



        } else {
            const currentBeefExists = currentInv[interval][selectedCategory]?.[item] || null;
            if (currentBeefExists) {
                const singleInventoryLevel = categories[selectedCategory][item];
                chartDataArray.push({
                    interval,
                    category: selectedCategory,
                    itemType: item,
                    InventoryLevel: singleInventoryLevel,
                    OUL: storedOULResults[item]?.OUL || 0, // Add OUL for beef
                    SafetyStock: storedOULResults[item]?.safetyStock || 0, // Add Safety Stock for beef
                });
            }
        }


    } else {
        // console.log.log("No current inventory level data found");
    }



    chartDataArray.sort((a, b) => (a.interval > b.interval ? 1 : -1));
  
    return chartDataArray;
}

// Fetch inventory data and other calculations on mounted
onMounted(async () => {
    try {
        const currentUserId = sessionStorage.getItem("uid");
        await main(currentUserId); // Call the main function to initialize
        await fetchItemsInInventory(currentUserId);
        await fetchCurrentInventory(); // Add this line
    } catch (error) {
        // console.log.error("Error during mounted lifecycle:", error);
    }
});

// Fetch items in inventory
async function fetchItemsInInventory(restaurantId) {
    const restaurantCollection = doc(db, 'restaurant', restaurantId);
    const restaurantSnapshot = await getDoc(restaurantCollection);

    if (!restaurantSnapshot.exists()) {
        // console.log.log("Restaurant not found");
        return;
    }

    const restaurantData = restaurantSnapshot.data();
    inventoryData.value = restaurantData['inventoryTypes'] || {};
    inventoryDataLoaded.value = true;
    loading.value = false;

    const categories = Object.keys(inventoryData.value);
    if (categories.length > 0) {
        selectedCategory.value = categories[0];
        onCategoryChange();
    }
}

// Reactive computed property for filtered items based on selected category
const filteredItems = computed(() => {
    return selectedCategory.value ? inventoryData.value[selectedCategory.value] || {} : {};
});

// Change handler for category selection
function onCategoryChange() {
    selectedItem.value = null; // Reset selected item
    const items = Object.keys(filteredItems.value);

    if (items.length > 0) {
        selectedItem.value = items[0]; // Auto-select the first item

    }
}

// Watch for changes in selectedItem and update chartData
watch(selectedItem, (newItem) => {
    if (newItem) {
        updateChartData(newItem); // Update chart when item changes
    }
});

watch(serviceLevel, (newLevel) => {
    if (newLevel < 0 || newLevel > 100) {
        serviceLevelWarning.value = "Please enter a service level between 0 and 100.";
    } else {
        serviceLevelWarning.value = "";
        recalculateOULAndSS(newLevel); // Recalculate OUL and SS based on the new service level
    }
});

function recalculateOULAndSS(newLevel) {
    if (calculatedResults.value) { // Check if calculatedResults has data

        storedOULResults = calculateOULForAllItems(calculatedResults.value.itemMean, calculatedResults.value.itemSD, newLevel);

        if (selectedItem.value) {
            updateChartData(selectedItem.value);
        }
    } else {
        // console.log.log("No calculated results available for recalculating OUL and SS.");
    }
}



// Function to update chart data based on selected item
async function updateChartData(item) {
    if (item) {


        const oulValue = getOUL(item); // Fetch OUL for the selected item
        const ssValue = getSS(item);   // Fetch Safety Stock for the selected item

        try {
            const inventoryData = await fetchInventoryData(sessionStorage.getItem("uid")); // Await the fetch call
            if (inventoryData) {
                chartData.value = transformDataForChart(inventoryData, item);  // Assign to the existing chartData ref

            }

            updateCounter.value++;
        } catch (error) {
            // console.log.error("Error fetching inventory data:", error);
        }
    }
}


// Calculate mean demand and standard deviation
async function main(currentUserId) {
    const restaurantId = currentUserId; // Replace with your actual restaurant ID
    const results = await calculateMeanDemandAndSd(restaurantId);


    if (results) {
        calculatedResults.value = results;
        storedOULResults = calculateOULForAllItems(results.itemMean, results.itemSD, serviceLevel);

    } else {
        // console.log.log("No results returned.");
    }
}

// Fetch mean demand and standard deviation from Firestore
async function calculateMeanDemandAndSd(restaurantId) {
    const restaurantRef = doc(db, 'restaurant', restaurantId);
    const restaurantDoc = await getDoc(restaurantRef);

    if (!restaurantDoc.exists()) {
        // console.log.log("Restaurant not found");
        return;
    }

    const restaurantData = restaurantDoc.data();
    const actualDemand = restaurantData['actualDemand'] || {};
    const categoryMonthlySums = {};
    const itemTotals = {};

    for (const [month, categories] of Object.entries(actualDemand)) {
        for (const [category, items] of Object.entries(categories)) {
            const monthTotal = Object.values(items).reduce((sum, quantity) => sum + quantity, 0);
            if (!categoryMonthlySums[category]) {
                categoryMonthlySums[category] = [];
            }
            categoryMonthlySums[category].push(monthTotal);
        }

        for (const [category, items] of Object.entries(categories)) {
            for (const [item, quantity] of Object.entries(items)) {
                if (!itemTotals[item]) {
                    itemTotals[item] = { total: 0, count: 0, quantities: [] };
                }
                itemTotals[item].total += quantity;
                itemTotals[item].count++;
                itemTotals[item].quantities.push(quantity);
            }
        }
    }

    const categoryMean = {};
    const categorySD = {};
    for (const [category, monthlyTotals] of Object.entries(categoryMonthlySums)) {
        const totalSum = monthlyTotals.reduce((acc, total) => acc + total, 0);
        const monthCount = monthlyTotals.length;

        categoryMean[category] = monthCount > 0 ? totalSum / monthCount : 0;
        categorySD[category] = calculateStandardDeviation(monthlyTotals);
    }

    const itemMean = {};
    const itemSD = {};
    for (const [item, totals] of Object.entries(itemTotals)) {
        itemMean[item] = totals.count > 0 ? totals.total / totals.count : 0;
        itemSD[item] = calculateStandardDeviation(totals.quantities);
    }



    return {
        categoryMean,
        categorySD,
        itemMean,
        itemSD
    };
}

// Calculate standard deviation
function calculateStandardDeviation(values) {
    const n = values.length;
    if (n === 0) return 0;

    const mean = values.reduce((acc, val) => acc + val, 0) / n;
    const variance = values.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / n;
    return Math.sqrt(variance);
}

function calculateZScore(serviceLevel) {
    // Check if serviceLevel is a ref
    const level = serviceLevel.value !== undefined ? serviceLevel.value : serviceLevel; // Get value from ref or use the number directly

    if (level < 0 || level > 100) {
        throw new Error("Service level must be between 0 and 100.");
    }

    // Using the inverse of the standard normal cumulative distribution function
    return jStat.normal.inv(level / 100, 0, 1);
}




// Calculate OUL for all items
function calculateOULForAllItems(itemMean, itemSD, serviceLevel) {
    const T = 5; // Review time in Weeks
    const L = 1; // Lead time in Weeks
    const Z = calculateZScore(serviceLevel); // Z-score for 96% service level

    const totalTime = T + L;
    const OULResults = {};

    for (const item of Object.keys(itemMean)) {
        const meanDemand = itemMean[item] || 0;
        const stdDev = itemSD[item] || 0;
        const meanDemandTL = meanDemand * totalTime;
        const stdDevTL = stdDev * Math.sqrt(totalTime);
        const safetyStock = Z * stdDevTL;
        const OUL = meanDemandTL + safetyStock;

        OULResults[item] = {
            meanDemandTL,
            stdDevTL,
            safetyStock,
            OUL
        };
        
    }
    return OULResults;
}

// Get OUL and Safety Stock values
function getOUL(item) {
    if (storedOULResults[item]) {
        return storedOULResults[item]['OUL'] || null;
    }
}

function getSS(item) {
    if (storedOULResults[item]) {
        return storedOULResults[item]['safetyStock'] || null;
    }
}

// Add new methods for inventory table
async function fetchCurrentInventory() {
    try {
        const currentUserId = sessionStorage.getItem("uid");
        const inventoryDocRef = doc(db, "inventoryLevels", currentUserId);
        const docSnapshot = await getDoc(inventoryDocRef);

        if (docSnapshot.exists()) {
            const data = docSnapshot.data();
            selectedInterval.value = getSelectedInterval(data.currentInventoryLevel);

            if (selectedInterval.value) {
                currentInventoryLevels.value = {};
                const inventoryData = data.currentInventoryLevel[selectedInterval.value];

                if (selectedInterval.value.endsWith("-5")) {
                    if (inventoryData.afterOrder) {
                        currentInventoryLevels.value = inventoryData.afterOrder;
                    } else if (inventoryData.beforeOrder) {
                        currentInventoryLevels.value = inventoryData.beforeOrder;
                    }
                } else {
                    currentInventoryLevels.value = inventoryData;
                }

                updatedLevels.value = JSON.parse(JSON.stringify(currentInventoryLevels.value));
            }
        }
    } catch (error) {
        // console.log.error("Error fetching inventory data:", error);
    } finally {
        loadingTable.value = false;
    }
}

function getSelectedInterval(inventoryLevels) {
    const intervals = Object.keys(inventoryLevels);
    intervals.sort((a, b) => (a > b ? -1 : 1));
    return intervals[0];
}

async function submitUpdatedLevels() {
    const currentUserId = sessionStorage.getItem("uid");
    const inventoryDocRef = doc(db, "inventoryLevels", currentUserId);
    const restaurantDocRef = doc(db, "restaurant", currentUserId);

    try {
        const docSnapshot = await getDoc(inventoryDocRef);

        if (docSnapshot.exists()) {
            const data = docSnapshot.data();
            const currentInterval = selectedInterval.value;
            const updatedInterval = nextIntervalDisplay.value;
            let currentData = data.currentInventoryLevel[currentInterval];

            // Step 2: Check for interval "-5" and confirm order status
            if (currentInterval.endsWith("-5") && !currentData?.afterOrder) {
                const proceedWithoutOrder = window.confirm(
                    "You haven't placed an order for this month. Would you like to proceed without placing an order?"
                );
                if (!proceedWithoutOrder) return;
            }

            // Step 3: Move the current inventory level to `pastInventoryLevels`
            const currentIntervalData = data.currentInventoryLevel[currentInterval];
            const pastInventoryUpdate = {
                ...data.pastInventoryLevels,
                [currentInterval]: currentIntervalData
            };

            // Step 4: Prepare new `currentInventoryLevel` data based on interval
            let newCurrentLevel = {};
            if (currentInterval.endsWith("-4")) {
                newCurrentLevel = {
                    [updatedInterval]: { beforeOrder: updatedLevels.value }
                };
            } else {
                newCurrentLevel = { [updatedInterval]: updatedLevels.value };
            }

            // Step 5: Calculate the difference, using `afterOrder` if it exists (for "-5" intervals); otherwise, compare directly
            const demandDifference = {};
            const comparisonSource = currentInterval.endsWith("-5")
                ? (currentIntervalData?.afterOrder || currentIntervalData?.beforeOrder)
                : currentIntervalData;

            for (const category in comparisonSource) {
                demandDifference[category] = {};
                for (const item in comparisonSource[category]) {
                    const oldValue = comparisonSource[category][item] || 0;
                    const newValue = updatedLevels.value[category]?.[item] || 0;
                    demandDifference[category][item] = oldValue - newValue;
                }
            }

            // Step 6: Update Firestore with the new data
            await updateDoc(inventoryDocRef, {
                pastInventoryLevels: pastInventoryUpdate,
                currentInventoryLevel: newCurrentLevel
            });

            // Step 7: Store demand difference in `actualDemand` for `restaurant` collection
            await updateDoc(restaurantDocRef, {
                [`actualDemand.${currentInterval}`]: demandDifference
            });

            openDialog("Updated", "Inventory updated, archived, and demand recorded successfully!");
            // alert("Inventory updated, archived, and demand recorded successfully!");
            await fetchCurrentInventory();
        } else {
            // console.log.error("No document found for the provided user ID:", currentUserId);
        }
    } catch (error) {
        // console.log.error("Error updating inventory:", error);
        // alert("Failed to update inventory.");
        openDialog("Error", "Failed to update inventory.");
    }
}


</script>

<style scoped>
/* Add the table styles */
table {
    width: 100%;
    border-collapse: collapse;
}

th,
td {
    border: 1px solid #ddd;
    padding: 8px;
}

.chart-container {
    width: 100%;
    height: 100%;
}
</style>
