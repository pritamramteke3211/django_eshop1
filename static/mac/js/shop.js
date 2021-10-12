// ShopHome

// Get Cart Item Number



console.log('It\'s working');

var dataURL = `/Json/`
$.ajax({
    method: 'GET',
    url: dataURL,
    success:function(response){
        console.log('RESPONSE:', response)
        // console.log('RESPONSE:', response.length)
        document.getElementById('cart').innerHTML = response.length;
    }
    
    })

// console.log('working');