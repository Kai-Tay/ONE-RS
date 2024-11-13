<script setup>
import { Input } from '@/components/ui/input'
import { Switch } from '@/components/ui/switch'
import { Label } from '@/components/ui/label'
import { ref } from 'vue';
import { Button } from '@/components/ui/button'
import Skeleton from '../ui/skeleton/Skeleton.vue';
import {
    Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle,
} from '@/components/ui/card'
import { collection, query, getDocs, where } from "firebase/firestore";
import { db } from '../../firebase.js';
import { TagsInput, TagsInputItem, TagsInputItemDelete, TagsInputItemText } from '@/components/ui/tags'
import axios from 'axios';
</script>

<template>
    <div class=" mx-auto my-5 px-8 " v-if="loading">
        <div class="flex items-center justify-between mb-6">
            <div>
                <Skeleton class="h-[20px] w-[140px] rounded-xl my-1" />
                <Skeleton class="h-[20px] w-[180px] rounded-xl" />
            </div>
        </div>
        <Skeleton class="h-[35px] rounded-xl my-1 my-5" />

        <Skeleton class="h-[400px] w-full rounded-xl mt-20" />
    </div>

    <div v-else>
    <!-- Filter Bar from Search -->
    <div class="mt-5 mb-5 px-8">
        <div>
            <h2 class="text-2xl font-bold">Suppliers</h2>
            <p class="text-sm">Find and Connect with Suppliers</p>
        </div>
        <!-- Search Bar Section -->
        <div class="mt-4">
            <div class="flex items-center space-x-5">
                <Input class="" :placeholder="searchPlaceholder" v-model="searchQuery" />
                <Button class="rounded-full px-5 py-2 text-md" @click="filterListings">🔎 Search</Button>
            </div>
            <div class="my-4 mx-2 flex items-center justify-center">
                <Switch id="aiSearch" :checked="isAiSearch" @update:checked="handleSwitchToggle" />
                <Label for="aiSearch" class="text-gray-700 ml-2 text-lg">Use AI Search {{ isAiSearch ? 'Enabled' :
                    'Disabled' }}</Label>
            </div>

        </div>
        <TagsInput v-model="searchResult">
            <TagsInputItem v-for="item in searchResult" :key="item" :value="item">
                <TagsInputItemText />
                <TagsInputItemDelete @click="handleFilterBoxClose" />
            </TagsInputItem>
        </TagsInput>
    </div>

    <!-- Listings Section -->
    <div class="grid grid-cols-1 gap-4 px-8">
        <div class="mb-4" v-for="listing in filteredListings" :key="listing.id">
            <Card>
                <CardContent class="flex flex-col sm:flex-row items-center pt-4">
                    <!-- Centered Placeholder Image on the Left -->
                    <div class="w-1/5 flex items-center justify-center">
                        <img :src="listing.imageData || './images/placeholder.svg'" alt="Supplier Image"
                            class="w-auto h-auto max-h-40 object-cover rounded-md">
                    </div>

                    <!-- Supplier Content on the Right -->
                    <div class="sm:ml-4 w-3/5 flex flex-col items-center sm:items-start">
                        <CardHeader class="px-0 sm:px-6 text-center sm:text-left">
                            <CardTitle>
                                <div class="text-md sm:text-2xl text-center sm:text-left">{{ listing.supplierName }}</div>
                            </CardTitle>
                            <CardDescription class="text-lg px-0 text-center sm:text-left">
                                {{
                                    Array.from(new Set(listing.inventory.map(item => item.category))).join(", ")
                                }}
                            </CardDescription>
                        </CardHeader>
                        <CardFooter class="px-0 sm:px-6">
                            <Button @click="handleSupplierClick(listing.id)">View Supplier</Button>
                        </CardFooter>
                    </div>
                    <div class="w-3/5">
                        <CardContent class="px-0 sm:px-6 ">
                            <div class="flex flex-col items-center sm:items-start">
                                <CardDescription class="text-md font-bold">Available Ingredients</CardDescription>
                                <CardDescription class="text-md" v-for="item in listing.inventory"
                                    :key="item.productName">
                                    {{ item.productName }} - {{ item.subcategory }}
                                </CardDescription>
                            </div>
                        </CardContent>
                    </div>
                </CardContent>
            </Card>
        </div>
    </div>
</div>
</template>

<style scoped>
.w-20 {
    width: 200px;
}

.h-20 {
    height: 200px;
}
</style>






<script>
const isAiSearch = ref(false);

// Handler function for when the switch is toggled
const handleSwitchToggle = (newValue) => {
    isAiSearch.value = newValue;
};


