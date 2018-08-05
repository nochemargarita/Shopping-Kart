"use strict";
$(document).ready(function() {
    function appendCartProducts(results) {
      let cartProduct = results;
      let productAndQuantity = {};
      
      for (let product in cartProduct) {
          let addButton = `<button class=${product}-add><i class="fas fa-plus"></i></button>`;
          let removeButton = `<button class=${product}-remove><i class="fas fa-minus"></i></button>`;
          $('tbody').append(`<tr class=${product}>
                              <th class='product-name' scope="row">${product}</th>
                              <td id=${product}> ${cartProduct[product]} </td>
                              <td>${removeButton} &nbsp; ${addButton}</td>
                             </tr>`);

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
      }

    }

    function getCartProdducts() {
        $.get('/kart', appendCartProducts);
    }
      
    getCartProdducts();
});