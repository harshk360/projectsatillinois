$(document).ready(function() {
    $.ajax({
        url: "/api/admin/logins",
        method: "GET",
        success: function(response) {
            Morris.Line({
              element: 'line-chart',
              data: JSON.parse(response),
              xkey: 'y',
              ykeys: ['a'],
              labels: ['Logins']
          });

        } 
    });
});