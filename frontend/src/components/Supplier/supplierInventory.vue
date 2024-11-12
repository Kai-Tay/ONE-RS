<script setup lang="ts">
import { Badge } from '@/components/ui/badge'
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from '@/components/ui/breadcrumb'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import { Input } from '@/components/ui/input'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'
import { CircleUser, File, Home, LineChart, ListFilter, MoreHorizontal, Package, Package2, PanelLeft, PlusCircle, Search, Settings, ShoppingCart, Users2 } from 'lucide-vue-next'
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '@/components/ui/dialog' // Import Dialog components
import { ref, onMounted, computed, watch } from 'vue'
import { getFirestore, doc, getDoc, setDoc, updateDoc } from 'firebase/firestore';
import { useRouter } from 'vue-router';
import { auth } from '../../firebase.js'; // Assuming you have auth initialized


// Initialize Firebase Firestore
const db = getFirestore();
const router = useRouter();

// Reactive variables to store fetched data
const inventoryData = ref([]);
const companyName = ref('');
const supplierDocId = ref('');
const userId = ref('');

// Variables for editing
const isEditing = ref(false);
const selectedItem = ref(null);
const editedProductName = ref('');
const editedQuantity = ref('');
const editedUnit = ref('');
const editedPricePerUnit = ref('');
const editedCategory = ref('');
const editedSubcategory = ref('');

// Predefined categories and subcategories
const categories = [
  { name: 'Meat', subcategories: ['Poultry', 'Beef', 'Pork', 'Lamb', 'Fish', 'Shellfish'] },
  { name: 'Fruits & Vegetables', subcategories: ['Vegetables', 'Fruits'] },
  { name: 'Dairy', subcategories: ['Eggs', 'Milk', 'Cheese'] },
  { name: 'Carbohydrates', subcategories: ['Grains', 'Pasta', 'Bread'] }
];

// Dynamic subcategory list
const availableSubcategories = ref([]);

// Watch for changes to the category and update subcategories
watch(editedCategory, (newCategory) => {
  const selectedCategory = categories.find(cat => cat.name === newCategory);
  if (selectedCategory) {
    availableSubcategories.value = selectedCategory.subcategories;
  } else {
    availableSubcategories.value = [];
  }
});

// Fetch user and supplier data
const fetchUserAndSuppliers = async () => {
  const currentUser = auth.currentUser;

  if (currentUser) {
    userId.value = currentUser.uid;

    // Fetch user's company name from the "user" collection
    const userDoc = await getDoc(doc(db, "users", userId.value));
    if (userDoc.exists()) {
      const userData = userDoc.data();
      companyName.value = userData.companyName;

      const supplierDocRef = doc(db, "supplierListing", userId.value);
      const supplierDoc = await getDoc(supplierDocRef);

      if (!supplierDoc.exists()) {
        await setDoc(supplierDocRef, {
          supplierName: companyName.value,
          inventory: []
        });
      } else {
        supplierDocId.value = supplierDoc.id;
        const supplierData = supplierDoc.data();
        inventoryData.value = supplierData.inventory;
      }
    }
  }
};

// Navigate to the form page for adding products
const navigateToFormPage = () => {
  router.push({ name: 'addIngredientForm' });
};

// Open edit form for selected item
const editItem = (item) => {
  selectedItem.value = item;
  editedProductName.value = item.productName;
  editedQuantity.value = item.quantity;
  editedUnit.value = item.unit;
  editedPricePerUnit.value = item.pricePerUnit;
  editedCategory.value = item.category;
  editedSubcategory.value = item.subcategory; // Prepopulate subcategory
  isEditing.value = true;
};

