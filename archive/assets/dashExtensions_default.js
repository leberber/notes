window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(feature, latlng) {
            const flag = L.icon({
                iconUrl: `assets/${feature.properties.iso2}.svg`,
                iconSize: [64, 48]
            });
            return L.marker(latlng, {
                icon: flag
            });

        }
    }
});