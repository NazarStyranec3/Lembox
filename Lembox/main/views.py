from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from random import sample
from .models import Category, Product, To_Buy, To_Buy_Product,Save_user_data, Comment
from decimal import Decimal
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import Save_user_data_form, Product_form
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth.models import User
import json
# Create your views here.
def home(request):
    categories = Category.objects.filter(parent=None)
    return render(request, 'main/home.html', {
        'categories': categories
    })
    
from django.http import JsonResponse
from django.contrib import messages

def admin_panel(request):
    to_buy_products = To_Buy_Product.objects.all()
    to_buy = To_Buy.objects.all()
    error = ''

    return render(request, 'main/admin_panel.html', {
        'to_buy_products': to_buy_products,
        'to_buy': to_buy,

    })
def admin_product(request):
    error = ''
    products = Product.objects.all()
    form = Product_form()
    if request.method == 'POST':
        form = Product_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = Product_form()
        else:
            error = 'помилка'

    return render(request, 'main/admin_product.html', {
        'form': form,
        'error': error,
        'products':products,
    })

def product_detail_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    print('VIEW CALLED', request.method)
    if request.method == 'POST':
        form = Product_form(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail_edit', product_id=product.id)
    else:
        form = Product_form(instance=product)

    return render(request, 'main/product_detail_edit.html', {
        'form': form,
        'product': product,
    })

def add_product(request):
    form = Product_form()
    if request.method == 'POST':
        form = Product_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = Product_form()

    return render(request, 'main/add_product.html', {
        'form': form,
    })

def product_detail_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    product.delete()
    return redirect('home')

def comment_remove(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    comment.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))

def close_order(request):
    order_id = request.POST.get('order_id')

    order = get_object_or_404(To_Buy, id=order_id)

    # Закриваємо замовлення
    order.status = False
    order.save()

    # (опціонально) закриваємо всі товари в замовленні
    To_Buy_Product.objects.filter(to_buy=order).update(status=False)

    return JsonResponse({
        'success': True,
        'order_id': order.id
    })


