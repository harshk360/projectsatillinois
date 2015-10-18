'use strict';

angular
    .module('projects', [
        'ngRoute',
        'ui.bootstrap'
    ])
    .config(function ($routeProvider) {
        $routeProvider
            .when('/completed', {
                templateUrl: 'static/views/completed.html',
                controller:'CompletedCtrl'
            })
            .when('/inprogress', {
                templateUrl: 'static/views/inprogress.html',
                controller: 'InProgressCtrl'
            })
            .when('/profile/:profileId', {
                templateUrl: 'static/views/profile.html',
                controller: 'ProfileCtrl'
            })
            .when('/project/:projectId', {
                templateUrl: 'static/views/project.html',
                controller: 'ProjectCtrl'
            })
            .otherwise('/completed');
    });

angular.module('projects')
    .controller('NavCtrl', function($scope, $http, $location) {

        $scope.user = "";
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

        $scope.loggedIn = false;
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
    .controller('CompletedCtrl', function ($scope, $http, $routeParams, $location) {

        $http
            .get('api/v1/projects/COMPLETED')
            .success(function(value) {
                $scope.projects = value.projects;
            });

        $scope.go = function ( path ) {
            $location.path( path );
        };
    })
    .controller('InProgressCtrl', function ($scope, $http, $routeParams, $location) {

        $http
            .get('api/v1/projects/IN_PROGRESS')
            .success(function(value) {
                $scope.projects = value.projects;
            });

        $scope.go = function ( path ) {
            $location.path( path );
        };

    })
    .controller('ProjectCtrl', function ($scope, $routeParams, $http, $route) {
        $scope.project = {};

        $http
            .get('api/v1/project/' + $routeParams.projectId)
            .success(function(value) {
                if (value.project.status === "IN_PROGRESS") {
                    value.project.status = "In Progress";
                } else {
                    value.project.status = "Completed";
                }
                $scope.project = value;
                console.log(value);
            })
            .error(function(err) {
                console.log(err);
            });
    })
    .controller('ProfileCtrl', function ($scope, $routeParams, $http, $route, $sce) {
        $scope.user = {};
        $http
            .get('api/user/' + $routeParams.profileId)
            .success(function(value) {
                console.log(value);
                $http
                    .get('api/user/current')
                    .success(function(currUser) {
                        if (currUser.id == value.id) {
                            $scope.setEditable = true;
                        }
                        $scope.user = value;
                    });
                $http
                    .get('/user/update')
                    .success(function(html){
                        $scope.updateForm = $sce.trustAsHtml(html);
                    })
            })
            .error(function(err) {
                console.log(err);
            });

        $scope.updateUserDetails = function() {

        }
    });