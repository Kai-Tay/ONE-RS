<script setup>
import Navbar from './Navbar.vue';
import { db } from '../firebase.js';
import {collection, doc, getDoc, getDocs} from "firebase/firestore";
</script>


<template>
    <Navbar />

</template>



<script>
async function fetchRestaurants() {
    const restaurantCollection = collection(db, 'restaurant'); // Reference to the restaurants collection
    const restaurantSnapshot = await getDocs(restaurantCollection); // Fetch the documents
    
    const restaurantList = restaurantSnapshot.docs.map(doc => ({
        id: doc.id, // Get the document ID
        ...doc.data() // Get the document data
    }));

    console.log("Restaurants:", restaurantList); // Log the retrieved restaurants
}

// Call the function to fetch restaurants
fetchRestaurants();


async function calculateMeanDemand(restaurantId) {
    const restaurantRef = doc(db, 'restaurant', restaurantId); // Use doc() to reference a specific document
    const restaurantDoc = await getDoc(restaurantRef); // Use getDoc() to retrieve the document

    if (!restaurantDoc.exists) {
        console.log("Restaurant not found");
        return;
    }

    const restaurantData = restaurantDoc.data();
    console.log("Restaurant Data:", restaurantData); 

    // const actualDemand = restaurantDoc.data().actualDemand || {}; //for once the database has been changed to actualDemand
    const actualDemand = restaurantDoc.data()['Actual Demand'] || {};

    const categoryTotals = {}; // To store total quantities and counts for categories
    const itemTotals = {}; // To store total quantities and counts for items
    
    console.log(Object.entries(actualDemand));

    for (const [month, categories] of Object.entries(actualDemand)) {
        console.log("Month:", month);
        // Iterate through each category in the month

        for (const [category, items] of Object.entries(categories)) {
            console.log("Category:", category);
            if (!categoryTotals[category]) {
                categoryTotals[category] = { total: 0, count: 0 };
            }

            // Iterate through each item in the category
            for (const [item, quantity] of Object.entries(items)) {
                console.log("Item:", item, "Quantity:", quantity);

                // Initialize item totals if not already done
                if (!itemTotals[item]) {
                    itemTotals[item] = { total: 0, count: 0 };
                }

                // Update totals for the category and item
                categoryTotals[category].total += quantity;
                categoryTotals[category].count++;

                // Update totals for the item
                itemTotals[item].total += quantity;
                itemTotals[item].count++;
            }
        }
    }

    // Calculate mean demand for each category
    const categoryMean = {};
    for (const [category, totals] of Object.entries(categoryTotals)) {
        categoryMean[category] = totals.count > 0 ? totals.total / totals.count : 0; // Avoid division by zero
    }


    // Calculate mean demand for each item
    const itemMean = {};
    for (const [item, totals] of Object.entries(itemTotals)) {
        itemMean[item] = totals.total / totals.count; // Mean demand for item
    }

    console.log("Mean Demand per Category:", categoryMean);
    console.log("Mean Demand per Item:", itemMean);
}

// Example usage
calculateMeanDemand("qpNHH54FfF9k1vXv8gNV");
</script>