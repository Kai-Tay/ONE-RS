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
</script>

<template>
    <Navbar />
    <!-- <div class="container">
        Search
        <div class="my-5">
            <h1>Find Suppliers 🔍</h1>
            <div class="search-container">
                <input type="text" v-model="searchQuery" @input="filterListings" class="search-box my-0"
                    :placeholder="searchPlaceholder" />
                <button @click="performSearch" class="btn btn-primary btn-lg search-btn mx-3">🔍</button>
            </div>
            <div class="form-check form-switch my-2 mx-2">
                <input class="form-check-input" type="checkbox" role="switch" v-model="isAiSearch">
                <label class="form-check-label fs-5" for="flexSwitchCheckDefault">Use AI Search {{ isAiSearch ?
                    'enabled' : 'disabled' }}</label>
            </div>
        </div>

        Listings
        <div class="row">
            <div class="col-md-4 mb-4" v-for="listing in filteredListings" :key="listing.id">
                <div class="card h-100">
                    <img :src="listing.image" class="card-img-top" alt="Listing Image" />
                    <div class="card-body">
                        <h5 class="card-title">{{ listing.title }}</h5>
                        <p class="card-text">{{ listing.description }}</p>
                        <p class="card-text"><strong>Price:</strong> {{ listing.price }}</p>
                    </div>
                    <div class="card-footer">
                        <a :href="`/listings/${listing.id}`" class="btn btn-primary">View Details</a>
                    </div>
                </div>
            </div>
        </div>
    </div> -->

    <!-- Header -->
    <header class="bg-dark tw-py-10">
        <!-- Bootstrap Grid System -->
        <div class="container-fluid">
            <div class="row justify-content-center mb-4">
                <div class="col-lg-9">
                    <div class="my-5">
                        <h1 class="tw-text-5xl fw-bolder tw-text-white tw-mb-10">Find Suppliers</h1>
                        <!-- Search Component -->
                        <div class="search-container tw- ">
                            <Input class="searchInput" :placeholder="searchPlaceholder" v-model="searchQuery" />
                        </div>
                        <div class="tw-my-4 tw-mx-2 tw-flex tw-items-center tw-align-middle tw-justify-center">
                            <Switch id="aiSearch" :checked="isAiSearch" @update:checked="handleSwitchToggle" />
                            <Label for="aiSearch" class="tw-text-white tw-ml-2 tw-text-lg">Use AI Search {{ isAiSearch ?
                                'Enabled'
                                : 'Disabled' }}</Label>
                        </div>
                        <div class="tw-flex tw-items-center tw-align-middle tw-justify-center tw-mt-8">
                            <Button class="tw-rounded-full tw-px-5 tw-py-5 tw-text-xl" @click.native="filterListings">🔎
                                &nbsp; Search</Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- Filter Bar from Search -->
    <div class="mt-5 mb-5 mx-4">
        <div class="tw-text-4xl tw-font-bold">Listings</div>

    </div>


    <!-- Listings -->
    <div class="tw-flex tw-flex-wrap tw-justify-center">
        <div class="row container-fluid ">
            <div class="col-xl-3 col-lg-4 col-md-6 mb-4 " v-for="listing in filteredListings" :key="listing.id">
                <Card>
                    <CardHeader>
                        <CardTitle>{{ listing.title }}</CardTitle>
                        <CardDescription>{{ listing.category }}</CardDescription>

                    </CardHeader>
                    <CardContent>
                        <img class="tw-w-full tw-h-72 tw-mx-auto tw-block tw-object-cover tw-my-4" :src="listing.image"
                            alt="Listing Image" />
                        <CardDescription class="tw-text-xl">Sold By {{ listing.supplier }}</CardDescription>
                        <CardDescription class="tw-text-xl">{{ listing.price }}</CardDescription>
                        {{ listing.description }}
                    </CardContent>
                    <CardFooter>
                        <Button >View Listing</Button>
                    </CardFooter>
                </Card>
            </div>
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
            listings: [
                {
                    id: 1,
                    title: 'Kampung Chicken',
                    description: 'Free-range poultry',
                    price: '$100',
                    image: 'https://placehold.co/600x400',
                    category: 'Meat: Poultry',
                    supplier: 'Farm Fresh Poultry Co.'
                },
                {
                    id: 2,
                    title: 'Beef Ribeye',
                    description: 'Premium ribeye cut',
                    price: '$200',
                    image: 'https://placehold.co/600x400',
                    category: 'Meat: Beef',
                    supplier: 'Prime Cuts Butchers'
                },
                {
                    id: 3,
                    title: 'Organic Carrots',
                    description: 'Fresh organic carrots',
                    price: '$10',
                    image: 'https://placehold.co/600x400',
                    category: 'Veg & Fruits: Vegetables',
                    supplier: 'Green Valley Farms'
                },
                {
                    id: 4,
                    title: 'Salmon Fillet',
                    description: 'Fresh Atlantic salmon',
                    price: '$250',
                    image: 'https://placehold.co/600x400',
                    category: 'Meat: Fish',
                    supplier: 'Ocean Catch Seafood'
                },
                {
                    id: 5,
                    title: 'Cheddar Cheese',
                    description: 'Aged cheddar',
                    price: '$50',
                    image: 'https://placehold.co/600x400',
                    category: 'Dairy: Cheese',
                    supplier: 'Cheese Masters Ltd.'
                },
                {
                    id: 6,
                    title: 'Whole Wheat Bread',
                    description: 'Freshly baked bread',
                    price: '$5',
                    image: 'https://placehold.co/600x400',
                    category: 'Carbohydrates: Bread',
                    supplier: 'Baker’s Delight'
                },
                {
                    id: 7,
                    title: 'Spaghetti',
                    description: 'High-quality pasta',
                    price: '$15',
                    image: 'https://placehold.co/600x400',
                    category: 'Carbohydrates: Pasta',
                    supplier: 'Pasta Perfection'
                },
                {
                    id: 8,
                    title: 'Pork Belly',
                    description: 'Tender pork belly',
                    price: '$180',
                    image: 'https://placehold.co/600x400',
                    category: 'Meat: Pork',
                    supplier: 'Meat Lovers Inc.'
                },
                {
                    id: 9,
                    title: 'Eggs',
                    description: 'Organic free-range eggs',
                    price: '$8',
                    image: 'https://placehold.co/600x400',
                    category: 'Dairy: Eggs',
                    supplier: 'Eggcellent Farms'
                },
                {
                    id: 10,
                    title: 'Bananas',
                    description: 'Fresh bananas ',
                    price: '$6',
                    image: 'https://upload.wikimedia.org/wikipedia/commons/8/8a/Banana-Single.jpg',
                    category: 'Veg & Fruits: Fruits',
                    supplier: 'Fruitful Harvest'
                }
            ],
            filteredListings: [],
        };
    },
    created() {
        // Initially set the filtered listings to all listings
        this.filteredListings = this.listings;
    },
    methods: {
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