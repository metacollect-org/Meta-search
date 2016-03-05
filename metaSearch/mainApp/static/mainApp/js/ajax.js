$(function(){

    $('#search').keyup(function() {
        if($('#search').val().length > 3){
          $.ajax({
              type: "GET",
              url: "/mainApp/search/autocomplete/",
              data: {
                  'q' : $('#search').val(),
              },
              success: searchSuccess,
              dataType: 'html'
          });
        }else{
          searchSuccess("",null ,null )
        }

    });

     $('input[name=category]').on('click', function() {
        var selected = []
        $('input[name=category]:checked').each(function() {
            selected.push($(this).val());
        })
        $.ajax({
            type: "GET",
            url: "/mainApp/search/autocomplete/",
            data: {
                'q' : $('#search').val(),
                'category' : selected.join()
            },
            success: searchSuccess,
            dataType: 'html'
        });

    });

});

function searchSuccess(data, textStatus, jqXHR)
{
    //$('#search-results').html('')
    $('#search-results').html(data);
}
