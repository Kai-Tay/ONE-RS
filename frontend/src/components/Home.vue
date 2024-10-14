<script setup>
import Navbar from './Navbar.vue';
</script>

<template>
    <Navbar />
    <div class="container">
        <!-- Search -->
        <div class="my-5">
            <h1>Find Suppliers 🔍</h1>
            <div class="search-container">
                <input type="text" v-model="searchQuery" @input="filterListings" class="search-box my-0"
                    :placeholder="searchPlaceholder" />
                <button @click="performSearch" class="btn btn-primary btn-lg search-btn mx-3">🔍</button>
            </div>
            <div class="form-check form-switch my-2 mx-2">
                <input class="form-check-input" type="checkbox" role="switch" v-model="isAiSearch">
                <label class="form-check-label fs-5" for="flexSwitchCheckDefault">Use AI Search {{ isAiSearch ? 'enabled' : 'disabled' }}</label>
            </div>
        </div>

        <!-- Listings -->
        <!-- <div class="row">
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
        </div> -->
    </div>
</template>

<script>
export default {
    name: 'Home',
    components: {
        Navbar,
    },
    data() {
        return {
            searchQuery: '',
            isAiSearch: false,
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
                const query = this.searchQuery.toLowerCase();
                this.filteredListings = this.listings.filter(listing =>
                    listing.title.toLowerCase().includes(query) ||
                    listing.description.toLowerCase().includes(query)
                );
            } else {
                this.filteredListings = this.listings;
            }
        },
    },
    computed: {
    // Computed property to dynamically set the placeholder
    searchPlaceholder() {
      return this.isAiSearch ? 'Tell me your dishes!' : 'Search...';
    }
  }
};
</script>

<style>
.container{
    height: 100vh; /* Make the container take up the full viewport height */
}

.search-box {
    border-radius: 20px;
    border-color: white;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.search-box:focus {
    outline: 0px;
}

.card {
    transition: transform 0.5s;
}

.card:hover {
    transform: scale(1.02);
}

.search-container {
    display: flex;
    justify-content: center;
    align-items: center;
}

.search-btn{
    border-radius: 20px;
}
</style>