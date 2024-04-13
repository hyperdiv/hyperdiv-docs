window.hyperdiv.registerPlugin("leaflet", ctx => {
  const L = window.L;

  const props = {...ctx.initialProps};

  const mapContainer = document.createElement("div");
  mapContainer.style.width = "100%";
  mapContainer.style.height = "100%";
  ctx.domElement.appendChild(mapContainer);

  const map = L.map(mapContainer);
  map.setView([props.lat, props.lng], props.zoom);

  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
  }).addTo(map);

  map.on("zoomend", () => {
    props.zoom = map.getZoom();
    ctx.updateProp("zoom", props.zoom);
  });

  map.on("moveend", () => {
    const center = map.getCenter();
    props.lat = center.lat;
    props.lng = center.lng;
    ctx.updateProp("lat", props.lat);
    ctx.updateProp("lng", props.lng);
  });

  ctx.onPropUpdate((propName, propValue) => {
    props[propName] = propValue;
    map.setView([props.lat, props.lng], props.zoom);
  });
  
  const resizeObserver = new ResizeObserver(() => map.invalidateSize());
  resizeObserver.observe(mapContainer);
});
