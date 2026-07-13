<?php
session_start([
    'cookie_httponly' => true,
    'cookie_samesite' => 'Strict',
]);

// ============================================================
// Database Configuration
// ============================================================

$db_path = __DIR__ . '/bookstore.db';
$db = new SQLite3($db_path);
$db->busyTimeout(5000);

// Create tables if they do not exist
$db->exec("CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER DEFAULT 2024,
    description TEXT DEFAULT '',
    added_by TEXT DEFAULT 'anonymous',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)");

$db->exec("CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'user'
)");

// Seed default data if tables are empty
if ($db->querySingle("SELECT COUNT(*) FROM users") == 0) {
    $stmt = $db->prepare(
        "INSERT INTO users (username, password, role) VALUES (:u, :p, :r)"
    );
    $defaults = [
        ['admin', 'admin123', 'admin'],
        ['staff', 'staff123', 'user'],
    ];
    foreach ($defaults as $u) {
        $stmt->bindValue(':u', $u[0], SQLITE3_TEXT);
        $stmt->bindValue(':p', password_hash($u[1], PASSWORD_DEFAULT), SQLITE3_TEXT);
        $stmt->bindValue(':r', $u[2], SQLITE3_TEXT);
        $stmt->execute();
        $stmt->reset();
    }
}

if ($db->querySingle("SELECT COUNT(*) FROM books") == 0) {
    $db->exec("INSERT INTO books (title, author, year, description) VALUES
        ('The Great Gatsby', 'F. Scott Fitzgerald', 1925, 'A novel set in the Jazz Age on Long Island'),
        ('To Kill a Mockingbird', 'Harper Lee', 1960, 'A classic of modern American literature'),
        ('1984', 'George Orwell', 1949, 'A dystopian novel about totalitarianism'),
        ('Pride and Prejudice', 'Jane Austen', 1813, 'A romantic novel of manners'),
        ('The Art of War', 'Sun Tzu', -500, 'An ancient Chinese military treatise')");
}

// ============================================================
// Security Helper Functions
// ============================================================

/**
 * Generate a CSRF token and store it in the session.
 */
function generate_csrf_token() {
    if (empty($_SESSION['csrf_token'])) {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
    }
    return $_SESSION['csrf_token'];
}

/**
 * Verify a submitted CSRF token against the stored session token.
 */
function verify_csrf_token($token) {
    return isset($_SESSION['csrf_token']) && hash_equals($_SESSION['csrf_token'], $token);
}

// ============================================================
// Output Sanitization Functions
// ============================================================

/**
 * Sanitize user input for safe display in HTML element content.
 * Encodes all special HTML characters including both quote types.
 */
function sanitize_output($text) {
    return htmlspecialchars($text, ENT_QUOTES, 'UTF-8');
}

/**
 * Sanitize plain text by removing HTML tags and escaping quotes.
 * Intended for tooltip and preview text where HTML is not expected.
 */
function sanitize_text($text) {
    $text = strip_tags($text);
    $text = str_replace("'", "&#039;", $text);
    return $text;
}

// ============================================================
// Authentication Helper Functions
// ============================================================

function is_logged_in() {
    return isset($_SESSION['username']);
}

function is_admin() {
    return isset($_SESSION['role']) && $_SESSION['role'] === 'admin';
}

function require_login() {
    if (!is_logged_in()) {
        header('Location: login.php');
        exit;
    }
}
?>
