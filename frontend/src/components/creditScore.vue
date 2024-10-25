<script setup>
import Navbar from './Navbar.vue';
import { Card, CardHeader, CardContent, CardTitle, CardDescription, CardFooter } from '@/components/ui/card';
</script>

<template>
    <div class="container mx-auto px-4 my-4">
        <div class="flex flex-wrap -mx-3">
            <div class="w-full lg:w-8/12 px-3">
                <!-- Shadcn Card Component -->
                <Card class="h-full">
                    <CardHeader class="text-center">
                        <CardTitle>Credit Score Bar</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <svg class="mt-6 mx-auto" viewBox="0 0 200 130">
                            <!-- Background arc -->
                            <path d="M 10 100 A 90 90 0 0 1 190 100" fill="none" stroke="#ddd" stroke-width="20" />

                            <!-- Progress arc (dynamic) -->
                            <path class="meter" d="M 10 100 A 90 90 0 0 1 190 100" fill="none" stroke="url(#gradient)"
                                stroke-width="20" :stroke-dasharray="dashArray" :stroke-dashoffset="dashOffset" />

                            <!-- Gradient Definition -->
                            <defs>
                                <linearGradient id="gradient">
                                    <stop offset="0%" stop-color="red" />
                                    <stop offset="30%" stop-color="orange" />
                                    <stop offset="50%" stop-color="yellow" />
                                    <stop offset="100%" stop-color="green" />
                                </linearGradient>
                            </defs>

                            <!-- Gauge Labels (300 and 1000) -->
                            <text x="2" y="115" fill="red" font-size="10px">300</text>
                            <text x="178" y="115" fill="green" font-size="10px">1000</text>
                        </svg>
                        <p class="text-center font-bold text-4xl mt-4">Current Credit Score: {{ points }}</p>
                    </CardContent>
                </Card>
            </div>
            <div class="w-full lg:w-4/12 px-3 mt-6 lg:mt-0">
                <!-- Shadcn Card Component -->
                <Card class="h-full">
                    <CardHeader>
                        <CardTitle>Credit Factors</CardTitle>
                        <CardDescription>Factors that affect your score</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div class="flex items-start">
                            <i class="bi bi-calendar2-check text-3xl"></i>
                            <div class="ml-4">
                                <p class="font-bold mb-1">On-time Payment</p>
                                <p class="text-gray-600">Payments made on time will increase your score</p>
                            </div>
                        </div>

                        <div class="flex items-start mt-6">
                            <i class="bi bi-calendar2-check text-3xl"></i>
                            <div class="ml-4">
                                <p class="font-bold mb-1">Good Rating from Suppliers</p>
                                <p class="text-gray-600">Suppliers that gives you a good rating will increase your score</p>
                            </div>
                        </div>

                        <div class="flex items-start mt-6">
                            <i class="bi bi-calendar2-check text-3xl"></i>
                            <div class="ml-4">
                                <p class="font-bold mb-1">Placeholder</p>
                                <p class="text-gray-600">Payments made on time will increase your score</p>
                            </div>
                        </div>
                    </CardContent>
                    <CardFooter>
                        <a href="#" class="inline-block bg-blue-500 text-white font-bold py-2 px-4 rounded mt-6">Go to
                            Payment History</a>
                    </CardFooter>
                </Card>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'creditScore',
    components: {
        Navbar,
    },
    data() {
        return {
            startPoints: 300,
            points: 0,
            minScore: 300,
            maxScore: 1000,
            radius: 90
        }
    },
    computed: {
        scorePercentage() {
            return ((this.startPoints - this.minScore) / (this.maxScore - this.minScore));
        },
        dashArray() {
            return parseInt(Math.PI * this.radius);
        },
        dashOffset() {
            return this.dashArray - (this.dashArray * this.scorePercentage);
        }
    },
    mounted() {
        // Simulate loading with a slight delay to trigger the animation
        setTimeout(() => {
            this.points = sessionStorage.points;
            this.startPoints = this.points;
        }, 10);
    }
}
</script>

<style>
body {
    background-color: #FBF7F0;
}

path {
    transition: stroke-dashoffset 1s ease;
}
</style>