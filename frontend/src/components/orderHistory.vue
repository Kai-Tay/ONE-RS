<script setup>
import Navbar from './Navbar.vue';
import Chat from './chat.vue';
import { Table, TableBody, TableCell, TableHeader, TableHead, TableRow } from './ui/table';
import { Button } from './ui/button';
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from './ui/dropdown-menu';
import CardContent from './ui/card/CardContent.vue';
import Card from './ui/card/Card.vue';
import { collection, getDocs, getDoc, doc } from "firebase/firestore";
import { db } from '../firebase';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger, DialogClose } from '@/components/ui/dialog'
</script>

<template>
    <div class="container mx-auto px-8 my-5">
        <div class="flex items-center justify-between mb-6">
            <div>
                <h2 class="text-2xl font-bold">Order History</h2>
                <p class="text-sm">Manage your recent orders</p>
            </div>
        </div>


        <div>
            <!-- Restaurant Order History -->
            <Card>
                <CardContent>
                    <Table v-if="userType == 'restaurant'">
                        <TableHeader>
                            <TableRow>
                                <TableHead>Order ID</TableHead>
                                <!-- Add icon for date to toggle asc or desc -->
                                <TableHead>Items Purchased</TableHead>
                                <TableHead>Total Cost</TableHead>
                                <TableHead>Payment Status</TableHead>
                                <TableHead>Order Date</TableHead>
                                <TableHead></TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            <TableRow v-for="order in orderHistory">
                                <TableCell class="w-[100px]">{{ order.orderID }}</TableCell>
                                <TableCell>
                                    <div v-for="item in order.orderedItems">
                                        <p>{{ item.productName }} x {{ item.purchaseQuantity }}</p>
                                    </div>
                                </TableCell>
                                <TableCell>{{ order.totalPrice }}</TableCell>
                                <TableCell>{{ order.paymentStatus }}</TableCell>
                                <TableCell class="w-[300px]">{{ order.date.toDate() }}</TableCell>
                                <TableCell class="flex flex-inline space-x-4">
                                    <!-- View More details about listing -->
                                    <Dialog>
                                        <DialogTrigger as-child>
                                            <Button variant="outline">
                                                View Order
                                            </Button>
                                        </DialogTrigger>
                                        <DialogContent class="sm:max-w-[425px]">
                                            <DialogHeader>
                                                <DialogTitle class="text-2xl font-bold">Order Details</DialogTitle>
                                            </DialogHeader>
                                            <div class="grid gap-4 py-4 overflow-y-auto ">
                                                <div class="flex flex-col justify-between h-[50dvh] space-y-5">
                                                    <div>
                                                        <p class="font-bold">Order ID:</p>
                                                        <p>{{ order.orderID }}</p>
                                                    </div>
                                                    <div>
                                                        <p class="font-bold">Supplier Details:</p>
                                                        <p>{{ order.supplierName }}</p>
                                                        <p>{{ order.supplierAddress }}</p>
                                                    </div>
                                                    <div>
                                                        <p class="font-bold">Supplier Number:</p>
                                                        <p>{{ order.supplierNumber }}</p>
                                                    </div>
                                                    <div>
                                                        <p class="font-bold">Items Purchased:</p>
                                                        <div v-for="item in order.orderedItems" :key="item.productName"
                                                            class="my-2 p-2 border border-gray-300 rounded-lg">
                                                            <p><strong>Product Name:</strong> {{ item.productName }}</p>
                                                            <p><strong>Category:</strong> {{ item.category }}</p>
                                                            <p><strong>Subcategory:</strong> {{ item.subcategory }}</p>
                                                            <p><strong>Price per Unit:</strong> ${{ item.pricePerUnit }}
                                                            </p>
                                                            <p><strong>Quantity:</strong> {{ item.purchaseQuantity }}
                                                            </p>
                                                            <p><strong>Sub Total:</strong> ${{ item.pricePerUnit *
                                                                item.purchaseQuantity }}</p>
                                                        </div>
                                                    </div>

                                                    <div>
                                                        <p class="font-bold">Total Cost:</p>
                                                        <p>{{ order.totalPrice }}</p>
                                                    </div>
                                                    <div>
                                                        <p class="font-bold">Payment Status:</p>
                                                        <p>{{ order.paymentStatus }}</p>
                                                    </div>
                                                    <div>
                                                        <p class="font-bold">Order Date:</p>
                                                        <p>{{ order.date.toDate() }}</p>
                                                    </div>
                                                </div>
                                            </div>
                                            <DialogFooter>
                                                <DialogClose as-child>
                                                    <Button type="button" variant="secondary">
                                                        Close
                                                    </Button>
                                                </DialogClose>
                                            </DialogFooter>
                                        </DialogContent>
                                    </Dialog>

                                    <!-- Chat with Supplier -->
                                    <router-link :to="`/chat/${order.supplierID}/${order.supplierName}`" v-if="order.supplierName">
                                        <Button class=" text-white">Chat with Supplier</Button>
                                    </router-link>
                                </TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>

                    <!-- Supplier Order History -->
                    <Table v-if="userType == 'supplier'">
                        <TableHeader>
                            <TableRow>
                                <TableHead>Order ID</TableHead>
                                <TableHead>Items Purchased</TableHead>
                                <TableHead>Total Cost</TableHead>
                                <TableHead>Payment Status</TableHead>
                                <TableHead>Order Date</TableHead>
                                <TableHead></TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            <TableRow v-for="order in orderHistory">
                                <TableCell class="w-[100px]">{{ order.orderID }}</TableCell>
                                <TableCell>
                                    <div v-for="item in order.orderedItems">
                                        <p>{{ item.productName }} x{{ item.purchaseQuantity }}</p>
                                    </div>
                                </TableCell>
                                <TableCell>{{ order.totalPrice }}</TableCell>
                                <TableCell>{{ order.paymentStatus }}</TableCell>
                                <TableCell class="w-[300px]">{{ order.date.toDate() }}</TableCell>
                                <TableCell class="flex flex-inline space-x-4">
                                    <!-- View more details about listing -->
                                    <Dialog>
                                        <DialogTrigger as-child>
                                            <Button variant="outline">
                                                View Order
                                            </Button>
                                        </DialogTrigger>
                                        <DialogContent class="sm:max-w-[425px]">
                                            <DialogHeader>
                                                <DialogTitle class="text-2xl font-bold">Order Details</DialogTitle>
                                            </DialogHeader>
                                            <div class="grid gap-4 py-4 overflow-y-auto ">
                                                <div class="flex flex-col justify-between h-[50dvh] space-y-5">
                                                    <div>
                                                        <p class="font-bold">Order ID:</p>
                                                        <p>{{ order.orderID }}</p>
                                                    </div>
                                                    <div>
                                                        <p class="font-bold">Buyer Details:</p>
                                                        <p>{{ order.buyerID.companyName }}</p>
                                                        <p>{{ order.address }}</p>
                                                    </div>
                                                    <div>
                                                        <p class="font-bold">Buyer Number:</p>
                                                        <p>{{ order.phoneNumber }}</p>
                                                    </div>
                                                    <div>
                                                        <p class="font-bold">Items Purchased:</p>
                                                        <div v-for="item in order.orderedItems" :key="item.productName"
                                                            class="my-2 p-2 border border-gray-300 rounded">
                                                            <p><strong>Product Name:</strong> {{ item.productName }}</p>
                                                            <p><strong>Category:</strong> {{ item.category }}</p>
                                                            <p><strong>Subcategory:</strong> {{ item.subcategory }}</p>
                                                            <p><strong>Price per Unit:</strong> ${{ item.pricePerUnit }}
                                                            </p>
                                                            <p><strong>Quantity:</strong> {{ item.purchaseQuantity }}
                                                            </p>
                                                            <p><strong>Sub Total:</strong> ${{ item.pricePerUnit *
                                                                item.purchaseQuantity }}</p>
                                                        </div>
                                                    </div>

                                                    <div>
                                                        <p class="font-bold">Total Cost:</p>
                                                        <p>{{ order.totalPrice }}</p>
                                                    </div>
                                                    <div>
                                                        <p class="font-bold">Payment Status:</p>
                                                        <p>{{ order.paymentStatus }}</p>
                                                    </div>
                                                    <div>
                                                        <p class="font-bold">Order Date:</p>
                                                        <p>{{ order.date.toDate() }}</p>
                                                    </div>
                                                </div>
                                            </div>
                                            <DialogFooter>
                                                <DialogClose as-child>
                                                    <Button type="button" variant="secondary">
                                                        Close
                                                    </Button>
                                                </DialogClose>
                                            </DialogFooter>
                                        </DialogContent>
                                    </Dialog>

                                    <!-- Chat with Buyer -->
                                    <router-link 
                                        :to="`/chat/${order.buyerID}/${order.buyerCompanyName}`"
                                        v-if="order.buyerCompanyName"
                                    >
                                        <Button class="bg-blue-500 text-white">Chat with Buyer</Button>
                                    </router-link>
                                </TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>

    </div>
