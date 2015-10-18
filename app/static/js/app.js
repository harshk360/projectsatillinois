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
        /**
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
        */

    })
    .controller('CompletedCtrl', function ($scope, $http, $routeParams, $location) {
        $scope.projects = [
            {
                name: "Berwin For President",
                description: "Berwin 2016.",
                picture: "https://scontent-ord1-1.xx.fbcdn.net/hphotos-xat1/v/t1.0-9/11350732_10207699662912723_1646685888682476380_n.jpg?oh=ad89e16c1a884d1aaac7f4a403b19a50&oe=5689DB7F"
            },
            {
                name: "Berwin For President",
                description: "Berwin 2016.",
                picture: "https://scontent-ord1-1.xx.fbcdn.net/hphotos-xat1/v/t1.0-9/11350732_10207699662912723_1646685888682476380_n.jpg?oh=ad89e16c1a884d1aaac7f4a403b19a50&oe=5689DB7F"
            },
            {
                name: "Berwin For President",
                description: "Berwin 2016.",
                picture: "https://scontent-ord1-1.xx.fbcdn.net/hphotos-xat1/v/t1.0-9/11350732_10207699662912723_1646685888682476380_n.jpg?oh=ad89e16c1a884d1aaac7f4a403b19a50&oe=5689DB7F"
            },
            {
                name: "Berwin For President",
                description: "Berwin 2016.",
                picture: "https://scontent-ord1-1.xx.fbcdn.net/hphotos-xat1/v/t1.0-9/11350732_10207699662912723_1646685888682476380_n.jpg?oh=ad89e16c1a884d1aaac7f4a403b19a50&oe=5689DB7F"
            },
            {
                name: "Berwin For President",
                description: "Berwin 2016.",
                picture: "https://scontent-ord1-1.xx.fbcdn.net/hphotos-xat1/v/t1.0-9/11350732_10207699662912723_1646685888682476380_n.jpg?oh=ad89e16c1a884d1aaac7f4a403b19a50&oe=5689DB7F"
            },
            {
                name: "Berwin For President",
                description: "Berwin 2016.",
                picture: "https://scontent-ord1-1.xx.fbcdn.net/hphotos-xat1/v/t1.0-9/11350732_10207699662912723_1646685888682476380_n.jpg?oh=ad89e16c1a884d1aaac7f4a403b19a50&oe=5689DB7F"
            },

        ];

        $scope.go = function ( path ) {
            $location.path( path );
        };
    })
    .controller('InProgressCtrl', function ($scope, $http, $routeParams, $location) {

        $scope.projects = [
            {
                name: "Donald For President",
                description: "Vote for Berwin Instead 2016.",
                picture: "http://static6.businessinsider.com/image/55918b77ecad04a3465a0a63/nbc-fires-donald-trump-after-he-calls-mexicans-rapists-and-drug-runners.jpg"
            },
            {
                name: "Donald For President",
                description: "Vote for Berwin Instead 2016.",
                picture: "http://static6.businessinsider.com/image/55918b77ecad04a3465a0a63/nbc-fires-donald-trump-after-he-calls-mexicans-rapists-and-drug-runners.jpg"
            },
            {
                name: "Donald For President",
                description: "Vote for Berwin Instead 2016.",
                picture: "http://static6.businessinsider.com/image/55918b77ecad04a3465a0a63/nbc-fires-donald-trump-after-he-calls-mexicans-rapists-and-drug-runners.jpg"
            },
            {
                name: "Donald For President",
                description: "Vote for Berwin Instead 2016.",
                picture: "http://static6.businessinsider.com/image/55918b77ecad04a3465a0a63/nbc-fires-donald-trump-after-he-calls-mexicans-rapists-and-drug-runners.jpg"
            },
            {
                name: "Donald For President",
                description: "Vote for Berwin Instead 2016.",
                picture: "http://static6.businessinsider.com/image/55918b77ecad04a3465a0a63/nbc-fires-donald-trump-after-he-calls-mexicans-rapists-and-drug-runners.jpg"
            },
        ];

        $scope.go = function ( path ) {
            $location.path( path );
        };

    })
    .controller('ProjectCtrl', function ($scope, $routeParams, $http, $route) {

    });