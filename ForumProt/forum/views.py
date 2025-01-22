from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .forms import RegistrationForm, LoginForm, PublicationForm, CommentForm, RegistrationStaffForm
from .models import UserPublication, Product, Comment, User_upvotes


def home_page(request):
    publications = UserPublication.objects.select_related().all()
    publications_data = []
    for publ in publications:
        publications_data.append({'id': publ.id, 'title': publ.title, 'category': publ.category,
                                  'product': publ.product.name, 'desc': publ.desc,
                                  'upvotes': len(User_upvotes.objects.filter(publication=publ)),
                                  'user': publ.user.first_name + ' ' + publ.user.last_name})
    publications_data = sorted(publications_data, key=lambda d: d['upvotes'], reverse=True)
    return render(request, 'mainPage.html', {'publications': publications_data})


def registration_regular_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = User.objects.create_user(username=name + "_" + surname,
                                            password=password, email=email,
                                            first_name=name, last_name=surname)
            user.save()
            return redirect('/login')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def login_regular_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            password = request.POST.get('password')
            user = authenticate(username=name + "_" + surname,
                                password=password
                                )
            if user is None:
                print('not found')
                return redirect('/login')
            login(request, user)
            return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect('/')


@login_required(login_url='/login')
def create_publication(request):
    if request.method == 'POST':
        form = PublicationForm(request.POST)
        if form.is_valid():
            title = request.POST.get('title')
            category = request.POST.get('category')
            desc = request.POST.get('desc')
            product = request.POST.get('product')
            product_related = Product.objects.get(name=product)
            UserPublication.objects.create(title=title, category=category,
                                           product=product_related, desc=desc,
                                           user=request.user, upvotes=0)
            return redirect('/')
    else:
        form = PublicationForm()
    return render(request, 'create_publication.html', {'form': form})


def get_user_role(groups, user):
    for group in groups:
        if user in group.user_set.all():
            return group.name
    return


def publication_view(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            desc = request.POST.get('desc')
            publication_id = request.POST.get('publication_id')
            publication_related = UserPublication.objects.get(id=publication_id)
            Comment.objects.create(desc=desc, user=request.user, publication=publication_related)
            return redirect(f'/publication?id={publication_id}')
    elif request.method == 'GET':
        form = CommentForm()
        publication = UserPublication.objects.select_related().get(id=request.GET.get('id'))
        comments = Comment.objects.select_related().filter(publication=publication)
        upvotes = User_upvotes.objects.select_related().filter(publication=publication)
        can_upvote = ""
        for upvote in upvotes:
            if upvote.user == request.user:
                can_upvote = 'disabled'
        groups = Group.objects.all()
        comments_data = []
        for comment in comments:
            comments_data.append({'user': comment.user.first_name + ' ' + comment.user.last_name,
                                  'desc': comment.desc, 'role': get_user_role(groups, comment.user)})
        return render(request, 'publication_view.html', {'publ': publication, 'comments': comments_data, 'form': form,
                                                         'upvote_disabled': can_upvote, 'num_of_upvotes': len(upvotes)})


@login_required(login_url='/login')
def edit_publication(request):
    if request.method == 'POST':
        publ_id = request.POST.get('publication_id')
        product = request.POST.get('product')
        product_related = Product.objects.get(name=product)
        UserPublication.objects.filter(id=publ_id).update(
            title=request.POST.get('title'),
            product=product_related,
            desc=request.POST.get('desc'),
            category=request.POST.get('category')
        )
        return redirect(f'/publication?id={publ_id}')
    elif request.method == 'GET':
        form = PublicationForm()
        publ_id = request.GET.get('id')
        publication = UserPublication.objects.select_related().get(id=publ_id)
        if request.user.username == publication.user.username or request.user.groups.filter(name='Модератор').exists():
            form.initial['title'] = publication.title
            form.initial['product'] = publication.product.name
            form.initial['category'] = publication.category
            form.initial['desc'] = publication.desc
            return render(request, 'edit_publication.html', {'form': form, 'publ_id': publ_id})
        return render(request, 'no_edit_no_delete.html', {'data': 'У вас нет прав на редактирование публикации!'})


@login_required(login_url='/login')
def delete_publication(request):
    if request.method == 'POST':
        publ_id = request.POST.get('publication_id')
        UserPublication.objects.get(id=publ_id).delete()
        return redirect('/')
    elif request.method == 'GET':
        publ_id = request.GET.get('id')
        publication = UserPublication.objects.select_related().get(id=publ_id)
        if request.user.username == publication.user.username or request.user.groups.filter(name='Модератор').exists():
            return render(request, 'delete_publication.html', {'publ': publication})
        return render(request, 'no_edit_no_delete.html', {'data': 'У вас нет прав на удаление публикации!'})


# def is_moderator(user):
#     return user.groups.filter(name='Модератор').exists()
#
#
# def is_support(user):
#     return user.groups.filter(name='Поддержка').exists()
#
#
# def is_analyst(user):
#     return user.groups.filter(name='Аналитик').exists()


@staff_member_required
def registration_staff(request):
    if request.method == 'POST':
        form = RegistrationStaffForm(request.POST)
        if form.is_valid():
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            role = request.POST.get('role')
            user = User.objects.create_user(username=name + "_" + surname,
                                            password=password, email=email,
                                            first_name=name, last_name=surname,
                                            )  # is_staff=True if role == 'Модератор' else False
            if role == 'Модератор':
                moderator_group, created = Group.objects.get_or_create(name='Модератор')
                user.groups.add(moderator_group)
            elif role == 'Поддержка':
                support_group, created = Group.objects.get_or_create(name='Поддержка')
                user.groups.add(support_group)
            elif role == 'Аналитик':
                analyst_group, created = Group.objects.get_or_create(name='Аналитик')
                user.groups.add(analyst_group)
            user.save()
            return redirect('/login')
    else:
        form = RegistrationStaffForm()
    return render(request, 'registration.html', {'form': form})


def publ_upvote(request):
    if request.method == 'POST':
        publ_id = request.POST.get('id')
        user_id = request.POST.get('user_id')
        User_upvotes.objects.create(publication=UserPublication.objects.get(id=publ_id),
                                    user=User.objects.get(id=user_id))
        # publ_id = request.POST.get('id')
        # publication = UserPublication.objects.get(id=publ_id)
        # publication.upvotes += 1
        # publication.save()
        return JsonResponse({'id': publ_id})


def error_404_view(request, exception):
    return render(request, '404.html')
