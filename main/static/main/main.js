

document.addEventListener("DOMContentLoaded", function() {
    
    // Перевіряємо, чи є на сторінці контейнер каруселі
    if (document.querySelector('.product-images')) {
        const swiper = new Swiper(".product-images", {
            slidesPerView: 1,
            spaceBetween: 10,
            loop: false, // можна поставити true, якщо хочеш нескінченну прокрутку
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
            // Додаємо підтримку миші та тачпаду
            keyboard: {
                enabled: true,
            },
        });
    }

    // // Функції для кнопок "+" та "-" (кількість товару)
    // const plusBtn = document.querySelector('.qty-btn.plus');
    // const minusBtn = document.querySelector('.qty-btn.minus');
    // const qtyInput = document.getElementById('quantity');

    // if (plusBtn && minusBtn && qtyInput) {
    //     plusBtn.addEventListener('click', () => qtyInput.stepUp());
    //     minusBtn.addEventListener('click', () => {
    //         if (qtyInput.value > 1) qtyInput.stepDown();
    //     });
    // }
});

// --- Swiper ініціалізація для add_product.html, раніше був у шаблоні ---

document.addEventListener("DOMContentLoaded", function() {
    
    // 1. Ініціалізація Swiper (Тільки ця частина керує каруселлю)
    if (typeof Swiper !== "undefined") {
        const swiper = new Swiper(".mySwiper", {
            slidesPerView: 1,
            spaceBetween: 10,
            loop: false, // можна поставити true, якщо хочеш нескінченну прокрутку
            navigation: {
                nextEl: ".swiper-button-next",
                prevEl: ".swiper-button-prev",
            },
            pagination: {
                el: ".swiper-pagination",
                clickable: true,
            },
            // Додаємо підтримку миші та тачпаду
            keyboard: {
                enabled: true,
            },
        });
    }

    // 2. Функція для прев'ю (FileReader)
    // Вона дозволяє бачити фото ВІДРАЗУ після вибору файлу
    function setupPreview(inputId, imgId, spanId) {
        const input = document.getElementById(inputId);
        const img = document.getElementById(imgId);
        const span = document.getElementById(spanId);

        if (input && img) {
            input.addEventListener('change', function() {
                const file = this.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        img.src = e.target.result;
                        img.style.display = 'block';
                        if (span) span.style.display = 'none';
                    };
                    reader.readAsDataURL(file);
                }
            });
        }
    }

    // Прив'язуємо прев'ю до полів Django форми
    setupPreview('id_image', 'preview_image', 'span_image');
    setupPreview('id_image_1', 'preview_image_1', 'span_image_1');
    setupPreview('id_image_2', 'preview_image_2', 'span_image_2');
});

// --- Інші функції (фільтри, замовлення тощо) залишай нижче ---





document.addEventListener("DOMContentLoaded", function () {
    const filterForDad = document.getElementById('filter-for-dad');
    const filterForMom = document.getElementById('filter-for-mom');
    const productItems = document.querySelectorAll('.product-item');
    
    // Перевіряємо тільки ті фільтри, які залишилися в HTML
    if (!filterForDad || !filterForMom) {
        return;
    }
    
    function filterProducts() {
        const showForDad = filterForDad.checked;
        const showForMom = filterForMom.checked;

        productItems.forEach(function(item) {
            const forDad = item.getAttribute('data-for-dad') === 'true';
            const forMom = item.getAttribute('data-for-mom') === 'true';
            const isAvailable = item.getAttribute('data-is-available') === 'true';

            let shouldShow = true;

            // ГОЛОВНА ЛОГІКА: Якщо товару немає в наявності — завжди ховаємо
            if (!isAvailable) {
                shouldShow = false;
            } else {
                // Якщо в наявності, перевіряємо інші фільтри
                if (showForDad && !forDad) {
                    shouldShow = false;
                }
                if (showForMom && !forMom) {
                    shouldShow = false;
                }
            }
            
            // Показуємо або приховуємо товар
            item.style.display = shouldShow ? '' : 'none';
        });
    }

    filterForDad.addEventListener('change', filterProducts);
    filterForMom.addEventListener('change', filterProducts);

    // Запускаємо фільтрацію одразу при завантаженні, 
    // щоб товари не в наявності зникли миттєво
    filterProducts();
});