export default {
    name: 'FindListings',
    components: {},
    data() {
        return {
            searchQuery: '',

            // Firebase Variables
            filteredListings: [],
            listings: [],

            // Filter Bar Variable
            searchResult: [],

            loading:true,
        };
    },
    mounted() {
        // Obtain Database Suppliers
        this.fetchListings();
    },

    methods: {
        handleSupplierClick(id) {
            this.$router.push({ name: 'viewSupplier', params: { id: id } });
        },
        handleFilterBoxClose() {
            if (this.searchResult.length > 0) {
                // Filter out listings that have the search result in their title or ingredients
                this.filteredListings = this.listings.filter(listing =>
                    // Check if any search term matches supplierName or any productName in inventory
                    this.searchResult.some(query =>
                        listing.supplierName.toLowerCase().includes(query.toLowerCase()) ||
                        listing.inventory.some(item => item.productName.toLowerCase().includes(query.toLowerCase()))
                    )
                );
            } else {
                this.filteredListings = this.listings;
            }
        },
        async fetchListings() {
            // Fetch all listings from the database
            try {
                // Get supplierListings Collection
                const supplierSnapshot = await getDocs(query(collection(db, "supplierListing")))
                const listingsArray = []
                supplierSnapshot.forEach((doc) => {
                    listingsArray.push({ id: doc.id, ...doc.data() })
                })

                // Get user details colleciton
                const usersSnapshot = await getDocs(query(collection(db, "users"), where("userType", "==", "supplier")))
                const usersArray = []
                usersSnapshot.forEach((doc) => {
                    usersArray.push({ id: doc.id, ...doc.data() })
                })

                // Merge the two arrays
                const mergedArray = listingsArray.map(listing => {
                    const company = usersArray.find(user => user.id === listing.id)

                    return { ...listing, supplierDescription: company.companyDescription, imageData: company.imageData || null }
                })

                this.listings = mergedArray;
                this.filteredListings = this.listings;

            } catch (error) {
                // console.log.error('Error fetching listings:', error)
            }
            // Simulate data fetching or delay
            setTimeout(() => {
                    this.loading = false; // Set loading to false once data is loaded
                }, 250);
        },

        filterListings() {
            if (this.searchQuery) {
                // Insert CHATGPT QUERY HERE
                // Check if AI Search is enabled
                if (isAiSearch.value) {
                    // Perform AI Search
                    this.performAiSearch();

                } else {
                    // Add search query to list of search results
                    this.searchResult.push(this.searchQuery);

                    // Make search query lower case
                    const query = this.searchQuery.toLowerCase();

                    // Filter out listings that have the search result in their title or ingredients
                    this.filteredListings = this.listings.filter(listing =>
                        // Check if any search term matches supplierName or any productName in inventory
                        this.searchResult.some(query =>
                            listing.supplierName.toLowerCase().includes(query.toLowerCase()) ||
                            listing.inventory.some(item => item.productName.toLowerCase().includes(query.toLowerCase()) ||
                                listing.inventory.some(item => item.category.toLowerCase().includes(query.toLowerCase())) ||
                                listing.inventory.some(item => item.subcategory.toLowerCase().includes(query.toLowerCase())))
                        )
                    );

                }
            } else {
                // console.log.log(this.searchResult)
                // If search is empty, revert it back to all listings
                this.filteredListings = this.listings;
            }

            // Clear the text input
            this.searchQuery = '';
        },
        performAiSearch() {
            let queryList = [];
            // console.log.log("Using AI Search now")
            // Perform AI search here by calling backend API (INSERT ACTUAL BACKEND SERVER URL)
            const url = "http://54.169.182.213/search-ai";
            axios.post(url, {
                "data": this.searchQuery,
            })
                .then((response) => {
                    // process response.data object
                    queryList = response.data[0].ingredients;
                    for (const query of queryList) {
                        this.searchResult.push(query);
                    }

                    // Filter out listings that have the search result in their title or ingredients
                    this.filteredListings = this.listings.filter(listing =>
                        // Check if any search term matches supplierName or any productName in inventory
                        this.searchResult.some(query =>
                            listing.supplierName.toLowerCase().includes(query.toLowerCase()) ||
                            listing.inventory.some(item => item.productName.toLowerCase().includes(query.toLowerCase()))
                            || listing.inventory.some(item => item.category.toLowerCase().includes(query.toLowerCase()))
                            || listing.inventory.some(item => item.subcategory.toLowerCase().includes(query.toLowerCase()))
                        )
                    );
                })
                .catch(error => {
                    // process error object
                    // console.log.log(error)
                });
        },
    },
    computed: {
        // Computed property to dynamically set the placeholder
        searchPlaceholder() {
            return isAiSearch.value ? 'Tell me your menu and we will find all your ingredients!' : 'Search for Ingredients, Category or Suppliers';
        },
    },
};
</script>
