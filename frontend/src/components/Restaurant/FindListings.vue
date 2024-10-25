<script setup>
import { Input } from '@/components/ui/input'
import { Switch } from '@/components/ui/switch'
import { Label } from '@/components/ui/label'
import { ref } from 'vue';
import { Button } from '@/components/ui/button'
import {
    Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle,
} from '@/components/ui/card'
import { collection, query, getDocs, where } from "firebase/firestore";
import { db } from '../../firebase.js';
import { TagsInput, TagsInputItem, TagsInputItemDelete, TagsInputItemText } from '@/components/ui/tags'
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
                    <!-- SUBHEADERR -->
                    <div class="text-gray-500 mt-5">
                        <!-- Search Component -->
                        <div class="search-container ">
                            <Input class="searchInput" :placeholder="searchPlaceholder" v-model="searchQuery" />
                        </div>
                        <div class="my-4 mx-2 flex items-center align-middle justify-center">
                            <Switch id="aiSearch" :checked="isAiSearch" @update:checked="handleSwitchToggle" />
                            <Label for="aiSearch" class="text-white ml-2 text-lg">Use AI Search {{ isAiSearch ?
                                'Enabled' : 'Disabled' }}</Label>
                        </div>
                        <div class="flex items-center align-middle justify-center mt-8">
                            <Button class="rounded-full px-5 py-5 text-xl" @click.native="filterListings">🔎 &nbsp;
                                Search</Button>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </header>

    <!-- Filter Bar from Search -->

    <div class="mt-5 mb-5 mx-5">
        <div class="text-4xl font-bold">Suppliers</div>
        <TagsInput v-model="searchResult">
            <TagsInputItem v-for="item in searchResult" :key="item" :value="item">
                <TagsInputItemText />
                <TagsInputItemDelete @click="handleFilterBoxClose"/>
            </TagsInputItem>
        </TagsInput>

    </div>



    <!-- Listings -->
    <div class="grid grid-cols-1 gap-4 mx-5">
        <div class="mb-4" v-for="listing in filteredListings" :key="listing.id">
            <Card>
                <CardHeader>
                    <CardTitle>
                        <div class="text-2xl">{{ listing.supplierName }}</div>
                    </CardTitle>
                    <CardDescription class="text-lg">{{ listing.supplierDescription }}</CardDescription>
                </CardHeader>
                <CardContent>
                    <div class="flex flex-inline justify-between">
                        <!-- Text -->
                        <div class="flex flex-col justify-center">
                            <CardDescription class="text-md">Available Ingredients:</CardDescription>
                            <CardDescription class="text-md">{{ listing }}</CardDescription>
                            {{ listing.description }}
                        </div>
                        <div class="">
                            <!-- <img class="w-40 h-40 mx-auto block object-cover my-4" :src="listing.image" alt="Listing Image" /> -->
                        </div>
                    </div>
                </CardContent>
                <CardFooter>
                    <Button>View Supplier</Button>
                </CardFooter>
            </Card>
        </div>
    </div>


</template>

<script>
const isAiSearch = ref(false);

// Handler function for when the switch is toggled
const handleSwitchToggle = (newValue) => {
    isAiSearch.value = newValue;
};


export default {
    name: 'Home',
    components: {},
    data() {
        return {
            searchQuery: '',
            filteredListings: [],
            listings: [],
            companyDetails: [],

            // Filter Bar Variable
            searchResult: [],
        };
    },
    mounted() {
        // Obtain Database Suppliers
        this.fetchListings();
    },

    methods: {
        handleFilterBoxClose() {
            // Clear text input and call the function to recheck the listings
            this.searchQuery = '';
            this.filterListings();
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

                    return { ...listing, supplierDescription: company.companyDescription }
                })

                this.listings = mergedArray;
                this.filteredListings = this.listings;

            } catch (error) {
                console.error('Error fetching listings:', error)
            }
        },

        filterListings() {
            if (this.searchQuery) {

                // Insert CHATGPT QUERY HERE
                // Check if AI Search is enabled
                if (isAiSearch.value) {
                    const query = this.performAiSearch();
                } else {
                    // Make search query lower case
                    const query = this.searchQuery.toLowerCase();

                    // Add search query to list of search results
                    this.searchResult.push(query);

                    // Filter out listings that have the search result in their title or ingredients
                    this.filteredListings = this.listings.filter(listing =>
                        // Check if any search term matches supplierName or any productName in inventory
                        this.searchResult.some(query =>
                            listing.supplierName.toLowerCase().includes(query.toLowerCase()) ||
                            listing.inventory.some(item => item.productName.toLowerCase().includes(query.toLowerCase()))
                        )
                    );
                    console.log(this.searchResult)
                    // this.filteredListings = this.listings.filter(listing =>
                    //     listing.supplierName.toLowerCase().includes(query) ||
                    //     listing.inventory.some(item => item.productName.toLowerCase().includes(query))
                    // );

                }
            } else {
                // If search is empty, revert it back to all listings
                this.filteredListings = this.listings;
            }

            // Clear the text input
            this.searchQuery = '';
        },
        performAiSearch() {
            // Perform AI search here by calling backend API (INSERT ACTUAL BACKEND SERVER URL)
            url = "http://localhost:5001/search-ai";
            axios.post(url, {
                "data": this.searchQuery,
            })
                .then(response => {
                    // process response.data object


                })
                .catch(error => {
                    // process error object
                });

        },
    },
    computed: {
        // Computed property to dynamically set the placeholder
        searchPlaceholder() {
            return isAiSearch.value ? 'Tell me your menu and we will find all your ingredients!' : 'Search for ingredients...';
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