<?php
require_once 'config.php';

$results = [];
$search_term = '';
$has_results = false;

if (isset($_GET['q']) && !empty(trim($_GET['q']))) {
    $has_results = true;
    $search_term = trim($_GET['q']);

    // Build the base query using a prepared statement for safety
    $query = "SELECT * FROM books WHERE (title LIKE :search OR author LIKE :search)";
    $params = [':search' => '%' . $search_term . '%'];

    // Apply year range filters if provided
    if (!empty($_GET['year_from'])) {
        $year_from = intval($_GET['year_from']);
        $query .= " AND year >= " . $year_from;
    }
    if (!empty($_GET['year_to'])) {
        $year_to = intval($_GET['year_to']);
        $query .= " AND year <= " . $year_to;
    }

    // Sorting — validate column name against a strict whitelist
    $allowed_sort = ['title', 'author', 'year'];
    $sort_col = isset($_GET['sort']) && in_array($_GET['sort'], $allowed_sort, true)
        ? $_GET['sort'] : 'title';
    $sort_dir = isset($_GET['dir']) && strtoupper($_GET['dir']) === 'DESC' ? 'DESC' : 'ASC';
    $query .= " ORDER BY " . $sort_col . " " . $sort_dir;

    $stmt = $db->prepare($query);
    foreach ($params as $key => $val) {
        $stmt->bindValue($key, $val, SQLITE3_TEXT);
    }
    $result = $stmt->execute();
    while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
        $results[] = $row;
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Search - Bookstore</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="header">
        <h1>Bookstore &mdash; Search</h1>
        <div class="nav"><a href="index.php">&larr; Back to Home</a></div>
    </div>

    <div class="block">
        <h2>Search</h2>
        <form method="GET" action="search.php">
            <input type="text" name="q" value="<?= sanitize_output($search_term) ?>"
                   placeholder="Title or author...">
            <label>From: <input type="number" name="year_from"
                   value="<?= isset($_GET['year_from']) ? intval($_GET['year_from']) : '' ?>"></label>
            <label>To: <input type="number" name="year_to"
                   value="<?= isset($_GET['year_to']) ? intval($_GET['year_to']) : '' ?>"></label>
            <select name="sort">
                <option value="title">Sort by Title</option>
                <option value="author">Sort by Author</option>
                <option value="year">Sort by Year</option>
            </select>
            <button type="submit">Search</button>
        </form>
    </div>

    <?php if ($has_results): ?>
    <div class="block">
        <?php if (count($results) === 0): ?>
            <p>No results found for &ldquo;<?= sanitize_output($search_term) ?>&rdquo;.
               <a href="index.php">Go back</a>.</p>
        <?php else: ?>
            <p>Found <?= count($results) ?> result(s) for
               &ldquo;<?= sanitize_output($search_term) ?>&rdquo;.
               <a href="index.php">Go back</a>.</p>
            <table>
                <tr><th>Title</th><th>Author</th><th>Year</th><th>Description</th></tr>
                <?php foreach ($results as $book): ?>
                <tr>
                    <td><?= sanitize_output($book['title']) ?></td>
                    <td><?= sanitize_output($book['author']) ?></td>
                    <td><?= intval($book['year']) ?></td>
                    <td><?= sanitize_output($book['description']) ?></td>
                </tr>
                <?php endforeach; ?>
            </table>
        <?php endif; ?>
    </div>
    <?php endif; ?>
</body>
</html>
