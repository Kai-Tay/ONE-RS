<script setup>
// Import necessary Firebase functions and Vue tools
import { ref } from 'vue';
import { getFirestore, doc, updateDoc, arrayUnion } from 'firebase/firestore';
import { useRouter } from 'vue-router';

// Initialize Firebase
const db = getFirestore();
const router = useRouter();

// Form fields for adding a new inventory item
const productName = ref('');
const pricePerUnit = ref('');
const quantity = ref('');
const unit = ref('');

// Function to submit the new ingredient item to the Firebase database
const addNewIngredient = async () => {
    // Replace 'SUPPLIER_DOCUMENT_ID' with the actual document ID of the supplier
    const supplierDocId = 'Dzy8ILt6qG4oHKWdRBqD'; // Make sure this is correct
    const supplierRef = doc(db, "supplierListing", supplierDocId);

    if (productName.value && pricePerUnit.value && quantity.value && unit.value) {
        try {
            // Update Firestore by appending a new item to the 'inventory' array
            await updateDoc(supplierRef, {
                inventory: arrayUnion({
                    productName: productName.value, 
                    quantity: parseInt(quantity.value), 
                    unit: unit.value,
                    pricePerUnit: parseFloat(pricePerUnit.value)
                })
            });

            // Redirect back to the inventory list after adding
            router.push('/supplierInventory');
        } catch (error) {
            console.error("Error adding new ingredient: ", error);
            alert("Failed to add ingredient.");
        }
    } else {
        alert('Please fill in all fields');
    }
};
</script>

<template>
    <div class="flex justify-center items-center min-h-screen bg-gray-100">
        <div class="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg">
            <h1 class="text-xl font-bold mb-4">Add New Ingredient</h1>

            <form @submit.prevent="addNewIngredient">
                <div class="mb-4">
                    <label for="productName" class="block text-sm font-medium text-gray-700">Product Name</label>
                    <input v-model="productName" type="text" id="productName" class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" required>
                </div>

                <div class="mb-4">
                    <label for="quantity" class="block text-sm font-medium text-gray-700">Quantity</label>
                    <input v-model="quantity" type="number" id="quantity" class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" required>
                </div>

                <div class="mb-4">
                    <label for="unit" class="block text-sm font-medium text-gray-700">Unit</label>
                    <input v-model="unit" type="text" id="unit" class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" required>
                </div>

                <div class="mb-4">
                    <label for="pricePerUnit" class="block text-sm font-medium text-gray-700">Price Per Unit</label>
                    <input v-model="pricePerUnit" type="number" step="0.01" id="pricePerUnit" class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" required>
                </div>

                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded">
                    Add Ingredient
                </button>
            </form>
        </div>
    </div>
</template>
