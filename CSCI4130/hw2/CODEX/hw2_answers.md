# Homework 2 Answers

## 1. Same-Origin Policy

中文解释：
Same-Origin Policy 只比较 `protocol + host + port`，路径是否不同不影响 origin。因此这题只需要看协议、主机名和端口号。

可填写英文答案：
- `http://example.com/dir2/page.html`: `Different host`
- `http://one.example.com:81/dir/ect.html`: `Different port`
- `http://one.example.com/dir/inner/another.html`: `No difference`
- `http://two.example.com/secure.html`: `Different host`

## 2. Code Review: Vulnerability Analysis

### 2.a Vulnerability 1

中文解释：
`admin.php` 在 GET 请求里正确限制了只有管理员才能进入页面，但在 POST 删除图书时只检查了“是否已登录”，没有检查“是否是管理员”。这意味着普通登录用户也可以直接构造 POST 请求删除图书，属于权限控制失效。

可填写英文答案：
- `Vulnerability type:` `Improper authorization / broken access control`
- `Why is it a vulnerability?` `The POST handler in admin.php checks only whether the user is logged in, so any authenticated non-admin user can send a POST request to delete books.`
- `How to fix:` `Require both authentication and the admin role for every state-changing request in admin.php, and return 403 for non-admin users.`

### 2.b Vulnerability 2

中文解释：
`search.php` 里虽然大部分搜索条件用了预编译语句，但 `year_to` 直接拼接进 SQL，没有做类型转换或参数绑定。攻击者可以通过这个参数注入恶意 SQL 片段，属于 SQL Injection。

可填写英文答案：
- `Vulnerability type:` `SQL injection`
- `Why is it a vulnerability?` `The year_to parameter is concatenated directly into the SQL query, so an attacker can inject arbitrary SQL through this field.`
- `How to fix:` `Cast year_to to an integer before appending it, or bind it as a prepared-statement parameter instead of concatenating raw input.`

### 2.c Vulnerability 3

中文解释：
`index.php` 把图书描述放进 `<span title="...">` 这个 HTML 属性里，但使用的 `sanitize_text()` 只去掉标签并转义单引号，没有转义双引号。攻击者可以提交像 `" onmouseover="alert(1)` 这样的描述，把 `title` 属性截断后再插入新属性，形成存储型 XSS。

可填写英文答案：
- `Vulnerability type:` `Stored XSS via HTML attribute injection`
- `Why is it a vulnerability?` `The description is inserted into the title attribute with insufficient escaping, so an attacker can inject a double quote and add a new event handler such as onmouseover.`
- `How to fix:` `Use context-aware output encoding for HTML attributes, such as htmlspecialchars(..., ENT_QUOTES, 'UTF-8'), before rendering the description.`

## 3. SQL Injection

### 3.a Login as admin without knowing the password

中文解释：
这里的 SQL 直接把用户名和密码拼起来，因此可以用单引号闭合原来的字符串，再用注释符把后面的密码判断注释掉。最直接的做法是让用户名变成 `admin' -- `。

可填写英文答案：
- `$uname =` `admin' -- `
- `$passwd =` `anything`

### 3.b Delete table users

中文解释：
这里利用的是多语句注入思路：先闭合前面的字符串，再执行 `DROP TABLE users`，最后把后面的内容注释掉。

可填写英文答案：
- `$uname =` `admin'; DROP TABLE users; -- `
- `$passwd =` `anything`

### 3.c Bypass naive single-quote escaping

中文解释：
如果服务器只是把 `'` 变成 `\'`，但没有处理原始输入中的反斜杠，那么攻击者可以先自己放一个反斜杠。这样服务端加上的反斜杠会和原始反斜杠组成 `\\`，MySQL 会把它解释成一个普通反斜杠，后面的单引号仍然可以结束字符串。再配合双引号包住 `admin`，就能绕过这种“只转义单引号”的防御。

可填写英文答案：
- `$uname =` `admin`
- `$passwd =` `\' OR username="admin" -- `

