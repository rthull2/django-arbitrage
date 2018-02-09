$(document).ready(function(){
    sortRatioTable();

    $('#ratiotable').on('click', 'tr', function(e){
        e.preventDefault();
        $('#markettable tbody tr').remove();
        var selected = $(this);
        $('#ratiotable tbody tr').each(function(){
            if ($(this).is(selected)){
                $(this).addClass('highlight');
            } else {
                $(this).removeClass('highlight');
            }
        });
        var coin = $(this).attr('name');
        $.getJSON('ajax/marketInfo', {'coin': coin}, function(data){
            $(data).each(function(i, market){
                var row = '<tr name="'+coin+'" exchange="'+market['source']+'"><td><a href="'+market['link']+'">'+market['source']+'</a></td><td>'+market['base']+'</td><td><span class="glyphicon ';
                if (market['wallet']){
                    row += 'glyphicon-minus';
                }
                row += '"></span></td><td class="text-right">'+market['volume']+'</td><td class="text-right">'+market['price']+'</td></tr>';
                $('#markettable').append(row);
            });
        });
    });

    $('#coinsearch').keyup(function() {
        $('#ratiotable tbody tr').each(function() {
            search = $('#coinsearch').val().toUpperCase();
            if ($(this).attr('name').toUpperCase().indexOf(search) >= 0 || $(this).attr('symbol').indexOf(search) >= 0){
                $(this).show();
            } else {
                $(this).hide();
            }
        })
    });

    $('div.exchanges').on('click', 'button', function(){
        $(this).toggleClass('btn-danger');
        $(this).toggleClass('btn-success');
        var cookie_exchanges = Cookies.get('exchanges');
        if (cookie_exchanges != undefined){
            cookie_exchanges = JSON.parse(cookie_exchanges)
            if ($(this).hasClass('btn-success')){
                cookie_exchanges.push($(this).prop('id'));
            } else if ($(this).hasClass('btn-danger')){
                cookie_exchanges.splice($.inArray($(this).prop('id'), cookie_exchanges), 1);
            }
        } else {
            cookie_exchanges = [];
            $('div.exchanges').children('button').each(function(){
                if ($(this).hasClass('btn-success')){
                    cookie_exchanges.push($(this).prop('id'));
                }
            });
        }
        Cookies.set('exchanges', JSON.stringify(cookie_exchanges));
    });

    $('tbody.marketInfo').on('click', '.glyphicon-minus', function(){
        var exchange = $($(this).closest('tr')).attr('exchange');
        var coin = $($(this).closest('tr')).attr('name');
        var row = $(this).closest('tr');
        $.getJSON('ajax/wallet_status', {'exchange': exchange, 'coin': coin}, function(data){
            row.siblings().addBack().each(function(){
                if ($(this).attr('exchange') == exchange){
                    $(this).find('.glyphicon').removeClass('glyphicon-minus');
                    if (data['status'] == true){
                        $(this).find('.glyphicon').addClass('glyphicon-ok');
                    } else {
                        $(this).find('.glyphicon').addClass('glyphicon-remove');
                    }
                }
            });
        });
    })
})

function sortRatioTable() {
    var rows = $('#ratiotable tbody tr').get();
    rows.sort(function(x,y){
        return $(y).find('.ratio').text() - $(x).find('.ratio').text();
    });
    for (var i = 0; i < rows.length; i++){
        $('#ratiotable').append(rows[i]);
    }
}