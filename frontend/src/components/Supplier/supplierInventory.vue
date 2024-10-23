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

import Navbar from '../Navbar.vue';
import { ref, onMounted } from 'vue'
import { getFirestore, collection, getDocs, doc, getDoc, setDoc, updateDoc } from 'firebase/firestore';
import { useRouter } from 'vue-router'; 
import { auth } from '../../firebase.js'; // Assuming you have auth initialized

// Initialize Firebase Firestore
const db = getFirestore();
const router = useRouter(); 

// Reactive variables to store fetched data
const inventoryData = ref([]); // Holds the list of inventory items
const supplierName = ref('');  // Holds the supplier name (company name)
const supplierDocId = ref(''); // Holds supplier document ID for updates
const userId = ref(''); // Holds current user's ID

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
      const companyName = userData.companyName;

      supplierName.value = companyName;

      // Check if the company already exists in "supplierListing"
      const supplierDocRef = doc(db, "supplierListing", companyName);
      const supplierDoc = await getDoc(supplierDocRef);

      if (!supplierDoc.exists()) {
        // Create a new supplier document if it doesn't exist
        await setDoc(supplierDocRef, {
          supplierName: companyName,
          inventory: []
        });
        console.log('Supplier document created for company:', companyName);
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

// Edit function (stub for future functionality)
const editItem = (item) => {
  console.log('Editing item:', item);
  
};

// Delete function to remove the item from Firebase
const deleteItem = async (item) => {
  try {
    const supplierRef = doc(db, "supplierListing", supplierDocId.value);
    const newInventory = inventoryData.value.filter((inventoryItem) => inventoryItem.index !== item.index);

    await updateDoc(supplierRef, {
      inventory: newInventory.map((i) => ({
        productName: i.productName,
        pricePerUnit: i.pricePerUnit,
        quantity: i.quantity,
        unit: i.unit,
      }))
    });

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
  <Navbar />
  <div class="flex min-h-screen w-full flex-col bg-muted/40">
    <div class="flex flex-col sm:gap-4 sm:py-4 sm:pl-14">
      <header
        class="sticky top-0 z-30 flex h-14 items-center gap-4 border-b bg-background px-4 sm:static sm:h-auto sm:border-0 sm:bg-transparent sm:px-6">
        <div class="flex w-full items-center justify-between">
          <!-- Supplier (Company) Name -->
          <h2 class="text-xl font-semibold">
            {{ supplierName }}
          </h2>

          <!-- Search Bar and Add Product Button -->
          <div class="flex items-center gap-2">
            <div class="relative w-full md:w-[200px] lg:w-[320px]">
              <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
              <Input type="search" placeholder="Search..." class="w-full rounded-lg bg-background pl-8" />
            </div>

            <Button @click="navigateToFormPage" size="sm" class="h-7 gap-1">
              <PlusCircle class="h-3.5 w-3.5" />
              <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
                Add Product
              </span>
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

            <div class="ml-auto flex items-center gap-2">
              <DropdownMenu>
                <DropdownMenuTrigger as-child>
                  <Button variant="outline" size="sm" class="h-7 gap-1">
                    <ListFilter class="h-3.5 w-3.5" />
                    <span class="sr-only sm:not-sr-only sm:whitespace-nowrap">
                      Filter
                    </span>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuLabel>Filter by</DropdownMenuLabel>
                  <DropdownMenuSeparator />
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>

          <TabsContent value="all">
            <Card>
              <CardHeader>
                <CardTitle>Inventory</CardTitle>
                <CardDescription>
                  Manage your products.
                </CardDescription>
              </CardHeader>

              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Product Name</TableHead>
                      <TableHead>Quantity</TableHead>
                      <TableHead>Unit</TableHead>
                      <TableHead>Price per Unit</TableHead>
                      <TableHead><span class="sr-only">Actions</span></TableHead>
                    </TableRow>
                  </TableHeader>

                  <TableBody>
                    <TableRow v-for="item in inventoryData" :key="item.index">
                      <TableCell>{{ item.productName }}</TableCell>
                      <TableCell>{{ item.quantity }}</TableCell>
                      <TableCell>{{ item.unit }}</TableCell>
                      <TableCell>{{ item.pricePerUnit }}</TableCell>
                      <TableCell>
                        <DropdownMenu>
                          <DropdownMenuTrigger class="text-indigo-600 hover:text-indigo-900 focus:outline-none">
                            Options
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuLabel>Actions</DropdownMenuLabel>
                            <DropdownMenuItem @click="editItem(item)">Edit</DropdownMenuItem>
                            <DropdownMenuItem @click="deleteItem(item)">Delete</DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </CardContent>

              <CardFooter>
                <div class="text-xs text-muted-foreground">
                  Showing all products
                </div>
              </CardFooter>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  </div>
</template>
