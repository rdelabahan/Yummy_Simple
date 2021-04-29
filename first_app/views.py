from django.shortcuts import render, redirect
from django.contrib import messages
from first_app.models import User, Recipe, RecipeImage
import bcrypt
from django.db.models import Count
from .forms import RecipeForm
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.core.paginator import Paginator



def index(request):
    context = {
        'recipes': Recipe.objects.all(),
    }
    return render(request, 'index.html', context)

def authenticate_user(request):
    if request.method == 'GET':
        return redirect('/')
    try:
        user = User.objects.get(username = request.POST['l_username'])
    except:
        messages.error(request, 'Invalid username.')
        return redirect('/')
    if bcrypt.checkpw(request.POST['l_pw'].encode(), user.password.encode()):
        request.session['user_id'] = user.id
        request.session['user_email'] = user.email
        request.session['username'] = user.username
        return redirect('/home')
    else:
        messages.error(request, 'Incorrect password.')
        return redirect('/')

def register(request):
    return render(request,'register.html')

def create_user(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.basic_validator(request.POST)
    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/register')
    else:
        pw_hash = bcrypt.hashpw(request.POST["pw"].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(
            username = request.POST['username'],
            email = request.POST['email'],
            birthday = request.POST['date'],
            password = pw_hash
        )
        request.session['user_id'] = user.id
        request.session['user_email'] = user.email
        request.session['username'] = user.username
        return redirect('/home')

def recipes(request):
    context = {
        'all_recipes': Recipe.objects.order_by('?'),
        'recipes': Recipe.objects.order_by('created_at').reverse()[:5],
        'most_liked_recipes': Recipe.objects.annotate(num_likes=Count('user_likes')).order_by('-num_likes')[:5],
    }
    return render(request,'recipes.html', context)

def logout(request):
    if "user_id" in request.session:
        del request.session["user_id"]
    if "user_email" in request.session:
        del request.session["user_email"]
    if "username" in request.session:
        del request.session['username']
    return redirect('/')

def display_upload(request):
    form = RecipeForm()
    context = {
        'form': form,
    }
    return render(request, 'upload.html', context)


def upload_recipe(request, id):
    errors = RecipeImage.objects.image_validator(request.FILES)
    content_error = Recipe.objects.recipe_validator(request.POST)
    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect('/upload')

    if content_error:
        for k, v in content_error.items():
            messages.error(request, v)
        return redirect('/upload')
    else:
        if request.method == 'POST':
            form = RecipeForm(request.POST)

            if form.is_valid():
                this_user = User.objects.get(id = id)
                this_recipe = Recipe.objects.create(
                    title = request.POST['title'],
                    content = request.POST['content'],
                    uploader = this_user,
                )
                for file in request.FILES.getlist('images'):
                    RecipeImage.objects.create(
                        recipe = this_recipe,
                        image = file,
                    )         
                return redirect('/home')
        

def display_recipe(request, recipe_id):
    context = {
        'recipe': Recipe.objects.get(id = recipe_id),
        'this_user': User.objects.get(id = request.session['user_id']),
    }
    return render(request,'single_recipe.html',context)

def add_likes(request, recipe_id):
    this_user = User.objects.get(id = request.session['user_id'])
    this_recipe = Recipe.objects.get(id = recipe_id)
    this_recipe.user_likes.add(this_user)
    return redirect(f'/recipes/{recipe_id}')

def display_user(request, user_id):
    context = {
        'user': User.objects.get(id = user_id),
    }
    return render(request,'profile.html',context)

def remove_likes(request, recipe_id):
    this_user = User.objects.get(id = request.session['user_id'])
    this_recipe = Recipe.objects.get(id = recipe_id)
    this_recipe.user_likes.remove(this_user)
    return redirect(f'/recipes/{recipe_id}')

def display_edit_profile(request, user_id):
    context = {
        'user': User.objects.get(id = user_id),
    }
    return render(request, 'edit_profile.html', context)

def update_info(request, user_id):
    errors = User.objects.update_info_validator(request.POST, user_id)
    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f'/users/{user_id}/edit')
    else:
        this_user = User.objects.get(id = user_id)
        this_user.username = request.POST['username']
        this_user.email = request.POST['email']
        this_user.birthday = request.POST['date']
        this_user.save()
        messages.success(request, 'Profile info successfully updated!')
        return redirect(f'/users/{user_id}/edit')

def update_pw(request, user_id):
    errors = User.objects.update_password_validator(request.POST, user_id)
    if errors:
        for k, v in errors.items():
            messages.error(request, v)
        return redirect(f'/users/{user_id}/edit')
    else:
        if request.POST['new_pw'] != '':
            this_user = User.objects.get(id = user_id)
            pw_hash = bcrypt.hashpw(request.POST["new_pw"].encode(), bcrypt.gensalt()).decode()
            this_user.password = pw_hash
            this_user.save()
            messages.success(request, 'Password successfully changed!')
        return redirect(f'/users/{user_id}/edit')

def delete_account(request, user_id):
    this_user = User.objects.get(id = user_id)
    this_user.delete()
    return redirect('/')

def delete_recipe(request, recipe_id):
    this_recipe = Recipe.objects.get(id = recipe_id)
    this_recipe.delete()
    return redirect('/home')

def display_edit_recipe(request, recipe_id):
    this_recipe = Recipe.objects.get(id = recipe_id)
    form = RecipeForm(initial={'title': this_recipe.title,'content': this_recipe.content,'images': this_recipe.images})
    
    context = {
        'form': form,
        'recipe': this_recipe,
    }
    return render(request, 'edit_recipe.html', context)

def update_recipe(request, recipe_id):
    content_error = Recipe.objects.recipe_validator(request.POST)
    if content_error:
        for k, v in content_error.items():
            messages.error(request, v)
        return redirect(f'/recipes/{recipe_id}/edit')
    else:
        if request.method == 'POST':
            form = RecipeForm(request.POST)

            if form.is_valid():
                this_recipe = Recipe.objects.get(id = recipe_id)
                this_recipe.title = request.POST['title']
                this_recipe.content = request.POST['content']
                this_recipe.save()
                if len(request.FILES) > 0:
                    images = this_recipe.images.all()
                    for img in images:
                        old_image = RecipeImage.objects.get(id = img.id)
                        old_image.delete()

                    for file in request.FILES.getlist('images'):
                        RecipeImage.objects.create(
                            recipe = this_recipe,
                            image = file,
                        )
                return redirect(f'/recipes/{recipe_id}')

def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        if search == '':
            context = {
                'search': search,
            }
            return render(request, 'results.html', context)
        else:
            context = {
                'recipes': Recipe.objects.filter(title__startswith = search),
            }
            return render(request, 'results.html', context)

def display_all_recipes(request):
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 5) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'all_results.html', {'page_obj': page_obj} )