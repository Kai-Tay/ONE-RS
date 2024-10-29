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
import { ref, onMounted } from 'vue'
import { getFirestore, doc, getDoc, setDoc, updateDoc } from 'firebase/firestore';
import { useRouter } from 'vue-router';
import { auth } from '../../firebase.js'; // Assuming you have auth initialized


const db = getFirestore();
const router = useRouter();

// Reactive variables to store fetched data
const inventoryData = ref([]); // Holds the list of inventory items
const companyName = ref('');  // Holds the company name from the user collection
const supplierDocId = ref(''); // Holds supplier document ID for updates
const userId = ref(''); // Holds current user's ID

// Variables for editing
const isEditing = ref(false); // Controls visibility of the edit form
const selectedItem = ref(null); // Holds the selected item to edit
const editedProductName = ref(''); // Holds the edited product name
const editedQuantity = ref(''); // Holds the edited quantity
const editedUnit = ref(''); // Holds the edited unit
const editedPricePerUnit = ref(''); // Holds the edited price per unit
const editedCategory = ref(''); // Holds the edited category

// Predefined categories for dropdown
const categories = ['Meat', 'Fruits & Vegetables', 'Dairy', 'Carbohydrates'];

// Fetch user and supplier data from Firebase on component mount
const fetchUserAndSuppliers = async () => {
  // Get the current user
  const currentUser = auth.currentUser;

  if (currentUser) {
    userId.value = currentUser.uid;

    // Fetch user's company name from "user" collection
    const userDoc = await getDoc(doc(db, "users", userId.value));
    if (userDoc.exists()) {
      const userData = userDoc.data();
      companyName.value = userData.companyName; // Set the companyName to display in the UI

      // Check if the user's document exists in "supplierListing" using userId as document ID
      const supplierDocRef = doc(db, "supplierListing", userId.value);
      const supplierDoc = await getDoc(supplierDocRef);

      if (!supplierDoc.exists()) {
        // Create a new supplier document using userId as document ID
        await setDoc(supplierDocRef, {
          supplierName: companyName.value, // Store company name in the supplier document
          inventory: []
        });
        console.log('Supplier document created for user:', currentUser.uid);
      } else {
        // If it exists, fetch the supplier's inventory
        supplierDocId.value = supplierDoc.id;
        const supplierData = supplierDoc.data();
        inventoryData.value = supplierData.inventory;
      }
    } else {
      console.error("User document not found!");
    }
  }
};

// Navigate to form page for adding products
const navigateToFormPage = () => {
  router.push({ name: 'addIngredientForm' });
};

// Open edit form for selected item
const editItem = (item) => {
  selectedItem.value = item; // Set the selected item
  editedProductName.value = item.productName; // Prepopulate the fields
  editedQuantity.value = item.quantity;
  editedUnit.value = item.unit;
  editedPricePerUnit.value = item.pricePerUnit;
  editedCategory.value = item.category; // Prepopulate the category
  isEditing.value = true; // Show the edit dialog
};

// Save the edited changes
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
          category: editedCategory.value // Update the category
        }
        : inventoryItem
    );

    // Update Firestore with the new inventory data
    await updateDoc(supplierRef, { inventory: updatedInventory });

    // Update the local inventory to reflect the changes
    inventoryData.value = updatedInventory;
    isEditing.value = false; // Hide the edit dialog after saving
    console.log('Item updated successfully');
  } catch (error) {
    console.error('Error updating item:', error);
  }
};

// Delete function to remove the item from Firebase
const deleteItem = async (item) => {
  try {
    const supplierRef = doc(db, "supplierListing", supplierDocId.value);

    // Filter out the item to delete based on a unique identifier (like productName)
    const newInventory = inventoryData.value.filter(inventoryItem => inventoryItem.productName !== item.productName);

    // Update the Firestore document with the new inventory array
    await updateDoc(supplierRef, {
      inventory: newInventory
    });

    // Update local inventory data to reflect the changes
    inventoryData.value = newInventory;
    console.log('Item deleted successfully');
  } catch (error) {
    console.error('Error deleting item:', error);
  }
};

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
          <!-- Company Name from user collection -->
          <h2 class="text-xl font-semibold">
            {{ companyName }}
          </h2>

          <!-- Search Bar and Add Product Button -->
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
          <div class="flex items-center">
            <TabsList>
              <TabsTrigger value="all">All</TabsTrigger>
            </TabsList>
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
                      <TableHead>Product Name</TableHead>
                      <TableHead>Quantity</TableHead>
                      <TableHead>Unit</TableHead>
                      <TableHead>Price per Unit</TableHead>
                      <TableHead>Category</TableHead>
                      <TableHead><span class="sr-only">Actions</span></TableHead>
                    </TableRow>
                  </TableHeader>

                  <TableBody>
                    <TableRow v-for="item in inventoryData" :key="item.productName">
                      <TableCell>{{ item.productName }}</TableCell>
                      <TableCell>{{ item.quantity }}</TableCell>
                      <TableCell>{{ item.unit }}</TableCell>
                      <TableCell>{{ "$" + parseFloat(item.pricePerUnit).toFixed(2) }}</TableCell>
                      <TableCell>{{ item.category }}</TableCell>
                      <TableCell class="flex justify-end gap-2">
                        <!-- Buttons aligned to the right using flex and justify-end -->
                        <Dialog>
                          <DialogTrigger as-child>
                            <Button variant="secondary" @click="editItem(item)">Edit</Button>
                          </DialogTrigger>
                          <DialogContent class="sm:max-w-[425px]">
                            <DialogHeader>
                              <DialogTitle>Edit Ingredient</DialogTitle>
                              <DialogDescription>
                                Make changes to the ingredient. Click save when you're done.
                              </DialogDescription>
                            </DialogHeader>
                            <div class="space-y-4">
                              <Input v-model="editedProductName" placeholder="Product Name" />
                              <Input v-model="editedQuantity" type="number" placeholder="Quantity" />
                              <Input v-model="editedUnit" placeholder="Unit" />
                              <Input v-model="editedPricePerUnit" type="number" step="0.01" placeholder="Price per Unit" />
                              <!-- Dropdown for editing category -->
                              <select v-model="editedCategory" class="w-full p-2 border border-gray-300 rounded-md">
                                <option value="" disabled>Select Category</option>
                                <option v-for="category in categories" :key="category" :value="category">{{ category }}</option>
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

