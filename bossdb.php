<?php

$link = mysqli_connect("localhost", "newuser1", "lab301", "newdb2");

if (!$link) {
	echo "Error: Unable to connect to MySQL." . PHP_EOL;
	echo "Debugging errno: " . mysqli_connect_errno() . PHP_EOL;
	echo "Debugging error: " . mysqli_connect_error() . PHP_EOL;
	exit;
}

$query = "SELECT * FROM Client_info";
$result = mysqli_query($link,$query) or trigger_error("Error ". mysqli_error($link));

if (mysqli_num_rows($result) > 0) {
    // output data of each row
    echo " | id | name | color | send_status | " . <br>;
    while($row = mysqli_fetch_assoc($result)) {
        echo " | " . $row["id"]. " | " . $row["name"]. " | " . $row["color"] . " | ". $row["send_status"] . " |" . <br>;
    }
} else {
    echo "0 results";
}

mysqli_close($link);
?> 