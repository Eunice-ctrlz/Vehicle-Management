document.addEventListener('DOMContentLoaded', function() {
    // Find the lat/lng input boxes
    const latInput = document.getElementById('id_latitude');
    const lngInput = document.getElementById('id_longitude');

    if (latInput && lngInput) {
        // Create a div for the map
        const mapDiv = document.createElement('div');
        mapDiv.id = 'admin-map';
        mapDiv.style.height = '300px';
        mapDiv.style.marginBottom = '20px';
        latInput.closest('.form-row').before(mapDiv);

        // Initialize the map
        const map = L.map('admin-map').setView([latInput.value || -1.28, lngInput.value || 36.81], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        // Add a draggable marker
        const marker = L.marker([latInput.value || -1.28, lngInput.value || 36.81], {draggable: true}).addTo(map);

        // Update inputs when marker is dragged
        marker.on('dragend', function(e) {
            const position = marker.getLatLng();
            latInput.value = position.lat.toFixed(6);
            lngInput.value = position.lng.toFixed(6);
        });

        // Update marker when inputs change manually
        [latInput, lngInput].forEach(input => {
            input.addEventListener('change', () => {
                marker.setLatLng([latInput.value, lngInput.value]);
                map.panTo([latInput.value, lngInput.value]);
            });
        });
    }
});