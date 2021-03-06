//= require jquery
//= require bootstrap
//= require ol-debug.js


var authKey;
var clusterLayer;
var map;
var popupContent = document.getElementById("popup-content");
$(document).ready(
	function() {
		$(".alert").alert();
		$(".alert").html("Setting up map...");

		var overlay = createOverlay();
		map = new ol.Map({
			layers: [new ol.layer.Tile({ source: new ol.source.OSM() })],
			target: "map",
			overlays: [overlay],
			view: new ol.View({
				center: [0, 0],
				zoom: 3
			})
		});

		map.on('singleclick', function(evt) {
			var feature = map.forEachFeatureAtPixel(evt.pixel, function(feature, layer) { return feature; });
			if (feature) {
				overlay.setPosition(evt.coordinate);
				popupContent.innerHTML = "";
				if (feature.getProperties().features.length > 1) {
					popupContent.innerHTML += "There are multiple features in this cluster. Please click on only one.";
				}	
				else {
					$.each(
						feature.getProperties().features[0].getProperties().attributes,
						function(i, x) {
							popupContent.innerHTML += "<b>" + i + ":</b> ";
							if (i == "Photos") { 
								popupContent.innerHTML += "<br>";
								$.each(
									x,
									function(j, y) {
										popupContent.innerHTML += 
											"<a id = 'href" + j + "' target = '_blank'>" + 
												"<img height = '100px' id = 'img" + j + "'/>" + 
											"</a><br><br>";
										$.ajax({
											contentType: "application/json",
											dataType: "json",
											headers: { "X-ApiToken": authKey },
											success: function (data) {
   												var imageUrl = data.photo.original;
												$("#href" + j).attr("href", imageUrl);
												$("#img" + j).attr("src", imageUrl);
											},
											url: "https://api.fulcrumapp.com/api/v2/photos/" + y.photo_id + ".json"
										});
									}
								);
							}
							else { popupContent.innerHTML += x + "<br>"; }
						}
					);
				}
			}
		});

		addClusterLayer();
		$(".alert").append(" Done!<br>");

		addFulcrumData();
	}
);

function addClusterLayer() {
	clusterLayer = new ol.layer.Vector({
		source: new ol.source.Cluster({
			distance: 20, 
			source: new ol.source.Vector()
		}),
		style: function(feature, resolution) {
			var size = feature.get('features').length;
			var style = new ol.style.Style({
				image: new ol.style.Circle({
					radius: 10,
					stroke: new ol.style.Stroke({
						color: '#000'
					}),
					fill: new ol.style.Fill({
						color: '#3399CC'
					})
				}),
				text: new ol.style.Text({
					text: size.toString(),
					fill: new ol.style.Fill({
						color: '#000'
					})
				})
			});


			return style;
		}
	});

	map.addLayer(clusterLayer);
}

function addFulcrumData() { getAuthenticationKey(); }

function addRecordsToMap(array) {	
	var features = [];
	$.each(
		array,
		function(i, x) {
			var point = new ol.geom.Point(ol.proj.transform([x.longitude, x.latitude], "EPSG:4326", "EPSG:3857"));
			delete x.latitude;
			delete x.longitude;
			var feature = new ol.Feature({
				attributes: x,
				geometry: point
			});
			features.push(feature);
		}	
	);

	clusterLayer.getSource().getSource().addFeatures(features);
}

function createOverlay() {
	var container = document.getElementById("popup");

	var closer = document.getElementById("popup-closer");
	closer.onclick = function() {
		overlay.setPosition(undefined);
		closer.blur();
		

		return false;
	};

	var overlay = new ol.Overlay( ({
		element: container,
		autoPan: true,
		autoPanAnimation: { duration: 250 }
	}));


	return overlay;
}

function getAuthenticationKey() {
	$(".alert").append("Getting user authentication key...");
	$.ajax({
		contentType: "application/json",
		dataType: "json",
		headers: { "Authorization": "Basic " + btoa(email + ":" + password) },
		success: function(data) { 
			$(".alert").append(" Done!<br>");
			authKey = data.user.contexts[0].api_token;
			getFormDetails(); 
		},
		url: "https://api.fulcrumapp.com/api/v2/users.json",
	});
}

function getFormDetails() {
	$(".alert").append("Getting form details...");
	$.ajax({
		contentType: "application/json",
		dataType: "json",
		headers: { "X-ApiToken": authKey },
		success: function (data) { 
   			$.each(
				data.forms,
				function(i, x) {
					if (x.name == "Starbucks") {
						$(".alert").append(" Done!<br>");
						getRecords(x, 1);
						

						return false;
					}
				}
			);
		},
		url: "https://api.fulcrumapp.com/api/v2/forms.json",
	});
}

function getRecords(form, pageNumber) { 
	$(".alert").append("Getting records... page " + pageNumber + "... ");

	var records = [];
	$.ajax({
		data: {form_id: form.id, page: pageNumber},
		contentType: "application/json",
		dataType: "json",
		headers: { "X-ApiToken": authKey},
		success: function (data) { 
			$(".alert").append(" Done!<br>");
			if (pageNumber < data.total_pages) { 
				pageNumber++;
				getRecords(form, pageNumber);
			}
			$.each(
				data.records,
				function(i, x) {
					var record = {latitude: x.latitude, longitude: x.longitude};
					$.each(
						x.form_values, 
						function(j, y) {				
							$.each(
								form.elements, 
								function(k, z) {
									if (z.key == j) {
										record[z.label] = y;
											
			
										return false;
									}
								}
							);
						}
					);
					records.push(record);
				}
			);
			addRecordsToMap(records);
		},
		url: "https://api.fulcrumapp.com/api/v2/records.json",
	});
}

