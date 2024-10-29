<script setup>
import Navbar from './Navbar.vue';
import Chat from './chat.vue';
import { Table, TableBody, TableCell, TableHeader, TableHead, TableRow } from './ui/table';
import { Button } from './ui/button';
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from './ui/dropdown-menu';
</script>

<template>
    <div class="container mx-auto px-8 my-5">
        <div class="flex items-center justify-between mb-6">
            <div>
                <h2 class="text-2xl font-bold">Order History</h2>
                <p class="text-sm">Manage your recent orders</p>
            </div>
            <div class="flex">
                <DropdownMenu>
                    <DropdownMenuTrigger>
                        <Button>Filter</Button>
                        <!-- Add icon in span -->
                    </DropdownMenuTrigger>
                    <DropdownMenuContent>
                        <DropdownMenuItem>By ID</DropdownMenuItem>
                        <DropdownMenuItem>By Date</DropdownMenuItem>
                        <DropdownMenuItem>By Name</DropdownMenuItem>
                    </DropdownMenuContent>
                </DropdownMenu>
                
                <span></span>
            </div>
        </div>

        <hr class="bg-gray-500 mb-6">

        <div class="border border-gray-200 rounded-md">
            <!-- Restaurant Order History -->
            <Table v-if="userType == 'restaurant'">
                <TableHeader>
                    <TableRow>
                        <TableHead>ID</TableHead>
                        <!-- Add icon for date to toggle asc or desc -->
                        <TableHead>Date</TableHead> 
                        <TableHead>Payment Status</TableHead>
                        <TableHead>Supplier</TableHead>
                        <TableHead></TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    <TableRow v-for="order in orders">
                        <TableCell>{{ order.id }}</TableCell>
                        <TableCell>{{ order.date }}</TableCell>
                        <TableCell>{{ order.status }}</TableCell>
                        <TableCell>{{ order.name }}</TableCell>
                        <TableCell class="text-end">
                            <Button class="bg-white hover:bg-gray-100 text-gray-800 font-semibold border border-gray-400 shadow mr-2">View</Button>
                            <router-link :to="`/chat/${order.id}/${order.name}`">
                                <Button class="bg-blue-500 text-white">Chat with Supplier</Button>
                            </router-link>
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>

            <!-- Supplier Order History -->
            <Table v-if="userType == 'supplier'">
                <TableHeader>
                    <TableRow>
                        <TableHead>ID</TableHead>
                        <TableHead>Date</TableHead>
                        <TableHead>Payment Status</TableHead>
                        <TableHead>Buyer</TableHead>
                        <TableHead></TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    <TableRow v-for="order in orders">
                        <TableCell>{{ order.id }}</TableCell>
                        <TableCell>{{ order.date }}</TableCell>
                        <TableCell>{{ order.status }}</TableCell>
                        <TableCell>{{ order.name }}</TableCell>
                        <TableCell class="text-end">
                            <Button class="bg-white hover:bg-gray-100 text-gray-800 font-semibold border border-gray-400 shadow mr-2">View</Button>
                            <Button class="bg-blue-500 text-white">Chat with Buyer</Button>
                        </TableCell>
                    </TableRow>
                </TableBody>
            </Table>
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
            orders: [
                { id: 1, date: '27/10/2024', status: 'Paid', name: 'Ann' },
                { id: 2, date: '27/10/2024', status: 'Pending', name: 'Bob' },
                { id: 3, date: '27/10/2024', status: 'Paid', name: 'Charles' }
            ]
        }
    }, 
    methods: {
        navigateToChat(supplierId, supplierName) {
            this.$router.push({
                name: 'chat',
                params: {
                    supplierId: supplierId,
                    supplierName: supplierName
                }
            });
        }
    }
}
</script>