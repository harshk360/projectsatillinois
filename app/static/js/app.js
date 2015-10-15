'use strict';

angular
    .module('projects', [
        'ngRoute'
    ])
    .config(function ($routeProvider) {
        $routeProvider
            .when('/home/:pageId', {
                templateUrl: 'static/views/home.html',
                controller: 'HomeCtrl'
            })
            .when('/profile/:profileId', {
                templateUrl: 'static/views/profile.html',
                controller: 'ProfileCtrl'
            })
            .when('/event/:eventId', {
                templateUrl: 'static/views/event.html',
                controller: 'EventCtrl'
            })
            .otherwise({
                templateUrl: 'static/views/home.html',
                controller: 'HomeCtrl'
            });
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
                     console.log(value.first_name);
                     $scope.user = value.first_name;
                     $scope.picture_url = value.picture_url;
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
    .controller('HomeCtrl', function ($scope, $http, $routeParams) {
        if ($routeParams.pageId === undefined){
            $routeParams.pageId = 1;
        }
        $http
            .get('/api/projects/page/' + $routeParams.pageId)
            .success(function(res){
                $scope.projects = res.projects;
                $scope.number_of_pages = new Array(res.number_of_pages);
                $scope.current_page = parseInt($routeParams.pageId);
                //TODO: More Error Handling
            }
        );

    })
    .controller('ProfileCtrl', function ($scope, $http, $routeParams) {
        $http
            .get('/api/user/' + $routeParams.profileId)
            .success(function(routeUser){
                $http
                    .get('/api/user/current')
                    .success(function(currUser){
                        if (currUser.id === routeUser.id){
                            $scope.setEditable = true;
                            $scope.user = currUser;
                        }else{
                            $scope.setEditable = false;
                            $scope.user = routeUser;
                        }
                    });
            });

        $scope.updateInfomation = function(){
            var obj = {academic_major:$scope.user.academic_major, graduation_year: $scope.user.graduation_year}
            $http
                .post('/api/user/current/update',obj)
                .success(function(){
                    alert("Successfully updated!")
                })
        }
    })
    .controller('EventCtrl', function ($scope, $routeParams, $http, $route) {

        $http
            .get('/api/project/' + $routeParams.eventId)
            .success(function(res) {
                $scope.event = res;
            
            });
        $http
            .get('api/user/current')
            .success(function(value){
                 if (value.error){
                     $scope.loggedIn = false;
                 }else{
                     $scope.user = value;
                     $scope.loggedIn = true;
                     $scope.user_id = value.id;
                 }
            });
        $scope.changeStatus = function(status){
            $http
                .get('/api/event/' + $routeParams.eventId + '/signup/' + $scope.user_id + "/" + status)
                .success(function (res){
                    $scope.status = res.status;
                    console.log(res);
                    $route.reload();

            });
        };
    });