@login_required
def add_comment(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product = get_object_or_404(Product, id=data.get('product_id'))

        comment = Comment.objects.create(
            user=request.user,
            product=product,
            text=data.get('text', '')
        )
    
        return JsonResponse({
            'success': True,
            'user': comment.user.username,
            'text': comment.text
        })

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def get_comments(request, product_id):
    comments = Comment.objects.filter(
        product_id=product_id
    ).order_by('created_at')

    data = []
    for c in comments:
        data.append({
            'id': c.id,                     # ← ОБОВʼЯЗКОВО
            'user': c.user.username,
            'text': c.text,
        })

    return JsonResponse({'comments': data})

def basket(request):
    """
    Обробка кошика покупок:
    - Відображення товарів у кошику
    - Додавання товарів (POST з action='add')
    - Оновлення кількості товарів (POST з action='update')
    - Видалення товарів (POST з action='remove')
    - Очищення кошика (POST з action='clear')
    """
    
    # Ініціалізація кошика в сесії, якщо його ще немає
    if 'basket' not in request.session:
        request.session['basket'] = {}

    basket = request.session['basket']
    
    # Обробка POST-запитів для маніпуляцій з кошиком
    if request.method == 'POST':
        action = request.POST.get('action', 'add')
        product_id = request.POST.get('product_id')
        
        if action == 'add':
            # Доhttps://byrutgame.org/давання товару до кошика
            if product_id:
                quantity = int(request.POST.get('quantity', 1))
                if product_id in basket:
                    basket[product_id] += quantity
                else:
                    basket[product_id] = quantity
                request.session['basket'] = basket
                request.session.modified = True
                messages.success(request, 'Товар додано до кошика')
        
        elif action == 'update':
            # Оновлення кількості товару
            if product_id:
                quantity = int(request.POST.get('quantity', 1))
                if quantity > 0:
                    basket[product_id] = quantity
                    request.session['basket'] = basket
                    request.session.modified = True
                    messages.success(request, 'Кількість товару оновлено')
                else:
                    # Якщо кількість 0 або менше, вид   аляємо товар
                    basket.pop(product_id, None)
                    request.session['basket'] = basket
                    request.session.modified = True
                    messages.info(request, 'Товар видалено з кошика')
        
        elif action == 'remove':
            # Видалення товару з кошика
            if product_id and product_id in basket:
                basket.pop(product_id, None)
                request.session['basket'] = basket
                request.session.modified = True
                messages.success(request, 'Товар видалено з кошика')
        

        
        elif action == 'buy':
            # Створення замовлення
            # Отримуємо ім'я з форми або з окремого поля
            # Одержуємо ім'я користувача (запасний варіант)
            customer_name = request.POST.get('name', '').strip() or request.POST.get('customer_name', '').strip()

            # Отримуємо або створюємо профіль користувача для збереження форми доставки
            user_data, created = Save_user_data.objects.get_or_create(user=request.user)
            form = Save_user_data_form(request.POST or None, instance=user_data)
            if form.is_valid():
                # Оновлюємо дані користувача в профілі
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                # Далі створюємо сам "To_Buy" (замовлення)
                from decimal import Decimal
                from .models import To_Buy, To_Buy_Product, Product

                # Отримуємо список відмічених товарів з чекбоксів
                selected_products = request.POST.getlist('selected_products')
                print('selected_products:',selected_products)
                if not selected_products:
                    messages.error(request, "Будь ласка, оберіть хоча б один товар для замовлення.")
                    return redirect('basket')

                else:
                    # Збираємо тільки відмічені товари з кошика
                    basket_items = []
                    total = Decimal('0.00')

                    if selected_products:

                        # Default all fields to None
                        address_nova_poshta = None
                        city_nova_poshta = None
                        region_nova_poshta = None
                        branch_nova_poshta = None
                        address_ukr_poshta = None
                        city_ukr_poshta = None
                        region_ukr_poshta = None
                        inbex_ukr_poshta = None
                        delivery_method = request.POST.get('delivery_method', '').strip()
                        if delivery_method == 'novaposhta':
                            address_nova_poshta = form.cleaned_data.get('address_nova_poshta')
                            city_nova_poshta = form.cleaned_data.get('city_nova_poshta')
                            region_nova_poshta = form.cleaned_data.get('region_nova_poshta')
                            branch_nova_poshta = form.cleaned_data.get('branch_nova_poshta')
                        elif delivery_method == 'ukrposhta':
                            address_ukr_poshta = form.cleaned_data.get('address_ukr_poshta')
                            city_ukr_poshta = form.cleaned_data.get('city_ukr_poshta')
                            region_ukr_poshta = form.cleaned_data.get('region_ukr_poshta')
                            inbex_ukr_poshta = form.cleaned_data.get('inbex_ukr_poshta')
                            # Самовивіз — очищаємо обидві групи
                        to_buy = To_Buy.objects.create(
                                name=customer_name if customer_name else instance.name,
                                total_price=total,

                                name_user = form.cleaned_data.get('name'),
                                phone = form.cleaned_data.get('phone'),
                                email = form.cleaned_data.get('email'),
                                address_nova_poshta = address_nova_poshta,
                                city_nova_poshta = city_nova_poshta,
                                region_nova_poshta = region_nova_poshta,
                                branch_nova_poshta = branch_nova_poshta,
                                # Ukrposhta
                                address_ukr_poshta = address_ukr_poshta,
                                city_ukr_poshta = city_ukr_poshta,
                                region_ukr_poshta = region_ukr_poshta,
                                inbex_ukr_poshta = inbex_ukr_poshta,
                            )
                        

                    for product_id in selected_products:
                        product_id_str = str(product_id)

                        if product_id_str not in basket:
                            continue

                        quantity = basket[product_id_str]

                        try:
                            product = Product.objects.get(id=int(product_id))
                        except Product.DoesNotExist:
                            continue

                        price = Decimal(str(product.price))
                        subtotal = price * quantity
                        total += subtotal

                        basket_items.append({
                            'product': product,
                            'quantity': quantity,
                            'price': price
                        })
                        basket.pop(str(product_id), None)

                    if not basket_items:
                        messages.error(request, "Кошик порожній або щось пішло не так з товарами.")
                        return redirect('basket')
                    else:

                        delivery_method = request.POST.get('delivery_method', '').strip()
                        for item in basket_items:
                            # Default all fields to None
                            address_nova_poshta = None
                            city_nova_poshta = None
                            region_nova_poshta = None
                            branch_nova_poshta = None
                            address_ukr_poshta = None
                            city_ukr_poshta = None
                            region_ukr_poshta = None
                            inbex_ukr_poshta = None

                            if delivery_method == 'novaposhta':
                                address_nova_poshta = form.cleaned_data.get('address_nova_poshta')
                                city_nova_poshta = form.cleaned_data.get('city_nova_poshta')
                                region_nova_poshta = form.cleaned_data.get('region_nova_poshta')
                                branch_nova_poshta = form.cleaned_data.get('branch_nova_poshta')
                            elif delivery_method == 'ukrposhta':
                                address_ukr_poshta = form.cleaned_data.get('address_ukr_poshta')
                                city_ukr_poshta = form.cleaned_data.get('city_ukr_poshta')
                                region_ukr_poshta = form.cleaned_data.get('region_ukr_poshta')
                                inbex_ukr_poshta = form.cleaned_data.get('inbex_ukr_poshta')
                            # Самовивіз — очищаємо обидві групи

                            To_Buy_Product.objects.create(
                                user=request.user,
                                data_user=instance,
                                to_buy=to_buy,
                                name=item['product'].name,
                                price=str(item['price']),
                                number=item['quantity'],
                                status=True,
                                name_user = form.cleaned_data.get('name'),
                                phone = form.cleaned_data.get('phone'),
                                email = form.cleaned_data.get('email'),
                                # Nova Poshta
                                address_nova_poshta = address_nova_poshta,
                                city_nova_poshta = city_nova_poshta,
                                region_nova_poshta = region_nova_poshta,
                                branch_nova_poshta = branch_nova_poshta,
                                # Ukrposhta
                                address_ukr_poshta = address_ukr_poshta,
                                city_ukr_poshta = city_ukr_poshta,
                                region_ukr_poshta = region_ukr_poshta,
                                inbex_ukr_poshta = inbex_ukr_poshta,
                            )
                        # Очищаємо кошик після покупки
                        # request.session['basket'] = {}
                        # request.session.modified = True
                        request.session['basket'] = basket
                        request.session.modified = True
                        messages.success(request, "Замовлення успішно створено!")
                        return redirect('office')
            else:
                # Не валідна форма - повертаємо форму для повторного введення
                messages.error(request, "Будь ласка, перевірте свої дані для доставки.")
    

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            basket_items, total = _get_basket_items(basket)
            return JsonResponse({
                "form":form,
                'success': True,
                'basket_items': basket_items,
                'total': total,
                'basket_count': sum(basket.values())
            })
    
    # Отримання товарів кошика та загальної суми
    basket_items, total = _get_basket_items(basket)
    
    # Підрахунок загальної кількості товарів у кошику
    basket_count = sum(basket.values())
    
    # Отримуємо дані користувача, якщо він авторизований
    form = None
    if request.user.is_authenticated:
        user_data, created = Save_user_data.objects.get_or_create(user=request.user)
        form = Save_user_data_form(instance=user_data)
    
    return render(request, 'main/basket.html', {
        'basket_items': basket_items,
        'total': total,
        'basket_count': basket_count,
        'is_empty': len(basket_items) == 0,
        'form': form,
    })


def _get_basket_items(basket):
    """
    Допоміжна функція для отримання інформації про товари в кошику.
    Повертає список товарів та загальну суму.
    """
    basket_items = []
    total = 0
    
    # Збір інформації про кожен товар у кошику
    for product_id, quantity in basket.items():
        try:
            product = Product.objects.get(id=product_id)
            
            # Обчислення суми для цього товару
            item_total = 0
            try:
                item_total = float(product.price) * int(quantity)
                total += item_total
            except (ValueError, TypeError):
                # Якщо ціна не є числом, пропускаємо підрахунок
                pass
            
            item = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image': product.image.url if product.image else '',
                'quantity': quantity,
                'total': item_total,
            }
            basket_items.append(item)
            
        except Product.DoesNotExist:
            # Якщо товар не знайдено, пропускаємо його
            continue
    
    return basket_items, total

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.children.all()

    product_list = Product.objects.filter(category=category)

    paginator = Paginator(product_list, 10)  # 🔥 10 товарів на сторінку
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    return render(request, 'main/category_detail.html', {
        'category': category,
        'subcategories': subcategories,
        'products': products,
    })

