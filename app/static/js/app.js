'use strict';

angular
    .module('projects', [
        'ngRoute'
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
                console.log(value);
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
        $scope.project = {
            name: "Berwin For President",
            description: "Berwin 2016.",
            picture: "https://scontent-ord1-1.xx.fbcdn.net/hphotos-xat1/v/t1.0-9/11350732_10207699662912723_1646685888682476380_n.jpg?oh=ad89e16c1a884d1aaac7f4a403b19a50&oe=5689DB7F",
            id: "1234",
            completed: true
        };
    });