// Define the Wayanad region
var wayanad = ee.Geometry.Polygon([
  [ 
    [75.93403139535545, 11.23242833402068], 
    [76.3322857898867, 11.23242833402068], 
    [76.3322857898867, 11.644308124929212], 
    [75.93403139535545, 11.644308124929212], 
    [75.93403139535545, 11.23242833402068]
  ]
]);

// Load DEM and calculate slope
var dem = ee.Image('USGS/SRTMGL1_003').clip(wayanad);
var slope = ee.Terrain.slope(dem).clip(wayanad);

// Load CHIRPS data for rainfall (June to August 2024)
var chirps = ee.ImageCollection('UCSB-CHG/CHIRPS/PENTAD')
               .filterBounds(wayanad)
               .filterDate('2000-06-01', '2024-08-02');

// Get the maximum rainfall image for the specified time period
var maxRainfall = chirps.max().clip(wayanad);

// Load built-up area data (single-band visualization)
var builtUp = ee.Image('ESA/GLOBCOVER_L4_200901_200912_V2_3').select('landcover').clip(wayanad);

// Load water bodies and drainage density
var hydro = ee.Image('WWF/HydroSHEDS/15ACC').clip(wayanad);

// Load soil texture data for 0 cm depth
var soil = ee.Image('OpenLandMap/SOL/SOL_TEXTURE-CLASS_USDA-TT_M/v02')
  .select('b0')
  .clip(wayanad);

// Load vegetation data (NDVI)
var sentinel2 = ee.ImageCollection('COPERNICUS/S2_SR')
  .filterBounds(wayanad)
  .filterDate('2023-01-01', '2023-12-31')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20))
  .median()
  .clip(wayanad);

var ndvi = sentinel2.normalizedDifference(['B8', 'B4']).rename('NDVI');

// Load deforestation patterns (tree cover loss)
var deforestation = ee.Image('UMD/hansen/global_forest_change_2022_v1_10')
  .select('loss')
  .clip(wayanad);

// Display added layers
Map.centerObject(wayanad, 10);
var ndviPalette = ['brown', 'yellow', 'green'];

Map.addLayer(ndvi, {min: -1, max: 1, palette: ndviPalette}, 'Vegetation (NDVI)');
Map.addLayer(dem, {min: 0, max: 3000, palette: ['white', 'black']}, 'Elevation (DEM)');
Map.addLayer(slope, {min: 0, max: 60, palette: ['00ff00', 'ff0000']}, 'Slope');
Map.addLayer(maxRainfall, {min: 0, max: 580, palette: ['#a8e6cf', '#d0f0c0', '#ffff00', '#ffcccb', '#ff0000']}, 'Total Rainfall (June-August)');
Map.addLayer(builtUp, {min: 0, max: 200, palette: ['green', 'orange', 'brown']}, 'Built-up Areas');
Map.addLayer(hydro, {min: 0, max: 1000, palette: ['blue', 'cyan']}, 'Drainage Density');
Map.addLayer(soil, {min: 2, max: 10, palette: ['yellow','orange','brown','black']}, 'Soil Texture');
Map.addLayer(deforestation, {min: 0, max: 2, palette: ['yellow','orange','red','brown']}, 'Deforestation Patterns');

