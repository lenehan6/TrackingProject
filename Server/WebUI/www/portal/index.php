<?php

include( "../cycleproPHP.php" );

$username   = $_REQUEST["cp_user"];
$pw         = $_REQUEST["cp_pw"];

if ( $username ) if ( $pw )
    login( $username, $pw );

//die( $user->key );
if ( user()->key )
{
    $newURL = "/portal/account?cp_user=".user()->id."&cp_key=".user()->key;
    header('Location: '.$newURL);
    exit();
}

?>



<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="../style.css"></link>
    <meta charset="UTF-8">
    <title>CyclePro - Login</title>
</head>
<body style="background-color: #153359">

<div class="portal-login-background-image">
    <img src="../graphics/portal-background.jpg" style="width: 100%;">
</div>

<div class="portal-login-dialog" align="right">
    <div class="portal-login-box" height="200px" width="50%">
        <img src="../graphics/banner.png" width="300px">
        <form>
        <table width="100%">
            <tr>
                <td>User:</td>
                <td><input name="cp_user" type="text" width="100%"/></td>
            </tr>
            <tr>
                <td>Password:</td>
                <td><input name="cp_pw" type="password" width="100%"/></td>
            </tr>
<?php
if ( user()->key == -1 )
{
?>
            <tr>
                <td colspan="2" style="font-weight: bold; color: red">Username or password is incorrect</td>
            </tr>
            </tr>
<?php
}
?>
            <tr>
                <td></td>
                <td style="text-align: right"><input type="submit" value="Login" style="width: auto;" /></td>
            </tr>
        </table>

        </form>
    </div>
</div>

</body>
</html>