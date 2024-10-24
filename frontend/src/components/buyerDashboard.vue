<script setup>
import { db } from '../firebase.js';
import {collection, doc, getDoc, getDocs} from "firebase/firestore";
import { AreaChart } from '@/components/ui/areaChart';
</script>


<template>

    <div>
        <h1>Testing AreaChart Component</h1>
        <AreaChart :data="testData" index="name" :categories="['total', 'predicted']" />
    </div>


</template>




<script>
// const testData = [
//   { name: '2023-01', total: 1500, predicted: 1600 },
//   { name: '2023-02', total: 1800, predicted: 1750 },
//   { name: '2023-03', total: 2000, predicted: 2100 },
// ];


// async function fetchRestaurants() {
//     const restaurantCollection = collection(db, 'restaurant'); // Reference to the restaurants collection
//     const restaurantSnapshot = await getDocs(restaurantCollection); // Fetch the documents
    
//     const restaurantList = restaurantSnapshot.docs.map(doc => ({
//         id: doc.id, // Get the document ID
//         ...doc.data() // Get the document data
//     }));

//     console.log("Restaurants:", restaurantList); // Log the retrieved restaurants
// }

// // Call the function to fetch restaurants
// fetchRestaurants();


// async function calculateMeanDemandAndSd(restaurantId) {
//     const restaurantRef = doc(db, 'restaurant', restaurantId); // Use doc() to reference a specific document
//     const restaurantDoc = await getDoc(restaurantRef); // Use getDoc() to retrieve the document

//     if (!restaurantDoc.exists) {
//         console.log("Restaurant not found");
//         return;
//     }

//     const restaurantData = restaurantDoc.data();
//     console.log("Restaurant Data:", restaurantData); 

//     // const actualDemand = restaurantDoc.data().actualDemand || {}; //for once the database has been changed to actualDemand
//     const actualDemand = restaurantDoc.data()['Actual Demand'] || {};

//     const categoryTotals = {}; // To store total quantities and counts for categories
//     const itemTotals = {}; // To store total quantities and counts for items
    
//     console.log(Object.entries(actualDemand));

//     for (const [month, categories] of Object.entries(actualDemand)) {
//         console.log("Month:", month);
//         // Iterate through each category in the month

//         for (const [category, items] of Object.entries(categories)) {
//             console.log("Category:", category);
//             if (!categoryTotals[category]) {
//                 categoryTotals[category] = { total: 0, count: 0 , quantities: []};
//             }

//             // Iterate through each item in the category
//             for (const [item, quantity] of Object.entries(items)) {
//                 console.log("Item:", item, "Quantity:", quantity);

//                 // Initialize item totals if not already done
//                 if (!itemTotals[item]) {
//                     itemTotals[item] = { total: 0, count: 0 , quantities: []};
//                 }

//                 // Update totals for the category and item
//                 categoryTotals[category].total += quantity;
//                 categoryTotals[category].count++;
//                 categoryTotals[category].quantities.push(quantity); // Collect quantities for SD


//                 // Update totals for the item
//                 itemTotals[item].total += quantity;
//                 itemTotals[item].count++;
//                 itemTotals[item].quantities.push(quantity); // Collect quantities for SD
//             }
//         }
//     }

//     // Calculate mean demand and standard deviation for each category
//     const categoryMean = {};
//     const categorySD = {};
//     for (const [category, totals] of Object.entries(categoryTotals)) {
//         categoryMean[category] = totals.count > 0 ? totals.total / totals.count : 0;
//         categorySD[category] = calculateStandardDeviation(totals.quantities); // Calculate SD for the category
//     }

//     // Calculate mean demand and standard deviation for each item
//     const itemMean = {};
//     const itemSD = {};
//     for (const [item, totals] of Object.entries(itemTotals)) {
//         itemMean[item] = totals.count > 0 ? totals.total / totals.count : 0;
//         itemSD[item] = calculateStandardDeviation(totals.quantities); // Calculate SD for the item
//     }

//     console.log("Mean Demand per Category:", categoryMean);
//     console.log("Standard Deviation per Category:", categorySD);
//     console.log("Mean Demand per Item:", itemMean);
//     console.log("Standard Deviation per Item:", itemSD);

//     // Return the results as an object
//     return {
//         categoryMean,
//         categorySD,
//         itemMean,
//         itemSD
//     };
// }

// function calculateStandardDeviation(values) {
//     const n = values.length;
//     if (n === 0) return 0;

//     const mean = values.reduce((acc, val) => acc + val, 0) / n;
//     const variance = values.reduce((acc, val) => acc + Math.pow(val - mean, 2), 0) / n;
//     return Math.sqrt(variance);
// }

// function calculateZScore(serviceLevel) {
//     if (serviceLevel < 0 || serviceLevel > 1) {
//         throw new Error("Service level must be between 0 and 1.");
//     }
//     // Using the inverse of the standard normal cumulative distribution function
//     return jStat.normal.inv(serviceLevel, 0, 1);
// }

// // Example usage
// const serviceLevel = 0.96; // this will be by user input in the future
// const zScore = calculateZScore(serviceLevel);
// console.log("Z-Score for 96% Service Level:", zScore);


// function calculateOULForAllItems(itemMean, itemSD) {
//     const T = 1; // Review time in Months
//     const L = 7 / 30; // Lead time in Months
//     const Z = 1.75; // Z-score for 96% service level needs to be updated to take in the zScore based on user input
//     const totalTime = T + L;

//     const OULResults = {};

//     for (const item of Object.keys(itemMean)) {
//         const meanDemand = itemMean[item] || 0; // Default to 0 if undefined
//         const stdDev = itemSD[item] || 0; // Default to 0 if undefined

//         // Mean demand during T + L
//         const meanDemandTL = meanDemand * totalTime;

//         // Standard deviation during T + L
//         const stdDevTL = stdDev * Math.sqrt(totalTime);

//         // Safety stock
//         const safetyStock = Z * stdDevTL;

//         // Order Up to Level
//         const OUL = meanDemandTL + safetyStock;

//         // Store the results
//         OULResults[item] = {
//             meanDemandTL,
//             stdDevTL,
//             safetyStock,
//             OUL
//         };
//     }

//     return OULResults;
// }



// // Example usage
// async function main() {
//     const restaurantId = "qpNHH54FfF9k1vXv8gNV"; // Replace with your actual restaurant ID
//     const results = await calculateMeanDemandAndSd(restaurantId); // gives the mean and sd as an object 

//     if (results) {
//         const OULResults = calculateOULForAllItems(results.itemMean, results.itemSD);

//         // Log OUL results for each item
//         for (const [item, params] of Object.entries(OULResults)) {
//             console.log(`Item: ${item}`);
//             console.log(`  Mean Demand TL: ${params.meanDemandTL}`);
//             console.log(`  Std Dev TL: ${params.stdDevTL}`);
//             console.log(`  Safety Stock: ${params.safetyStock}`);
//             console.log(`  Order Up to Level: ${params.OUL}`);
//         }
//     } else {
//         console.log("No results returned.");
//     }
// }

// main(); // Call the main function

</script>