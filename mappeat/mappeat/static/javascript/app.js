var app = angular.module('TableApp', [
     'ui.router',
     'restangular'
 ])
 
 app.config(function ($stateProvider, $urlRouterProvider, RestangularProvider) {
     // For any unmatched url, send to /route1
     $urlRouterProvider.otherwise("/");
     $stateProvider
         .state('index', {
 
             url: "/",
             templateUrl: "/static/html/partials/_table_list.html",
             controller: "TableList"
         })
 
        .state('new', {
 
             url: "/new",
             templateUrl: "/tables/table-form",
             controller: "TableFormCtrl"
         })
 })
 
app.controller("TableFormCtrl", ['$scope', 'Restangular', 'CbgenRestangular', '$q',
 function ($scope, Restangular, CbgenRestangular, $q) {
 
    $scope.submitTable = function () {
       var post_update_data = create_resource($scope, CbgenRestangular);
       $q.when(post_update_data.then(
                         function (object) {
                             // success!
                             console.log('%c My success here', "background: blue; color: black; padding-left:10px;");
                         },
 
                         function (object){
                             // error!
                             console.log('%c My error here', "background: blue; color: black; padding-left:10px;");
                             console.log(object.data)
                         }
                            
                     ))
                 }
 
 }])// end controller
 
 app.factory('CbgenRestangular', function (Restangular) {
         return Restangular.withConfig(function (RestangularConfigurer) {
             RestangularConfigurer.setBaseUrl('/api/v1');
         });
     })
 
 populate_scope_values = function ($scope) {
     return {number: $scope.number, type_table: $scope.type_table };
 },
 
 create_resource = function ($scope, CbgenRestangular) {
 var post_data = populate_scope_values($scope)
     return CbgenRestangular.all('table').post(post_data)
 },