var map;
var markers = [];
var markerRows = [];
var markerColors = ["green", "red", "black"];

var Settings;
GetSettings("GroupNames", function( data ){ Settings = data; });

var timer_divRunningTime = setInterval(myTimer, 100);

function myTimer() {
    var d = new Date();
    document.getElementById("divRunningTime").innerHTML = d.toLocaleTimeString();
}

function initMap() {

    var styledMapType = new google.maps.StyledMapType(

        [
            {
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#ebe3cd"
                    }
                ]
            },
            {
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#523735"
                    }
                ]
            },
            {
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "color": "#f5f1e6"
                    }
                ]
            },
            {
                "featureType": "administrative",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "color": "#c9b2a6"
                    }
                ]
            },
            {
                "featureType": "administrative.land_parcel",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "color": "#dcd2be"
                    }
                ]
            },
            {
                "featureType": "administrative.land_parcel",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#ae9e90"
                    }
                ]
            },
            {
                "featureType": "landscape.natural",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#dfd2ae"
                    }
                ]
            },
            {
                "featureType": "poi",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#dfd2ae"
                    }
                ]
            },
            {
                "featureType": "poi",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#93817c"
                    }
                ]
            },
            {
                "featureType": "poi.attraction",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.business",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.government",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#a5b076"
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#447530"
                    }
                ]
            },
            {
                "featureType": "poi.place_of_worship",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.school",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.sports_complex",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#f5f1e6"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#fdfcf8"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#f8c967"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "color": "#e9bc62"
                    }
                ]
            },
            {
                "featureType": "road.highway.controlled_access",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#e98d58"
                    }
                ]
            },
            {
                "featureType": "road.highway.controlled_access",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "color": "#db8555"
                    }
                ]
            },
            {
                "featureType": "road.local",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#806b63"
                    }
                ]
            },
            {
                "featureType": "transit.line",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#dfd2ae"
                    }
                ]
            },
            {
                "featureType": "transit.line",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#8f7d77"
                    }
                ]
            },
            {
                "featureType": "transit.line",
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "color": "#ebe3cd"
                    }
                ]
            },
            {
                "featureType": "transit.station",
                "elementType": "geometry",
                "stylers": [
                    {
                        "color": "#dfd2ae"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#b9d3c2"
                    }
                ]
            },
            {
                "featureType": "water",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#92998d"
                    }
                ]
            }
        ], {name: 'Styled Map'}

    );

    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 49.012750, lng: 8.427848},
        zoom: 17,
        disableDefaultUI: true,
        mapTypeControlOptions: {
            mapTypeIds: ['roadmap', 'satellite', 'hybrid', 'terrain',
                'styled_map']
        }
    });
    //Associate the styled map with the MapTypeId and set it to display.
    map.mapTypes.set('styled_map', styledMapType);
    map.setMapTypeId('styled_map');

    var kmlLayer = new google.maps.KmlLayer({
        url: "http://localhost:8081/api/course/get",
        map: map
    });

    //$.getJSON("/api/locations/get", data="", plotDevices );

    $.getJSON("/api/summary/get", data="", plotDevices2 );


}