document.addEventListener('DOMContentLoaded', function () {
    const deliverySelect = document.getElementById('delivery_method');
    const novaPoshtaFields = document.getElementById('nova-poshta-fields');
    const ukrPoshtaFields = document.getElementById('uke-poshta-fields');
    
    if (!deliverySelect || !novaPoshtaFields || !ukrPoshtaFields) return;

    function updateFields() {
        if (deliverySelect.value === 'novaposhta') {
            novaPoshtaFields.style.display = 'block';
            ukrPoshtaFields.style.display = 'none';
        } else if (deliverySelect.value === 'ukrposhta') {
            novaPoshtaFields.style.display = 'none';
            ukrPoshtaFields.style.display = 'block';
        } else {
            novaPoshtaFields.style.display = 'none';
            ukrPoshtaFields.style.display = 'none';
        }
    }

    deliverySelect.addEventListener('change', updateFields);

    // Одразу при завантаженні правильно показує поля
    updateFields();
});

document.addEventListener('DOMContentLoaded', function () {
    const orderForm = document.querySelector('.order-form');
    if (!orderForm) return;

    orderForm.addEventListener('submit', function () {
        const selected = document.querySelectorAll('.product-checkbox:checked');

        // 🔥 очищаємо старі hidden inputs
        orderForm.querySelectorAll('input[name="selected_products"]').forEach(e => e.remove());

        selected.forEach(cb => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'selected_products';
            input.value = cb.value;
            orderForm.appendChild(input);
        });


    });

});

function toggleDetails(button) {
    const details = button.nextElementSibling;

    if (details.style.display === "none" || details.style.display === "") {
        details.style.display = "block";
        button.innerText = "Сховати деталі";
    } else {
        details.style.display = "none";
        button.innerText = "Показати деталі";
    }
}

function closeOrder(button) {
    const orderId = button.dataset.orderId;

    if (!confirm('Закрити це замовлення?')) return;

    fetch('/close-order/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `order_id=${orderId}`
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            // міняємо UI
            button.innerText = 'Замовлення закрите';
            button.disabled = true;
            button.closest('.admin_panel_info').style.opacity = '0.6';
        }
    })
    .catch(err => console.error(err));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
    const inputOpen = document.getElementById('input_open');
    const inputClose = document.getElementById('input_close');
    const orders = document.querySelectorAll('.admin_panel_info');

    function filterOrders() {
        const showOpen = inputOpen.checked;
        const showClose = inputClose.checked;

        orders.forEach(order => {
            const status = order.dataset.status; // open | close

            if (
                (status === 'open' && showOpen) ||
                (status === 'close' && showClose)
            ) {
                order.style.display = '';
            } else {
                order.style.display = 'none';
            }
        });
    }

    inputOpen.addEventListener('change', filterOrders);
    inputClose.addEventListener('change', filterOrders);

    filterOrders(); // запуск одразу
});

document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById('commentForm');
    const container = document.getElementById('commentsContainer');
    if (!form || !container) return;

    const productId = form.dataset.productId;
    const addUrl = form.dataset.url;
    const csrfToken = form.dataset.csrf;

    // 🔄 Завантажити всі коментарі
    async function loadComments() {
        const res = await fetch(`/comments/${productId}/`);
        const data = await res.json();
    
        container.innerHTML = '';
    
        data.comments.forEach(c => {
            const div = document.createElement('div');
            div.classList.add('comment_text');
    
            const text = document.createElement('span');
            text.textContent = `${c.user}: ${c.text}`;
            div.appendChild(text);
    
            if (data.is_admin) {
                const del = document.createElement('a');
                del.href = `/comment_remove/${c.id}/`;
                del.textContent = ' видалити';
                del.classList.add('comment_delete');
                div.appendChild(del);
            }
    
            container.appendChild(div); // ← ЗАВЖДИ додаємо
        });
    }    

    // 📤 Відправка коментаря
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const text = document.getElementById('commentText').value.trim();
        if (!text) return;

        await fetch(addUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                text: text,
                product_id: productId
            })
        });

        document.getElementById('commentText').value = '';
        loadComments(); // оновлюємо одразу
    });

    // ▶️ старт
    loadComments();

    // 🔁 POLLING кожні 5 секунд
    setInterval(loadComments, 5000);
});

