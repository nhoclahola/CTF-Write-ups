<div class="container">
    <h2>Welcome to Your Dashboard</h2>
    <?php if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true): ?>
        <p class="message">Hello, <?php echo htmlspecialchars($_SESSION['username'], ENT_QUOTES, 'UTF-8'); ?>! Explore the
            features available to you.</p>
    <?php else: ?>
        <p>Please click the <a href="#" id="login-button">Login</a> button to access your dashboard.</p>
    <?php endif; ?>
</div>