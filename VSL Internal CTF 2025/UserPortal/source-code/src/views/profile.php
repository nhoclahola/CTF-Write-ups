<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Your Profile</title>
    <link rel="stylesheet" href="assets/css/styles.css">
</head>

<body>
    <?php include 'includes/header.php'; ?>

    <div class="container">
        <h2>Your Profile</h2>
        <?php if ($success): ?>
            <p class="message"><?php echo htmlspecialchars($success, ENT_QUOTES, 'UTF-8'); ?></p>
        <?php endif; ?>
        <?php if ($error): ?>
            <p class="error"><?php echo htmlspecialchars($error, ENT_QUOTES, 'UTF-8'); ?></p>
        <?php endif; ?>
        <form method="POST" action="index.php?page=profile">
            <label for="fullname">Full Name</label>
            <input type="text" id="fullname" name="fullname" placeholder="Enter your full name"
                value="<?php echo htmlspecialchars($fullname, ENT_QUOTES, 'UTF-8'); ?>" required>

            <label for="bio">Bio</label>
            <textarea id="bio" name="bio" placeholder="Tell us about yourself"
                required><?php echo htmlspecialchars($bio, ENT_QUOTES, 'UTF-8'); ?></textarea>

            <input type="submit" value="Update Profile">
        </form>

        <h3>Your Bio</h3>
        <p><?php echo nl2br(htmlspecialchars($bio, ENT_QUOTES, 'UTF-8')); ?></p>
    </div>

    <div class="footer">
        <p>&copy; 2024 VSL CTF Team. All rights reserved.</p>
    </div>
</body>

</html>