from django.shortcuts import render, redirect
from django.views import View

from products.models import Product
from countries.models import Countries, Regions
from offers.utils import opportunity_detection_algorithm_by_color

class NotificationSourceListView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        products = Product.objects.all()
        countries = self.request.user.countries.all()

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
            regions = Regions.objects.filter(country=selected_country)
        else:
            selected_country = None

        notifications = []
        if selected_product_id and selected_country_id:
            for region in regions:
                fp1 = region.get_best_f_offer(selected_product_id)
                if fp1:
                    offers_data = {}
                    offers_data["FP1"] = fp1
                    best_m_offers = region.get_best_m_offers(selected_product_id)
                    for i in range(len(best_m_offers)):
                        offers_data[f"M{i+1}"] = best_m_offers[i]
                        offers_data[f"M_COLOR_{i+1}"] = opportunity_detection_algorithm_by_color(
                            fp1, best_m_offers[i]
                        )
                        if i > 0:
                            offers_data[f"DIF{i}"] = best_m_offers[i].offer_m_price - best_m_offers[i-1].offer_m_price

                    red_offers = region.get_red_offers(selected_product_id, fp1.offer_f_price)
                    for red_offer in red_offers:
                        notification_data = {}
                        notification_data["notification_offer"] = red_offer
                        notification_data.update(offers_data)
                        notifications.append(notification_data)

        return render(request, "notifications/source/list.html", {
            "countries": countries,
            "products": products,
            "notifications": notifications,
            "selected_product": selected_product,
            "selected_country": selected_country,
        })


class NotificationSalesListView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        products = Product.objects.all()
        countries = self.request.user.countries.all()

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
            regions = Regions.objects.filter(country=selected_country)
        else:
            selected_country = None

        notifications = []
        if selected_product_id and selected_country_id:
            for region in regions:
                fp1 = region.get_best_f_offer(selected_product_id)
                if fp1:
                    offers_data = {}
                    offers_data["FP1"] = fp1
                    best_m_offers = region.get_best_m_offers(selected_product_id)
                    for i in range(len(best_m_offers)):
                        offers_data[f"M{i+1}"] = best_m_offers[i]
                        offers_data[f"M_COLOR_{i+1}"] = opportunity_detection_algorithm_by_color(
                            fp1, best_m_offers[i]
                        )
                        if i > 0:
                            offers_data[f"DIF{i}"] = best_m_offers[i].offer_m_price - best_m_offers[i-1].offer_m_price

                    green_offers = region.get_green_offers(selected_product_id, fp1.offer_f_price)
                    for green_offer in green_offers:
                        notification_data = {}
                        notification_data['color'] = 'text-success'
                        notification_data["notification_offer"] = green_offer
                        notification_data.update(offers_data)
                        notifications.append(notification_data)
                    
                    yellow_offers = region.get_yellow_offers(selected_product_id, fp1.offer_f_price)
                    for yellow_offer in yellow_offers:
                        notification_data = {}
                        notification_data['color'] = 'text-warning'
                        notification_data["notification_offer"] = yellow_offer
                        notification_data.update(offers_data)
                        notifications.append(notification_data)
                    
        print(notifications)
        return render(request, "notifications/sales/list.html", {
            "countries": countries,
            "products": products,
            "notifications": notifications,
            "selected_product": selected_product,
            "selected_country": selected_country,
        })