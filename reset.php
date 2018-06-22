<?php

$link = mysqli_connect("localhost", "newuser1", "lab301", "newdb2");

if (!$link) {
	echo "Error: Unable to connect to MySQL." . PHP_EOL;
	echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
	echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
	exit;
}

$query = "UPDATE Client_info SET color = 0, send_status = 0 WHERE send_status = 1";
$result = mysqli_query($link,$query) or trigger_error("Error ". mysqli_error($link));

$row = mysqli_fetch_row($result);

if($row[0]){
    echo "    clean db";
}
else{
    echo "    fail to clean db";
}

mysqli_close($link);
?>