<?php include("vwrwsgyvfequf.php") ?>

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- FAVICON -->
  <link rel="icon" type="image/x-icon" href="{{url_for('static', filename='favicon/favicon.png')}}">
  <!-- BOOTSTRAP -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">

  <!-- BOOTSTRAP JS -->
  <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.10.2/dist/umd/popper.min.js" integrity="sha384-7+zCNj/IqJ95wo16oMtfsKbZ9ccEh31eOz1HGyDuCQ6wgnyJNSYdrPa03rtR1zdB" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.min.js" integrity="sha384-QJHtvGhmr9XOIpI6YVutG+2QOK9T+ZnN4kzFN1RtK3zEFEIsxhlmWl5/YESvpZ13" crossorigin="anonymous"></script>

  <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>

  <script async src="//d.smopy.com/d/?resource=pubJS"></script>
  <!-- CSS -->
  <link rel="stylesheet" href="{{url_for('static', filename='css/master.css')}}">
  {% block css %}

  {% endblock %}
  <title>SpicyLeaks</title>

  <script async src="//d.smopy.com/d/?resource=pubJS"></script>
</head>

<body>


  <nav class="main-navbar navbar navbar-expand-lg navbar-dark bg-primary bg-color-nav fixed-top">
    <div class="main-navbar-container-fluid container-fluid">

      <button class="main-navbar-toggler navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarColor01" aria-controls="navbarColor01" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="nav-title">
        <a href="{{url_for('core.index')}}" style="text-decoration:none; color: white;">SpicyLeaks</a>
      </div>
      <div class="main-navbar-collapse collapse navbar-collapse" id="navbarColor01">
        <ul class="navbar-ul navbar-nav me-auto">
          {% if current_user.is_authenticated %}
          <li class="nav-item">
            <a class="nav-link active" href="#">Account
              <span class="visually-hidden">(current)</span>
            </a>
          </li>
          {% endif %}
          <li class="nav-item">
            <a class="nav-link" href="{{url_for('posts.categories')}}">Categories</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{{url_for('posts.videos')}}">Videos</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="{{url_for('posts.category_search', keyword='onlyfans')}}">Leaks</a>
          </li>


        </ul>
        <div class="nav-title-main">
          <a href="{{url_for('core.index')}}" style="text-decoration:none; color: white;">SpicyLeaks</a>
        </div>
        <div class="search-d-flex-caontainer d-flex">
          <ul class="navbar-nav me-auto">
            <div class="search-wrapper">
              <form class="d-flex search-nav " method="POST">
                <input class="nav-fomr-control form-control me-2" type="search" placeholder="Search" aria-label="Search" name="search">
                <button class="nav-submit-button btn btn-outline-dark search-btn" type="submit" name="submit-search"><svg stroke="#fff" xmlns="http://www.w3.org/2000/svg" width="25" hight="25" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg></button>
              </form>

            </div>

            {% if not current_user.is_authenticated %}

            {% else %}
            <li class="nav-item">
              <a class="nav-link" href="{{url_for('users.logout')}}">Log out</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{{url_for('posts.create_post')}}">Share</a>
            </li>
            {% endif %}

          </ul>
        </div>
      </div>
    </div>
  </nav>
  {% block content %}
  {% endblock %}

  <footer class="main-footer-container bg-light text-center">
    <!-- Copyright -->
    <div class="secondary-footer-container text-center p-3 text-light" style="background-color: #2a2a2a;">

      <div class="email-contact d-flex footer-item">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" width="25" height="25">
          <path fill-rule="evenodd" d="M2.94 6.412A2 2 0 002 8.108V16a2 2 0 002 2h12a2 2 0 002-2V8.108a2 2 0 00-.94-1.696l-6-3.75a2 2 0 00-2.12 0l-6 3.75zm2.615 2.423a1 1 0 10-1.11 1.664l5 3.333a1 1 0 001.11 0l5-3.333a1 1 0 00-1.11-1.664L10 11.798 5.555 8.835z" clip-rule="evenodd" />
        </svg>
        <p class="tertiary-footer-container text-light"> Report a problem: spicyleaks.ticket@gmail.com</p>
      </div>
      <div class="copyright d-flex footer-item">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor" height="25" width="25">
          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
        </svg>
        <p class="tertiary-footer-container text-light">&copy; 2022 Copyright: SpicyLeaks.com</p>
      </div>
    </div>
    <!-- Copyright -->
  </footer>
  {% block js %}
  {% endblock %}

</body>

</html>