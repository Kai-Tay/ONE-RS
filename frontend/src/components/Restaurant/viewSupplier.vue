<script setup>
import { loadStripe } from '@stripe/stripe-js';
import axios from 'axios';
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import {
    Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle,
} from '@/components/ui/card'
import {
    Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from '@/components/ui/table'
import { doc, getDoc, getDocs, collection, setDoc, updateDoc } from "firebase/firestore";
import { db } from '../../firebase.js';
import { useRoute } from 'vue-router';
import { Stepper, StepperDescription, StepperIndicator, StepperItem, StepperSeparator, StepperTitle, StepperTrigger, } from '@/components/ui/stepper'
import { Dialog, DialogHeader, DialogContent, DialogTitle, DialogDescription, DialogClose, DialogFooter } from '@/components/ui/dialog';
</script>

<template>
    <!-- Filter Bar from Search -->

    <div class="mt-5 mb-5 mx-5 space-y-10">
        <div class="text-4xl font-bold h-10">{{ supplierListing.supplierName }}</div>
    </div>

    <div class="sm:flex justify-center my-10 hidden ">
        <Stepper v-model="activeStep">
            <StepperItem v-for="item in steps" :key="item.step" class="" :step="item.step">
                <StepperTrigger @click="goToStep(item.step)">
                    <StepperIndicator>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                            stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round" :d="item.iconValue" />
                        </svg>

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
                    <CardTitle>
                        <div class="text-2xl">Company Description</div>
                    </CardTitle>
                    <CardDescription class="text-lg mt-4">{{ supplierListing.supplierDescription }}</CardDescription>
                </CardHeader>
                <CardHeader>
                    <CardTitle>
                        <div class="text-2xl">Company Address</div>
                    </CardTitle>
                    <CardDescription class="text-lg mt-4">{{ supplierListing.supplierAddress }}</CardDescription>
                </CardHeader>
                <CardHeader>
                    <CardTitle>
                        <div class="text-2xl">Company Number</div>
                    </CardTitle>
                    <CardDescription class="text-lg mt-4">{{ supplierListing.supplierNumber }}</CardDescription>
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
                                <TableHead class="w-[100px]">
                                    <!-- Placeholder Image Header -->
                                    <span class="sr-only">Image</span>
                                </TableHead>
                                <TableHead>
                                    Name
                                </TableHead>
                                <TableHead class="w-[150px]">Category</TableHead>
                                <TableHead class="w-[150px]">Sub Category</TableHead>
                                <TableHead class="w-[100px]">Stock</TableHead>
                                <TableHead class="w-[150px]">Qty /Kg</TableHead>
                                <TableHead class="w-[150px]">Price Per Unit</TableHead>
                                <TableHead class="w-[100px]">
                                    Quantity
                                </TableHead>
                            </TableRow>
                        </TableHeader>
                        <!-- For Loop Here -->
                        <TableBody v-for="(item, index) in supplierListing.inventory" :key="item.id">
                            <TableRow>
                                <TableCell class="flex items-center justify-center">
                                    <img :src="item.imageData || './images/placeholder.svg'" alt="Product Image"
                                        class="w-12 h-12 object-cover rounded-md">
                                </TableCell>
                                <TableCell class="font-semibold">
                                    {{ item.productName }}
                                </TableCell>
                                <TableCell>
                                    {{ item.category }}
                                </TableCell>
                                <TableCell>
                                    {{ item.subcategory }}
                                </TableCell>
                                <TableCell>
                                    <Label :for="`stock-${index}`" class="sr-only">
                                        Stock
                                    </Label>
                                    {{ item.quantity }}
                                </TableCell>
                                <TableCell>
                                    <Label :for="`unit-${index}`" class="sr-only">
                                        Unit
                                    </Label>
                                    {{ item.unit }} kg
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
                                    <Input :id="`qty-${index}`" type="number" default-value="" min="1"
                                        :max="item.quantity" v-model="item.purchaseQuantity" />
                                </TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    </div>
    <div v-else-if="activeStep === 2">
        <!-- Checkout -->
        <div class="grid grid-cols-1 gap-4 mx-5">
            <Card>
                <CardHeader>
                    <CardTitle>Checkout</CardTitle>
                    <CardDescription>
                        View Your Purchase
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead class="w-[100px]">
                                    <!-- Placeholder Image Header -->
                                    <span class="sr-only">Image</span>
                                </TableHead>
                                <TableHead>
                                    Name
                                </TableHead>
                                <TableHead class="w-[200px]">Qty /Kg</TableHead>
                                <TableHead class="w-[200px]">Price Per Unit</TableHead>
                                <TableHead class="w-[200px]">Qty Purchasing</TableHead>
                                <TableHead class="">
                                    Sub Total
                                </TableHead>
                            </TableRow>
                        </TableHeader>
                        <!-- For Loop Here -->
                        <TableBody v-for="(item, index) in orderCart" :key="item.id">
                            <TableRow>
                                <TableCell class="flex items-center justify-center">
                                    <img :src="item.imageData || './images/placeholder.svg'" alt="Product Image"
                                        class="w-12 h-12 object-cover rounded-md">
                                </TableCell>
                                <TableCell class="font-semibold">
                                    {{ item.productName }}
                                </TableCell>
                                <TableCell class="font-semibold">
                                    {{ item.unit }} kg
                                </TableCell>
                                <TableCell>
                                    <Label class="sr-only">
                                        Price
                                    </Label>
                                    ${{ item.pricePerUnit }}
                                </TableCell>
                                <TableCell>
                                    <Label class="sr-only">
                                        Purchase Quantity
                                    </Label>
                                    {{ item.purchaseQuantity }}
                                </TableCell>
                                <TableCell>
                                    <Label class="sr-only">
                                        Sub Total
                                    </Label>
                                    ${{ item.pricePerUnit * item.purchaseQuantity }}
                                </TableCell>
                            </TableRow>
                        </TableBody>
                        <TableBody>
                            <!-- Total Amount -->
                            <TableRow>
                                <TableCell class="font-semibold">
                                    Total
                                </TableCell>
                                <TableCell></TableCell>
                                <TableCell></TableCell>
                                <TableCell></TableCell>
                                <TableCell>
                                    ${{ orderCart.reduce((acc, item) => acc + (item.pricePerUnit *
                                        item.purchaseQuantity), 0) }}
                                </TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    </div>
    <div v-else-if="activeStep === 3">
        <!-- Confirm User Address -->
        <div class="grid grid-cols-1 gap-4 mx-5">
            <Card>
                <CardHeader>
                    <CardTitle>Delivery Information</CardTitle>
                    <CardDescription>
                        Confirm your delivery address
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div class="flex flex-col space-y-4">
                        <Label for="address" class="font-semibold">Address</Label>
                        <Input id="address" type="text" v-model="restaurantAddress" />
                        <Label for="phone" class="font-semibold">Phone Number</Label>
                        <Input id="phone" type="number" placeholder="6512345678" v-model="restaurantPhoneNumber" />
                    </div>
                </CardContent>
            </Card>
        </div>
    </div>

    <div v-else-if="activeStep === 4">
        <div class="grid grid-cols-1 gap-4 mx-5">
            <Card>
                <CardHeader>
                    <CardTitle class="text-2xl font-bold">Order Details</CardTitle>
                </CardHeader>
                <CardContent>
                    <div v-for="item in orderCart" class="flex justify-between py-2 border-b">
                        <div>
                            <p class="font-semibold">{{ item.productName }}</p>
                            <p class="text-sm text-gray-500">{{ item.category }} - {{ item.subcategory }}</p>
                            <p class="text-sm text-gray-500">Quantity: {{ item.purchaseQuantity }}</p>
                        </div>
                        <div class="text-right">
                            <p class="font-semibold">${{ item.pricePerUnit.toFixed(2) }}</p>
                            <p class="text-sm text-gray-500">Total: ${{ (item.pricePerUnit *
                                item.purchaseQuantity).toFixed(2) }}</p>
                        </div>
                    </div>
                    <div class="mt-4 flex justify-between">
                        <p class="font-semibold">Total Amount</p>
                        <p class="font-bold">${{ orderAmount.toFixed(2) }}</p>
                    </div>
                </CardContent>
            </Card>
            <Card>
                <CardHeader>
                    <CardTitle>Stripe Checkout</CardTitle>
                    <CardDescription>
                        Complete your Purchase
                    </CardDescription>
                </CardHeader>
                <CardContent class="py-6 ">
                    <form @submit.prevent="handlePayment">
                        <div id="checkout-form"><!-- Stripe card element will be mounted here --></div>
                        <Button id="submit" class="w-full mt-10" @click="nextStep">
                            <div class="spinner hidden" id="spinner"></div>
                            <span id="button-text">Pay ${{ orderAmount.toFixed(2) }}</span>
                        </Button>
                    </form>
                </CardContent>
            </Card>
            <div v-if="errorMessage" class="error">{{ errorMessage }}</div>
        </div>
    </div>



    <div class="flex flex-inline justify-center my-4 space-x-20">
        <Button @click="previousStep" variant="grey">Previous</Button>
        <Button @click="nextStep" v-if="activeStep !== 4">{{ buttonText }}</Button>
    </div>

    <Dialog :open="showDialog">
        <DialogContent>
            <DialogHeader>
                <DialogTitle class="tw-text-xl">{{ status }}</DialogTitle>
            </DialogHeader>
            <DialogDescription>
                {{ description }}
            </DialogDescription>
            <DialogFooter class="sm:justify-start">
                <DialogClose as-child>
                    <Button type="button" variant="secondary" @click="closeDialog">
                        Close
                    </Button>
                </DialogClose>
            </DialogFooter>
        </DialogContent>
    </Dialog>

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
                iconValue: "M15.75 10.5V6a3.75 3.75 0 1 0-7.5 0v4.5m11.356-1.993 1.263 12c.07.665-.45 1.243-1.119 1.243H4.25a1.125 1.125 0 0 1-1.12-1.243l1.264-12A1.125 1.125 0 0 1 5.513 7.5h12.974c.576 0 1.059.435 1.119 1.007ZM8.625 10.5a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Zm7.5 0a.375.375 0 1 1-.75 0 .375.375 0 0 1 .75 0Z",
            }, {
                step: 2,
                title: 'Checkout',
                description: 'Confirm your Order',
                iconValue: "M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 0 0-3 3h15.75m-12.75-3h11.218c1.121-2.3 2.1-4.684 2.924-7.138a60.114 60.114 0 0 0-16.536-1.84M7.5 14.25 5.106 5.272M6 20.25a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Zm12.75 0a.75.75 0 1 1-1.5 0 .75.75 0 0 1 1.5 0Z",
            }, {
                step: 3,
                title: 'Delivery Information',
                description: 'Provide delivery information',
                iconValue: "M8.25 18.75a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m3 0h6m-9 0H3.375a1.125 1.125 0 0 1-1.125-1.125V14.25m17.25 4.5a1.5 1.5 0 0 1-3 0m3 0a1.5 1.5 0 0 0-3 0m3 0h1.125c.621 0 1.129-.504 1.09-1.124a17.902 17.902 0 0 0-3.213-9.193 2.056 2.056 0 0 0-1.58-.86H14.25M16.5 18.75h-2.25m0-11.177v-.958c0-.568-.422-1.048-.987-1.106a48.554 48.554 0 0 0-10.026 0 1.106 1.106 0 0 0-.987 1.106v7.635m12-6.677v6.677m0 4.5v-4.5m0 0h-12",
            }, {
                step: 4,
                title: 'Payment',
                description: 'Pay for your order',
                iconValue: "M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 0 0 2.25-2.25V6.75A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25v10.5A2.25 2.25 0 0 0 4.5 19.5Z",
            }],

            supplierId: "",
            supplierListing: {},
            userInfo: {},

            // Dialog stuff
            showDialog: false,
            status: "",
            description: "",

            restaurantPhoneNumber: "",
            restaurantAddress: "",

            // Stripe
            elements: null,
            errorMessage: "",
            stripe: null,
        };
    },
    computed: {
        // Get all the inventory listings with purchase Quantity more than 1 from supplierListing
        orderCart() {
            return this.supplierListing.inventory.filter(item => item.purchaseQuantity > 0);
        },
        buttonText() {
            // Return different text based on the active step
            switch (this.activeStep) {
                case 1:
                    return "Checkout";
                case 2:
                    return "Continue";
                case 3:
                    return "Make Payment";
                case 4:
                    return "Complete Order";
                default:
                    return "Next";
            }
        },
        orderAmount() {
            return this.orderCart.reduce((acc, item) => acc + (item.pricePerUnit * item.purchaseQuantity), 0)
        }
    },
    watch: {
        // Watch each item’s purchaseQuantity in inventory
        'supplierListing.inventory': {
            handler(inventory) {
                inventory.forEach(item => {
                    if (item.purchaseQuantity > item.quantity) {
                        item.purchaseQuantity = item.quantity; // Reset to max stock if exceeded
                    }
                });
            },
            deep: true
        }
    },
    methods: {
        // Stepper Methods
        goToStep(index) {
            if (this.activeStep == 2) {
                // Check if there are items in the cart
                if (this.orderCart.length > 0) {
                    this.activeStep = index;
                } else {
                    this.status = "No Items Selected";
                    this.description = "Please select at least one item to proceed";
                    this.showDialog = true;
                    this.activeStep = 1;
                }
            } else if (this.activeStep == 4) {
                // Check if address is filled
                if (this.restaurantAddress == "" || this.restaurantPhoneNumber == "") {
                    this.status = "No Address/Phone Number Provided";
                    this.description = "Please provide an address/phone number to proceed";
                    this.showDialog = true;
                    this.activeStep = 3;
                } else {
                    this.createPayment();
                    this.activeStep = index;
                }
            }
            else {
                this.activeStep = index;
            }
        },
        nextStep() {

            if (this.activeStep == 1) {
                // Check if there are items in the cart
                if (this.orderCart.length > 0) {
                    this.activeStep++;
                } else {
                    this.status = "No Items Selected";
                    this.description = "Please select at least one item to proceed";
                    this.showDialog = true;
                }
            } else if (this.activeStep == 3) {
                // Check if address is filled
                if (this.restaurantAddress == "" || this.restaurantPhoneNumber == "") {
                    this.status = "No Address/Phone Number Provided";
                    this.description = "Please provide an address/phone number to proceed";
                    this.showDialog = true;
                } else {
                    this.createPayment();
                    this.activeStep++;
                }
            } else if (this.activeStep == 4) {
                // Call the payment function
                this.completePayment();
            }
            else
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

        // Close Dialog
        closeDialog() {
            this.showDialog = false;
            if (this.status == "Order Confirmed") {
                this.$router.push("/buyerOrders");
            }
            if (this.status == "Inventory not Updated") {
                this.$router.push("/buyerdashboard");
            }
        },

        // Database Methods
        // Fetch the supplier listing from the database
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
                    supplierDescription: userSnap.data().companyDescription,
                    supplierAddress: userSnap.data().companyAddress,
                    supplierNumber: userSnap.data().companyNumber,
                };

                // Add quantity key to each inventory item
                mergedData.inventory = mergedData.inventory.map(item => ({
                    ...item,
                    purchaseQuantity: 0
                }));

                this.supplierListing = mergedData;

            } catch (error) {
                console.error('Error fetching listings:', error)
            }
        },

        // Fetch User Data
        async fetchUser() {
            // Fetch the user
            const userRef = doc(db, "users", sessionStorage.getItem("uid"));
            const userSnap = await getDoc(userRef);

            // User info
            this.userInfo = userSnap.data();

            // Add Address to restaurantAddress
            this.restaurantAddress = this.userInfo.companyAddress;

            // Add Phone Number to restaurantPhoneNumber
            this.restaurantPhoneNumber = this.userInfo.companyNumber;
            console.log(this.userInfo);
        },
        async createPayment() {
            try {
                // Calculate the total amount in cents (multiply by 100 for Stripe's format)
                const amountInCents = this.orderCart.reduce((acc, item) => acc + (item.pricePerUnit * item.purchaseQuantity * 100), 0);

                // Make Axios POST request to backend to create PaymentIntent
                const response = await axios.post("http://54.169.182.213//create-checkout", {
                    amount: amountInCents
                });

                // Get the clientSecret from the response
                this.clientSecret = response.data.clientSecret;

                // Initialize Stripe
                this.stripe = await loadStripe('pk_test_51QHnfFELG51EPCRqyoGXIJ4L3B1Y7HAk0L6Gc1qo9Mn4MUkz3DiffFQzgTV2gCU3xxu3pLTkMFJ05WgcCNkmX3N900l2hWpuqe'); // Replace with your Stripe publishable key

                const appearance = {
                    theme: 'stripe',
                };

                this.elements = this.stripe.elements({ appearance, clientSecret: this.clientSecret },);

                const paymentElementOptions = {
                    layout: "tabs",
                    business: {
                        name: "ONE.RS"
                    },
                };

                const paymentElement = this.elements.create("payment", paymentElementOptions);

                // Mount the checkout form to the page
                paymentElement.mount('#checkout-form');

            } catch (error) {
                console.error("Error during payment process:", error);
                this.errorMessage = error.message || 'An error occurred during the payment process.';
            }

        },
        async completePayment() {

            const { error, paymentIntent } = await this.stripe.confirmPayment({
                elements: this.elements,
                confirmParams: {
                    return_url: "http://localhost:5173/#",
                },
                redirect: 'if_required',
            });

            // Handle errors or success messages
            if (error) {
                if (error.type === "card_error" || error.type === "validation_error") {
                    message.value = error.message;
                } else {
                    message.value = "An unexpected error occurred.";
                }
            }

            // If payment succeeds, add order to Firebase

            if (paymentIntent && paymentIntent.status === "succeeded") {
                await this.handleConfirmedOrder();
            }

        },

        async handleConfirmedOrder() {
            try {
                // UPDATE SUPPLIERLISTING DATABASE
                // Fetch the supplier listing
                const listingRef = doc(db, "supplierListing", this.supplierId);

                const updateQuantity = this.supplierListing.inventory.map(listingItem => {

                    this.orderCart.map(orderItem => {
                        if (listingItem.productName == orderItem.productName) {
                            listingItem.quantity -= orderItem.purchaseQuantity;
                        }
                    });
                    console.log(listingItem)
                    return listingItem;
                });

                console.log(updateQuantity);
                // Send data to database
                await updateDoc(listingRef, {
                    inventory: updateQuantity,
                });


                // UPDATE ORDERHISTORY DATABASE
                // Get length of orderHistory database
                const querySnapshot = await getDocs(collection(db, "orderHistory"));
                const length = querySnapshot.size;

                // Updated orderHistory database and give a order id based on the number of items in the database
                const orderRef = doc(db, "orderHistory", length.toString());
                const orderSnapshot = await getDoc(orderRef);

                // Create order data

                const orderData = {
                    orderID: length.toString(),
                    date: new Date(),
                    paymentStatus: "Paid",
                    buyerID: sessionStorage.getItem("uid"),
                    supplierID: this.supplierId,
                    orderedItems: this.orderCart,
                    totalPrice: this.orderCart.reduce((acc, item) => acc + (item.pricePerUnit * item.purchaseQuantity), 0),
                    address: this.restaurantAddress,
                    phoneNumber: this.restaurantPhoneNumber,
                };

                await setDoc(orderRef, orderData).then(() => {
                    this.status = "Order Confirmed";
                    this.description = "Your order has been confirmed. Please wait for the supplier to contact you.";
                    this.showDialog = true;
                })

            } catch (error) {
                alert('Error updating listings:', error)
            }
            // UPDATE INVENTORYLISTING DATABASE
            this.updateInventoryLevels();

        },
        async checkInventoryLevels() {
            // Fetch the inventory listing and retrieve the latest month documet YYYY-MM-number
            const inventoryRef = doc(db, "inventoryLevels", sessionStorage.getItem("uid"));

            //Check if the latest document last number is a 4 
            const inventorySnapshot = await getDoc(inventoryRef);
            const inventoryData = inventorySnapshot.data().currentInventoryLevel;

            // Sort document keys by YYYY-MM-HighestNumber
            const sortedKeys = Object.keys(inventoryData)
                .sort((a, b) => {
                    // Split each key into [YYYY, MM, Number]
                    const [yearA, monthA, numberA] = a.split('-').map(Number);
                    const [yearB, monthB, numberB] = b.split('-').map(Number);

                    // Sort by year, then month, then number
                    return yearB - yearA || monthB - monthA || numberB - numberA;
                });

            // Retrieve the latest document key
            const docTitle = sortedKeys[0];

            // Check if month is currentMonth
            const currentMonth = new Date().getMonth() + 1;

            // Check if currentMonth is correct month
            if (docTitle.split("-")[1] != currentMonth) {
                this.status = "Inventory not Updated";
                this.description = "Please update inventory to latest month!";
                this.showDialog = true;
            }
        },
        async updateInventoryLevels() {
            // Fetch the inventory listing and retrieve the latest month documet YYYY-MM-number
            const inventoryRef = doc(db, "inventoryLevels", sessionStorage.getItem("uid"));

            //Check if the latest document last number is a 4 
            const inventorySnapshot = await getDoc(inventoryRef);
            const inventoryData = inventorySnapshot.data().currentInventoryLevel;

            // Sort document keys by YYYY-MM-HighestNumber
            const sortedKeys = Object.keys(inventoryData)
                .sort((a, b) => {
                    // Split each key into [YYYY, MM, Number]
                    const [yearA, monthA, numberA] = a.split('-').map(Number);
                    const [yearB, monthB, numberB] = b.split('-').map(Number);

                    // Sort by year, then month, then number
                    return yearB - yearA || monthB - monthA || numberB - numberA;
                });

            // Retrieve the latest document key
            const docTitle = sortedKeys[0];

            console.log("Doc Title: ", docTitle);

            // Check if docTitle is not undefined
            if (docTitle) {
                const month = docTitle.split("-")[1];

                console.log("Month: ", month);
                // Check if its the 5th interval
                if (docTitle[docTitle.length - 1] === "5") {

                    // Consolidate orderHistory for past month
                    const orderHistoryRef = collection(db, "orderHistory");
                    const orderHistorySnapshot = await getDocs(orderHistoryRef);
                    const orderHistoryData = orderHistorySnapshot.docs.map(doc => doc.data());

                    // Filter out data from user for the month
                    const filteredOrderHistory = orderHistoryData.filter(order => {
                        const orderMonth = order.date.toDate().getMonth() + 1;
                        console.log(orderMonth, month);
                        return orderMonth == month && order.buyerID == sessionStorage.getItem("uid");
                    });
                    console.log("Filtered Order History: ", filteredOrderHistory);

                    // Calculate total qty based on {category: {subcategory:qty}}
                    const totalQty = filteredOrderHistory.reduce((acc, order) => {
                        order.orderedItems.forEach(item => {
                            //lower case all category and subcategory
                            item.category = item.category.toLowerCase();
                            item.subcategory = item.subcategory.toLowerCase();
                            if (acc[item.category]) {
                                if (acc[item.category][item.subcategory]) {
                                    acc[item.category][item.subcategory] += item.purchaseQuantity;
                                } else {
                                    acc[item.category][item.subcategory] = item.purchaseQuantity;
                                }
                            } else {
                                acc[item.category] = { [item.subcategory]: item.purchaseQuantity };
                            }
                        });
                        return acc;
                    }, {});

                    // Merge the inventory levels by adding totalQty to beforeOrder (if totalqty keys not in beforeOrder, add it)
                    const beforeOrder = JSON.parse(JSON.stringify(inventoryData[docTitle].beforeOrder));
                    console.log(inventoryData[docTitle].beforeOrder)
                    const mergedOrder = Object.keys(totalQty).reduce((acc, category) => {
                        // Initialize category if it doesn't exist
                        acc[category] = acc[category] || {};

                        Object.keys(totalQty[category]).forEach(subcategory => {
                            // Initialize subcategory if it doesn't exist
                            acc[category][subcategory] = (acc[category][subcategory] || 0) + totalQty[category][subcategory];
                        });

                        return acc;
                    }, { ...beforeOrder });  // Start with a copy of beforeOrder

                    console.log("Merged Order: ", mergedOrder);

                    // Update the inventory levels with afterOrder in inventoryData[docTitle]
                    const updatedInventoryData = {
                        ...inventoryData,
                        [docTitle]: {
                            beforeOrder: inventoryData[docTitle].beforeOrder,
                            afterOrder: mergedOrder,
                        }
                    };

                    // Send data to database
                    // await updateDoc(inventoryRef, {
                    //     currentInventoryLevel: updatedInventoryData,
                    // });

                    // Add categories to restaurant database
                    const restaurantRef = doc(db, "restaurant", sessionStorage.getItem("uid"));
                    const restaurantSnapshot = await getDoc(restaurantRef);
                    const restaurantData = restaurantSnapshot.data().inventoryTypes;

                    // Look into mergedOrder, check if category exists in restaurantData else add it
                    Object.keys(mergedOrder).forEach(category => {
                        if (!restaurantData[category]) {
                            restaurantData[category] = {};
                        }
                        Object.keys(mergedOrder[category]).forEach(subcategory => {
                            if (!restaurantData[category][subcategory]) {
                                restaurantData[category][subcategory] = 0;
                            }
                            restaurantData[category][subcategory] = 0;
                        });
                    });
                    console.log(restaurantData)

                    // Send data to database
                    await updateDoc(restaurantRef, {
                        inventoryTypes: restaurantData,
                    });
                }
            } else {
                console.log("No inventory data found");
            }
        },
    },
    mounted() {
        // Get the supplier ID from the URL
        const route = useRoute();
        this.supplierId = route.params.id;

        // Obtain Database Suppliers
        this.fetchListing();

        // Obtain User Info
        this.fetchUser();


        // TESTING
        // Check Inventory Levels if is in current month...
        // this.checkInventoryLevels();

        // this.updateInventoryLevels();

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