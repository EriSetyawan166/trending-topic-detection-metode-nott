<?php

include("../util/koneksi.php");

$sql = "TRUNCATE TABLE dokumen";
$conn->query($sql);
$conn->close();
header("Location: ../index.php");
?>