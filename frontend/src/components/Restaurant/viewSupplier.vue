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
import { Stepper, StepperDescription, StepperIndicator, StepperItem, StepperSeparator, StepperTitle, StepperTrigger, } from '@/components/ui/stepper'
</script>

<template>
    <!-- Filter Bar from Search -->

    <div class="mt-5 mb-5 mx-5 space-y-10">
        <div class="text-4xl font-bold h-10">{{ supplierListing.supplierName }}</div>
        <Card>
            <CardHeader>
                <CardTitle>
                    <div class="text-2xl">Company Description</div>
                </CardTitle>
                <CardDescription class="text-lg mt-4">{{ supplierListing.supplierDescription }}</CardDescription>
            </CardHeader>
        </Card>
    </div>


    <div class="sm:flex justify-center my-10 hidden ">
        <Stepper v-model="activeStep">
            <StepperItem v-for="item in steps" :key="item.step" class="" :step="item.step">
                <StepperTrigger @click="goToStep(item.step)">
                    <StepperIndicator>
                        <component :is="item.icon" class="w-4 h-4" />
                    </StepperIndicator>
                    <div class="flex flex-col">
                        <StepperTitle>
                            {{ item.title }}
                        </StepperTitle>
                        <StepperDescription>
                            {{ item.description }}
                        </StepperDescription>
                    </div>
                </StepperTrigger>
            </StepperItem>
        </Stepper>
    </div>

    <!-- Step Content Based on Active Step -->
    <div v-if="activeStep === 1">
        <!-- Listings -->
        <div class="grid grid-cols-1 gap-4 mx-5">
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
                                <TableHead>
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
                        <TableBody v-for="(item, index) in supplierListing.inventory" :key="item.id">
                            <TableRow>
                                <TableCell class="font-semibold">
                                    {{ item.productName }}
                                </TableCell>
                                <TableCell>
                                    <Label :for="`stock-${index}`" class="sr-only">
                                        Stock
                                    </Label>
                                    {{ item.quantity }}
                                </TableCell>
                                <TableCell>
                                    <Label :for="`price-${index}`" class="sr-only">
                                        Price
                                    </Label>
                                    ${{ item.pricePerUnit }}
                                </TableCell>
                                <TableCell>
                                    <Label :for="`qty-${index}`" class="sr-only">
                                        Qty
                                    </Label>
                                    <Input :id="`qty-${index}`" type="number" default-value="" min="1" :max="item.quantity" />
                                </TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    </div>
    <div v-else-if="activeStep === 2">
        <p>Content for Step 2</p>
    </div>
    <div v-else-if="activeStep === 3">
        <p>Content for Step 3</p>
    </div>



    <div class="flex flex-inline justify-center my-4 space-x-20">
        <Button @click="previousStep" variant="grey">Previous</Button>
        <Button @click="nextStep" :disabled="activeStep === steps.length">Continue</Button>
    </div>

</template>

<script>


export default {
    name: 'ViewSupplier',
    components: {},

    data() {
        return {
            //Stepper
            activeStep: 1,
            steps: [{
                step: 1,
                title: 'Add to Cart',
                description: 'Select your items!',
                icon: null,
            }, {
                step: 2,
                title: 'Checkout',
                description: 'Confirm your Order',
                icon: null,
            }, {
                step: 3,
                title: 'Delivery Information',
                description: 'Provide delivery information',
                icon: null,
            }, {
                step: 4,
                title: 'Payment',
                description: 'Pay for your order',
                icon: null,
            }],
            supplierId: "",
            supplierListing: {},

            orderCart: {},
        };
    },
    mounted() {
        // Get the supplier ID from the URL
        const route = useRoute();
        this.supplierId = route.params.id;

        // Obtain Database Suppliers
        this.fetchListing();
    },

    methods: {
        // Stepper Methods
        goToStep(index) {
            this.activeStep = index;
        },
        nextStep() {
            if (this.activeStep == 1){
                this.handleInventoryQuantity();
            }
            if (this.activeStep < this.steps.length) {
                this.activeStep++;
            }
        },
        previousStep() {
            if (this.activeStep > 1) {
                this.activeStep--;
            } else {
                this.$router.push("/find");
            }
        },

        // Database Methods
        async fetchListing() {
            // Fetch listings from the database supplierListing and users
            try {
                // Fetch the supplier listing
                const listingRef = doc(db, "supplierListing", this.supplierId);
                const listingSnap = await getDoc(listingRef);

                // Fetch the user
                const userRef = doc(db, "users", this.supplierId);
                const userSnap = await getDoc(userRef);

                // Combine the data (Add company description from user database to merged data)
                const mergedData = {
                    ...listingSnap.data(),
                    supplierDescription: userSnap.data().companyDescription
                };

                this.supplierListing = mergedData;

            } catch (error) {
                console.error('Error fetching listings:', error)
            }
        },


        // On Qty Change
        handleInventoryQuantity() {
            // Get the qty values for each listing and update the orderCart
            const qtyInputs = document.querySelectorAll('input[type="number"]');
            console.log(qtyInputs);
        }
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