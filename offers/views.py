from django.shortcuts import render, redirect
from django.views import View

from countries.models import Countries, Regions
from products.models import Product
from offers.models import Offers
from suppliers.models import Suppliers
from offers.utils import opportunity_detection_algorithm_by_color

class OffersVisualMapView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        countries = Countries.objects.all()
        products = Product.objects.all()

        destination_markers = Regions.objects.none

        selected_product_id = request.GET.get('product', None)
        if selected_product_id:
            selected_product = Product.objects.get(id=selected_product_id)
            products = products.exclude(id=selected_product_id)
        else:
            selected_product = None

        selected_country_id = request.GET.get('country', None)
        if selected_country_id:
            selected_country = Countries.objects.get(id=selected_country_id)
            countries = countries.exclude(id=selected_country_id)
            destination_markers = Regions.objects.filter(country=selected_country)
        else:
            selected_country = None

        selected_region_id = request.GET.get('region', None)
        if selected_region_id:
            selected_region = Regions.objects.get(id=selected_region_id)
            destination_markers = Regions.objects.filter(id=selected_region_id)
        else:
            selected_region = None

        offers_details_by_region = {}
        if selected_product_id and selected_country:
            for region in destination_markers:
                region_details = {}

                region_details['FP1'] = region.get_best_f_offer(selected_product_id)

                best_m_offers = region.get_best_m_offers(selected_product_id)
                for i in range(len(best_m_offers)):
                    region_details[f"M{i+1}"] = best_m_offers[i]
                    region_details[f"M_COLOR_{i+1}"] = opportunity_detection_algorithm_by_color(
                        region_details['FP1'], best_m_offers[i]
                    )
                    if i > 0:
                        region_details[f"DIF{i}"] = best_m_offers[i].offer_m_price - best_m_offers[i-1].offer_m_price
    
                    offers_details_by_region[region.id] = region_details

        return render(request, "offers/visual_map.html", {
            "countries": countries,
            "products": products,
            "selected_product": selected_product,
            "selected_country": selected_country,
            "selected_region": selected_region,
            "destination_markers": destination_markers,
            "offers_details_by_region": offers_details_by_region
        })


class OfferDetailView(View):

    def get(self, request, pk):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        offer = Offers.objects.get(id=pk)
        supplier_prices = offer.supplier.get_supplier_prices()
        print(supplier_prices)
        return render(request, "offers/detail.html", {
            "offer": offer,
            "supplier_prices": supplier_prices
        })
