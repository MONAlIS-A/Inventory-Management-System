from django.shortcuts import render, redirect
from . forms import CreateUserForm, UserUpdateForm, ProfileUpdateForm, ProductForm, OrderForm
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from . models import Product, Order
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.

#@login_required(login_url='user-login')
@login_required
def Home(request):
    orders = Order.objects.all()
    orders_count = orders.count()
    products = Product.objects.all()
    products_count = products.count()
    workers = User.objects.all()
    worker_count = workers.count()
    if request.user.is_staff and request.user.is_superuser:
        # Superuser dashboard
        context ={
            'orders': orders,
            'products':products,
            'worker_count': worker_count,
            'products_count': products_count,
            'orders_count': orders_count,
        }
        return render(request, 'dashboard/admin_index.html', context)

   #elif request.user.is_staff:
        # Staff dashboard
       # return render(request, 'dashboard/staff_index.html')

    else:
        # active and staff  user dashboard
        
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                instance =form.save(commit=False)
                instance.staff = request.user
                product =instance.product
                ordered_qty = instance.order_quantity
                if product.quantity >= ordered_qty:
                    product.quantity -= ordered_qty
                    product.save()
                    instance.save()
                    messages.success(request, f'Order Placed for {product.name}. Remaining Stock : {product.quantity}')
                    return redirect('dashboard-home')
                
                else:
                    messages.error(request, f'Not enough stock of {product.name}, Available: {product.quantity}')
            
        else:
            form = OrderForm()

        context ={
            'orders': orders,
            'form' : form,
            'products':products
        }
        return render(request, 'dashboard/staff_index.html', context)
   


@login_required
def Staff(request):
    workers = User.objects.all()
    worker_count = workers.count()
    orders = Order.objects.all()
    orders_count = orders.count()
    products = Product.objects.all()
    products_count = products.count()
    context = {
        'workers': workers,
        'worker_count': worker_count,
        'products_count': products_count,
        'orders_count': orders_count,
    }
    return render(request, 'dashboard/staff.html', context)

@login_required
def staff_detail(request , pk):
    workers = User.objects.get(id=pk)
    context ={
        'workers': workers
    }
    return render(request, 'dashboard/staff_detail.html', context)

@login_required
def Product_View(request):
    items=Product.objects.all() # using ORM
    #items =Product.objects.raw('SELECT * FROM dashboard_product')
    # creating product 
    products_count=items.count()
    orders = Order.objects.all()
    orders_count = orders.count()
    workers = User.objects.all()
    worker_count = workers.count()
    
    if request.method =='POST':
        form = ProductForm(request.POST)
        if form.is_valid:
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
            return redirect('dashboard-product')

    else:
        form = ProductForm()

    context ={
        'items':items,
        'form' : form,
        'worker_count': worker_count,
        'products_count': products_count,
        'orders_count': orders_count,
    }
    return render(request, 'dashboard/product.html', context)

@login_required
def Product_delete(request, pk):
    item =Product.objects.get(id=pk)
    if request.method=='POST':
        item.delete()
        return redirect('dashboard-product')
    return render(request, 'dashboard/product_delete.html')

@login_required
def Product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form =ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save() 
            return redirect('dashboard-product')
    
    else:
        form =ProductForm(instance=item)

    context ={
        'form': form
    }
    return render(request, 'dashboard/product_update.html', context)


@login_required
def Order_By(request):
    orders = Order.objects.all()
    orders_count = orders.count()
    products = Product.objects.all()
    products_count = products.count()
    workers = User.objects.all()
    worker_count = workers.count()

    context ={
        'orders': orders,
        'worker_count': worker_count,
        'products_count': products_count,
        'orders_count': orders_count,
    }
    return render(request, 'dashboard/order.html', context)


@login_required
def Profile(request):
    return render(request, 'user/profile.html')


@login_required
def Profile_update(request):
    if request.method =='POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            return redirect('user-profile')
            print('update')
    else:
        user_form = UserUpdateForm( instance=request.user)
        profile_form = ProfileUpdateForm( instance=request.user.profile)

    context={
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'user/profile_update.html', context)

def Register(request):
    if request.method == 'POST':
        form =CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            #form = CreateUserForm()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account has been created for {username}. Continue to Log in')
            return redirect('user-login')
    else:
        form = CreateUserForm()
    context ={
        'form':form
    }
    return render(request, 'user/register.html', context)

@require_POST
def logout_view(request):
    logout(request)  # This clears the session and sets is_authenticated to False
   # print(request.user.is_authenticated)
    return render(request, 'user/logout.html')  # Or wherever you want to send the user
    

    


