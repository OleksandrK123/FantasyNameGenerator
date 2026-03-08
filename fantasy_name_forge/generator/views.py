from django.shortcuts import render, redirect
import random
from .models import NameCategory, FantasyName, FavoriteName
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token

# Create your views here.
# Префиксы суфиксы и тд
NAME_PARTS = {
    'Elf': {
        'prefixes': ['El', 'Ari', 'Luth', 'Syl', 'Faer', 'Nim', 'Thal', 'Elen', 'Isil', 'Ser'],
        'roots': ['lith', 'mir', 'wen', 'riel', 'thas', 'nor', 'sari', 'myr', 'ael', 'indra'],
        'suffixes': ['iel', 'wyn', 'ara', 'eth', 'ion', 'enor', 'lisse', 'indra', 'thiel', 'anya']
    },

    'Orc': {
        'prefixes': ['Gor', 'Thok', 'Brak', 'Zug', 'Krul', 'Urg', 'Mok', 'Drog', 'Snar', 'Grum'],
        'roots': ['gash', 'mok', 'drok', 'zug', 'krag', 'thrak', 'brok', 'snok', 'grak', 'vrog'],
        'suffixes': ['ar', 'og', 'uk', 'ash', 'dum', 'rak', 'mokh', 'zugh', 'grom', 'nakh']
    },
    'Mage': {
        'prefixes': ['Al', 'Mer', 'Thaum', 'Zan', 'Eld', 'Vel', 'Quor', 'Iri', 'Sol', 'Xen'],
        'roots': ['zor', 'vex', 'mir', 'thal', 'arc', 'nex', 'aer', 'lum', 'eth', 'syg'],
        'suffixes': ['us', 'ion', 'or', 'an', 'ix', 'ar', 'en', 'ius', 'eth', 'orim']
    },
    'Demon': {
        'prefixes': ['Nyx', 'Az', 'Bel', 'Mal', 'Xar', 'Vul', 'Zar', 'Draz', 'Khar', 'Noct'],
        'roots': ['goth', 'zeth', 'vhar', 'draz', 'noct', 'shul', 'xeth', 'morg', 'raz', 'vrax'],
        'suffixes': ['ar', 'azul', 'eth', 'or', 'rax', 'zoth', 'mirg', 'ul', 'aaz', 'thul']
    },
    'Legendary': {
        'prefixes': ['Xar', 'Vel', 'Nyx', 'Thaur', 'Zar', 'Quor', 'Elyr', 'Draz'],
        'roots': ['veth', 'mirg', 'zul', 'aeth', 'nex', 'syg', 'vrax', 'morg'],
        'suffixes': ['ion', 'azul', 'orim', 'thul', 'aaz', 'ethar', 'xen', 'ul']
    }

}


def generate_name(category_name):
    parts = NAME_PARTS.get(category_name)
    if not parts:
        return "Unknown race"
    return (
            random.choice(parts["prefixes"]) +
            random.choice(parts["roots"]) +
            random.choice(parts["suffixes"])
    )


def home(request):
    name = None
    category = None
    favorites = None

    # Показываем избранное только авторизованным
    if request.user.is_authenticated:
        favorites = FavoriteName.objects.filter(user=request.user).order_by('-added_at')

    # Обработка генерации имени
    if request.method == 'POST':
        category_name = request.POST.get('category')
        category = NameCategory.objects.filter(name=category_name).first()
        if category:
            generated = generate_name(category.name)
            name = [generated]  # ← обернули в список
            FantasyName.objects.create(name=generated, category=category)

            # Удаляем всё, кроме последних 50
            extra_ids = FantasyName.objects.order_by('-created_at').values_list('id', flat=True)[50:]
            FantasyName.objects.filter(id__in=extra_ids).delete()

    categories = NameCategory.objects.all()
    filter_category = request.GET.get('filter')

    # История последних 50 имён
    if filter_category:
        recent_names = FantasyName.objects.select_related('category') \
                           .filter(category__name=filter_category) \
                           .order_by('-created_at')[:50]
    else:
        recent_names = FantasyName.objects.select_related('category') \
                           .order_by('-created_at')[:50]

    return render(request, 'generator/home.html', {
        'names': name,
        'categories': categories,
        'selected_category': category.name if category else None,
        'recent_names': recent_names,
        'filter_category': filter_category,
        'favorites': favorites,
    })


@login_required
def add_favorite(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        race = request.POST.get('race', '')
        if name:
            exists = FavoriteName.objects.filter(user=request.user, name=name, race=race).exists()
            if not exists:
                FavoriteName.objects.create(user=request.user, name=name, race=race)
    return redirect('home')


def custom_logout(request):
    logout(request)
    return redirect("home")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'generator/register.html', {'form': form})


@login_required
def my_favorites(request):
    favorites = FavoriteName.objects.filter(user=request.user)
    return render(request, 'generator/my_favorites.html', {'favorites': favorites})


@require_POST
def generate_name_ajax(request):
    category_name = request.POST.get('category')
    category = NameCategory.objects.filter(name=category_name).first()
    if not category:
        return JsonResponse({'error': 'Unknown category'}, status=400)

    if category.name != 'Legendary' and random.random() > 0.5:
        legendary = NameCategory.objects.filter(name='Legendary').first()
        if legendary:
            category = legendary

    # Генерируем имя
    parts = NAME_PARTS.get(category.name)
    if not parts:
        return JsonResponse({'error': f'No name parts for category {category.name}'}, status=500)
    generated = (
            random.choice(parts["prefixes"]) +
            random.choice(parts["roots"]) +
            random.choice(parts["suffixes"])
    )

    is_legendary = category.name == 'Legendary'

    # Сохраняем в базу
    FantasyName.objects.create(name=generated, category=category)

    # Удаляем старые, оставляем 50
    extra_ids = FantasyName.objects.order_by('-created_at') \
                    .values_list('id', flat=True)[50:]
    FantasyName.objects.filter(id__in=extra_ids).delete()

    return JsonResponse({
        'name': generated,
        'category': category.name,
        'is_legendary': category.name == 'Legendary',
        'csrf_token': get_token(request)
    })


def get_recent_names_ajax(request):
    race = request.GET.get('race')
    if race:
        names = FantasyName.objects.select_related('category') \
                    .filter(category__name=race) \
                    .order_by('-created_at')[:50]
    else:
        names = FantasyName.objects.select_related('category') \
                    .order_by('-created_at')[:50]

    data = [
        {
            'name': n.name,
            'race': n.category.name,
            'created': n.created_at.strftime('%H:%M:%S, %d.%m.%Y')
        }
        for n in names
    ]
    return JsonResponse({'names': data})
