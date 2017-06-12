<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="../../style.css"></link>
    <meta charset="UTF-8">
    <title>CyclePro - Account</title>
</head>

<?php
require_once( $_SERVER['DOCUMENT_ROOT'].'/wp-header-for-custom-file.php' );

require $_SERVER['DOCUMENT_ROOT'].'/cycleproPHP.php';

?>
<body>

<div class="container" style="font-size: smaller;">

<div class="boxDiv420">
    <div>User Details</div>
    <table>
        <tr>
            <td>User:</td>
            <td><?php echo user()->username." (".user()->id.")"; ?></td>
        </tr>
    </table>
</div>


<div class="boxDiv">
    <div>Events</div>
    <div id="divEventList">
    <?php
        $q = "SELECT e.* FROM `events` AS e INNER JOIN `eventaccessrights` AS a WHERE a.user=".user()->id." AND a.starts<NOW() AND a.expires>NOW() LIMIT 50";
        $result = mysqli_query( GetDbConnection(), $q );
        if ($result->num_rows > 0 ) {
    ?>
        <table style="position: static">
            <thead>
                <tr>
                    <th>#</th>
                    <th>Name</th>
                    <th>Location</th>
                    <th>Public Link</th>
                    <th></th>
                </tr>
            </thead>
            <tbody id="tabEventList">
            <?php
            while($row = $result->fetch_assoc()) {
                ?>
                <tr>
                    <td><a href="<?php echo "http://".$_SERVER["HTTP_HOST"]."/".$row["id"]."?cp_user=".$cp_user->id."&cp_key=".$cp_user->key; ?>"><?php echo $row["id"]; ?></a></td>
                    <td><?php echo $row["name"]; ?></td>
                    <td><?php echo $row["location"]; ?></td>
                    <td><a href="<?php echo "http://".$_SERVER["HTTP_HOST"]."/".$row["shortName"]; ?>"><?php echo "http://".$_SERVER["HTTP_HOST"]."/".$row["shortName"]; ?></a></td>
                    <td><button type="button" target="<?php echo "http://".$_SERVER["HTTP_HOST"]."/".$row["id"]."?cp_user=".$cp_user->id."&cp_key=".$cp_user->key; ?>">Open</button></td>
                </tr>
            <?php
            }
            if ( $result->num_rows == 50 )
            {
                echo "<tr colspan='5' onclick='LoadNextRecords(50)'>Load next 50 records<tr>";
            }
            ?>

            </tbody>
        </table>
    <?php } else { ?>
        No events assigned to this account.
    <?php } ?>
    </div>
</div>
</div>

</body>

<?php

require $_SERVER['DOCUMENT_ROOT'].'/wp-footer-for-custom-file.php';

?> 