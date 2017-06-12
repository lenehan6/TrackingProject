<?php
/**
 * Created by PhpStorm.
 * User: jameslenehan
 * Date: 09.06.17
 * Time: 10:41
 */

$g_link = false;

function GetDbConnection(){
    global $g_link;
    if ( $g_link )
        return $g_link;

    $servername = "localhost";
    $username = "php";
    $password = "SN30beelnezQjU3W";
    $dbname = "data";

    $g_link = new mysqli($servername, $username, $password, $dbname);
    if ($g_link->connect_error) {
        die("Connection failed: " . $g_link->connect_error);
    }
    return $g_link;
}


?>