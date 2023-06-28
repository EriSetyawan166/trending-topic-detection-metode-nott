<?php

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
    <link href="../assets/vendor/fontawesome-free/css/all.min.css" rel="stylesheet" type="text/css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet" type="text/css">
    <script src="../assets/vendor/jquery/jquery.min.js"></script>
    <script src="../assets/js/simple-bootstrap-paginator.js"></script>
    <link
        href="https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i"
        rel="stylesheet">

    <!-- Custom styles for this template-->
    <link href="../assets/css/sb-admin-2.min.css" rel="stylesheet">

</head>

<body id="page-top">

    <!-- Page Wrapper -->
    <div id="wrapper">

        <!-- Sidebar -->
        <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">

            <!-- Sidebar - Brand -->
            <a class="sidebar-brand d-flex align-items-center justify-content-center" href="../index.php">
                <div class="sidebar-brand-icon rotate-n-15">
                    <i class="fas fa-laugh-wink"></i>
                </div>
                <div>Deteksi Trending Topik</div>
            </a>

            <!-- Divider -->
            <hr class="sidebar-divider my-0">

            <!-- Nav Item - Dashboard -->
            <li class="nav-item">
                <a class="nav-link" href="../index.php">
                    <i class="fas fa-fw fa-magnifying-glass"></i>
                    <span>Tarik Data</span></a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="preprocessing.php">
                    <i class="fas fa-fw fa-file-word"></i>
                    <span>Preprocessing</span></a>
            </li>

            <!-- Nav Item - Pages Collapse Menu -->
            <li class="nav-item active">
                <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapseTwo"
                    aria-expanded="true" aria-controls="collapseTwo">
                    <i class="fas fa-fw fa-cog"></i>
                    <span>Modelling</span>
                </a>
                <div id="collapseTwo" class="collapse show" aria-labelledby="headingTwo" data-parent="#accordionSidebar">
                    <div class="bg-white py-2 collapse-inner rounded">
                        <a class="collapse-item" href="clustering.php">ClusterSing</a>
                        <a class="collapse-item active" href="scoring.php">Scoring</a>
                        <a class="collapse-item" href="lda.php">LDA Topic</a>
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


                </nav>
                <!-- End of Topbar -->

                <!-- Begin Page Content -->
                <div class="container-fluid">

                <!-- Content Row -->

                <!-- Content Row -->
                <div class="row">

                <div class="col-lg-12 mb-4">

                <!-- Project Card Example -->
                <!-- Content Column -->
                <div class="col-lg-12 mb-4">

                   <!-- Project Card Example -->
                    <div class="card shadow mb-4">
                        <div class="card-header py-3">
                            <h6 class="m-0 font-weight-bold text-primary">Scoring</h6>
                        </div>
                        <div class="card-body">
                            <div class="col-md-12 mb-4 text-center">
                                <div class="border p-3">
                                    <img src="../assets/img/cluster_ranking_scores_top.png" alt="top-5 score Image" class="img-fluid">
                                </div>
                            </div> 
                            <div class="col-md-12 mb-4 text-center">
                                <div class="border p-3">
                                    <img src="../assets/img/cluster_ranking_scores.png" alt="score Image" class="img-fluid">
                                </div>
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
                        url:"../controller/load_all_text.php",
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
    <script src="../assets/vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

    <!-- Core plugin JavaScript-->
    <script src="../assets/vendor/jquery-easing/jquery.easing.min.js"></script>

    <!-- Custom scripts for all pages-->
    <script src="../assets/js/sb-admin-2.min.js"></script>

    <!-- Page level plugins -->
    <script src="../assets/vendor/chart.js/Chart.min.js"></script>

    <!-- Page level custom scripts -->
    <script src="../assets/js/demo/chart-area-demo.js"></script>
    <script src="../assets/js/demo/chart-pie-demo.js"></script>

</body>
</html>