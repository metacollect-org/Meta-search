$(function(){

    $('#search').keyup(function() {

        $.ajax({
            type: "GET",
            url: "/mainApp/search/",
            data: {
                'q' : $('#search').val()
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