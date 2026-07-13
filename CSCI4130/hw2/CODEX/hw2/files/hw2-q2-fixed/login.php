<?php
require_once 'config.php';

// Handle logout
if (isset($_GET['action']) && $_GET['action'] === 'logout') {
    session_destroy();
    header('Location: index.php');
    exit;
}

// Redirect if already logged in
if (is_logged_in()) {
    header('Location: index.php');
    exit;
}

$error = '';

// Handle login form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = trim($_POST['username'] ?? '');
    $password = $_POST['password'] ?? '';

    if (!empty($username) && !empty($password)) {
        // Verify CSRF token
        if (!verify_csrf_token($_POST['csrf_token'] ?? '')) {
            $error = 'Invalid request.';
        } else {
        // Use prepared statement to prevent SQL injection
        $stmt = $db->prepare("SELECT * FROM users WHERE username = :username");
        $stmt->bindValue(':username', $username, SQLITE3_TEXT);
        $result = $stmt->execute();
        $user = $result->fetchArray(SQLITE3_ASSOC);

        if ($user && password_verify($password, $user['password'])) {
            session_regenerate_id(true);
            $_SESSION['username'] = $user['username'];
            $_SESSION['role'] = $user['role'];
            $_SESSION['user_id'] = $user['id'];
            header('Location: index.php');
            exit;
        } else {
            $error = 'Invalid username or password.';
        }
        }
    } else {
        $error = 'Please fill in all fields.';
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Login - Bookstore</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="header">
        <h1>Bookstore &mdash; Login</h1>
        <div class="nav"><a href="index.php">&larr; Back to Home</a></div>
    </div>

    <div class="block">
        <?php if (!empty($error)): ?>
            <p class="error"><?= sanitize_output($error) ?></p>
        <?php endif; ?>

        <form method="POST" action="login.php">
            <input type="hidden" name="csrf_token" value="<?= generate_csrf_token() ?>">
            <label>Username: <input type="text" name="username" required></label>
            <label>Password: <input type="password" name="password" required></label>
            <input type="submit" value="Login">
        </form>
        <p class="hint">Demo accounts: admin/admin123, staff/staff123</p>
    </div>
</body>
</html>