const saveChanges = async () => {
  try {
    const supplierRef = doc(db, "supplierListing", supplierDocId.value);

    // Update the specific item within the inventory
    const updatedInventory = inventoryData.value.map((inventoryItem) =>
      inventoryItem.productName === selectedItem.value.productName
        ? {
          ...inventoryItem,
          productName: editedProductName.value,
          quantity: parseInt(editedQuantity.value),
          unit: editedUnit.value,
          pricePerUnit: parseFloat(editedPricePerUnit.value),
          category: editedCategory.value,
          subcategory: editedSubcategory.value // Update the subcategory
        }
        : inventoryItem
    );

    // Update Firestore with the new inventory data
    await updateDoc(supplierRef, { inventory: updatedInventory });

    // Update the local inventory to reflect the changes
    inventoryData.value = updatedInventory;

    // Close the edit dialog manually
    isEditing.value = false;

    console.log('Item updated successfully');
  } catch (error) {
    console.error('Error updating item:', error);
  }
};


// Delete function to remove the item
const deleteItem = async (item) => {
  try {
    const supplierRef = doc(db, "supplierListing", supplierDocId.value);
    const newInventory = inventoryData.value.filter(inventoryItem => inventoryItem.productName !== item.productName);

    await updateDoc(supplierRef, { inventory: newInventory });

    inventoryData.value = newInventory;
  } catch (error) {
    console.error('Error deleting item:', error);
  }
};

// Computed property to filter the inventory based on the selected category
const selectedCategory = ref('All');
const filteredInventory = computed(() => {
  if (selectedCategory.value === 'All') {
    return inventoryData.value;
  }
  return inventoryData.value.filter(item => item.category === selectedCategory.value);
});

// Define computed properties for best-selling product, total sales amount, and low stock items
const bestSellingProduct = computed(() => {
  let maxSalesProduct = null;
  let maxSalesQuantity = 0;

  inventoryData.value.forEach(item => {
    if (item.purchaseQuantity > maxSalesQuantity) {
      maxSalesQuantity = item.purchaseQuantity;
      maxSalesProduct = item.productName;
    }
  });

  return maxSalesProduct;
});


const lowStockItems = computed(() => {
  return inventoryData.value
    .filter(item => item.quantity <= 20)
    .map(item => item.productName);
});


// Fetch user and supplier data when the component is mounted
onMounted(() => {
  fetchUserAndSuppliers();
});
</script>

