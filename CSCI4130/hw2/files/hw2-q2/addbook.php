<?php
require_once 'config.php';

// Authentication check — only logged-in users can add books
require_login();

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: index.php');
    exit;
}

// CSRF protection
if (!verify_csrf_token($_POST['csrf_token'] ?? '')) {
    http_response_code(403);
    die('Invalid request token. <a href="index.php">Go back</a>.');
}

// Validate required fields
$title = trim($_POST['title'] ?? '');
$author = trim($_POST['author'] ?? '');
$year = intval($_POST['year'] ?? date('Y'));
$description = trim($_POST['description'] ?? '');

if (empty($title) || empty($author)) {
    die('Title and author are required. <a href="index.php">Go back</a>.');
}

// Enforce input length limits to prevent abuse
if (strlen($title) > 200 || strlen($author) > 200 || strlen($description) > 500) {
    die('Input exceeds maximum length. <a href="index.php">Go back</a>.');
}

// Remove any HTML tags from the description for safe storage
$description = strip_tags($description);

// Insert the book using a prepared statement to prevent SQL injection
$stmt = $db->prepare(
    "INSERT INTO books (title, author, year, description, added_by)
     VALUES (:title, :author, :year, :desc, :user)"
);
$stmt->bindValue(':title', $title, SQLITE3_TEXT);
$stmt->bindValue(':author', $author, SQLITE3_TEXT);
$stmt->bindValue(':year', $year, SQLITE3_INTEGER);
$stmt->bindValue(':desc', $description, SQLITE3_TEXT);
$stmt->bindValue(':user', $_SESSION['username'], SQLITE3_TEXT);
$stmt->execute();

header('Location: index.php');
?>
