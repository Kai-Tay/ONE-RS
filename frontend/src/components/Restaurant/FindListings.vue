<script setup>
import Navbar from '../Navbar.vue';
import { Input } from '@/components/ui/input'
import { Switch } from '@/components/ui/switch'
import { Label } from '@/components/ui/label'
import { ref } from 'vue';
import { Button } from '@/components/ui/button'
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

    <header class="bg-dark tw-py-10">
        <!-- Bootstrap Grid System -->
        <div class="container">
            <div class="row justify-content-center mb-4">
                <div class="col-lg-9">
                    <div class="my-5">
                        <h1 class="tw-text-5xl fw-bolder tw-text-white tw-mb-10">Find 🔎</h1>
                        <div class="search-container ">
                            <Input class="searchInput" :placeholder="searchPlaceholder" v-model="searchQuery" />
                        </div>
                        <div class="tw-my-4 tw-mx-2 tw-flex tw-items-center tw-align-middle tw-justify-center">
                            <Switch id="aiSearch" :checked="isAiSearch" @update:checked="handleSwitchToggle" />
                            <Label for="aiSearch" class="tw-text-white tw-ml-2">Use AI Search {{ isAiSearch ? 'Enabled'
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
                { id: 1, title: 'Listing 1', description: 'Description for listing 1', price: '$100', image: 'https://via.placeholder.com/150' },
                { id: 2, title: 'Listing 2', description: 'Description for listing 2', price: '$200', image: 'https://via.placeholder.com/150' },
                { id: 3, title: 'Listing 3', description: 'Description for listing 3', price: '$300', image: 'https://via.placeholder.com/150' },
                // Add more mock listings as needed
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
            return isAiSearch.value ? 'Tell me your dishes!' : 'Search...';
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