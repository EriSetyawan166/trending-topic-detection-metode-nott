<?php
   include 'util/koneksi.php';
   $page = 'index';
   $no = 1;


   $query = "SELECT COUNT(*) AS totalRows FROM dokumen";
   $query_user = "SELECT COUNT(distinct(user_screen_name)) AS totalUser FROM dokumen";
   
   $result = mysqli_query($conn, $query);
   $result_user = mysqli_query($conn, $query_user);

   $row = mysqli_fetch_assoc($result);
   $totalTexts = $row['totalRows'];

   $row_user = mysqli_fetch_assoc($result_user);
   $totalUsers = $row_user['totalUser'];

    $perPage = 5;
    $sqlQuery = "SELECT * FROM dokumen";
    $result = mysqli_query($conn, $sqlQuery);
    $totalRecords = mysqli_num_rows($result);
    $totalPages = ceil($totalRecords/$perPage);

    // if(isset($_POST['cari']))
    // {
    //     // mysqli_query($conn, "DELETE FROM tweet2");
    //     $text = $_POST['text'];
    //     $output = passthru("python controller/tarik_data.py $text");
    //     passthru("python util/word_cloud.py");
    //     passthru("python util/sering.py");
    //     header("Location: index.php");
    // }

    

    // passthru("python util/word_cloud.py");
    // passthru("python util/sering.py");
?>


<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>Deteksi Trending Topik</title>

    <!-- Custom fonts for this template-->
    <link href="assets/vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet" type="text/css">
    <script src="assets/vendor/jquery/jquery.min.js"></script>
    <script src="assets/js/simple-bootstrap-paginator.js"></script>
    <link
        href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i"
        rel="stylesheet">

    <!-- Custom styles for this template-->
    <link href="assets/css/sb-admin-2.min.css" rel="stylesheet">

</head>

