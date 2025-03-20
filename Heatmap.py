// Create a heatmap by reducing points to an image based on probability
var heatmap = landslideData.reduceToImage({
  properties: ['landslide_probability'],
  reducer: ee.Reducer.mean()
});

// Create a Gaussian kernel to smooth the heatmap
var gaussianKernel = ee.Kernel.gaussian({
  radius: 2,  // Increase radius for more smoothing
  sigma: 3,  // Adjust sigma for different smoothness levels
  units: 'pixels'
});

// Apply the Gaussian filter (convolve the image with the kernel)
var smoothedHeatmap = heatmap.convolve(gaussianKernel);

// Mask regions with probability below 0.7
var highProbabilityAreas = smoothedHeatmap.updateMask(smoothedHeatmap.gt(0.70));

// Define visualization parameters for high probability areas
var highProbabilityVisParams = {
  min: 0.7,  // Minimum value for visualization
  max: 1,     // Maximum value for visualization
  palette: ['#FFFF00',    // Light Yellow for low probabilities
    '#FFD700',    // Yellow for moderate probabilities
    '#FF8C00',    // Orange-Yellow for slightly higher probabilities
    '#FF4500','#FF4433']  // Red color for high probabilities
};

// Visualize the filtered heatmap
Map.centerObject(landslideData, 10); // Zoom into the area of interest
Map.addLayer(highProbabilityAreas, highProbabilityVisParams, 'High Probability Areas');

// Add layers for reference
//Map.addLayer(nonLandslideAreas, {color: 'blue'}, 'Non-Landslide Areas');
//Map.addLayer(landslideAreas, {color: 'red'}, 'Landslide Areas');

// Export the high probability heatmap as a KML file for Google Earth
Export.image.toDrive({
  image: highProbabilityAreas,
  description: 'high_probability_landslide_heatmap',
  scale: 30,  // Keep the higher resolution for better output
  region: landslideData.geometry()
});
