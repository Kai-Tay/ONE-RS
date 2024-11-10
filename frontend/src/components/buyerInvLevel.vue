<!--
<template>
    <div>
        <h2>Inventory Levels</h2>

    <div v-if="loadingTable" class="text-center">Loading...</div>

    <div v-else class="w-full">
        <table class="min-w-full table-auto">
            <thead>
                <tr>
                    <th class="px-4 py-2 text-left w-1/4">Category</th>
                    <th class="px-4 py-2 text-left w-1/4">Item</th>
                    <th class="px-4 py-2 text-left w-1/4">
                        Current Level ({{ currentIntervalDisplay }})
                    </th>
                    <th class="px-4 py-2 text-left w-1/4">
                        Update Level ({{ nextIntervalDisplay }})
                    </th>
                </tr>
            </thead>
            <tbody>
                <template v-for="(items, category) in currentInventoryLevels" :key="category">
                <tr v-for="(level, item, index) in items" :key="item">
                    <td v-if="index === 0" :rowspan="Object.keys(items).length" class="border px-4 py-2 w-1/4">
                    {{ category }}
                    </td>
                    <td class="border px-4 py-2 w-1/4">{{ item }}</td>
                    <td class="border px-4 py-2 w-1/4">{{ level }}</td>
                    <td class="border px-4 py-2 w-1/4">
                    <input type="number" v-model.number="updatedLevels[category][item]" class="w-full" />
                    </td>
                </tr>
                </template>
            </tbody>
        </table>
    </div>

    <button @click="submitUpdatedLevels" class="mt-4 bg-blue-500 text-white px-4 py-2 rounded">Submit</button>
  </div>
</template>

<script>
import { db } from '../firebase.js';
import { doc, getDoc, updateDoc } from "firebase/firestore";

