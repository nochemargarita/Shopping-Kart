"use strict";
$(document).ready(function() {
    function appendCartProducts(results) {
      let cartProduct = results;
      let productAndQuantity = {};
      
      for (let product in cartProduct) {
          let forClassUse = product.split(" ").join('-');
          let addButton = `<button class=${forClassUse}-add><i class="fas fa-plus"></i></button>`;
          let removeButton = `<button class=${forClassUse}-remove><i class="fas fa-minus"></i></button>`;
          
          $('tbody').append(`<tr class=${forClassUse}>
                              <th class='product-name' scope="row">${product}</th>
                              <td id=${forClassUse}> ${cartProduct[product]} </td>
                              <td>${removeButton} &nbsp; ${addButton}</td>
                             </tr>`);

          $('.'+forClassUse+'-add').unbind('click').click(function(evt){
              evt.preventDefault();
              $('#'+forClassUse).html(Number($('#'+forClassUse).html()) + 1);
              productAndQuantity[$('#products').val()] += 1
          });

          $('.'+forClassUse+'-remove').unbind('click').click(function(evt){
              evt.preventDefault();
              if (Number($('#'+forClassUse).html() > 1)){
              $('#'+forClassUse).html(Number($('#'+forClassUse).html()) - 1)
              productAndQuantity[$('#products').val()] -= 1
              } else {
                  $('.'+forClassUse).remove();
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