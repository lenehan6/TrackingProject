/**
 * Created by jameslenehan on 09.06.17.
 */

var user = <?php echo $_REQUEST["cp_user"]; ?>;
console.log( user );


var div = document.getElementById("menu-item-13");
console.log( div );


if ( user )
{
    div.innerHTML = "";

    var table = ce("table");
    var tr = ce("tr");

    var a = ce("a");
    a.href = "/portal/logout.php";
    a.className = "slide-btn-sm";
    tr.appendChild( a );
    table.appendChild( tr );

    var tr = ce("tr");
    tr.innerHTML = "You are logged in as user " + user;
    table.appendChild( tr );

    div.appendChild( table );

}