var landslideAreas = ee.FeatureCollection([
  ee.Feature(ee.Geometry.Polygon([[[76.0011, 11.5121], [75.9968, 11.5090], [75.9910, 11.5046], [75.9980, 11.4985], [76.0061, 11.5014], [76.0120, 11.5031], [76.0011, 11.5121]]]), {'landslide': 1}),
  //ee.Feature(ee.Geometry.Polygon([[[76.06492886455786, 11.412836958181938], [76.06336245449316, 11.413867592258034], [76.06278309734594, 11.414519624128346], [76.06001505764257, 11.412794891405468], [76.05827698620092, 11.412395256717945], [76.05750451000463, 11.411911487659184], [76.05739722164404, 11.41085981294792], [76.0583628168894, 11.41085981294792], [76.0604871264292, 11.411574952175497], [76.06235394390356, 11.41252145720636], [76.06372723491918, 11.41237422329775]]]), {'landslide': 1}),
  ee.Feature(ee.Geometry.Polygon([[[76.12886963553443, 11.497798646566379], [76.13032875723853, 11.496915508352801], [76.13148747153296, 11.499144375662663], [76.1341053075315, 11.499102321725735], [76.14041386313453, 11.501162957250358], [76.14213047690406, 11.502803044135653], [76.14333210654273, 11.504779546405326], [76.14208756155982, 11.50469544020846], [76.13745270438208, 11.50208813564223], [76.13389073081031, 11.501835814564112], [76.13286076254859, 11.502172242618025], [76.13054333395972, 11.501289118119152], [76.12977085776343, 11.49880794399139]]]), {'landslide': 1}),
  ee.Feature(ee.Geometry.Polygon([[[76.13419050862464, 11.467344503027705], [76.13547796895179, 11.464652734962268], [76.13770956685218, 11.46583038664708], [76.14079947163734, 11.468606260477895], [76.14474768330726, 11.472055035410637], [76.14560599019202, 11.474242041588758], [76.14886755635413, 11.477270176014624], [76.14921087910804, 11.479625369214633], [76.15547651936683, 11.48441980890349], [76.15975489823813, 11.488252406374032], [76.16147151200767, 11.495990523078774], [76.15735163896079, 11.50507412799955], [76.14533534257407, 11.499691286378425], [76.15288844316001, 11.493635466575089], [76.1522017976522, 11.488252406374032], [76.1467086335897, 11.482196340783982], [76.14293208329673, 11.476813062208704], [76.13915553300376, 11.472102609213294]]]), {'landslide': 1}),
  //ee.Feature(ee.Geometry.Polygon([[[76.23361429564844, 11.412000853795194], [76.2344726025332, 11.409603030523183], [76.23541674010644, 11.408004470424085], [76.2361463009585, 11.407115977914607], [76.23709043853174, 11.406821504414411], [76.2376054226626, 11.408167666493942], [76.23786291472803, 11.409850360118618], [76.23786291472803, 11.411701311586574], [76.23769125335107, 11.413131583999869], [76.23721918456445, 11.414645982228437], [76.23696169249902, 11.415066646968851], [76.23623213164697, 11.412542649173123], [76.2361463009585, 11.410733770279226], [76.23477300994287, 11.412752983180106], [76.23400053374658, 11.413131583999869]]]), {'landslide': 1}),
  ee.Feature(ee.Geometry.Polygon([[[76.06381693370862,11.41455784727513], [76.06725016124769,11.416408768043217], [76.06467524059339,11.419269258207631], [76.06261530406995,11.416577032968897], [76.05849543102308,11.415399176393667], [76.05712214000745,11.411024237741659],[76.06381693370862,11.41455784727513]]]), {'landslide': 1}),
  ee.Feature(ee.Geometry.Polygon([[[76.2368350616039,11.41534413477794], [76.22893863826405,11.411305731479318], [76.23357349544179,11.40221911402469],[76.23803669124257,11.405921104380036], [76.23786502986562,11.413661473720198], [76.2368350616039,11.41534413477794]]]), {'landslide': 1})]);

// Define non-landslide areas
var nonLandslideAreas = ee.FeatureCollection([
  ee.Feature(ee.Geometry.Polygon([[[75.93506136361648, 11.27042058324548],[75.93437471810867, 11.250217753266979],[75.95703401986648, 11.253921711587148],[75.9635571521907, 11.262339621461324],[75.93506136361648, 11.27042058324548]]]),{'landslide': 0}),
  ee.Feature(ee.Geometry.Polygon([[[75.93505732058698, 11.338698513884776],[75.93471399783307, 11.326916507671985],[75.94020716189557, 11.326916507671985],[75.93986383914167, 11.338698513884776],[75.93505732058698, 11.338698513884776]]]),{'landslide': 0}),
  ee.Feature(ee.Geometry.Polygon([[[76.26087465707351,11.245840286572685], [76.26156130258133,11.27143068750205],[76.23409548226883,11.28018477569239],[76.20388307992508,11.260656059183047], [76.2052563709407,11.238432114530205], [76.26087465707351,11.245840286572685]]]),{'landslide': 0}),
  ee.Feature(ee.Geometry.Polygon([[[76.19881792907553,11.592215734078797], [76.1747853363021,11.572035814653306], [76.1967579925521,11.555218103229487],[76.22697039489584,11.567326957276316], [76.22765704040366,11.595578912312734], [76.19881792907553,11.592215734078797]]]), {'landslide': 0}),
  ee.Feature(ee.Geometry.Polygon([[[76.28544635044328, 11.359993235249794],[76.27892321811906, 11.363695774918648],[76.27926654087297, 11.354944240052939],[76.28544635044328, 11.359993235249794]]]),{'landslide': 0})
]);

// Define landslide and non-landslide areas
Map.addLayer(nonLandslideAreas, {color: 'blue'}, 'Non-Landslide Areas');
Map.addLayer(landslideAreas, {color: 'red'}, 'Landslide Areas');

// Combine layers into a single image
var combinedFeatures = dem
  .addBands(slope)
  .addBands(maxRainfall)
  .addBands(builtUp)
  .addBands(hydro)
  .addBands(soil)
  .addBands(ndvi)
  .addBands(deforestation)
  .rename(['elevation', 'slope', 'rainfall', 'builtUp', 'hydro', 'soil', 'vegetation', 'deforestation']);

// Sample features at landslide and non-landslide locations
var samples = combinedFeatures.sampleRegions({
  collection: landslideAreas.merge(nonLandslideAreas),
  properties: ['landslide'],
  scale: 30,
  tileScale: 8
});

// Export sample data for model training
Export.table.toDrive({
  collection: samples,
  description: 'Wayanad_Landslide_Samples',
  folder: 'EarthEngine Exports',
  fileFormat: 'CSV'
});

