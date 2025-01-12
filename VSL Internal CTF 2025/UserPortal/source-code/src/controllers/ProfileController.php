<?php
require_once __DIR__ . '/../includes/init.php';

class ProfileController
{
    public function index()
    {
        if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true) {
            header("Location: index.php?page=login");
            exit();
        }
        $success = "";
        $error = "";
        if ($_SERVER["REQUEST_METHOD"] == "POST") {
            $fullname = isset($_POST['fullname']) ? trim($_POST['fullname']) : '';
            $bio = isset($_POST['bio']) ? trim($_POST['bio']) : '';

            if (!empty($fullname) && !empty($bio)) {
                $_SESSION['fullname'] = $fullname;
                $_SESSION['bio'] = $bio;
                $success = "Profile updated successfully.";
            } else {
                $error = "All fields are required.";
            }
        }
        $fullname = isset($_SESSION['fullname']) ? $_SESSION['fullname'] : "";
        $bio = isset($_SESSION['bio']) ? $_SESSION['bio'] : "";
        include __DIR__ . '/../views/profile.php';
    }
}
?>