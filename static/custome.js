$(document).ready(function () {
    $('#loadmore').on('click',function () {
            var _curentProducts = $('.product-box').length;
            var _limit=$(this).attr('data-limit');
            var _total=$(this).attr('data-total');
            console.log(_curentProducts,_limit,_total)
    //    start ajax
            $.ajax({
                url : '/loadmode_data',
                data : {
                    'limit':_limit,
                    'offset':_curentProducts,
                    'total':_total
                },
                dataType : 'json',
                beforeSend : function () {
                    $('#loadmore').attr('disabled',true);
                    $('.load-more-icon').addClass('fa-spin');
                },
                success : function (res) {
                    console.log(res.data)
                    $('#filteredproducts').append(res.data);
                    $('#loadmore').attr('disabled',false);
                    $(".load-more-icon").removeClass('fa-spin');
                    // remove the loadmore button
                    var _totalshowing = $('.product-box').length;
                    if ( _totalshowing==_total){
                        $('#loadmore').remove()
                    }
                }
            });
    // end ajax
    });

    // product variation price based on color and wuantity
    $('.choose-size').hide();
    //    end


//    show sizes according selecting colors
    $('.choose-color').on('click',function () {
        $('.choose-size').removeClass('active');
        $('.choose-color').removeClass('focused');
        $(this).addClass('focused');

        var _color = $(this).attr('data-color');
        // console.log(_color)
        $('.choose-size').hide();
        $('.color'+_color).show();
        $('.color'+_color).first().addClass('active')
        var _price = $('.color'+_color).first().attr('data-price');
          $('.product-price').text(_price)
    });
//    end


// show the first selected color first selected size
    $(".choose-color").first().addClass('focused');
    var _color = $('.choose-color').first().attr('data-color');
    var _price = $('.choose-size').first().attr('data-price');
    $('.color'+_color).show();
    $('.color'+_color).first().addClass('active');
    // $(".product-price").text(_price);

    //    end

//    show the price according the selected size
    $('.choose-size').on('click',function () {
        var _price = $(this).attr('data-price');
        $('.choose-size').removeClass('active');
        $(this).addClass('active')
        console.log(_price)
        $('.product-price').text(_price)
    });
//    end

//    add to cart functionality
        $(document).on('click','#addToCart',function () {
            var _vm=$(this);
            var _qty = $('#product-qty').val();
            var _productid = $('.product-id').val();
            var _producttitle = $('.product-title').val();
            var _productprice = $('.product-price').text();
            var _productimage = $('.product-image').val();
            // console.log(_productimage)
            // console.log(_qty,_productid,_producttitle,_productprice,_productimage)
        //    ajax
            $.ajax({
                url : '/add_to_cart',
                data : {
                    'id':_productid,
                    'qty': _qty,
                    'title':_producttitle,
                    'price':_productprice,
                    'image':_productimage
                },
                dataType: 'json',
                beforeSend:function () {
                    _vm.attr('disabled',true)
                },
                success:function (res) {
                    console.log(res.data);
                    $('.cart-list').text(res.totalitems);
                    _vm.attr('disabled',false);

                }
            });
        //    end ajax


        });
//    end add to cart functionality
    //    delete cart item
        $(document).on('click','.delete-item',function () {
                var _pid = $(this).attr('data-item');
                var _vm = $(this);
                console.log(_pid);
            //    ajax code
                $.ajax({
                    url : '/delete_from_cart',
                    data:{
                        'id':_pid
                    },
                    contentType:'json',
                    beforeSend:function () {
                        _vm.attr('disabled',true);
                    },
                    success:function (res) {
                        console.log(res );
                        _vm.attr('disabled',false);
                        $('.cart-list').text(res.totalitems);
                        $('#cartlist').html(res.data)

                    }
                });
            //    ajax end
            });
        //    end for delete cart item

//    update cart item in cart list page
    $(document).on('click','.update-data',function () {
            var p_id = $(this).attr('data-item');
            var p_qty = $('.product-qty-'+p_id).val();
            var _vm=$(this);
            console.log(p_id,p_qty)
    //    ajax start
            $.ajax({
                url : '/update_cart_item',
                data:{
                    'id':p_id,
                    'qty':p_qty
                },
                contentType: 'json',
                beforeSend:function () {
                    _vm.attr('disabled',true)
                },
                success:function (res) {
                    console.log(res.data);
                    _vm.attr('disabled',false);
                    $('#cartlist').html(res.data)

                }
            });
    //    ajax end
    });
//    end update item in cart list page

});