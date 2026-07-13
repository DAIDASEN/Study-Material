<?php
require_once 'config.php';

// -------------------------------------------------------
// Access Control: Only admins can view the management page
// -------------------------------------------------------
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    if (!is_logged_in() || !is_admin()) {
        http_response_code(403);
        echo '<!DOCTYPE html><html><head><title>403</title>';
        echo '<link rel="stylesheet" href="style.css"></head><body>';
        echo '<div class="header"><h1>403 Forbidden</h1></div>';
        echo '<div class="block"><p>You need admin privileges to access this page.</p>';
        echo '<a href="index.php">Return to homepage</a></div>';
        echo '</body></html>';
        exit;
    }
}

// -------------------------------------------------------
// Handle POST actions (book management operations)
// -------------------------------------------------------
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Verify that the user is authenticated and authorized as admin
    if (!is_logged_in() || !is_admin()) {
        http_response_code(403);
        die('Admin privileges required.');
    }

    // Validate CSRF token to prevent cross-site request forgery
    if (!verify_csrf_token($_POST['csrf_token'] ?? '')) {
        http_response_code(403);
        die('Invalid request token.');
    }

    if (isset($_POST['action']) && $_POST['action'] === 'delete') {
        $book_id = intval($_POST['book_id']);
        $stmt = $db->prepare("DELETE FROM books WHERE id = :id");
        $stmt->bindValue(':id', $book_id, SQLITE3_INTEGER);
        $stmt->execute();
        header('Location: admin.php?msg=deleted');
        exit;
    }
}

$csrf = generate_csrf_token();

// Fetch all books for management view
$books = [];
$result = $db->query("SELECT * FROM books ORDER BY id ASC");
while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $books[] = $row;
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel - Bookstore</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="header">
        <h1>Admin Panel</h1>
        <div class="nav">
            <span>Logged in as <?= sanitize_output($_SESSION['username']) ?>
                  (<?= sanitize_output($_SESSION['role']) ?>)</span>
            <a href="index.php">&larr; Back to Home</a>
            <a href="login.php?action=logout">Logout</a>
        </div>
    </div>

    <?php if (isset($_GET['msg']) && $_GET['msg'] === 'deleted'): ?>
        <div class="block alert-success">Book has been deleted successfully.</div>
    <?php endif; ?>

    <div class="block">
        <h2>Manage Books</h2>
        <table>
            <tr>
                <th>ID</th><th>Title</th><th>Author</th>
                <th>Year</th><th>Added By</th><th>Action</th>
            </tr>
            <?php foreach ($books as $book): ?>
            <tr>
                <td><?= intval($book['id']) ?></td>
                <td><?= sanitize_output($book['title']) ?></td>
                <td><?= sanitize_output($book['author']) ?></td>
                <td><?= intval($book['year']) ?></td>
                <td><?= sanitize_output($book['added_by']) ?></td>
                <td>
                    <form method="POST" action="admin.php" style="display:inline">
                        <input type="hidden" name="csrf_token" value="<?= $csrf ?>">
                        <input type="hidden" name="action" value="delete">
                        <input type="hidden" name="book_id" value="<?= intval($book['id']) ?>">
                        <button type="submit" onclick="return confirm('Are you sure?')">Delete</button>
                    </form>
                </td>
            </tr>
            <?php endforeach; ?>
        </table>
    </div>
</body>
</html>
