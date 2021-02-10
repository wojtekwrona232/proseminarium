<!DOCTYPE html>
<html lang="en">

<head>
    <!-- Required meta tags always come first -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <title>Wypożycz książkę</title>

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.11.2/css/all.css">
    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
    <!-- Material Design Bootstrap -->
    <link href="css/mdb.css" rel="stylesheet">
    <!-- Your custom styles (optional) -->
    <link rel="stylesheet" href="css/style.css">
    <link rel="preconnect" href="https://fonts.gstatic.com">
    <link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@1,600&display=swap" rel="stylesheet">
    <style>


        .intro-2 {
            background: url("https://mdbootstrap.com/img/Photos/Others/forest1.jpg") no-repeat center center;
            background-size: cover;
        }
        .card-body{
            padding: 30px;
        }
        button{
            width:300px;
        }

    </style>

</head>

<body>

<!--Main Navigation-->
<header>

    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top scrolling-navbar">
        <div class="container">
            <a class="navbar-brand" href="afterlogon_user.html"><strong>Ametyst Czytelnik</strong></a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent-7"
                    aria-controls="navbarSupportedContent-7" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent-7">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="search_book_user.html">Wyszukaj</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="login.html">Wyloguj</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>
    <!-- Navbar -->

    <!--Intro Section-->
    <section class="view intro-2">
        <div class="mask rgba-gradient">
            <div class="container h-100 d-flex justify-content-center align-items-center">

                <!--Grid row-->
                <div class="row  pt-5 mt-3">

                    <!--Grid column-->
                    <div class="col-md-12">
                        <div class="card wow fadeIn" data-wow-delay="0.3s">
                            <div class="card">
                                <div class="card-body">

                                    <!--Header-->
                                    <div class="form-header mbutton" style="border-radius: 0.2em;" >
                                        <h3><i class="fas fa-book"></i>&nbsp;&nbsp;Wypożycz książkę</h3>
                                    </div>
                                    <form action="" method="post">
                                    <select name="ksiazka" class="mdb-select md-form" searchable="Wyszukaj książkę...">
                                    <?php // książki
                                    $cURLConnection = curl_init();

                                    curl_setopt($cURLConnection, CURLOPT_URL, 'http://127.0.0.1:7010/api/v1/get-books-availability/all');
                                    curl_setopt($cURLConnection, CURLOPT_RETURNTRANSFER, true);

                                    $List = curl_exec($cURLConnection);
                                    curl_close($cURLConnection);

                                    $jsonArrayResponse - json_decode($List);
                                    ?> 
                                        <option value="1" data-secondary-text="Aleksander Fredro">Zemsta
                                        </option>
                                        <option value="2" data-secondary-text="Bolesław Prus">Lalka
                                        </option>
                                        <option value="3" data-secondary-text="Johann Wolfgang von Goethe">Cierpienia młodego Wertera

                                        </option>
                                    </select>
                                    <label class="mdb-main-label">Książka</label>
                                    <div class="md-form mb-2">
                                        <input placeholder="Selected date" type="text" name="date-pick" id="date-picker-example"
                                               class="form-control datepicker" data-value="2021/01/14">
                                        <label for="date-picker-example">Do</label>
                                    </div>



                                    <div class="text-center mt-4">
                                        <button type="submit" name='submit' class="btn mbutton special_button ">Wypożycz książkę</button>
                                    </div>
                                    </form>
                                </div>
                                <!--/Form with header-->
                                <?php
                                if (isset($_POST['submit'])) {
                                    $selected = $_POST['ksiazka'];
                                    $data = $_POST['date-pick'];
                                    $postRequest = array(
                                        'book' => $selected,
                                        'date' => $data
                                    );
                                    
                                    $cURLConnection = curl_init('http://127.0.0.1:7010/api/v1/add-reservation');
                                    curl_setopt($cURLConnection, CURLOPT_POSTFIELDS, $postRequest);
                                    curl_setopt($cURLConnection, CURLOPT_RETURNTRANSFER, true);
                                    
                                    $apiResponse = curl_exec($cURLConnection);
                                    curl_close($cURLConnection);
                                }
                                ?>
                            </div>

                        </div>
                        <!--Grid column-->
                    </div>
                </div>
                <!--Grid row-->

            </div>
        </div>
    </section>
    <!--Intro Section-->

</header>
<!--Main Navigation-->

<!--  SCRIPTS  -->
<!-- JQuery -->
<script type="text/javascript" src="js/jquery.min.js"></script>
<!-- Bootstrap tooltips -->
<script type="text/javascript" src="js/popper.min.js"></script>
<!-- Bootstrap core JavaScript -->
<script type="text/javascript" src="js/bootstrap.min.js"></script>
<!-- MDB core JavaScript -->
<script type="text/javascript" src="js/mdb.min.js"></script>
<script>
    new WOW().init();
    $(document).ready(function () {
        $('.mdb-select').materialSelect();
    });
    $('.datepicker').pickadate();
</script>
</body>

</html>
