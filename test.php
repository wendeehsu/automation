<?php

$link = mysqli_connect("localhost", "newuser1", "lab301", "newdb2");

if (!$link) {
	echo "Error: Unable to connect to MySQL." . PHP_EOL;
	echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
	echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
	exit;
}

$usr_no=$_GET["client"];
$usr_order=$_GET["merchandise"];
echo "Client no: ";
echo ($usr_no);
echo "    Object color:" ;
echo ($usr_order);

$query = "UPDATE Client_info SET color = $usr_order WHERE id = $usr_no";
$result = mysqli_query($link,$query) or trigger_error("Error ". mysqli_error($link));

$sent = "SELECT send_status FROM Client_info WHERE id = $usr_no";
$result = mysqli_query($link, $sent) or trigger_error("Error" . mysqli_error($link));
$row = mysqli_fetch_row($result);

if($row[0]){
    echo "    Package delivered";
}
else{
    echo "    Stop and stare";
}

mysqli_close($link);
?>