def hom(request):
    products = Product.objects.all()
    return render(request, 'main/hom.html', {
        'products': products
    })
    
def product_detail(request, category_id, product_id):
    category = get_object_or_404(Category, id=category_id)
    product = get_object_or_404(Product, id=product_id, category=category)
    comments = Comment.objects.filter(product_id=product.id)
    return render(request, 'main/product_detail.html', {
        'product': product,
        'category': category,
        'comments': comments
    })



########################################################################################################################

########################################################################################################################
@login_required
def order_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect('order')
    else:
        form = OrderForm()

    return render(request, 'main/order.html', {'form': form})




def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Невірні дані для входу")
    else:
        form = CustomLoginForm()
    return render(request, 'main/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Реєстрація успішна. Ви увійшли як новий користувач.")
            return redirect('home')
        else:
            messages.error(request, "Будь ласка, перевірте правильність заповнення форми.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def office_view(request):
    # Отримуємо або створюємо об'єкт Save_user_data для поточного користувача
    user_data, created = Save_user_data.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = Save_user_data_form(request.POST, instance=user_data)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'Дані успішно збережено!')
            return redirect('office')
    else:
        form = Save_user_data_form(instance=user_data)  
    
    # беремо всі замовлення, де є хоча б один товар цього користувача
    to_buy_list = To_Buy.objects.filter(
        to_buy_products__user=request.user
    ).distinct().order_by('-created_at')
    return render(request, 'main/office.html', {
        'form': form,
        'to_buy_list': to_buy_list,
        })