export default {
    data() {
        return {
            loadingTable: true,  // Moved `loading` here to make it part of the Vue instance
            restaurantId: 'GYFKVpkDpI74zYTzzsfY', // Assuming you have this available
            currentInventoryLevels: {}, // To hold the data to display in the table
            updatedLevels: {}, // To hold the user's modified data
            selectedInterval: "", // Make selectedInterval reactive
        };
    },
    computed: {
        currentIntervalDisplay() {
            // Use the actual current interval value here
            const currentInterval = this.selectedInterval; // Assuming this is stored in `selectedInterval`
            return currentInterval;
            console.log(this.selectedInterval);
        },
        nextIntervalDisplay() {
            const [year, month, interval] = this.selectedInterval.split('-').map(Number);
            if (interval === 5) {
                const nextMonth = month === 12 ? 1 : month + 1;
                const nextYear = month === 12 ? year + 1 : year;
                return `${nextYear}-${nextMonth}-1`;
            }
            return `${year}-${month}-${interval + 1}`;
        },
    },
    methods: {
        async fetchCurrentInventory() {
        try {
        const inventoryDocRef = doc(db, "inventoryLevels", this.restaurantId);
        const docSnapshot = await getDoc(inventoryDocRef);

        if (docSnapshot.exists()) {
            const data = docSnapshot.data();
          
            // Assuming you want to display only one interval, let's select the most recent one or a specific interval
            this.selectedInterval = this.getSelectedInterval(data.currentInventoryLevel);  // Use a method or logic to pick the interval

            if (this.selectedInterval) {
            // Initialize `currentInventoryLevels` for that selected interval
            this.currentInventoryLevels = {};

            const inventoryData = data.currentInventoryLevel[this.selectedInterval];
            console.log(inventoryData.afterOrder);

            if (this.selectedInterval.endsWith("-5")) {
                // Handle intervals that end with "-5"
                if (inventoryData.beforeOrder && inventoryData.afterOrder) {
                    // If both beforeOrder and afterOrder exist, display only afterOrder
                    this.currentInventoryLevels = inventoryData.afterOrder;

                } else if (inventoryData.beforeOrder) {
                    // If only beforeOrder exists, display beforeOrder
                    this.currentInventoryLevels = inventoryData.beforeOrder;

                } else if (inventoryData.afterOrder) {
                    // If only afterOrder exists, display afterOrder
                    this.currentInventoryLevels = inventoryData.afterOrder;
                }

            } else {
                // For intervals not ending in "-5", show the normal inventory
                this.currentInventoryLevels = inventoryData;
            }
          
            // Initialize `updatedLevels` to allow for user edits
            this.updatedLevels = JSON.parse(JSON.stringify(this.currentInventoryLevels));
            } else {
                console.error("No valid interval found for the current data.");
            }
        } else {
            console.error("No document found for the provided restaurant ID:", this.restaurantId);
        }
        } catch (error) {
            console.error("Error fetching inventory data:", error);
        } finally {
            this.loadingTable = false;  // Set loading to false once the data fetching is complete
        }
        },

    // Method to select the most recent interval, or a specific interval as needed
    getSelectedInterval(inventoryLevels) {
        const intervals = Object.keys(inventoryLevels);
        // Assuming the most recent interval is the highest number or you can use another criterion
        intervals.sort((a, b) => (a > b ? -1 : 1)); // Sort intervals in descending order
        return intervals[0]; // Return the most recent interval
    },

    async submitUpdatedLevels() {
        const inventoryDocRef = doc(db, "inventoryLevels", this.restaurantId);

        try {
            // Step 1: Retrieve the current inventory data
            const docSnapshot = await getDoc(inventoryDocRef);

            if (docSnapshot.exists()) {
                const data = docSnapshot.data();

                // Step 2: Check if selected interval ends with "-5" and requires `afterOrder`
                if (this.selectedInterval.endsWith("-5") && !data.currentInventoryLevel[this.selectedInterval]?.afterOrder) {
                    // Prompt the user to confirm if they want to proceed without ordering
                    const proceedWithoutOrder = confirm(
                        "AfterOrder data is missing. Would you like to proceed without ordering a new shipment?"
                    );

                    if (!proceedWithoutOrder) {
                        // If the user selects "No," exit the function without updating
                        return;
                    }
                }

                // Step 3: Move the current inventory level to pastInventoryLevels
                const currentIntervalData = data.currentInventoryLevel[this.selectedInterval];
                const pastInventoryUpdate = {
                    ...data.pastInventoryLevels,
                    [this.selectedInterval]: currentIntervalData
                };

                // Step 4: Prepare the new `currentInventoryLevel` data based on selected interval
                let newCurrentLevel = {};

                if (this.selectedInterval.endsWith("-4")) {
                    // Handle case for interval ending with -4 (updating for -5)
                    const updatedData = {
                        beforeOrder: this.updatedLevels // Update with the new levels under beforeOrder
                    };
                    newCurrentLevel = {
                        [this.nextIntervalDisplay]: updatedData
                    };
                } else {
                    // For all other intervals, move the whole data as usual
                    newCurrentLevel = {
                        [this.nextIntervalDisplay]: this.updatedLevels
                    };
                }

                // Step 5: Update Firestore with the moved data
                await updateDoc(inventoryDocRef, {
                    pastInventoryLevels: pastInventoryUpdate,
                    currentInventoryLevel: newCurrentLevel
                });

                alert("Inventory updated and archived successfully!");
            } else {
                console.error("No document found for the provided restaurant ID:", this.restaurantId);
            }
        } catch (error) {
            console.error("Error updating inventory:", error);
            alert("Failed to update inventory.");
        }
    }
    },

    mounted() {
        // Automatically fetch the current inventory when the component is mounted
        this.fetchCurrentInventory();

    }
};



</script>

<style scoped>
table {
    width: 100%;
    border-collapse: collapse;
  
}
th, td {
    border: 1px solid #ddd;
    padding: 8px;
}
</style>
