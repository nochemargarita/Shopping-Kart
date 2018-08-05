"use strict";
$(document).ready(function() {
            
            // AJAX calls to get all the product from the database
            let productNames = [];

            function listProducts(results) {
              let products = results;
              for (let product in products) {
                
                productNames.push(products[product]);
              }
            }

            function getProducts() {
                $.get('/suggestions', listProducts);
            }
              
            getProducts();

            // for the autocomplete, reference: https://jqueryui.com/autocomplete/
            $('#products').autocomplete({
              source: productNames,
              autoFocus: true

            });

            $('#products').autocomplete('widget').addClass('fixed-height');

            

            // Event listener for adding product.
            let productAndQuantity = {};
            $('.add-product').click(function(evt){
                evt.preventDefault();
                let product = $('#products').val().split(" ").join('-');

                let addButton = `<button class=${product}-add><i class="fas fa-plus"></i></button>`;
                let removeButton = `<button class=${product}-remove><i class="fas fa-minus"></i></button>`;

                if ($('tr').hasClass(product)){
                  $('#'+product).html(Number($('#'+product).html()) + 1);
                  productAndQuantity[$('#products').val()] += 1 ;
                } else {
                  $('tbody').append(`<tr class=${product}>
                                      <th class='product-name' scope="row">${$('#products').val()}</th>
                                      <td id=${product}> 1 </td>
                                      <td>${removeButton} &nbsp; ${addButton}</td>
                                     </tr>`);
                  productAndQuantity[$('#products').val()] = 1
                }
                // adding and removing products from the cart using minus and plus icons.
                $('.'+product+'-add').unbind('click').click(function(evt){
                  evt.preventDefault();
                  $('#'+product).html(Number($('#'+product).html()) + 1);
                  productAndQuantity[$('#products').val()] += 1
                });

                $('.'+product+'-remove').unbind('click').click(function(evt){
                  evt.preventDefault();
                  if (Number($('#'+product).html() > 1)){
                    $('#'+product).html(Number($('#'+product).html()) - 1)
                    productAndQuantity[$('#products').val()] -= 1
                  } else {
                    $('.'+product).remove();
                    productAndQuantity[$('#products').val()] -= 1
                  } 
                });
            });

            function alerCustomer(result) {
                alert(result);
            }

            $('.logout').click(function(evt){
                let cartProducts = {data: JSON.stringify(productAndQuantity)};
                $.post('/kartItem', cartProducts, alerCustomer);
            });
          
      });  
