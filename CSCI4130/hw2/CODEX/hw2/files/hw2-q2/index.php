<?php
require_once 'config.php';
$csrf = generate_csrf_token();

// Fetch all books for the listing
$books = [];
$result = $db->query("SELECT * FROM books ORDER BY created_at DESC");
while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
    $books[] = $row;
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Bookstore</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="header">
        <h1>Bookstore</h1>
        <div class="nav">
            <?php if (is_logged_in()): ?>
                <span>Welcome, <?= sanitize_output($_SESSION['username']) ?></span>
                <?php if (is_admin()): ?>
                    <a href="admin.php">Admin Panel</a>
                <?php endif; ?>
                <a href="login.php?action=logout">Logout</a>
            <?php else: ?>
                <a href="login.php">Login</a>
            <?php endif; ?>
        </div>
    </div>

    <div class="block">
        <h2>Search for a Book</h2>
        <form method="GET" action="search.php">
            <input type="text" name="q" placeholder="Enter title or author...">
            <label>From year: <input type="number" name="year_from" placeholder="e.g. 1900"></label>
            <label>To year: <input type="number" name="year_to" placeholder="e.g. 2024"></label>
            <button type="submit">Search</button>
        </form>
    </div>

    <?php if (is_logged_in()): ?>
    <div class="block">
        <h2>Add a New Book</h2>
        <form method="POST" action="addbook.php">
            <input type="hidden" name="csrf_token" value="<?= $csrf ?>">
            <label>Title: <input type="text" name="title" required></label>
            <label>Author: <input type="text" name="author" required></label>
            <label>Year: <input type="number" name="year" value="2024"></label>
            <label>Description: <input type="text" name="description" placeholder="Brief description"></label>
            <input type="submit" value="Add Book">
        </form>
    </div>
    <?php endif; ?>

    <div class="block">
        <h2>All Books</h2>
        <?php if (empty($books)): ?>
            <p>No books in the database yet.</p>
        <?php else: ?>
        <table>
            <tr><th>Title</th><th>Author</th><th>Year</th></tr>
            <?php foreach ($books as $book): ?>
            <tr>
                <td>
                    <span title="<?= sanitize_text($book['description']) ?>">
                        <?= sanitize_output($book['title']) ?>
                    </span>
                </td>
                <td><?= sanitize_output($book['author']) ?></td>
                <td><?= intval($book['year']) ?></td>
            </tr>
            <?php endforeach; ?>
        </table>
        <?php endif; ?>
    </div>
</body>
</html>