</template>


<!-- dummy orders -->
<script>
export default {
    name: 'orderHistory',
    components: {
        Navbar,
    },
    data() {
        return {
            userType: "restaurant",
            orderHistory: [],
        }
    },
    methods: {
        async fetchUserDetails(userId) {
            try {
                const userRef = doc(db, "users", userId);
                const userSnap = await getDoc(userRef);
                
                if (userSnap.exists()) {
                    return userSnap.data();
                }
                return null;
            } catch (error) {
                console.error("Error fetching user details:", error);
                return null;
            }
        },
        
        async fetchOrderHistory() {
            try {
                const orderHistoryRef = collection(db, "orderHistory");
                const orderHistorySnapshot = await getDocs(orderHistoryRef);
                const currentUserId = sessionStorage.getItem("uid");
                
                // Clear existing orders
                this.orderHistory = [];

                // Collect all orders that involve the current user
                const orders = [];
                orderHistorySnapshot.forEach(doc => {
                    const data = doc.data();
                    if (data.buyerID === currentUserId || data.supplierID === currentUserId) {
                        orders.push(data);
                    }
                });

                // Fetch user details for each order
                for (const order of orders) {
                    // For restaurants (buyers) viewing supplier details
                    if (order.supplierID) {
                        const supplierDetails = await this.fetchUserDetails(order.supplierID);
                        if (supplierDetails) {
                            order.supplierName = supplierDetails.companyName;
                            order.supplierAddress = supplierDetails.companyAddress;
                            order.supplierNumber = supplierDetails.companyNumber;
                        }
                    }

                    // For suppliers viewing buyer details
                    if (order.buyerID) {
                        const buyerDetails = await this.fetchUserDetails(order.buyerID);
                        if (buyerDetails) {
                            order.buyerCompanyName = buyerDetails.companyName;
                            order.buyerAddress = buyerDetails.companyAddress;
                            order.buyerNumber = buyerDetails.companyNumber;
                        }
                    }

                    this.orderHistory.push(order);
                }

                console.log("Order History with user details:", this.orderHistory);
            } catch (error) {
                console.error("Error fetching order history:", error);
            }
        }
    },
    mounted() {
        this.fetchOrderHistory();

        // Check for user type
        if (sessionStorage.getItem("userType") === "supplier") {
            this.userType = "supplier";
        }
    }
}
</script>