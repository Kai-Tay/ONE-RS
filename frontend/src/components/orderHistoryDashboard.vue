<script setup>
import Navbar from './Navbar.vue';
import { collection, getDocs, getDoc, doc } from "firebase/firestore";
import { db } from '../firebase';
import { Card, CardHeader, CardTitle, CardContent } from "./ui/card";
import { AreaChart } from "./ui/areaChart";
</script>

<template>
    <!-- Restaurant Dashboard -->
    <section v-if="userType == 'restaurant'">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mx-auto px-8 my-5">
            <!-- Total Spent Card -->
            <Card class="p-4 flex flex-col justify-center">
                <p class="text-sm font-medium text-green-600">Total Spent</p>
                <p class="text-2xl font-semibold">${{ total }}</p>
            </Card>

            <!-- Monthly Spent Changes Card Card -->
            <Card class="p-4 flex flex-col justify-center">
                <p class="text-sm font-medium">Monthly Spent Changes</p>
                <p class="text-3xl font-semibold">{{ changeType }}{{ percentageChange }}%</p>
            </Card>

            <!-- Most Purchased Category Card -->
            <Card class="p-4 flex flex-col justify-center">
                <p class="text-sm font-medium">Most Purchase Category</p>
                <p class="text-2xl font-semibold">{{ bestCategory }}</p>
            </Card>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mx-auto px-8 my-5">
            <div>
                <Card>
                    <CardHeader>
                        <CardTitle class="text-center">Total Spent Graph</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <AreaChart v-if="monthlyTotals.length" :data="monthlyTotals" index="month"
                            :categories="['total']" />
                    </CardContent>
                </Card>
            </div>
            <div>
                <Card>
                    <CardHeader>
                        <CardTitle class="text-center">Categories Purchased</CardTitle>
                    </CardHeader>
                    <CardContent>

                    </CardContent>
                </Card>
            </div>
        </div>
    </section>

    <!-- Supplier Dashboard -->
    <section v-if="userType == 'supplier'" class="">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mx-auto px-8 my-5">
            <!-- Total Earned Card -->
            <Card class="p-4 flex flex-col justify-center">
                <p class="text-sm font-medium text-green-600">Total Earned</p>
                <p class="text-2xl font-semibold">${{ total }}</p>
            </Card>

            <!-- Monthly Earned Changes Card -->
            <Card class="p-4 flex flex-col justify-center">
                <p class="text-sm font-medium">Monthly Earned Changes</p>
                <p class="text-3xl font-semibold">{{ changeType }}{{ percentageChange }}%</p>
            </Card>

            <!-- Most Sold Category Card -->
            <Card class="p-4 flex flex-col justify-center">
                <p class="text-sm font-medium">Most Sold Category</p>
                <p class="text-2xl font-semibold">{{ bestCategory }}</p>
            </Card>
        </div>
        <div class="container grid grid-cols-2 gap-4 mx-auto px-8 my-5">
            <Card>
                <CardHeader>
                    <CardTitle class="text-center">Total Earned Graph</CardTitle>
                </CardHeader>
                <CardContent>
                    <AreaChart v-if="monthlyTotals.length" :data="monthlyTotals" index="month"
                        :categories="['total']" />
                </CardContent>
            </Card>
            <Card>
                <CardHeader>
                    <CardTitle class="text-center">Categories Sold</CardTitle>
                </CardHeader>
                <CardContent>

                </CardContent>
            </Card>
        </div>
    </section>
</template>

<script>
export default {
    name: 'orderHistoryDashboard',
    components: {
        Navbar,
    },
    data() {
        return {
            userId: "",
            userType: "",
            orderHistory: [],
            monthlyTotals: [],
            total: 0,
            percentageChange: 0,
            changeType: "",
            bestCategory: "Meat",
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
        async fetchOrderData() {
            try {
                const orderHistoryRef = collection(db, "orderHistory");
                const orderHistorySnapshot = await getDocs(orderHistoryRef);
                const currentUserId = sessionStorage.getItem("uid");

                // Clear existing orders
                this.orderHistory = [];

                // Object to store monthly totals
                const monthlyTotals = {};

                // Collect and process all orders that involve the current user
                const orders = [];
                orderHistorySnapshot.forEach(doc => {
                    const data = doc.data();
                    if (data.buyerID === currentUserId || data.supplierID === currentUserId) {
                        // Convert Firestore timestamp to Date object
                        const dateObject = data.date.toDate();

                        // Format the date to extract the month name
                        const options = { day: 'numeric', month: 'long' };
                        const formattedDate = dateObject.toLocaleDateString("en-GB", options);

                        // Split the formatted date string to get the month name
                        const [day, monthName] = formattedDate.split(' ');

                        // Ensure totalPrice is a number and accumulate monthly totals
                        const totalPrice = parseFloat(data.totalPrice) || 0;
                        if (!monthlyTotals[monthName]) {
                            monthlyTotals[monthName] = 0;
                        }
                        monthlyTotals[monthName] += totalPrice;

                        orders.push(data);
                    }
                });

                this.orderHistory = orders;

                // For sorting the months in order
                const monthOrder = [
                    "January", "February", "March", "April", "May", "June",
                    "July", "August", "September", "October", "November", "December"
                ];

                // Convert monthlyTotals object to an array for charting
                this.monthlyTotals = Object.keys(monthlyTotals)
                    .sort((a, b) => monthOrder.indexOf(a) - monthOrder.indexOf(b))
                    .map(month => ({
                        month,
                        total: monthlyTotals[month]
                    }));

                console.log("Monthly Totals for Chart:", this.monthlyTotals);

                // Calculate Total
                for (let month in monthlyTotals) {
                    this.total += monthlyTotals[month];
                }

                // Calculate Percentage
                const currentMonthData = this.monthlyTotals[this.monthlyTotals.length - 1];
                const previousMonthData = this.monthlyTotals[this.monthlyTotals.length - 2];

                if (currentMonthData && previousMonthData) {
                    const currentTotal = currentMonthData.total;
                    const previousTotal = previousMonthData.total;

                    if (previousTotal !== 0) {
                        this.percentageChange = (((currentTotal - previousTotal) / previousTotal) * 100).toFixed(2);

                        // Determine if percentage change is increase or decrease
                        if (this.percentageChange > 0) {
                            this.changeType = '+';
                        } else if (this.percentageChange < 0) {
                            this.changeType = '-';
                        } else {
                            this.changeType = '=';
                        }
                        console.log(this.changeType);
                    }
                    else {
                        console.log(`Previous month's total is 0, cannot calculate percentage change.`);
                    }
                }

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
        this.userId = sessionStorage.uid;
        this.userType = sessionStorage.userType;
        this.fetchOrderData();
    }
}
</script>