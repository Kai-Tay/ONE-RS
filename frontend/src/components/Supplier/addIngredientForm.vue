<script setup>
// Import necessary Firebase functions and Vue tools
import { ref, watch } from 'vue';
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
const category = ref(''); // Field for category
const subcategory = ref(''); // Field for subcategory

// Predefined categories and their subcategories
const categories = [
    { name: 'Meat', subcategories: ['Poultry', 'Beef', 'Pork', 'Lamb', 'Fish', 'Shellfish'] },
    { name: 'Fruits & Vegetables', subcategories: ['Vegetables', 'Fruits'] },
    { name: 'Dairy', subcategories: ['Eggs', 'Milk', 'Cheese'] },
    { name: 'Carbohydrates', subcategories: ['Grains', 'Pasta', 'Bread'] }
];

// Reactive subcategories based on selected category
const availableSubcategories = ref([]);

// Watch the category change and update available subcategories
watch(category, (newCategory) => {
    const selectedCategory = categories.find(cat => cat.name === newCategory);
    if (selectedCategory) {
        availableSubcategories.value = selectedCategory.subcategories; // Update available subcategories
        subcategory.value = ''; // Reset the subcategory when the category changes
    }
});

// Function to submit the new ingredient item to the Firebase database
const addNewIngredient = async () => {
    // Get the current logged-in user
    const user = auth.currentUser;

    if (user) {
        const supplierDocRef = doc(db, "supplierListing", user.uid); // Use user's UID as the document ID
        const supplierDoc = await getDoc(supplierDocRef); // Fetch the supplier document

        if (supplierDoc.exists()) {
            // Add the new ingredient to the supplier's inventory
            if (productName.value && pricePerUnit.value && quantity.value && unit.value && category.value && subcategory.value) {
                try {
                    await updateDoc(supplierDocRef, {
                        inventory: arrayUnion({
                            productName: productName.value,
                            quantity: parseInt(quantity.value),
                            unit: unit.value,
                            pricePerUnit: parseFloat(pricePerUnit.value),
                            category: category.value,
                            subcategory: subcategory.value // Subcategory selected by the user
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
            console.error("Supplier document not found for user ID:", user.uid);
            alert('Supplier document not found.');
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

                <div class="mb-4">
                    <label for="category" class="block text-sm font-medium text-gray-700">Category</label>
                    <select v-model="category" id="category" class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" required>
                        <option value="" disabled>Select Category</option>
                        <option v-for="cat in categories" :key="cat.name" :value="cat.name">{{ cat.name }}</option>
                    </select>
                </div>

                <!-- Subcategory is selected by user, and options are dynamically updated based on category -->
                <div class="mb-4">
                    <label for="subcategory" class="block text-sm font-medium text-gray-700">Subcategory</label>
                    <select v-model="subcategory" id="subcategory" class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm" required>
                        <option value="" disabled>Select Subcategory</option>
                        <option v-for="sub in availableSubcategories" :key="sub" :value="sub">{{ sub }}</option>
                    </select>
                </div>

                <button type="submit" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded">
                    Add Ingredient
                </button>
            </form>
        </div>
    </div>
</template>