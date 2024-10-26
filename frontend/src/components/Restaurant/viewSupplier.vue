<script setup>
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import {
    Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle,
} from '@/components/ui/card'
import {
    Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from '@/components/ui/table'
import { doc, getDoc } from "firebase/firestore";
import { db } from '../../firebase.js';
import { useRoute } from 'vue-router';
</script>

<template>
    <header class="bg-gray-900 py-5 h-80 justify-center">
        <div class="px-5 row gx-5 justify-center">
            <div class="col-lg-6">
                <div class="text-center my-10 ">
                    <!-- Welcome Text -->
                    <div class="text-4xl font-bold">
                        <h1 class="display-5 fw-bolder text-white mb-2">Find Suppliers</h1>
                    </div>
                </div>
            </div>
        </div>
    </header>


    <!-- Filter Bar from Search -->

    <div class="mt-5 mb-5 mx-5">
        <div class="text-4xl font-bold h-10">{{ supplierListing.supplierName }}</div>
    </div>

    <!-- Listings -->
    <div class="grid grid-cols-1 gap-4 mx-5">
        <Card>
            <CardHeader>
                <CardTitle>
                    <div class="text-2xl">Company Description</div>
                </CardTitle>
                <CardDescription class="text-lg mt-4">{{ supplierListing.supplierDescription }}</CardDescription>
            </CardHeader>
        </Card>

        <Card>
            <CardHeader>
                <CardTitle>Inventory</CardTitle>
                <CardDescription>
                    Select your items
                </CardDescription>
            </CardHeader>
            <CardContent>
                <Table>
                    <TableHeader>
                        <TableRow>
                            <TableHead >
                                Name
                            </TableHead>
                            <TableHead class="w-[100px]">Stock</TableHead>
                            <TableHead class="w-[200px]">Price Per Unit</TableHead>
                            <TableHead class="">
                                Quantity
                            </TableHead>
                        </TableRow>
                    </TableHeader>
                    <!-- For Loop Here -->
                    <TableBody v-for="item in supplierListing.inventory">
                        <TableRow>
                            <TableCell class="font-semibold">
                                {{ item.productName }}
                            </TableCell>
                            <TableCell>
                                <Label for="stock-1" class="sr-only">
                                    Stock
                                </Label>
                                {{ item.quantity }}
                            </TableCell>
                            <TableCell>
                                <Label for="price-1" class="sr-only">
                                    Price
                                </Label>
                                ${{  item.pricePerUnit }}   
                            </TableCell>
                            <TableCell>
                                <Label for="price-1" class="sr-only">
                                    Qty
                                </Label>
                                <Input id="price-1" type="number" default-value="0" min="0" :max="item.quantity"/>
                            </TableCell>
                        </TableRow>
                    </TableBody>
                </Table>
            </CardContent>
        </Card>
    </div>



</template>

<script>


export default {
    name: 'ViewSupplier',
    components: {},

    data() {
        return {
            supplierId: "",
            supplierListing: {},
        };
    },
    mounted() {
        const route = useRoute();
        this.supplierId = route.params.id;
        // Obtain Database Suppliers
        this.fetchListing();
    },

    methods: {
        async fetchListing() {
            // Fetch listings from the database supplierListing and users
            try {
                // Fetch the supplier listing
                const listingRef = doc(db, "supplierListing", this.supplierId);
                const listingSnap = await getDoc(listingRef);

                // Fetch the user
                const userRef = doc(db, "users", this.supplierId);
                const userSnap = await getDoc(userRef);

                // Combine the data
                const mergedData = {
                    ...listingSnap.data(), // Spread listing data
                    supplierDescription: userSnap.data().companyDescription  // Spread company data
                };

                this.supplierListing = mergedData;

            } catch (error) {
                console.error('Error fetching listings:', error)
            }
        },
    },
};
</script>

<style>
.searchInput {
    width: 100%;
    height: 50px;
    border-radius: 20px;
    border: 1px solid #000;
    padding: 0 20px;
    font-size: 16px;
    outline: none;
    transition: all 0.3s;
}
</style>