<script>
// simply write cookie information
document.cookie="your sensitive cookie information";
</script>

<?php
if(isset($_GET['name'])) {
   $name = $_GET['name'];
   echo "Welcome $name<br>";
}
else{
   echo "No parameter 'name' specified.<br>";
   echo "Use url like: http://localhost:8001/hw2-xss.php?name=xxx <br>";
}
?>
