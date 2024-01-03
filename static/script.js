const resultsBox = document.querySelector(".result-box");
const inputBox = document.getElementById("input-box");

inputBox.addEventListener('keyup', () => {
    var inputValue = inputBox.value;
    var len = inputValue.length;
    var apiURL = `https://db.ygoprodeck.com/api/v7/cardinfo.php?fname=${inputValue}`;
    const empty = [];
    if(len > 3){
        fetch(apiURL)
        .then(res => {
            return res.json();
        })
        .then(data => {
            namesArray = data.data.map(item => item.name);
            // console.log(namesArray);
            display(namesArray);
        })
    } else {
        display(empty);
        resultsBox.innerHTML = '';
    }

})

function display(result){
    const content = result.map((list)=>{
        return "<li onclick=selectInput(this)>" + list + "</li>";

    });
    resultsBox.innerHTML = "<ul>" + content.join('') + "</ul>";
}

function selectInput(list){
    inputBox.value = list.innerHTML;
    resultsBox.innerHTML = '';
}


const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');
let iconCart = document.querySelector('.iconCart');
let cart = document.querySelector('.cart');
let container = document.querySelector('.container');
let close = document.querySelector('.close');

registerLink.addEventListener('click', ()=> {
    wrapper.classList.add('active');
});

loginLink.addEventListener('click', ()=> {
    wrapper.classList.remove('active');
});

btnPopup.addEventListener('click', ()=> {
    wrapper.classList.add('active-popup');
});

iconClose.addEventListener('click', ()=> {
    wrapper.classList.remove('active-popup');
});

iconCart.addEventListener('click', ()=>{
    if(cart.style.right == '-100%'){
        cart.style.right = '0';
        // container.style.transform = 'translateX(-400px)';
    } else {
        cart.style.right = '-100%';
        // container.style.transform = 'translateX(0)';
    }
})

close.addEventListener('click', ()=>{
    cart.style.right = '-100%';
    // container.style.transform = 'translateX(0)';
})


$(document).ready(function() {
    $('.increase, .decrease').click(function(e) {
        e.preventDefault();
        var action = $(this).val();
        var itemId = $(this).closest('form').find('input[name="item_id"]').val();

        $.ajax({
            url: '/updatequantity',
            type: 'POST',
            data: { action: action, item_id: itemId },
            success: function(data) {
                if (data.success) {
                    // Update the quantity on the page
                    var updatedQuantity = data.quantity[0].qty;
                    var totalPrice = (data.ppc[0].ppc * updatedQuantity).toFixed(2);
                    console.log("Updated Quantity:", updatedQuantity);
                    console.log("Item ID:", data.itemID);
                    console.log("Price:", data.ppc[0].ppc);
                    $('#quantity' + data.itemID).text(updatedQuantity);
                    $('#totalQty').text(data.totalQty);
                    $('#totalPrice' + data.itemID).text("$" + totalPrice);

                } else {
                    console.error('Failed to update quantity');
                }
            },
            error: function() {
                console.error('AJAX request failed');
            }
        });
    });
});

