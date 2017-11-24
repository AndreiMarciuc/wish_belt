from django.shortcuts import render,redirect
from django.contrib import messages
from ..login_app.models import User
from models import Item
import datetime
from time import gmtime,strftime 

# Create your views here.
def index(request):
    if 'name' not in request.session:
        return redirect('/')
    context = {
        'my_items' : Item.objects.filter(creator = User.objects.get(id = request.session['id'])),
        'other_items' : Item.objects.exclude(all_users = User.objects.get(id = request.session['id'])),
        'cur_user': User.objects.get(id=request.session['id']),
    }

    return render(request, 'wishlist_app/index.html', context)

def render_item_build(request):
    if 'name' not in request.session:
        return redirect('/')
    return render(request, 'wishlist_app/item_build.html')


def add_item(request):
    results = Item.objects.validateItem(request.POST)

    if results['status'] == False:
        for error in results['errors']:
            messages.success(request,error)
            return redirect ('/main/render_item_build')
    else:
        x = User.objects.get(id = request.POST['session_user'])
        y = Item.objects.create(name = request.POST['name'], creator = x)

        y.all_users.add(x)
        y.save()
        return redirect('/main/')

    return redirect('/main/')

def remove_item(request,item_id):
    item=Item.objects.get(id=item_id)
    user=User.objects.get(id=request.session['id'])
    user.all_items.remove(item)
    return redirect('/main/')

def delete_item(request, item_id):
    deleted = Item.objects.get(id = item_id)
    deleted.delete()

    return redirect('/main/')

def display_item(request, item_id):
    if 'name' not in request.session:
        return redirect('/')
    context = {
        'shown_item' : Item.objects.get(id = item_id)
    }
    return render(request, 'wishlist_app/item_display.html', context)

def add_to_wishlist(request, item_id):
    x = User.objects.get(id = request.session['id'])
    y = Item.objects.get(id = item_id)

    x.all_items.add(y)
    x.save()

    return redirect('/main/')