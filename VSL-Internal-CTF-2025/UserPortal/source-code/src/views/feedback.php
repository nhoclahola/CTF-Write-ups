<div class="container">
    <h2>Submit Your Feedback</h2>
    <?php if ($success): ?>
        <p class="message"><?php echo htmlspecialchars($success, ENT_QUOTES, 'UTF-8'); ?></p>
    <?php endif; ?>
    <?php if ($error): ?>
        <p class="error"><?php echo htmlspecialchars($error, ENT_QUOTES, 'UTF-8'); ?></p>
    <?php endif; ?>
    <form method="POST" action="index.php?page=feedback">
        <label for="feedback">Your Feedback</label>
        <textarea id="feedback" name="feedback" placeholder="Enter your feedback here" required></textarea>

        <input type="submit" value="Submit Feedback">
    </form>
</div>