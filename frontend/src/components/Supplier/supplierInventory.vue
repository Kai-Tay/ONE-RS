<script setup>
// Import necessary Firebase functions and Vue tools
import Navbar from '../Navbar.vue';
import { ref, onMounted } from 'vue';
import { getFirestore, collection, getDocs, doc, updateDoc } from 'firebase/firestore';
import { useRouter } from 'vue-router'; // Import the router
import { useVueTable, FlexRender, getCoreRowModel } from '@tanstack/vue-table';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';

// Initialize Firebase
const db = getFirestore();
const router = useRouter(); // Initialize the router

// Refs for holding the fetched data and the supplier name
const inventoryData = ref([]);
const supplierName = ref('');
const supplierDocId = ref(''); // Hold supplier document ID for updates

// Fetch supplier data from Firebase on component mount
const fetchSuppliers = async () => {
    const querySnapshot = await getDocs(collection(db, "supplierListing"));
    const inventories = [];

    // For now, assuming we're showing inventory of the first supplier
    querySnapshot.forEach(docSnapshot => {
        const supplier = docSnapshot.data();
        supplierDocId.value = docSnapshot.id; // Capture the document ID
        supplierName.value = supplier.supplierName;
        supplier.inventory.forEach((item, index) => {
            inventories.push({
                index, // Store the index of the ingredient in the inventory array
                productName: item.productName,
                pricePerUnit: item.pricePerUnit,
                quantity: item.quantity,
                unit: item.unit
            });
        });
    });

    inventoryData.value = inventories;
};

// Function to navigate to the form page when the button is clicked
const navigateToFormPage = () => {
    router.push({ name: 'addIngredientForm' }); // The name of the route for the form page
};

// Edit function (stub)
const editItem = (item) => {
    console.log('Editing item:', item);
    // Add your edit logic here, e.g., navigating to an edit page
};

// Delete function to remove the ingredient from Firebase
const deleteItem = async (item) => {
    console.log('Deleting item:', item);

    // Get the supplier document
    const supplierRef = doc(db, "supplierListing", supplierDocId.value);

    // Fetch current inventory and filter out the deleted item
    const newInventory = inventoryData.value.filter((_, idx) => idx !== item.index);

    // Update the document with the new inventory
    await updateDoc(supplierRef, {
        inventory: newInventory
    });

    // Update local inventoryData to reflect the deletion
    inventoryData.value = newInventory;
};

onMounted(() => {
    fetchSuppliers();
});

// Define columns for the table, with an added 'Actions' column for the dropdown
const columnsInventory = [
    { accessorKey: 'productName', header: 'Product Name' },
    { accessorKey: 'quantity', header: 'Quantity' },
    { accessorKey: 'unit', header: 'Unit' },
    { accessorKey: 'pricePerUnit', header: 'Price Per Unit' },
    {
        accessorKey: 'actions',
        header: ' ',
        cell: ({ row }) => `
            <DropdownMenu>
                <DropdownMenuTrigger class="text-indigo-600 hover:text-indigo-900 focus:outline-none">
                    Options
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                    <DropdownMenuItem @click="editItem(row.original)">
                        Edit
                    </DropdownMenuItem>
                    <DropdownMenuItem @click="deleteItem(row.original)">
                        Delete
                    </DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>
        `
    }
];

// Set up the table
const table = useVueTable({
    data: inventoryData.value,
    columns: columnsInventory,
    getCoreRowModel: getCoreRowModel(),
});
</script>



<template>
    <Navbar />
    <div class="px-4 sm:px-6 lg:px-8">
        <!-- Title dynamically set to the supplier's name -->
        <div class="flex justify-between items-center mb-4">
            <h1 class="text-xl font-bold">{{ supplierName }} Inventory</h1>
            <!-- Button to navigate to the form page -->
            <button
                @click="navigateToFormPage"
                class="bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
            >
                Add New Item
            </button>
        </div>

        <div class="mt-8 flow-root">
            <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
                    <table class="min-w-full divide-y divide-gray-300">
                        <thead>
                            <tr v-for="headerGroup in table.getHeaderGroups()" :key="headerGroup.id">
                                <th v-for="header in headerGroup.headers" :key="header.id" scope="col"
                                    class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                                    <FlexRender :render="header.column.columnDef.header" :props="header.getContext()" />
                                </th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            <!-- Loop through inventoryData and display products -->
                            <tr v-for="(item, index) in inventoryData" :key="index">
                                <td class="px-6 py-4 whitespace-nowrap text-left text-sm font-medium text-gray-900">
                                    {{ item.productName }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-left text-sm text-gray-500">
                                    {{ item.quantity }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-left text-sm text-gray-500">
                                    {{ item.unit }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-left text-sm text-gray-500">
                                    {{ item.pricePerUnit }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                                    <DropdownMenu>
                                        <DropdownMenuTrigger class="text-indigo-600 hover:text-indigo-900 focus:outline-none">
                                            Options
                                        </DropdownMenuTrigger>
                                        <DropdownMenuContent>
                                            <DropdownMenuItem @click="editItem(item)">
                                                Edit
                                            </DropdownMenuItem>
                                            <DropdownMenuItem @click="deleteItem(item)">
                                                Delete
                                            </DropdownMenuItem>
                                        </DropdownMenuContent>
                                    </DropdownMenu>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>


