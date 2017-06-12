<?php
/**
 * Created by PhpStorm.
 * User: jameslenehan
 * Date: 09.06.17
 * Time: 12:45
 */

include( $_SERVER['DOCUMENT_ROOT']."/wp-blog-header.php" );

//Now, you need to get the active theme's folder, and get a relative path to that folder
$homeurl=home_url();
$ddir= get_bloginfo( 'template_directory');
$current_theme_relative_path=substr_replace($ddir, "", 0, strlen($homeurl));
//echo "<br/>The relative path to the currently active theme is ".$current_theme_relative_path;

//Once you have the path, include the header and footer, adding your custom php code in between.
// Include the specific theme header you need
include( $_SERVER['DOCUMENT_ROOT'].$current_theme_relative_path."/header.php" );


?>

