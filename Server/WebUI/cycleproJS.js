/**
 * Created by jameslenehan on 05.06.17.
 */

function popup( link, name ){

    var div = ce("div");
    div.className = "popupBackground";
    div.id = "popupBackground";
    div.edited = false;
    div.align = "center";
    div.onclick = function(){
        var close = true;
        if ( this.edited )
            close = confirm( "Save?" )

        if ( close )
            document.body.removeChild( div );

    };


    var divBody = ce("div");
    divBody.className = "popupBody";
    divBody.id = "popup" + name;
    divBody.onclick = function(){
        event.stopPropagation();
    };
    div.appendChild( divBody );

    $.ajax({
        url: link,
        success: function (result) {
            divBody.innerHTML = result;
        }
    });

    document.body.appendChild( div );

}



function gei(id){
    return document.getElementById(id);
}

function ce(e){
    return document.createElement(e);
}

function ac(p, c){
    return p.appendChild(c);
}

function GetSettings( str, callback )
{
    $.getJSON("/api/settings/get", data=str, callback)
}

function timeformat( secs ){
    var str = "";

    var h = Math.floor(secs / 60 / 60);
    if ( h > 0 )
        str += h + "h";

    var m = Math.floor( (secs - (h*60*60))/60 );
    if ( (h > 0) ||
        (m > 0) )
        str += ((m<10 && h>0)?"0":"") + m + '"';

    var s = Math.floor( secs )%60;
    str += (((m>0 || h>0) & (s<10))?"0":"") + s + "'";

    return str;
}


