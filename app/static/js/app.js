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
                })
        };
    })
    .controller('ProjectsCtrl', function ($scope, $http, $routeParams, $location, $sce, $route) {

        $scope.defaultImage = "http://academics.triton.edu/faculty/fheitzman/uiuc%20computer%20building%202.jpg";

        $scope.initialLoad = function() {
           if ($route.current.$$route.originalPath === '/completed') {
               $scope.completed = true;
               $http
                   .get('api/v1/projects/COMPLETED')
                   .success(function(value) {
                       $scope.projects = value.projects;
                   });
           } else {
               $scope.completed = false;
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
    .controller('ProjectCtrl', function ($scope, $routeParams, $http, $route, $sce) {
        $scope.project = {};
        $scope.defaultImage = "http://academics.triton.edu/faculty/fheitzman/uiuc%20computer%20building%202.jpg";

        $http
            .get('api/v1/project/' + $routeParams.projectId)
            .success(function(value) {
                if (value.project.status === "IN_PROGRESS") {
                    value.project.status = "In Progress";
                } else {
                    value.project.status = "Completed";
                }
                $scope.project = value.project;

                $http
                    .get('api/user/current')
                    .success(function(currUser) {
                        if (currUser.id == value.project.owner.id) {
                            $scope.setEditable = true;
                        }
                    });
                $http
                    .get('/project/edit/' + $routeParams.projectId)
                    .success(function(html){
                        $scope.updateProject = $sce.trustAsHtml(html);
                    });
                $http
                    .get('/project/add/' + value.project.id +'/image')
                    .success(function(html) {
                        $scope.imageUploader = $sce.trustAsHtml(html);
                    })
                    .error(function(err){
                        console.log(err);
                    });
            })
            .error(function(err) {
                console.log(err);
            });
    })
    .controller('ProfileCtrl', function ($scope, $routeParams, $http, $route, $sce) {
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
                            })

                    })
                    .error(function(err){
                        console.log("No User Logged In");
                    });

            })
            .error(function(err) {
                console.log(err);
            });
    })
    .controller('AddProjectCtrl', function($scope, $http, $sce) {
        $http
            .get('/project/add')
            .success(function(html){
                $scope.createProjectForm = $sce.trustAsHtml(html);
                console.log(html);
            });
    });