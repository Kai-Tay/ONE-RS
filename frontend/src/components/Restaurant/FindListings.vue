<script setup>
import Navbar from '../Navbar.vue';
import { Input } from '@/components/ui/input'
import { Switch } from '@/components/ui/switch'
import { Label } from '@/components/ui/label'
import { ref } from 'vue';
import { Button } from '@/components/ui/button'
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from '@/components/ui/card'
import FilterBar from './filterBar.vue';
import { collection, query, getDocs } from "firebase/firestore";
import { db } from '../../firebase.js';
</script>

<template>
    <Navbar />
    
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
        <div class="text-4xl font-bold">Listings</div>
        
        <FilterBar></FilterBar>
    </div>
    


    <!-- Listings -->
    <div class="grid grid-cols-1 gap-4 mx-5">
        <div class="mb-4" v-for="listing in listings" :key="listing.id">
            <Card>
                <CardHeader>
                    <CardTitle><div class="text-2xl">{{ listing.supplierName }}</div></CardTitle>
                    <CardDescription>{{ listing.category }}</CardDescription>
                </CardHeader>
                <CardContent>
                    <div class="flex flex-inline justify-between">
                        <!-- Text -->
                        <div class="flex flex-col justify-center">
                            <CardDescription class="text-xl">Data {{ listing }}</CardDescription>
                            <CardDescription class="text-xl">{{ listing.price }}</CardDescription>
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
    components: {
        Navbar,
    },
    data() {
        return {
            searchQuery: '',
            filteredListings: [],
            listings: [],
        };
    },
    created() {
        // Initially set the filtered listings to all listings
        this.filteredListings = this.listings;
    },
    mounted() {
        // Obtain Database
        this.fetchListings();
    },
    
    methods: {
        async fetchListings() {
            try {
                console.log(this.listings)
                const querySnapshot = await getDocs(query(collection(db, "supplierListing"))) 
                const listingsArray = []
                querySnapshot.forEach((doc) => {
                    listingsArray.push({ id: doc.id, ...doc.data() }) 
                })
                this.listings = listingsArray; // Update the listings array with fetched data
                
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
                    const query = this.searchQuery.toLowerCase();
                }
                // this.filteredListings = this.listings.filter(listing =>
                //     listing.title.toLowerCase().includes(query) ||
                //     listing.description.toLowerCase().includes(query)
                // );
            } else {
                this.filteredListings = this.listings;
            }
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
            return isAiSearch.value ? 'Tell me your menu and we will find all your ingredients!' : 'Search...';
        }
    }
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