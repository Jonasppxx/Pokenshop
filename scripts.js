document.addEventListener('DOMContentLoaded', () => {
    fetch('products.json')
        .then(response => response.json())
        .then(data => {
            const productsContainer = document.getElementById('products');
            data.products.forEach(product => {
                const productDiv = document.createElement('div');
                productDiv.className = 'product';
                productDiv.innerHTML = `
                    <div class="image-container">
                        <img src="${product.image}" alt="${product.name}" class="default-image">
                        <img src="${product.hoverImage}" alt="${product.name}" class="hover-image">
                    </div>
                    <h2>${product.name}</h2>
                    <p>Price: CHF${product.price}</p>
                    <p>${product.set}</p>
                    <button class="add-to-cart">Add to Cart</button>
                `;
                productsContainer.appendChild(productDiv);

                // Ensure both images are always shown
                const defaultImage = productDiv.querySelector('.default-image');
                const hoverImage = productDiv.querySelector('.hover-image');
                defaultImage.style.display = 'block';
                hoverImage.style.display = 'block';

                const addToCartButton = productDiv.querySelector('.add-to-cart');
                addToCartButton.addEventListener('click', () => {
                    addToCart(product);
                });
            });
        })
        .catch(error => console.error('Error fetching products:', error));

    const cartItems = [];
    const cartItemsContainer = document.getElementById('cart-items');
    const cartTotalElement = document.getElementById('cart-total');
    const cartNotification = document.getElementById('cart-notification');

    function addToCart(product) {
        if (!cartItems.some(item => item.name === product.name)) {
            cartItems.push(product);
            updateCart();
            showNotification();
        }
    }

    function removeFromCart(productName) {
        const index = cartItems.findIndex(item => item.name === productName);
        if (index !== -1) {
            cartItems.splice(index, 1);
            updateCart();
        }
    }

    function updateCart() {
        cartItemsContainer.innerHTML = '';
        let total = 0;
        cartItems.forEach(item => {
            const cartItem = document.createElement('li');
            cartItem.textContent = `${item.name} - CHF${item.price}`;
            const removeButton = document.createElement('button');
            removeButton.textContent = 'Remove';
            removeButton.addEventListener('click', () => {
                removeFromCart(item.name);
            });
            cartItem.appendChild(removeButton);
            cartItemsContainer.appendChild(cartItem);
        });

        total = cartItems.reduce((sum, item) => sum + item.price, 0);
        cartTotalElement.textContent = total.toFixed(2);
    }

    function showNotification() {
        cartNotification.style.display = 'block';
        setTimeout(() => {
            cartNotification.style.display = 'none';
        }, 2000); // Hide after 2 seconds
    }

    document.getElementById('cart-icon').addEventListener('click', function() {
        var cart = document.getElementById('cart');
        cart.classList.toggle('open');
    });
});