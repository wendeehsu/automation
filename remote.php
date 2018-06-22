<?php

$link = mysqli_connect("localhost", "newuser1", "lab301", "newdb2");

if (!$link) {
	echo "Error: Unable to connect to MySQL." . PHP_EOL;
	echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
	echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
	exit;
}

#remote.php?move=1&clamp=0

$move_no=$_GET["move"];
$clamp_no=$_GET["clamp"];
echo "move no: ";
echo ($move_no);
echo "    clamp status:" ;
echo ($clamp_no);

$query = "UPDATE remote SET Direction = $move_no, Clamp = $clamp_no";
$result = mysqli_query($link,$query) or trigger_error("Error ". mysqli_error($link));

$sent = "SELECT send_status FROM remote";
$result = mysqli_query($link, $sent) or trigger_error("Error" . mysqli_error($link));
$row = mysqli_fetch_row($result);
if($row[0]){
    echo "    remote delivered";
}
else{
    echo "   fail";
}
mysqli_close($link);
?>