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
  <title> StockX </title>
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

   <!-- <div id="canvas-container">
      <canvas id="subtitle-canvas"></canvas>
    </div> -->

    <section class="top-title">
      <h1 id="table_name">The Table.</h1>
    </section>

    <section class="cards">
      <main class="card-container">
        <section class="card">
          <div>
            <div class="card__icon">
              <img src="images/icon-1.png">
              <h3>Card 1</h3>
            </div>
            <p>This is a table of all the data from the database. (Possible a href)
              more explanation on what this is, etc. More info...
            </p>
          </div>
        </section>
        <section class="card">
          <div>
            <div class="card__icon">
              <img src="images/icon-1.png">
              <h3>Card 2</h3>
            </div>
            <p>This is a table of all the data from the database. (Possible a href) 
            more explanation on what this is, etc. More info...
            </p>
          </div>
        </section>
        <section class="card">
          <div>
            <div class="card__icon">
              <img src="images/icon-1.png">
              <h3>Card 3</h3>
            </div>
            <p>This is a table of all the data from the database. (Possible a href)
            more explanation on what this is, etc. More info...
            </p>
          </div>
        </section>
      </main>
    </section>




     
    <script src="app.js"></script>
    <script src="http://cdnjs.cloudflare.com/ajax/libs/ScrollMagic/2.0.7/ScrollMagic.min.js"></script>
    <script src="http://cdnjs.cloudflare.com/ajax/libs/ScrollMagic/2.0.7/plugins/debug.addIndicators.min.js"></script>
    <script src="http://cdnjs.cloudflare.com/ajax/libs/ScrollMagic/2.0.7/plugins/debug.addIndicators.js"></script>
</body>
</html>