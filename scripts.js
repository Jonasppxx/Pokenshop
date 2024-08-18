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
                    <p class="product-price">Price: CHF${product.price}</p>
                    <p>${product.set}</p>
                    <button class="add-to-cart" data-name="${product.name}">Add to Cart</button>
                `;
                productsContainer.appendChild(productDiv);

                const addToCartButton = productDiv.querySelector('.add-to-cart');
                if (isInCart(product.name)) {
                    addToCartButton.textContent = 'In Cart';
                    addToCartButton.disabled = true;
                }

                addToCartButton.addEventListener('click', () => {
                    addToCart(product);
                    addToCartButton.textContent = 'In Cart';
                    addToCartButton.disabled = true;
                });

                // Add click event to images to open modal
                const images = productDiv.querySelectorAll('.image-container img');
                images.forEach(image => {
                    image.addEventListener('click', () => {
                        openModal(image.src);
                    });
                });
            });
        })
        .catch(error => console.error('Error fetching products:', error));

    const cartItems = [];
    const cartItemsContainer = document.getElementById('cart-items');
    const cartTotalElement = document.getElementById('cart-total');
    const cartNotification = document.getElementById('cart-notification');

    function isInCart(productName) {
        return cartItems.some(item => item.name === productName);
    }

    function addToCart(product) {
        if (!isInCart(product.name)) {
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
            const addToCartButton = document.querySelector(`.product button[data-name="${productName}"]`);
            if (addToCartButton) {
                addToCartButton.textContent = 'Add to Cart';
                addToCartButton.disabled = false;
            }
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

    // Modal functionality
    const modal = document.getElementById('image-modal');
    const modalImage = document.getElementById('modal-image');
    const closeModal = document.getElementsByClassName('close')[0];

    function openModal(src) {
        modal.style.display = 'block';
        modalImage.src = src;
    }

    closeModal.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    }
});