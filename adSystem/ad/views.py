from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Ad, Individual, City, Type, Offer
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, CreateAdForm, EditAdForm, IndividualForm, OfferCreate
from django.contrib import messages
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from urllib.parse import urlencode
from django.db.models import Count


class adListView(generic.ListView):
    model = Ad
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_list'] = Type.objects.all()
        context['city_list'] = City.objects.all()
        return context

    def get_queryset(self):  # new
        type = self.request.GET.get("type")
        query = self.request.GET.get("search")
        city = self.request.GET.get("city")
        if query or type or city:
            object_list = Ad.objects.filter(
                Q(name__icontains=query, city__name__icontains=city, type__name__icontains=type) |
                Q(description__icontains=query, city__name__icontains=city, type__name__icontains=type)
            )
        else:
            object_list = Ad.objects.all()
        return object_list


@login_required
def profileView(request: HttpRequest):
    individual = Individual.objects.get(user__exact=request.user)

    user = request.user
    ad_list = Ad.objects.filter(
                Q(owner__exact=individual)
            )
    # try:
    #     offers = Offer.objects.filter(ad__owner__user__exact=request.user).annotate(total_offers=Count('ad'))
    # except Offer.DoesNotExist:
    #     offers = None


    offers = Offer.objects.filter(ad__owner__user__exact=request.user)

    ad_offers = {}

    for ad in Ad.objects.filter(offer__in=offers.all()).distinct():
        ad_offers[ad.id] = []
        ad_offers[ad.id].append({'ad': ad, 'offer_list': offers.filter(ad__exact=ad)})

    ad_offers = list(ad_offers.values())

    tab = '1'
    if request.GET.get('tab'):
        tab = request.GET.get('tab')

    context = {
        'ad_list': ad_list,
        'individual': individual,
        'user': user,
        'form': IndividualForm(instance=individual),
        'tab': tab,
        'ad_offers': ad_offers
    }

    return render(request, 'ad/profile.html', context)


class adDetailView(generic.DetailView):
    model = Ad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = self.get_object()
        object_list = Ad.objects.filter(Q(type__name__icontains = ad.type.name)).exclude(Q(name__exact=ad.name))
        context['ad_list'] = object_list
        context['offer_form'] = OfferCreate
        context['is_owner'] = self.request.user == ad.owner.user
        return context


def register_view(request: HttpRequest):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request: HttpRequest):
    logout(request)
    return redirect('/')

@login_required
def create_ad(request: HttpRequest):
    if request.method == 'POST':
        form = CreateAdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.owner = Individual.objects.get(user__exact=request.user)
            ad.name = form.cleaned_data['name']
            ad.description = form.cleaned_data['description']
            ad.price = form.cleaned_data['price']
            ad.city = form.cleaned_data['city']
            ad.street = form.cleaned_data['street']
            ad.house = form.cleaned_data['house']
            ad.type.id = form.cleaned_data['type']
            if 'image' in request.FILES:
                ad.img = request.FILES['image']
            else:
                ad.img = None
            ad.save()
            return HttpResponseRedirect(ad.get_absolute_url())
    else:
        form = CreateAdForm()
    return render(request, 'ad/create_ad.html', {'form': form})

@login_required
def edit_ad(request: HttpRequest, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if request.method == 'POST':
        form = EditAdForm(request.POST, request.FILES)
        if form.is_valid():
            ad.owner = Individual.objects.get(user__exact=request.user)
            ad.name = form.cleaned_data['name']
            ad.description = form.cleaned_data['description']
            ad.price = form.cleaned_data['price']
            ad.city = form.cleaned_data['city']
            ad.street = form.cleaned_data['street']
            ad.house = form.cleaned_data['house']
            ad.type.id = form.cleaned_data['type']
            if 'image' in request.FILES:
                ad.img = request.FILES['image']
            ad.save()
            return HttpResponseRedirect(ad.get_absolute_url())
    else:
        form = EditAdForm(instance=ad)
    return render(request, 'ad/edit_ad.html', {'form': form, 'ad': ad})

def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    rdr = '/'
    if request.GET.get('rdr'):
        rdr = request.GET.get('rdr')
    if ad.owner == Individual.objects.get(user__exact=request.user):
        ad.delete()
    return HttpResponseRedirect(rdr)  # Redirect to the success page


@login_required
def edit_user(request):
    params = {'tab': 3}
    url = reverse('profile') + '?' + urlencode(params)
    individual = get_object_or_404(Individual, user=request.user)

    if request.method == 'POST':
        form = IndividualForm(request.POST, request.FILES, instance=individual)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные были успешно обновлены')
            return redirect(url)

    return redirect(url)

@login_required
def create_offer(request):

    if request.method == 'POST':
        ad = get_object_or_404(Ad, id=request.POST.get('ad_id'))
        form = OfferCreate(request.POST)
        if form.is_valid() and ad.owner.user != request.user:
            offer = form.save(commit=False)
            offer.ad = ad
            offer.customer = request.user
            offer.save()
    else:
        ad = get_object_or_404(Ad, id=request.GET.get('ad_id'))


    return redirect(ad.get_absolute_url())

def delete_offer(request):
    params = {'tab': 2}
    url = reverse('profile') + '?' + urlencode(params)
    if request.method == 'POST':
        offer = get_object_or_404(Offer, id=request.POST.get('offer_id'))
        offer.delete()
    return redirect(url)

# def

# class adListView(generic.ListView) :
#     model = Ad
#     paginate_by = 5
