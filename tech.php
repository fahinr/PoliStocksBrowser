<?php
include("database.php");
?>
<!DOCTYPE html>
<html lang="en">
<html>
<head>
  <link rel="stylesheet" href="styles.css">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title> Table </title>
</head>
<body>

<nav class="navbar">
    <div class="navbar__container">
      <a href="/" id="navbar__logo"> </a>
      <div class="navbar__toggle" id="mobile-menu">
        <span class="bar"></span>
        <span class="bar"></span>
        <span class="bar"></span>
      </div>
      <ul class="navbar__menu" id="navbar__menu">
        <li class="navbar__menu-item"><a href="/stockx/index.php" class="navbar__menu-link">Home</a></li>
        <li class="navbar__menu-item"><a href="/" class="navbar__menu-link">About</a></li>
        <li class="navbar__menu-item"><a href="/stockx/tech.php" class="navbar__menu-link">The Table</a></li>
      </div>
    </nav> 


<div class="container">
 <div class="row">
   <div class="col-sm-8">
    <?php echo $deleteMsg??''; ?>
    <div class="table-responsive">
      <table class="table table-bordered">
       <thead><tr>
         <th>Politician</th>
         <th>Issuer</th>
         <th>Ticker</th>
         <th>Trade Date</th>
         <th>Type</th>
         <th>Size</th>
         <th>Price</th>
         <th>Analyst Rating</th>
    </thead>
    <tbody>
  <?php
      if(is_array($fetchData)){      
      $sn=1;
      foreach($fetchData as $data){
    ?>
      <tr>
      <td><?php echo $data['politician']??''; ?></td>
      <td><?php echo $data['issuer']??''; ?></td>
      <td><?php echo $data['ticker']??''; ?></td>
      <td><?php echo $data['trade_date']??''; ?></td>
      <td><?php echo $data['type']??''; ?></td>
      <td><?php echo $data['size']??''; ?></td>
      <td><?php echo $data['price']??''; ?></td> 
      <td><?php echo $data['analyst_rating']??''; ?></td> 
     </tr>
     <?php
      $sn++;}}else{ ?>
      <tr>
        <td colspan = "9">
    <?php echo $fetchData; ?>
  </td>
    <tr>
    <?php
    }?>
    </tbody>
     </table>
   </div>
</div>
</div>
</div>

</body>
</html>