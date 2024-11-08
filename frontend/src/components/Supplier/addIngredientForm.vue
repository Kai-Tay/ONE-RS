<script setup>
// Import necessary Firebase functions and Vue tools
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import { getFirestore, doc, getDoc, updateDoc, arrayUnion } from 'firebase/firestore';
import { useRouter } from 'vue-router';
import { auth } from '../../firebase'; // Import the Firebase auth module
import Button from '../ui/button/Button.vue';
import 'vue-advanced-cropper/dist/style.css';
import ImageCropper from './ImageCropper.vue'; 


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
    { name: 'Meat', subcategories: ['Beef', 'Fish', 'Lamb', 'Pork', 'Poultry', 'Shellfish'] },
    { name: 'Fruits & Vegetables', subcategories: ['Fruits', 'Vegetables'] },
    { name: 'Dairy', subcategories: ['Cheese', 'Egg', 'Milk'] },
    { name: 'Carbohydrates', subcategories: ['Bread', 'Grains', 'Pasta'] }
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


// Form fields for image 
const showCropper = ref(false);
const selectedFile = ref(null);
const imageFile = ref(null);
const imagePreview = ref('');
const isLoading = ref(false); 

// Handle image upload
const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
        selectedFile.value = file;
        showCropper.value = true;
    }
};

// Convert file to base64
const fileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => resolve(reader.result);
        reader.onerror = error => reject(error);
    });
};

// Handle cropped image
const handleCropComplete = ({ file, url }) => {
    imageFile.value = file;
    imagePreview.value = url;
    showCropper.value = false;
};

// Cleanup function
onBeforeUnmount(() => {
    if (imagePreview.value) {
        URL.revokeObjectURL(imagePreview.value);
    }
});

// Function to submit the new ingredient item to the Firebase database
const addNewIngredient = async () => {
    if (!imageFile.value) {
        alert('Please select an image');
        return;
    }

    try {
        isLoading.value = true;
        const user = auth.currentUser;
        if (!user) {
            alert('User not logged in');
            return;
        }

        // Convert image to base64
        const base64Image = await fileToBase64(imageFile.value);

        const supplierDocRef = doc(db, "supplierListing", user.uid);
        const supplierDoc = await getDoc(supplierDocRef);

        if (supplierDoc.exists()) {
            if (productName.value && pricePerUnit.value && quantity.value && unit.value && category.value && subcategory.value) {
                await updateDoc(supplierDocRef, {
                inventory: arrayUnion({
                productName: productName.value,
                quantity: parseInt(quantity.value),
                unit: unit.value,
                pricePerUnit: parseFloat(pricePerUnit.value),
                category: category.value,
                subcategory: subcategory.value,
                purchaseQuantity: 0,
                imageData: base64Image // Store as base64 instead of URL
                })
        });

        router.push('/supplierInventory');
        } else {
            alert('Please fill in all fields');
        }
        } else {
            alert('Supplier document not found.');
        }
    } catch (error) {
        console.error("Error adding new ingredient: ", error);
        alert("Failed to add ingredient.");
    } finally {
        isLoading.value = false;
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
                    <label for="unit" class="block text-sm font-medium text-gray-700">Unit (In Kg)</label>
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

                <!-- Image Upload Section -->
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700">Product Image</label>
                    <input 
                        type="file" 
                        accept="image/*" 
                        @change="handleImageUpload" 
                        class="mt-1 block w-full text-sm text-gray-500
                        file:mr-4 file:py-2 file:px-4
                        file:rounded-full file:border-0
                        file:text-sm file:font-semibold
                        file:bg-blue-50 file:text-blue-700
                        hover:file:bg-blue-100"
                        required
                    >
                </div>

                <!-- Image Preview -->
                <div v-if="imagePreview" class="mb-4">
                    <img 
                        :src="imagePreview" 
                        alt="Preview" 
                        class="w-32 h-32 object-cover rounded-lg"
                    >
                </div>

                <Button type="submit" class="w-full text-white font-bold py-2 px-4 ">
                    Add Ingredient
                </Button>
            </form>

            <!-- Image Cropper Modal -->
            <ImageCropper
                v-if="showCropper && selectedFile"
                :image-file="selectedFile"
                @crop-complete="handleCropComplete"
                @cancel="() => showCropper = false"
            />
        </div>
    </div>
</template>