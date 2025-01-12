<?php
include 'includes/router.php';
$page = isset($_GET['page']) ? $_GET['page'] : 'home';
routeRequest($page);
?>