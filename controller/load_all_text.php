<?php
    include_once("../util/koneksi.php"); 
    $perPage = 5;
    $page = 0;

    if (isset($_POST['page'])) { 
        $page  = $_POST['page']; 
    } else { 
        $page=1; 
    };

    $startFrom = ($page-1) * $perPage; 
    $sqlQuery = "SELECT id, user_screen_name, text , text_bersih FROM dokumen ORDER BY id ASC LIMIT $startFrom, $perPage";  

    $result = mysqli_query($conn, $sqlQuery); 
    $paginationHtml = '';

    while ($row = mysqli_fetch_assoc($result)) {  
        $paginationHtml.='<tr>';  
        $paginationHtml.='<td>'.$row["id"].'</td>';
        $paginationHtml.='<td>'.$row["user_screen_name"].'</td>';
        $paginationHtml.='<td>'.$row["text"].'</td>';  
        $paginationHtml.='<td>'.$row["text_bersih"].'</td>';  
        $paginationHtml.='</tr>';  
    }

    $jsonData = array(
        "html"  => $paginationHtml, 
    );
    
    echo json_encode($jsonData); 
?>