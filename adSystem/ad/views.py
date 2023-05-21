from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Ad, Individual, City, Type
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm, CreateAdForm
from django.http import HttpRequest, HttpResponseRedirect


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
    context = {
        'ad_list': ad_list,
        'individual': individual,
        'user': user,
    }
    return render(request, 'ad/profile.html', context)


class adDetailView(generic.DetailView):
    model = Ad

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = self.get_object()
        object_list = Ad.objects.filter(Q(type__name__icontains = ad.type.name)).exclude(Q(name__exact=ad.name))
        context['ad_list'] = object_list
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
            return HttpResponseRedirect('/')
    else:
        form = CreateAdForm()
    return render(request, 'ad/create_ad.html', {'form': form})

def delete_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if ad.owner == Individual.objects.get(user__exact=request.user):
        ad.delete()
    return HttpResponseRedirect('/')  # Redirect to the success page

# class adListView(generic.ListView) :
#     model = Ad
#     paginate_by = 5