<body id="page-top">

    <!-- Page Wrapper -->
    <div id="wrapper">

        <!-- Sidebar -->
        <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">

            <!-- Sidebar - Brand -->
            <a class="sidebar-brand d-flex align-items-center justify-content-center" href="index.php">
                <div class="sidebar-brand-icon rotate-n-15">
                    <i class="fas fa-laugh-wink"></i>
                </div>
                <div>Deteksi Trending Topik</div>
            </a>

            <!-- Divider -->
            <hr class="sidebar-divider my-0">

            <!-- Nav Item - Dashboard -->
            <li class="nav-item active">
                <a class="nav-link" href="index.php">
                    <i class="fas fa-fw fa-magnifying-glass"></i>
                    <span>Tarik Data</span></a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="view/preprocessing.php">
                    <i class="fas fa-fw fa-file-word"></i>
                    <span>Preprocessing</span></a>
            </li>

            <!-- Nav Item - Pages Collapse Menu -->
            <li class="nav-item">
                <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapseTwo"
                    aria-expanded="true" aria-controls="collapseTwo">
                    <i class="fas fa-fw fa-cog"></i>
                    <span>Modelling</span>
                </a>
                <div id="collapseTwo" class="collapse" aria-labelledby="headingTwo" data-parent="#accordionSidebar">
                    <div class="bg-white py-2 collapse-inner rounded">
                        <a class="collapse-item" href="view/clustering.php">Clustering</a>
                        <a class="collapse-item" href="view/scoring.php">Scoring</a>
                        <a class="collapse-item" href="view/lda.php">LDA Topic</a>
                    </div>
                </div>
            </li>

            <!-- Divider -->
            <hr class="sidebar-divider d-none d-md-block">
        </ul>
        <!-- End of Sidebar -->

        <!-- Content Wrapper -->
        <div id="content-wrapper" class="d-flex flex-column">

            <!-- Main Content -->
            <div id="content">

                <!-- Topbar -->
                <nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">

                    <!-- Sidebar Toggle (Topbar) -->
                    <button id="sidebarToggleTop" class="btn btn-link d-md-none rounded-circle mr-3">
                        <i class="fa fa-bars"></i>
                    </button>

                    <!-- Topbar Search -->
                    <form action="" method="POST" name="form1"
                        class="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search">
                        <div class="input-group">
                            <input type="text" name="text" class="form-control bg-light border-0 small" placeholder="Cari Tweet"
                                aria-label="Search" aria-describedby="basic-addon2">
                            <div class="input-group-append">
                                <input class="btn btn-primary" type="submit" name="cari"></input>
                            </div>
                        </div>
                    </form>

                    <!-- Topbar Navbar -->
                    <ul class="navbar-nav ml-auto">

                        <!-- Nav Item - Search Dropdown (Visible Only XS) -->
                        <li class="nav-item dropdown no-arrow d-sm-none">
                            <a class="nav-link dropdown-toggle" href="#" id="searchDropdown" role="button"
                                data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <i class="fas fa-search fa-fw"></i>
                            </a>
                            <!-- Dropdown - Messages -->
                            <div class="dropdown-menu dropdown-menu-right p-3 shadow animated--grow-in"
                                aria-labelledby="searchDropdown">
                                <form class="form-inline mr-auto w-100 navbar-search">
                                    <div class="input-group">
                                        <input type="text" class="form-control bg-light border-0 small"
                                            placeholder="Search for..." aria-label="Search"
                                            aria-describedby="basic-addon2">
                                        <div class="input-group-append">
                                            <button class="btn btn-primary" type="button">
                                                <i class="fas fa-search fa-sm"></i>
                                            </button>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </li>
                    </ul>

                </nav>
                <!-- End of Topbar -->

                <!-- Begin Page Content -->
                <div class="container-fluid">

                    <!-- Page Heading -->
                    <div class="d-sm-flex align-items-center justify-content-between mb-4">
                        <h1 class="h3 mb-0 text-gray-800">Raw Data</h1>
                        <a href="#" class="d-none d-sm-inline-block btn btn-sm btn-danger shadow-sm" data-toggle="modal" data-target="#deleteConfirmationModal"><i class="fas fa-trash fa-sm text-white-50"></i> Hapus Data</a>

                    </div>

                    <div class="modal" id="deleteConfirmationModal" tabindex="-1" role="dialog" aria-labelledby="deleteConfirmationModalLabel" aria-hidden="true">
                    <div class="modal-dialog" role="document">
                        <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="deleteConfirmationModalLabel">Konfirmasi Penghapusan Data</h5>
                            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                            </button>
                        </div>
                        <div class="modal-body">
                            Apakah Anda yakin ingin menghapus semua data?
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-dismiss="modal">Batal</button>
                            <form method="post" action="controller/hapus_data_raw.php">
                                <input type="submit" name="hapus_data" value="Hapus Data" class="btn btn-danger">
                            </form>
                        </div>
                        </div>
                    </div>
                    </div>

                    <!-- Content Row -->
                    <div class="row">

                        <!-- Earnings (Monthly) Card Example -->
                        <div class="col-xl-6     col-md-6 mb-4">
                            <div class="card border-left-primary shadow h-100 py-2">
                                <div class="card-body">
                                    <div class="row no-gutters align-items-center">
                                        <div class="col mr-2">
                                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                                Jumlah tweet</div>
                                            <div class="h5 mb-0 font-weight-bold text-gray-800"><?=$totalTexts ?></div>
                                        </div>
                                        <div class="col-auto">
                                            <i class="fas fa-comments fa-2x text-gray-300"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Earnings (Monthly) Card Example -->
                        <div class="col-xl-6 col-md-6 mb-4">
                            <div class="card border-left-success shadow h-100 py-2">
                                <div class="card-body">
                                    <div class="row no-gutters align-items-center">
                                        <div class="col mr-2">
                                            <div class="text-xs font-weight-bold text-success text-uppercase mb-1">
                                                Jumlah User</div>
                                            <div class="h5 mb-0 font-weight-bold text-gray-800"><?=$totalUsers?></div>
                                        </div>
                                        <div class="col-auto">
                                            <i class="fas fa-users fa-2x text-gray-300"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Content Row -->

                    <div class="row">

                        <!-- Area Chart -->
                        <div class="col-xl-8 col-lg-7">
                            <div class="card shadow mb-4">
                                <!-- Card Header - Dropdown -->
                                <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                    <h6 class="m-0 font-weight-bold text-primary">Wordcloud</h6>
                                </div>
                                <!-- Card Body -->
                                <div class="card-body">
                                    <div class="chart-area">
                                        <img src="assets/img/wordcloud.png" alt="" style="max-width: 100%; max-height: 100%;">
                                    </div>
                                </div>
                            </div>
                        </div>


                        <!-- Pie Chart -->
                        <div class="col-xl-4 col-lg-5">
                            <div class="card shadow mb-4">
                                <!-- Card Header - Dropdown -->
                                <div
                                    class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                                    <h6 class="m-0 font-weight-bold text-primary">Frekuensi Kata</h6>
                                </div>
                                <!-- Card Body -->
                                <div class="card-body">
                                    <img src="assets/img/sering.png" alt="" style="max-width: 100%; max-height: 100%;">
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Content Row -->
                    <div class="row">

                        <!-- Content Column -->
                        <div class="col-lg-12 mb-4">

                            <!-- Project Card Example -->
                            <div class="card shadow mb-4">
                                <div class="card-header py-3">
                                    <h6 class="m-0 font-weight-bold text-primary">Data Hasil Pencarian</h6>
                                </div>
                                <div class="card-body">
                                    <div class="table-responsive mt-3">
                                    <table id="datatableSimple" class="table table-bordered" >
                                        <thead>
                                            <tr>
                                                <th>No</th>
                                                <th>Username</th>
                                                <th>Tweet</th>
                                            </tr>
                                        </thead>
                                        <tbody  id="datatext">
                                        
                                            
                                            
                                        </tbody>
                                        </table>
                                    </div>
                                    <div id="pagination"></div>    
                                    <input type="hidden" id="totalPages" value="<?php echo $totalPages; ?>">
                                </div>
                            </div>

                            

                        </div>

                        
                    </div>

                </div>
                <!-- /.container-fluid -->

            </div>
            <!-- End of Main Content -->

            <!-- Footer -->
            <footer class="sticky-footer bg-white">
                <div class="container my-auto">
                    <div class="copyright text-center my-auto">
                        <span>Copyright &copy; Your Website 2021</span>
                    </div>
                </div>
            </footer>
            <!-- End of Footer -->

        </div>
        <!-- End of Content Wrapper -->

    </div>
    <!-- End of Page Wrapper -->

    <!-- Scroll to Top Button-->
    <a class="scroll-to-top rounded" href="#page-top">
        <i class="fas fa-angle-up"></i>
    </a>

    <!-- Logout Modal-->
    <div class="modal fade" id="logoutModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel"
        aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="exampleModalLabel">Ready to Leave?</h5>
                    <button class="close" type="button" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">×</span>
                    </button>
                </div>
                <div class="modal-body">Select "Logout" below if you are ready to end your current session.</div>
                <div class="modal-footer">
                    <button class="btn btn-secondary" type="button" data-dismiss="modal">Cancel</button>
                    <a class="btn btn-primary" href="login.html">Logout</a>
                </div>
            </div>
        </div>
    </div>

    

    <script type="text/javascript">
        $(document).ready(function(){
            var totalPage = parseInt($('#totalPages').val());   
            console.log("==totalPage=="+totalPage);

            var pag = $('#pagination').simplePaginator({
                totalPages: totalPage,
                maxButtonsVisible: 5,
                currentPage: 1,
                nextLabel: 'Next',
                prevLabel: 'Prev',
                firstLabel: 'First',
                lastLabel: 'Last',
                clickCurrentPage: true,
                pageChange: function(page) {            
                    $("#datatext").html('<tr><td colspan="6"><strong>loading...</strong></td></tr>');
                    $.ajax({
                        url:"controller/load_raw_text.php",
                        method:"POST",
                        dataType: "json",       
                        data:{page: page},
                        success:function(responseData){
                            $('#datatext').html(responseData.html);
                        }
                    });
                }       
            });
        });
    </script>

    <!-- Bootstrap core JavaScript-->
    <script src="assets/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

    <!-- Core plugin JavaScript-->
    <script src="assets/vendor/jquery-easing/jquery.easing.min.js"></script>

    <!-- Custom scripts for all pages-->
    <script src="assets/js/sb-admin-2.min.js"></script>

    <!-- Page level plugins -->
    <script src="assets/vendor/chart.js/Chart.min.js"></script>

    <!-- Page level custom scripts -->
    <script src="assets/js/demo/chart-area-demo.js"></script>
    <script src="assets/js/demo/chart-pie-demo.js"></script>

</body>
</html>