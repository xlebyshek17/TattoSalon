# логика, выборка из бд для вывода ее в шаблон html
from __future__ import unicode_literals
from decimal import Decimal
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import login, authenticate
from salon.forms import OrdForm, RegistrationForm, LoginForm
from salon.models import Category, Order, CartItem, Cart, Ord


# Create your views here.

def base_view(request):
	# cart = Cart.objects.first()
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)

	categories = Category.objects.all()
	orders = Order.objects.all()
	context = {
		'categories' : categories,
		'orders': orders,
		'cart': cart,
	}
	return render(request, 'base.html', context)


def order_view(request, order_slug):
	# cart = Cart.objects.first()
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)

	order = Order.objects.get(slug=order_slug)
	categories = Category.objects.all()
	context = {
		'order': order,
		'categories' : categories,
		'cart': cart,
	}
	return render(request, 'order.html', context)


def category_view(request, category_slug):
	category = Category.objects.get(slug=category_slug)
	categories = Category.objects.all()
	orders_of_category = Order.objects.filter(category=category)
	context = {
		'category': category,
		'categories' : categories,
		'orders_of_category': orders_of_category,
	}
	return render(request, 'category.html', context)


def cart_view(request):
	#cart = Cart.objects.first()
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	categories = Category.objects.all()
	context = {
		'cart': cart,
		'categories': categories
	}
	return render(request, 'cart.html', context)


def add_to_cart_view(request):#, order_slug):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)

	order_slug = request.GET.get('order_slug')
	order = Order.objects.get(slug=order_slug)
	cart.add_to_cart(order.slug)
	new_cart_total = 0.00
	for item in cart.items.all():
		new_cart_total += float(item.item_total)
	cart.cart_total = new_cart_total
	cart.save()
	return JsonResponse(
		{'cart_total': cart.items.count(),
		'cart_total_price': cart.cart_total})


def remove_from_cart_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)

	order_slug = request.GET.get('order_slug')
	order = Order.objects.get(slug=order_slug)
	cart.remove_from_cart(order.slug)
	new_cart_total = 0.00
	for item in cart.items.all():
		new_cart_total += float(item.item_total)
	cart.cart_total = new_cart_total
	cart.save()
	return JsonResponse(
		{'cart_total': cart.items.count(),
		'cart_total_price': cart.cart_total})

def change_item_qty(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	qty = request.GET.get('qty')
	item_id = request.GET.get('item_id')
	cart_item = CartItem.objects.get(id=int(item_id))
	cart.change_qty(qty, item_id)
	return JsonResponse(
		{'cart_total': cart.items.count(), 
		'item_total': cart_item.item_total,
		'cart_total_price': cart.cart_total})

def checkout_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	categories = Category.objects.all()
	context = {
		'cart': cart,
		'categories': categories
	}
	return render(request, 'checkout.html', context)

def order_create_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	categories = Category.objects.all()
	form = OrdForm(request.POST or None)
	context = {
		'form': form,
		'cart': cart,
		'categories': categories
	}
	return render(request, 'ord.html', context)

def make_order_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	form = OrdForm(request.POST or None)
	categories = Category.objects.all()
	if form.is_valid():
		name = form.cleaned_data['name']
		last_name = form.cleaned_data['last_name']
		phone = form.cleaned_data['phone']
		buying_type = form.cleaned_data['buying_type']
		#address = form.cleaned_data['address']
		comments = form.cleaned_data['comments']
		new_order = Ord.objects.create(
				user=request.user,
				items=cart,
				total=cart.cart_total,
				first_name=name,
				last_name=last_name,
				phone=phone,
				#address=address,
				buying_type=buying_type,
				comments=comments
			)
		request.session['total'] = cart.items.count()
		del request.session['cart_id']
		del request.session['total']
		return render(request, 'thank_you.html', {'categories': categories})
	return render(request, 'ord.html', {'categories': categories})

def account_view(request):
	orde = Ord.objects.filter(user=request.user).order_by('-id')
	categories = Category.objects.all()
	context = {
		'orde': orde,
		'categories': categories
	}
	return render(request, 'account.html', context)

def registration_view(request):
	form = RegistrationForm(request.POST or None)
	categories = Category.objects.all()
	if form.is_valid():
		new_user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		email = form.cleaned_data['email']
		first_name = form.cleaned_data['first_name']
		last_name = form.cleaned_data['last_name']

		new_user.username = username
		new_user.set_password(password)
		new_user.first_name = first_name
		new_user.last_name = last_name
		new_user.email = email
		new_user.save()	

		login_user = authenticate(username=username, password=password)
		if login_user:
			login(request, login_user)
			return HttpResponseRedirect(reverse('base'))
	context = {
		'form': form,
		'categories': categories
	}
	return render(request, 'registration.html', context)

def login_view(request):
	form = LoginForm(request.POST or None)
	categories = Category.objects.all()
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		login_user = authenticate(username=username, password=password)
		if login_user:
			login(request, login_user)
			return HttpResponseRedirect(reverse('base'))
	context = {
		'form': form,
		'categories': categories
	}
	return render(request, 'login.html', context)