## 4. XSS Attacks and Defense

### 4.a Why does an attacker bother with XSS?

中文解释：
如果攻击者只是做一个恶意页面，这个页面上的脚本运行在攻击者自己的 origin 下，浏览器的 Same-Origin Policy 不允许它直接读取别的网站 cookie。XSS 的关键价值就在于让恶意脚本“借壳”在受害网站自己的 origin 中执行，于是就能访问该网站下的 cookie、DOM 和会话信息。

可填写英文答案：
- `The reason:` `Because the browser's Same-Origin Policy prevents a malicious page from reading cookies from another origin, while XSS lets the attacker's script run in the vulnerable site's origin.`

### 4.b Crafted URL parameter for XSS

中文解释：
`hw2-xss.php` 直接把 `name` 原样输出到 HTML 中，所以最直接的 payload 就是插入 `<script>` 标签并弹出 `document.cookie`。

可填写英文答案：
- `name=` `<script>alert(document.cookie)</script>`

### 4.c Attack after removing all recognizable `<script>` tags

中文解释：
既然只删 `<script>`，那就改用事件处理器触发 XSS，例如图片加载失败时执行 `onerror`。这种 payload 不依赖 `<script>` 标签，仍然可以执行 JavaScript。

可填写英文答案：
- `name=` `<img src=x onerror=alert(document.cookie)>`

### 4.d A method to fix this kind of XSS

中文解释：
根本修复方式是“按输出上下文做编码”。在这里属于 HTML 文本上下文，应在输出前对用户输入做 HTML escaping，例如用 PHP 的 `htmlspecialchars`。

可填写英文答案：
- `Use context-aware output encoding (for example, htmlspecialchars) before rendering untrusted input into HTML.`

## 5. CSRF Attacks and Defense

### 5.a Another way to launch CSRF besides XSS

中文解释：
除了 XSS 之外，攻击者还可以诱导受害者访问自己控制的恶意页面，页面里放一个隐藏表单、自动提交脚本，或者 `<img>`、`<iframe>`、`<form>` 之类的跨站请求载体。只要受害者此时已经登录目标网站，浏览器就会自动携带 cookie 发出请求，目标站点就可能误以为这是用户本人操作。

可填写英文答案：
- `An attacker can host a malicious page or send a phishing link that contains a hidden form, an auto-submitting script, or an image/request tag, causing the victim's browser to send an authenticated request to the target site.`

### 5.b Responses from each server

中文解释：
这题的核心是：访问 `http://malicious-server:8002/index.html` 后，攻击者服务器会先收到对 `index.html` 的请求；随后页面中的脚本会让浏览器自动请求 `http://localhost:8000/hw2-xss.php?name=atk%20msg`，所以受害网站服务器也会留下对应日志。时间戳和源端口每次运行都会不同，下面给的是可填写的示例格式。

可填写英文答案：
- `For index.html:` `127.0.0.1 - - [09/Apr/2026 12:15:54] "GET /index.html HTTP/1.1" 200 -`
- `For hw2-xss.php:` `[Thu Apr 09 12:15:54 2026] 127.0.0.1:<random-port> [200]: "GET /hw2-xss.php?name=atk%20msg HTTP/1.1"`

### 5.c If the browser directly forbids cross-site requests

中文解释：
直接禁止跨站请求可以挡住 CSRF，因为 CSRF 本质上依赖“受害者浏览器跨站代发请求”。但这并不能防住 XSS，因为 XSS 的脚本本来就是在目标网站自己的 origin 中执行的，不依赖跨站读写。

可填写英文答案：
- `For XSS:` `No`
- `For CSRF:` `Yes`

## Extra Note

中文说明：
我已经另外生成了第二题需要提交的修复 diff 文件，路径是 `hw2/q2.diff`。  
第三题和第四题要求的截图文件 `q3b.jpg`、`q4b.jpg` 属于作业附件，不在这个 Markdown 文本答案里。
