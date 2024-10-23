<script setup>
// Import necessary Firebase functions and Vue tools
import { ref } from 'vue';
import { getFirestore, doc, getDoc, updateDoc, arrayUnion } from 'firebase/firestore';
import { useRouter } from 'vue-router';
import { auth } from '../../firebase'; // Import the Firebase auth module

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
    // Get the current logged-in user
    const user = auth.currentUser;

    if (user) {
        const userDocRef = doc(db, "users", user.uid); // Get the user document reference
        const userDoc = await getDoc(userDocRef); // Fetch the user document

        if (userDoc.exists()) {
            const userData = userDoc.data();
            const companyName = userData.companyName; // Get the user's company name

            if (companyName) {
                // Fetch the document in supplierListing matching the companyName
                const supplierDocRef = doc(db, "supplierListing", companyName);
                const supplierDoc = await getDoc(supplierDocRef);

                if (supplierDoc.exists()) {
                    // Add the new ingredient to the supplier's inventory
                    if (productName.value && pricePerUnit.value && quantity.value && unit.value) {
                        try {
                            await updateDoc(supplierDocRef, {
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
                } else {
                    console.error("Supplier document not found for company: ", companyName);
                    alert('Supplier document not found.');
                }
            } else {
                console.error("User does not have a companyName.");
                alert('User does not have a company associated.');
            }
        } else {
            console.error("User document not found.");
            alert('User document not found.');
        }
    } else {
        alert('User not logged in');
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
