'use strict';

angular
    .module('projects', [
        'ngRoute'
    ])
    .config(function ($routeProvider) {
        $routeProvider
            .when('/completed', {
                templateUrl: 'static/views/home.html',
                controller:'ProjectsCtrl'
            })
            .when('/inprogress', {
                templateUrl: 'static/views/home.html',
                controller: 'ProjectsCtrl'
            })
            .when('/recommended', {
                templateUrl: 'static/views/home.html',
                controller: 'ProjectsCtrl'
            })
            .when('/trending', {
                templateUrl: 'static/views/home.html',
                controller: 'ProjectsCtrl'
            })
            .when('/profile/:profileId', {
                templateUrl: 'static/views/profile.html',
                controller: 'ProfileCtrl'
            })
            .when('/project/:projectId', {
                templateUrl: 'static/views/project.html',
                controller: 'ProjectCtrl'
            })
            .when('/createproject', {
                templateUrl: 'static/views/addProject.html',
                controller: 'AddProjectCtrl'
            })
            .otherwise('/completed');
    });

angular.module('projects')
    .controller('NavCtrl', function($scope, $http, $location) {
        $scope.user = "";
        $scope.loggedIn = false;

        $http
            .get('api/user/current')
            .success(function(value){
                 if (value.error){
                     $scope.loggedIn = false;
                 }else{
                     $scope.loggedIn = true;
                     $scope.user = value.full_name;
                     $scope.avatar = value.avatar;
                     $scope.userRoute = "/#/profile/" + value.id;
                 }
            });

        $scope.logIn = function() {
            var req = {
                method: 'GET',
                url: 'facebook_login',
                headers: {
                    'Access-Control-Allow-Origin': '*','Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type, X-Requested-With'
                }
            };
            $http(req)
                .success(function(){
                    $scope.loggedIn = true;
                    $scope.user = "";
                    $location.path('/home');
                });

        };

        $scope.logOut = function() {
            $http
                .get('logout')
                .success(function(){
                    $scope.loggedIn = false;
                    $location.path('/home');
                })
        };
    })
    .controller('ProjectsCtrl', function ($scope, $http, $routeParams, $location, $sce, $route) {

        $(document).ready(function() {
            $("#view-project").click(function() {
                $('html, body').animate({
                    scrollTop: $(".index").offset().top
                }, 1000);
            });
        });

        $http
            .get('api/user/current')
            .success(function(value){
               if (value.error){
                   $scope.loggedIn = false;
               }else{
                   $scope.loggedIn = true;
                   $scope.user = value.full_name;
                   $scope.avatar = value.avatar;
                   $scope.userRoute = "/#/profile/" + value.id;
                   $('#create-project').show();
               }
            })
            .error(function(err){
                $('#create-project').hide();
                 $scope.loggedIn = false;
            });

        $scope.defaultImage = "/static/img/hero_blur.jpg";

        $scope.initialLoad = function() {
            if ($route.current.$$route.originalPath === '/completed') {
                $scope.status = "completed";
                $http
                    .get('api/v1/projects/COMPLETED')
                    .success(function(value) {
                        $scope.projects = value.projects;
                    });
           } else if($route.current.$$route.originalPath === '/recommended') {
               $scope.status = "recommended";
               $http
                   .get('recommend')
                   .success(function(value) {
                       var projects = [];
                       for (var i of value.value) {
                         projects.push(i.project);
                       }
                       $scope.projects = projects;
                   })
                   .error(function(value){
                      $scope.projects = [];
                   });
           } else if ($route.current.$$route.originalPath === '/trending') {
               $scope.status = "trending";
               $http
                   .get('projects/trending')
                   .success(function(value) {
                       $scope.projects = value.projects;
                   });
           } else {
               $scope.status = "in_progress";
               $http
                   .get('api/v1/projects/IN_PROGRESS')
                   .success(function(value) {
                       $scope.projects = value.projects;
                   });
           }
        }();

        $scope.go = function(path){
            $location.path(path);
        };
    })
    .controller('ProjectCtrl', function ($scope, $routeParams, $http, $route, $sce, $timeout) {
        $scope.project = {};
        $scope.defaultImage = "/static/img/hero_blur.jpg";
        $http
            .get('api/v1/project/' + $routeParams.projectId)
            .success(function(value) {
                $scope.project = value.project;
                $http
                    .get('api/user/current')
                    .success(function(currUser) {
                        if (currUser.id == value.project.owner.id) {
                            $scope.setEditable = true;
                            $scope.isOwner = true;
                        }
                        if (value.error){
                            $scope.loggedIn = false;
                        } else {
                            $scope.loggedIn = true;
                        }
                    });
                $http
                    .get('/project/edit/' + $routeParams.projectId)
                    .success(function(html){
                        $scope.updateProject = $sce.trustAsHtml(html);
                        $timeout(function() {
                            $scope.setupForm();
                        });
                    });
                $http
                    .get('/project/add/' + value.project.id +'/image')
                    .success(function(html) {
                        $scope.imageUploader = $sce.trustAsHtml(html);
                        $timeout(function() {
                            $scope.setupImageForm();
                        });
                    })
                    .error(function(err){
                        console.log(err);
                    });
                $http
                    .get('/project/add/' + value.project.id +'/team_member')
                .success(function(html) {
                        $scope.teamMemberUploader = $sce.trustAsHtml(html);
                        $timeout(function() {
                            $scope.setupTeamMemberForm();
                        });
                    })
                $http
                    .get('/project/add/' + value.project.id +'/comment')
                .success(function(html) {
                        $scope.commentUploader = $sce.trustAsHtml(html);
                        $timeout(function() {
                            $scope.setupCommentForm();
                        });
                    })
            })
            .error(function(err) {
                console.log(err);
            });
        $scope.removeImage = function(index) {
            $http
                .get('/api/v1/delete/image/' + index)
                .success(function(value) {
                    console.log(value);
                    location.reload();
                })
        };
        $scope.setupForm = function () {
            $('#my-select').multiSelect();
            var form = $('#project_form');
            $("#submit_project").click(function(event) {
                event.preventDefault();
                $.ajax( {
                    type: "POST",
                    url: form.attr('action'),
                    data: form.serialize(),
                    success: function(response) {
                        form.replaceWith(response);
                        console.log(response);
                        $scope.setupForm();
                    }
                });
            });
        };
        $scope.setupImageForm = function () {
            var form = $('#image_form');
            $("#image-submit").click(function(event) {
                event.preventDefault();
                $.ajax({
                    type: "POST",
                    url: form.attr('action'),
                    data: form.serialize(),
                    statusCode: {
                        200: function (response) {
                            form.replaceWith(response);
                            $scope.setupImageForm();
                        },
                        201: function (response) {
                            $timeout(function(){
                                location.reload();
                            });
                        }
                    }
                });
            });
        }
        $scope.setupTeamMemberForm = function () {
            var form = $('#team-member-form');
            $("#team-member-submit").click(function(event) {
                event.preventDefault();
                $.ajax({
                    type: "POST",
                    url: form.attr('action'),
                    data: form.serialize(),
                    statusCode: {
                        200: function (response) {
                            form.replaceWith(response);
                            $scope.setupTeamMemberForm();
                        },
                        201: function (response) {
                            $timeout(function(){
                                location.reload();
                            });
                        }
                    }
                });
            });
        }

        $scope.setupCommentForm = function () {
            var form = $('#comment-form');
            $("#comment-submit").click(function(event) {
                event.preventDefault();
                $.ajax({
                    type: "POST",
                    url: form.attr('action'),
                    data: form.serialize(),
                    statusCode: {
                        200: function (response) {
                            form.replaceWith(response);
                            $scope.setupCommentForm();
                        },
                        201: function (response) {
                            $timeout(function(){
                                location.reload();
                            });
                        }
                    }
                });
            });
        }
        $scope.toggleEditable = function () {
            $scope.setEditable = !$scope.setEditable;
        }

        $scope.getYoutubeEmbed = function(id) {
            return $sce.trustAsResourceUrl("https://www.youtube.com/embed/" + id.substr(-11));
        };

        $scope.removeTeamMember = function(project_id, user_id) {
            $http
                .get('/api/v1/delete/team_member/' + project_id + "/" + user_id)
                .success(function(value) {
                    location.reload();
                })
        };

    })
    .controller('ProfileCtrl', function ($scope, $routeParams, $http, $route, $sce, $timeout, $location) {
        $scope.user = {};
        $scope.setEditable = false;
        $http
            .get('api/user/' + $routeParams.profileId)
            .success(function(value) {
                $scope.user = value;
                $http
                    .get('api/user/current')
                    .success(function(currUser) {
                        if (currUser.id == value.id) {
                            $scope.setEditable = true;
                        }
                        $http
                            .get('/user/update')
                            .success(function(html){
                                $scope.updateForm = $sce.trustAsHtml(html);
                                $timeout(function() {
                                     $scope.setupUserForm();
                                });
                            })

                    })
                    .error(function(err){
                        console.log("No User Logged In");
                    });

            })
            .error(function(err) {
                alert("This user does not exist!")
                $location.path("/home");
                console.log(err);
            });

        $scope.setupUserForm = function () {
            $('#my-select').multiSelect();
            var form = $('#user-form');
            $("#submit-user").click(function(event) {
                event.preventDefault();
                $.ajax( {
                    type: "POST",
                    url: form.attr('action'),
                    data: form.serialize(),
                    success: function(response) {
                        form.replaceWith(response);
                        console.log(response);
                        $scope.setupUserForm();
                    }
                });
            });
        };
    })
    .controller('AddProjectCtrl', function($scope, $http, $sce, $timeout, $location) {
        $http
            .get('api/user/current')
            .error(function(value){
                $location.path('/home');
            });
        $http
            .get('/project/add')
            .success(function(html){
                $scope.createProjectForm = $sce.trustAsHtml(html);
                $timeout(function() {
                    $scope.setupForm();
                });
            });
        $scope.setupForm = function () {
            $('#my-select').multiSelect();
            var form = $('#project_form');
            $("#submit_project").click(function(event) {
                event.preventDefault();
                $.ajax( {
                    type: "POST",
                    url: form.attr('action'),
                    data: form.serialize(),
                    statusCode: {
                        200: function (response) {
                            form.replaceWith(response);
                            $scope.setupForm();
                        },
                        201: function (response) {
                            $timeout(function(){
                                $location.path(response);
                            });
                        }
                    }
                });
            });
        };
    });
