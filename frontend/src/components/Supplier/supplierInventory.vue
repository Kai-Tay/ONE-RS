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
const isEditing = ref(true);
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

// Fetch user and supplier data when the component is mounted
onMounted(() => {
  fetchUserAndSuppliers();
});
</script>

<template>
  <div class="flex min-h-screen w-full flex-col bg-muted/40">
    <div class="flex flex-col sm:gap-4 sm:py-4 sm:pl-14">
      <header
        class="sticky top-0 z-30 flex h-14 items-center gap-4 border-b bg-background px-4 sm:static sm:h-auto sm:border-0 sm:bg-transparent sm:px-6">
        <div class="flex w-full items-center justify-between">
          <h2 class="text-xl font-semibold">{{ companyName }}</h2>
          <div class="flex items-center gap-2">
            <div class="relative w-full md:w-[200px] lg:w-[320px]">
              <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input type="search" placeholder="Search..." class="w-full rounded-lg bg-background pl-8" />
            </div>
            <Button @click="navigateToFormPage" size="sm" class="h-7 gap-1">
              <PlusCircle class="h-3.5 w-3.5" />
              <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">Add Product</span>
            </Button>
          </div>
        </div>
      </header>

      <main class="grid flex-1 items-start gap-4 p-4 sm:px-6 sm:py-0 md:gap-8">
        <Tabs default-value="all">
          <div class="flex items-center justify-between">
            <TabsList>
              <TabsTrigger value="all">All</TabsTrigger>
            </TabsList>
            <div class="flex items-center justify-end w-full">
              <div class="mb-4 flex">
                <select id="categoryFilter" v-model="selectedCategory" class="p-2 border border-gray-300 rounded-md">
                  <option value="All">All</option>
                  <option v-for="category in categories" :key="category.name" :value="category.name">{{ category.name }}
                  </option>
                </select>
              </div>
            </div>
          </div>

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
                      <TableHead>Unit</TableHead>
                      <TableHead>Price per Unit</TableHead>
                      <TableHead>Category</TableHead>
                      <TableHead><span class="sr-only">Actions</span></TableHead>
                    </TableRow>
                  </TableHeader>

                  <TableBody>
                    <TableRow v-for="item in filteredInventory" :key="item.productName">
                      <TableCell class="hidden sm:table-cell">
                        <img alt="Product image" class="aspect-square rounded-md object-cover" height="64"
                          src="./images/placeholder.svg" width="64">
                      </TableCell>
                      <TableCell>{{ item.productName }}</TableCell>
                      <TableCell :class="{ 'text-red-600': item.quantity <= 20 }">{{ item.quantity }}</TableCell>
                      <TableCell>{{ item.unit }}</TableCell>
                      <TableCell>{{ "$" + parseFloat(item.pricePerUnit).toFixed(2) }}</TableCell>
                      <TableCell>{{ item.category }}</TableCell>
                      <TableCell class="flex justify-end gap-2">
                        <!-- Keep DialogTrigger always rendered -->
                        <Dialog>
                          <DialogTrigger as-child>
                            <Button variant="secondary" @click="editItem(item)">Edit</Button>
                          </DialogTrigger>
                          <!-- Use v-if only on DialogContent -->
                          <DialogContent v-if="isEditing" class="sm:max-w-[425px]">
                            <DialogHeader>
                              <DialogTitle>Edit Ingredient</DialogTitle>
                              <DialogDescription>Make changes to the ingredient. Click save when you're done.
                              </DialogDescription>
                            </DialogHeader>
                            <div class="space-y-4">
                              <Input v-model="editedProductName" placeholder="Product Name" />
                              <Input v-model="editedQuantity" type="number" placeholder="Quantity" />
                              <Input v-model="editedUnit" placeholder="Unit" />
                              <Input v-model="editedPricePerUnit" type="number" step="0.01"
                                placeholder="Price per Unit" />
                              <!-- Dropdown for editing category -->
                              <select v-model="editedCategory" class="w-full p-2 border border-gray-300 rounded-md">
                                <option value="" disabled>Select Category</option>
                                <option v-for="category in categories" :key="category.name" :value="category.name">{{
                                  category.name }}</option>
                              </select>
                              <!-- Dropdown for editing subcategory based on the selected category -->
                              <select v-model="editedSubcategory" class="w-full p-2 border border-gray-300 rounded-md">
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