document.addEventListener("DOMContentLoaded", function () {
    const addProductBtn = document.querySelector('.add_product_admin_panel_button'); 
    const panel = document.querySelector('.add_product_admin_panel');

    if (addProductBtn && panel) {
        // Initially hide the panel
        panel.style.display = 'none';

        // Add scrollability to the modal content
        const formBox = panel.querySelector('.form-box');
        if (formBox) {
            formBox.style.maxHeight = '90vh';
            formBox.style.overflowY = 'auto';
        }

        // Show panel on button click
        addProductBtn.addEventListener('click', function () {
            panel.style.display = 'flex';
        });

        // Allow closing modal when clicking on the overlay, but NOT when clicking inside .form-box
        panel.addEventListener('click', function (e) {
            if (e.target === panel) {
                panel.style.display = 'none';
            }
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const see_text_button = document.querySelector('.comment_write_button'); 
    const see_text_input = document.querySelector('.comment_write');

    if (see_text_button && see_text_input) {
        // Hide the comment input by default
        see_text_input.style.display = 'none';

        see_text_button.addEventListener('click', function () {
            // Toggle visibility
            if (see_text_input.style.display === 'none') {
                see_text_input.style.display = 'block';
            } else {
                see_text_input.style.display = 'none';
            }
        });
    }
    
});
document.addEventListener('DOMContentLoaded', () => {
    const overlay = document.querySelector('.comment_write');
    const openBtn = document.querySelector('.comment_write_button');

    if (!overlay || !openBtn) return;

    overlay.style.display = 'none';

    openBtn.addEventListener('click', () => {
        overlay.style.display = 'block';
    });

    overlay.addEventListener('click', e => {
        if (e.target === overlay) {
            overlay.style.display = 'none';
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {

    document.querySelectorAll('.quantity-selector').forEach(block => {
        const input = block.querySelector('.number_input');
        const plus = block.querySelector('.plus');
        const minus = block.querySelector('.minus');

        if (!input || !plus || !minus) return;

        plus.addEventListener('click', () => input.stepUp());
        minus.addEventListener('click', () => input.stepDown());
    });

    document.querySelectorAll('.item-quantity').forEach(block => {
        const input = block.querySelector('.quantity-input');
        const plus = block.querySelector('.plus');
        const minus = block.querySelector('.minus');

        if (!input || !plus || !minus) return;

        plus.addEventListener('click', () => {
            input.stepUp();
        });

        minus.addEventListener('click', () => {
            if (parseInt(input.value, 10) > 1) {
                input.stepDown();
            }
        });
    });
});


document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('.to_buy_button');
    const section = document.querySelector('.order-form-section');

    if (!button || !section) return;

    section.style.display = 'none';

    // відкрити
    button.addEventListener('click', e => {
        e.stopPropagation();
        section.style.display = 'block';
    });

    // не закривати при кліку всередині
    section.addEventListener('click', e => {
        e.stopPropagation();
    });

    // клік по фону — закрити
    document.addEventListener('click', () => {
        section.style.display = 'none';
    });
});


document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.image-upload input[type="file"]').forEach(input => {
        input.addEventListener('change', e => {
            const file = e.target.files[0];
            if (!file) return;

            const wrap = e.target.closest('.image-upload');
            const img = wrap.querySelector('img');
            const span = wrap.querySelector('span');

            img.src = URL.createObjectURL(file);
            img.style.display = 'block';
            if (span) span.style.display = 'none';
        });
    });
});
