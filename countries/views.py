from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import JsonResponse
from accounts.models import User
from django.views import View

from .models import Countries, Regions
from offers.utils import generate_offers_for_new_departments, \
    generate_offers_for_department_on_location_update
from countries.utils import closest_location

class TransportationSetupView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        countries = Countries.objects.all()
        selected_country = request.GET.get("country")
        print(selected_country)
        if selected_country:
            country = Countries.objects.get(id=selected_country)
        else:
            country = Countries.objects.first()

        return render(request, "countries/transportation_setup.html", {
            "countries": countries,
            "country": country
        })

    def post(self, request):
        print(request.POST)

        r = Regions.objects.get(id=request.POST.get('id'))
        r.price = request.POST.get('price')
        r.coefficient_distance = request.POST.get('coefficient_distance')
        r.coefficient_price = request.POST.get('coefficient_price')
        r.save()

        return redirect(reverse('countries:transportation_setup') + f"?country={r.country.id}")


class CountryCreateView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        users = User.objects.all()
        return render(request, "countries/country/create.html", {
            "users": users,
        })

    def post(self, request):
        country_name = request.POST.get("name", None)
        if country_name:
            country = Countries.objects.create(
                name=country_name
            )
        
            for user in User.objects.all():
                if self.request.POST.get(f"user{user.id}") == "on":
                    user.countries.add(country)

            return redirect(reverse('countries:transportation_setup') + f"?country={country.id}")
        return redirect('countries:transportation_setup')


class CountryUpdateView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        users = User.objects.all()
        country = get_object_or_404(Countries, pk=pk)
        return render(request, "countries/country/update.html", {
            "users": users,
            "country": country
        })

    def post(self, request, pk):
        country = get_object_or_404(Countries, pk=pk)
        
        for user in User.objects.all():
            if self.request.POST.get(f"user{user.id}") == "on":
                user.countries.add(country)
            else:
                user.countries.remove(country)

        return redirect(reverse('countries:transportation_setup') + f"?country={country.id}")


class CountryDeleteView(View):

    def get_object(self, pk):
        return get_object_or_404(Countries, pk=pk)

    def get(self, request, pk):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        country = self.get_object(pk)
        regions = ", ".join(Regions.objects.filter(country=country).values_list("name", flat=True))
        return render(request, "countries/country/delete.html", {
            "country": country,
            "regions": regions,
        })

    def post(self, request, pk):
        country = self.get_object(pk)
        country.delete()

        return redirect(reverse('countries:transportation_setup'))

class RegionCreateView(View):

    def get(self, request, pk):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        country = get_object_or_404(Countries, id=pk)
        return render(request, "countries/region/create.html", {
            "country": country
        })

    def post(self, request, pk):
        region = Regions.objects.create(
            country_id=pk,
            name=request.POST.get("name"),
            price=request.POST.get("price"),
            coefficient_price=request.POST.get("coefficient_price"),
            coefficient_distance=request.POST.get("coefficient_distance"),
            center_lat=request.POST.get("center_lat"),
            center_lng=request.POST.get("center_lng"),
        )

        generate_offers_for_new_departments(region)
        return redirect(reverse('countries:transportation_setup') + f"?country={pk}")


class RegionDeleteView(View):

    def get_object(self, pk):
        return get_object_or_404(Regions, pk=pk)

    def get(self, request, pk):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        region = self.get_object(pk)
        return render(request, "countries/region/delete.html", {
            "region": region
        })

    def post(self, request, pk):
        region = self.get_object(pk)
        country = region.country
        region.delete()

        return redirect(reverse('countries:transportation_setup') + f"?country={country.id}")


class RegionLocationUpdateView(View):

    def get_object(self, pk):
        return get_object_or_404(Regions, pk=pk)

    def get(self, request, pk):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        region = self.get_object(pk)
        return render(request, 'countries/region/location.html', {
            "region": region
        })

    def post(self, request, pk):
        region = self.get_object(pk)
        coordinates = self.request.POST.get('center').split(",")
        region.center_lat = coordinates[0]
        region.center_lng = coordinates[1]
        region.save()

        generate_offers_for_department_on_location_update(region)

        return redirect(reverse('countries:transportation_setup') + f"?country={region.country.id}")


class ClosestRegionByCoordinatesView(View):

    def post(self, request):
        lat = float(request.POST.get('lat'))
        lng = float(request.POST.get('lng'))

        region = closest_location(
            lat, lng, Regions.objects.all()
        )

        return JsonResponse({
            "region_id": region.id,
            "region_name": region.name
        })