<template>
  <div class="flex min-h-screen w-full flex-col bg-muted/40">
    <div class="mx-2 md:mx-auto sm:px-8 sm:my-5">

      <!-- Title and Summary Display Section -->
      <div class="mb-8">
        <h2 class="text-2xl font-bold">{{ companyName }}</h2>
        <p class="text-sm mb-4">Manage your Inventory</p>

        <!-- Summary Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <!-- Best Selling Product Card -->
          <Card class="p-4 flex flex-col justify-center">
              <p class="text-sm font-medium text-green-600">Best Selling Product</p>
              <p class="text-2xl font-semibold">{{ bestSellingProduct || 'No sales data available' }}</p>
          </Card>

          <!-- Low Stock Items Card -->
          <Card class="p-4  flex flex-col justify-center">
              <p class="text-sm font-medium text-red-500">Low Stock Items</p>
              <p class="text-2xl font-semibold">
                <span v-if="lowStockItems.length > 0">{{ lowStockItems.join(', ') }}</span>
                <span v-else>No items with low stock</span>
              </p>
          </Card>
        </div>
      </div>

      <!-- Controls: Add Product Button and Filter Dropdown -->
      <div class="flex items-center justify-between mb-4">
        <div>
        </div>
        <div class="flex items-center gap-4">
          <Button @click="navigateToFormPage">Add Product</Button>
          <select id="categoryFilter" v-model="selectedCategory" class="p-2 border border-gray-300 rounded-md">
            <option value="All">All</option>
            <option v-for="category in categories" :key="category.name" :value="category.name">
              {{ category.name }}
            </option>
          </select>
        </div>
      </div>

      <!-- Inventory Management Section -->
      <main>
        <Tabs default-value="all">
          <TabsContent value="all">
            <Card>
              <CardHeader>
                <CardTitle>Inventory</CardTitle>
                <CardDescription>Manage your products.</CardDescription>
              </CardHeader>

              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead class="hidden w-[100px] sm:table-cell">
                        <span class="sr-only">img</span>
                      </TableHead>
                      <TableHead>Product Name</TableHead>
                      <TableHead>Quantity</TableHead>
                      <TableHead>Unit (in Kg)</TableHead>
                      <TableHead>Price per Unit</TableHead>
                      <TableHead>Category</TableHead>
                      <TableHead><span class="sr-only">Actions</span></TableHead>
                    </TableRow>
                  </TableHeader>

                  <TableBody>
                    <TableRow v-for="item in filteredInventory" :key="item.productName">
                      <TableCell class="hidden sm:table-cell">
                        <img 
                            :src="item.imageData" 
                            :alt="item.productName"
                            class="aspect-square rounded-md object-cover" 
                            height="64"
                            width="64"
                            @error="e => (e.target as HTMLImageElement).src = '/images/placeholder.svg'"
                        >
                    </TableCell>
                      <TableCell>{{ item.productName }}</TableCell>
                      <TableCell :class="{ 'text-red-600': item.quantity <= 20 }">{{ item.quantity }}</TableCell>
                      <TableCell>{{ item.unit }}</TableCell>
                      <TableCell>{{ "$" + parseFloat(item.pricePerUnit).toFixed(2) }}</TableCell>
                      <TableCell>{{ item.category }}</TableCell>
                      <TableCell class="flex justify-end gap-2">
                        <Dialog>
                          <DialogTrigger as-child>
                            <Button variant="secondary" @click="editItem(item)">Edit</Button>
                          </DialogTrigger>
                          <DialogContent v-if="isEditing" class="sm:max-w-[425px]">
                            <DialogHeader>
                              <DialogTitle>Edit Ingredient</DialogTitle>
                              <DialogDescription>Make changes to the ingredient. Click save when you're done.
                              </DialogDescription>
                            </DialogHeader>
                            <div class="space-y-4">
                            <!-- Add image preview -->
                              <div class="mb-4">
                                  <img 
                                      :src="selectedItem?.imageData" 
                                      :alt="selectedItem?.productName"
                                      class="w-32 h-32 object-cover rounded-lg"
                                      @error="e => (e.target as HTMLImageElement).src = '/images/placeholder.svg'"
                                  >
                              </div>

                              <label for="editedProductName" class="block text-sm font-medium text-gray-700">Product
                                Name</label>
                              <Input id="editedProductName" v-model="editedProductName" placeholder="Product Name" />

                              <label for="editedQuantity"
                                class="block text-sm font-medium text-gray-700">Quantity</label>
                              <Input id="editedQuantity" v-model="editedQuantity" type="number"
                                placeholder="Quantity" />

                              <label for="editedUnit" class="block text-sm font-medium text-gray-700">Unit (in
                                Kg)</label>
                              <Input id="editedUnit" v-model="editedUnit" placeholder="Unit" />

                              <label for="editedPricePerUnit" class="block text-sm font-medium text-gray-700">Price per
                                Unit</label>
                              <Input id="editedPricePerUnit" v-model="editedPricePerUnit" type="number" step="0.01"
                                placeholder="Price per Unit" />

                              <label for="editedCategory"
                                class="block text-sm font-medium text-gray-700">Category</label>
                              <select id="editedCategory" v-model="editedCategory"
                                class="w-full p-2 border border-gray-300 rounded-md">
                                <option value="" disabled>Select Category</option>
                                <option v-for="category in categories" :key="category.name" :value="category.name">
                                  {{ category.name }}
                                </option>
                              </select>

                              <label for="editedSubcategory"
                                class="block text-sm font-medium text-gray-700">Subcategory</label>
                              <select id="editedSubcategory" v-model="editedSubcategory"
                                class="w-full p-2 border border-gray-300 rounded-md">
                                <option value="" disabled>Select Subcategory</option>
                                <option v-for="sub in availableSubcategories" :key="sub" :value="sub">{{ sub }}</option>
                              </select>
                            </div>
                            <DialogFooter>
                              <Button type="submit" @click="saveChanges">Save Changes</Button>
                            </DialogFooter>
                          </DialogContent>
                        </Dialog>
                        <Button variant="secondary" @click="deleteItem(item)">Delete</Button>
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </CardContent>

              <CardFooter>
                <div class="text-xs text-muted-foreground">Showing all products</div>
              </CardFooter>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  </div>
</template>
