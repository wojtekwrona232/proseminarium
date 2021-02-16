<!DOCTYPE html>
<html lang="en">

<head>
    <!-- Required meta tags always come first -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <title>Wyszukaj książkę</title>

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

        td p{
            margin-bottom: 0;
        }
        td {
            padding-top:15px!important;
            padding-bottom: 15px!important;
        }
        td button{
            color: white!important;
            padding-left: 10px!important;
            padding-right: 10px!important;
        }
        .c1{
            background-color: #9068c7!important;
        }
        .c2{
            background-color: #6864D1!important;
        }
        .c3{
            background-color: #405fdb!important;
        }
    </style>

</head>

<body>

<!--Main Navigation-->
<header>

    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top scrolling-navbar">
        <div class="container">
            <a class="navbar-brand" href="afterlogon_pracownik.html"><strong>Ametyst Pracownik</strong></a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent-7"
                    aria-controls="navbarSupportedContent-7" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent-7">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item dropdown">
                        <a class="nav-link dropdown-toggle" id="navbarDropdownMenuLink-333" data-toggle="dropdown"
                           aria-haspopup="true" aria-expanded="false">Dodaj
                        </a>
                        <div class="dropdown-menu dropdown-default" aria-labelledby="navbarDropdownMenuLink-333">
                            <a class="dropdown-item" href="addbook.html">Książkę</a>
                            <a class="dropdown-item" href="addauthor.html">Autora</a>
                            <a class="dropdown-item" href="addtranslator.html">Tłumacza</a>
                            <a class="dropdown-item" href="addpublisher.html">Wydawcę</a>
                            <a class="dropdown-item" href="addlibrary.html">Bibliotekę</a>
                        </div>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Wyszukaj</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="package_status.html">Status przesyłki</a>
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

                                    <div class="form-header mbutton" style="margin-bottom: 37px;">
                                        <h3><i class="fas fa-search mt-2"></i> Wyszukaj książkę</h3>
                                    </div>
                                    <!--Header-->
                                    <div class="md-form">
                                        <input type="text" id="form1" class="form-control">
                                        <label for="form1">Wyszukaj książkę</label>
                                    </div>
                                    <div class='table-responsive'>
                                        <!--Table-->
                                        <table id="tablePreview" class="table table-hover">
                                            <!--Table head-->
                                            <thead>
                                            <tr>
                                                <th>#</th>
                                                <th>Tytuł</th>
                                                <th>Autor</th>
                                                <th>Dostępność</th>
                                                <th>Opcje</th>

                                            </tr>
                                            </thead>
                                            <!--Table head-->
                                            <?php // książki
                                            $cURLConnection = curl_init();

                                            curl_setopt($cURLConnection, CURLOPT_URL, 'http://127.0.0.1:7010/api/v1/get-books-availability/all');
                                            curl_setopt($cURLConnection, CURLOPT_RETURNTRANSFER, true);

                                            $List = curl_exec($cURLConnection);
                                            curl_close($cURLConnection);

                                            $jsonArrayResponse - json_decode($List);
                                            ?>
                                            <!--Table body-->
                                            <tbody>
                                            <tr>
                                                <th name='id' scope="row">1</th>
                                                <td>Zemsta</td>
                                                <td>Aleksander Fredro</td>
                                                <td><p>Ametyst: 5</p><p>Szmaragd: 5</p></td>
                                                <td><a href="view_book_pracownik.html">
                                                    <button type="button" class="btn btn-sm c1">Podgląd</button></a>
                                                    <a href="<?header("Location: borrow_pracownik.php?id=".$_POST['id']);?>">
                                                    <button type="button" class="btn btn-sm c2">Wypożycz</button></a>
                                                    <a href="<?header("Location: reserve_pracownik.php?id=".$_POST['id']);?>">
                                                    <button type="button" class="btn btn-sm c3">Zarezerwuj</button></a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <th scope="row">2</th>
                                                <td>Lalka</td>
                                                <td>Bolesław Prus</td>
                                                <td><p>Ametyst: 6</p><p>Szmaragd: 2</p></td>
                                                <td><a href="view_book_pracownik.html">
                                                    <button type="button" class="btn btn-sm c1">Podgląd</button></a>
                                                    <a href="borrow_pracownik.html">
                                                        <button type="button" class="btn btn-sm c2">Wypożycz</button></a>
                                                    <a href="reserve_pracownik.html">
                                                        <button type="button" class="btn btn-sm c3">Zarezerwuj</button></a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <th scope="row">3</th>
                                                <td>Cierpienia młodego Wertera</td>
                                                <td>Johann Wolfgan </td>
                                                <td><p>Ametyst: 4</p><p>Szmaragd: 1</p></td>
                                                <td><a href="view_book_pracownik.html">
                                                    <button type="button" class="btn btn-sm c1">Podgląd</button></a>
                                                    <a href="borrow_pracownik.html">
                                                        <button type="button" class="btn btn-sm c2">Wypożycz</button></a>
                                                    <a href="reserve_pracownik.html">
                                                        <button type="button" class="btn btn-sm c3">Zarezerwuj</button></a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <th scope="row">4</th>
                                                <td>W pustyni i w puszczy</td>
                                                <td>Henryk Sienkiewicz</td>
                                                <td><p>Ametyst: 9</p><p>Szmaragd: brak</p></td>
                                                <td><a href="view_book_pracownik.html">
                                                    <button type="button" class="btn btn-sm c1">Podgląd</button></a>
                                                    <a href="borrow_pracownik.html">
                                                        <button type="button" class="btn btn-sm c2">Wypożycz</button></a>
                                                    <a href="reserve_pracownik.html">
                                                        <button type="button" class="btn btn-sm c3">Zarezerwuj</button></a>
                                                </td>
                                            </tr>
                                            <tr>
                                                <th scope="row">5</th>
                                                <td>Dziady cz. III</td>
                                                <td>Adam Mickiewicz</td>
                                                <td><p>Ametyst: brak</p><p>Szmaragd: 2</p></td>
                                                <td><a href="view_book_pracownik.html">
                                                    <button type="button" class="btn btn-sm c1">Podgląd</button></a>
                                                    <a href="borrow_pracownik.html">
                                                        <button type="button" class="btn btn-sm c2">Wypożycz</button></a>
                                                    <a href="reserve_pracownik.html">
                                                        <button type="button" class="btn btn-sm c3">Zarezerwuj</button></a>
                                                </td>
                                            </tr>

                                            </tbody>
                                            <!--Table body-->
                                        </table>
                                        <!--Table-->
                                    </div>
                                </div>
                                <!--/Form with header-->

                                </div>
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
        $("tr:odd").css("color", "#370064");

    });

</script>
</body>

</html>