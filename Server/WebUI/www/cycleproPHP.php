<?php
/**
 * Created by PhpStorm.
 * User: jameslenehan
 * Date: 09.06.17
 * Time: 10:38
 */

$cp_user = false;

#require( $_SERVER['HTTP_HOST']."/db.php" );
include_once( "db.php" );


class _user
{
    var $id;
    var $username;
    var $key;
}

function getKey( $id )
{
    return hash( "sha256", $id."--cp--" );
}

function checkKey( $id )
{
    return hash( "sha256", $id."--cp--") == $id;
}

function login( $username, $password )
{
    $user = new _user();

    $q = "SELECT * FROM users WHERE (id='".$username."' OR user='".$username."') AND pw='".$password."'";
    $result = mysqli_query( GetDbConnection() , $q );

    if ($result->num_rows > 0 ) {
        // output data of each row
        while($row = $result->fetch_assoc()) {
            $user->id           = (int) $row["id"];
            $user->username     = (string) $row["user"];
            $user->key          = (string) getKey( $row["id"] );

        }
    } else {
        die( "ERROR: ".mysqli_error() );
    }

    setcookie("cp_id",      $user->id,          time() + 60*60*24, "/");
    setcookie("cp_uname",   $user->username,    time() + 60*60*24, "/");
    setcookie("cp_key",     $user->key,         time() + 60*60*24, "/");

    global $cp_user;
    $cp_user        = $user;

    return $user;

}

function user(){
    global $cp_user;
    if ( $cp_user )
        return $cp_user;

    $cp_user            = new _user();
    $cp_user->id        = $_COOKIE["cp_id"];
    $cp_user->key       = $_COOKIE["cp_key"];
    $cp_user->username  = $_COOKIE["cp_uname"];

    return $cp_user;
}





?>