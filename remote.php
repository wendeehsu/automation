<?php

$link = mysqli_connect("localhost", "newuser1", "lab301", "newdb2");

if (!$link) {
	echo "Error: Unable to connect to MySQL." . PHP_EOL;
	echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
	echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
	exit;
}

<<<<<<< HEAD
#remote.php?move=1&clamp=0
=======
#remote.php?move=&clamp=0
>>>>>>> a10495655ed758eafc7abade5150cfc2e430ca29

$move_no=$_GET["move"];
$clamp_no=$_GET["clamp"];
echo "move no: ";
echo ($move_no);
echo "    clamp status:" ;
echo ($clamp_no);

<<<<<<< HEAD
$query = "UPDATE REMOTE SET Direction = $move_no, Clamp = $clamp_no";
$result = mysqli_query($link,$query) or trigger_error("Error ". mysqli_error($link));

$sent = "SELECT send_status FROM REMOTE";
$result = mysqli_query($link, $sent) or trigger_error("Error" . mysqli_error($link));
$row = mysqli_fetch_row($result);

=======
$query = "UPDATE remote SET Direction = $move_no, Clamp = $clamp_no";
$result = mysqli_query($link,$query) or trigger_error("Error ". mysqli_error($link));

echo($result);
echo "type of move_no=" . gettype($move_no) . "type of clamp_no= " . gettype($clamp_no);

$row = mysqli_fetch_row($result);
if($row[0]){
    echo "    remote delivered";
}
else{
    echo "   fail";
}
>>>>>>> a10495655ed758eafc7abade5150cfc2e430ca29
mysqli_close($link);
?>