function plotDevices( list ){
    for (var i = 0; i < list.length; i++){
        m = list[i];
        var marker;
        //console.log( m, markers );
        if ( markers[m.id] ){
            marker = markers[m.id];
        } else {
            marker = new google.maps.Marker({
                position: {lat: m.details.lat, lng: m.details.lng},
                map: map,
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: 8,
                    strokeColor: markerColors[0]
                }
            });

            var table = gei("tabDevices");
            var tr = ce("tr");

            var td = ce("td");
            td.style.backgroundColor = markerColors[0];
            tr.appendChild( td );

            //chk
            var td = ce("td");
            var chk = ce("input");
            chk.type = "checkbox";
            chk.deviceId = m.id;
            chk.checked = m.isEnabled;
            chk.id = "device" + m.id + "_isEnabled";
            td.appendChild(chk);
            tr.appendChild( td );
            marker.isEnabled = chk;
            chk.onclick = function()
            {
                gei("btnDevicesSave").hidden = false;
            }


            //name
            var td = ce("td");

            var btn = ce("button");
            btn.type = "button";
            btn.innerHTML = "<img width='10px' src='http://findicons.com/files/icons/99/office/128/edit.png'/>";
            btn.style.marginRight = "6px";
            btn.td = td;
            btn.tr = tr;
            btn.hidden = true;
            td.appendChild( btn );
            tr.btn = btn;
            btn.onclick = function(){
                this.tr.edit();
            }
            tr.onmouseover = function(){
                if ( !this.isEditing )
                    this.btn.hidden = false;
            }
            tr.onmouseout = function(){
                if ( !this.isEditing )
                    this.btn.hidden = true;
            }

            var p = ce("div");
            p.style.display = "inline";
            p.id = "device" + m.id + "_name";
            p.innerHTML = m.name;
            td.appendChild( p );

            tr.p = p;
            tr.isEditing = false;

            var input = ce("input");
            input.type = "text";
            input.hidden = true;
            input.value = m.name;
            td.appendChild( input );

            tr.input = input;

            tr.appendChild( td );
            marker.name = td;


            tr.edit = function(){
                this.isEditing      = true;
                this.p.style.display = "none";
                this.btn.hidden     = true;
                this.input.hidden   = false;
                this.input.value    = this.name;

                gei("btnDevicesSave").hidden = false;

            }

            tr.save = function(){
                this.isEditing      = false;
                this.btn.hidden     = false;
                this.p.style.display = "inline";
                this.input.hidden   = true;
                this.p.innerHTML    = this.input.value;
                this.name           = this.input.value;

                gei("btnDevicesSave").hidden = true;
            }



            //label
            var td = ce("td");
            td.id = "device" + m.id + "_speed";
            var div = ce("div");
            div.innerHTML = m.speed;
            marker.speed = div;
            td.appendChild( div );
            tr.appendChild( td );
            marker.label = td;

            //distance
            var td = ce("td");
            td.id = "device" + m.id + "_distance";
            td.innerHTML = m.distance;
            tr.appendChild( td );
            marker.distance = td;

            table.appendChild( tr );

            marker.getSaveData = function()
            {
                var s = {};
                s.id        = this.deviceId;
                s.isEnabled = this.isEnabled.checked;
                s.name      = this.name;
                return s;
            }

            marker.tr = tr;
            markers[ m.id ] = marker;
            markers[ m.id ].data = m;

            markerColors = markerColors.slice(1);

        }

        marker.data = m;
        marker.setPosition({lat: m.details.lat, lng: m.details.lng});
        //marker.name.innerHTML = m.name;
        marker.distance.innerHTML = m.distance.toFixed(1);
        marker.speed.innerHTML = m.speed.toFixed(1);
        //marker.label.innerHTML = m.label;
        //marker.isEnabled.checked = m.isEnabled;
        marker.deviceId = m.id;

    }

    window.setTimeout( function(){
        $.getJSON("/api/locations/get", data="", plotDevices );
    }, 100);

}

function plotDevices2( data ){
    var groups = data.groups;


    plotDevices( data.devices );

    window.setTimeout( function(){
        $.getJSON("/api/summary/get", data="", plotDevices2 );
    }, 100);
}

function Save_Devices(){
    gei("btnDevicesSave").enabled = false;
    var list = [];
    for ( var m in markers ){
        var mkr = markers[m];
        mkr.tr.save();
        list[ "'" + mkr.deviceId + "'" ] = mkr.getSaveData();
    };

    console.log( list );

    var req = $.ajax({
        url:            "/api/locations/set",
        type:           "POST",
        data:           list,
        dataType:       "json",
        success:        function(){
            gei("btnDevicesSave").enabled = true;
            gei("btnDevicesSave").hidden = true;
        },
        fail:           function()
        {
            alert( "/api/locations/set FAILED, try again");
            gei("btnDevicesSave").enabled = true;
        }
    });

}




/**
 * Created by jameslenehan on 22.05.17.
 */
