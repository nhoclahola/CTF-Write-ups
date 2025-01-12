<?php
require_once __DIR__ . '/../includes/init.php';
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>User Portal</title>
    <link rel="stylesheet" href="/assets/css/styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
</head>

<body>
    <div class="header">
        <img src="/assets/images/logo.png" alt="Logo">
        <h1>User Portal</h1>
    </div>

    <div class="navbar">
        <a href="index.php?page=home">Home</a>
        <a href="index.php?page=about">About</a>
        <?php if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true): ?>
            <a href="index.php?page=feedback">Feedback</a>
            <a href="index.php?page=profile">Profile</a>
            <a href="#" id="logout-link">Logout</a>
        <?php else: ?>
            <a href="#" id="login-link">Login</a>
        <?php endif; ?>
    </div>