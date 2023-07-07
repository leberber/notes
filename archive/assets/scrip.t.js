window.myNamespace = Object.assign({}, window.myNamespace, {


    point2: {
        pointToLayer: function(feature, latlng) {
            // console.log(feature.properties.is_gig)
            const flag = L.icon({
                iconUrl: `assets/${feature.properties.is_gig}.svg`,
                iconSize: [12, 12]
            });
            return L.marker(latlng, {
                icon: flag
            });

        }
    },

    point: {
        pointToLayer: function(feature, latlng, context) {

            const {
                classes,
                colorscale,
                circleOptions,
                colorProp
            } = context.props.hideout;

            const value = feature.properties[colorProp]; // get value the determines the color

            for (let i = 0; i < classes.length; ++i) {

                if (value == classes[i]) {

                    circleOptions.fillColor = colorscale[i]; // set the fill color according to the class
                    console.log(colorscale[i])
                }
            }

            return L.circleMarker(latlng, circleOptions); // sender a simple circle marker.
        },

    },

    cluster: {
        pointToLayer: function(feature, latlng, index, context) {
            const {
                classes,
                colorscale,
                colorProp
            } = context.props.hideout;
            const leaves = index.getLeaves(feature.properties.cluster_id);

            const counts = {};
            for (let i = 0; i < leaves.length; ++i) {
                counts[leaves[i].properties[colorProp]] = counts[leaves[i].properties[colorProp]] ? counts[leaves[i].properties[colorProp]] + 1 : 1;
            }

            function createCharty(coun) {

                let svg = '<svg  viewBox="0 0 20 20">';
                let wedges = []
                var pieData = Object.values(coun)
                var totals = pieData.reduce(add, 0);

                function add(accumulator, a) {
                    return accumulator + a;
                }
                const mt = { 'NONE GIG': 'black', 'GIG': 'red' }
                let co = 0
                for (const [key, value] of Object.entries(coun)) {

                    co += value;
                    perr = (co * 100) / totals

                    s = `<circle r = "5" cx = "10" cy = "10"
                    fill = "transparent"
                    stroke = "${mt[key]}""
                    stroke-width = "10"
                    stroke-dasharray = "calc(${perr} * 31.4 / 100) 31.4"
                    transform = "rotate(-90) translate(-20)"/>`
                    wedges.push(s)
                }
                wedges = wedges.reverse()
                num_points = feature.properties.point_count_abbreviated
                svg += wedges
                svg += '<circle r="6" cx="10" cy="10" fill="white"/>'
                svg += `<g class="chart-text">
                    <text x="50%" y="50%" class="chart-number">
                      ${num_points}
                    </text>
                  </g>`
                svg += '</svg>';

                return svg

            }

            const icon = L.divIcon.scatter({
                html: createCharty(counts),
                className: "marker-cluster",
                iconSize: L.point(40, 40),
            });

            return L.marker(latlng, {
                icon: icon
            })
        }
    },

    dbscanArea: {
        style: function(feature) {
            return {
                fillColor: 'transparent',
                weight: 2,
                opacity: 1,
                color: '#A020F0', //Outline color
                fillOpacity: 0.5
            };
        }

    },




    gig_poly: {
        style: function(feature) {
            return {
                fillColor: 'transparent',
                weight: 4,
                opacity: 1,
                color: 'red', //Outline color
                fillOpacity: 0.5
            };
        }

    },

    none_gig_poly: {
        style: function(feature) {
            return {
                fillColor: 'transparent',
                weight: 4,
                opacity: 1,
                color: 'black', //Outline color
                fillOpacity: 0.5
            };
        }

    },



    censusGroup: {
        style: function() {
            return {
                fillColor: 'pink',
                weight: 0.8,
                opacity: 1,
                color: 'white', //Outline color
                fillOpacity: 0.5
            };
        }
    },


    censusBlock: {
        style: function() {
            return {
                fillColor: 'red',
                weight: 0.8,
                opacity: 1,
                color: 'white', //Outline color
                fillOpacity: 0.5
            };
        }
    },

    censusPlace: {
        style: function() {
            return {
                fillColor: 'green',
                weight: 0.8,
                opacity: 1,
                color: 'white', //Outline color
                fillOpacity: 0.5
            };
        }
    }
})


window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        large_params_function: function(largeValue1, largeValue2) {
            return someTransform(largeValue1, largeValue2);
        }
    }
});