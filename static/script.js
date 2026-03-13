let cart = JSON.parse(localStorage.getItem("cart")) || [];

function addToCart(name,price){

cart.push({
name:name,
price:price
});

localStorage.setItem("cart",JSON.stringify(cart));

updateCartCount();

alert(name + " added to cart");

}

function updateCartCount(){

document.getElementById("cart-count").innerText = cart.length;

}

updateCartCount();