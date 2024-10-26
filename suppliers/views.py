from django.shortcuts import render, redirect
from django.views import View

from products.models import Product
from countries.models import Regions, Countries
from .forms import FileForm
from .models import Suppliers, SupplierPrices, CertificationDocumentSuppliers, SpecificationDocumentSuppliers
from .utils import calculate_price_from_source, calculate_price_from_sales
from offers.utils import generate_offers, \
    generate_offers_for_new_supplier, generate_offers_for_supplier_new_price, \
    delete_offers_of_suppliers_on_supplier_delete

class SuppliersListView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        suppliers = Suppliers.objects.all().order_by('-id')
        products = Product.objects.all()
        countries = Countries.objects.all()

        selected_product_id = request.GET.get('product', None)
        if selected_product_id:
            selected_product = Product.objects.get(id=selected_product_id)
            products = products.exclude(id=selected_product_id)
            suppliers = suppliers.filter(product_id=selected_product_id)
        else:
            selected_product = None

        selected_country_id = request.GET.get('country', None)
        if selected_country_id:
            selected_country = Countries.objects.get(id=selected_country_id)
            countries = countries.exclude(id=selected_country_id)
            suppliers = suppliers.filter(region__country_id=selected_country_id)
        else:
            selected_country = None

        search = request.GET.get('search', "")
        if search:
            suppliers = suppliers.filter(company_name__icontains=search).order_by('-id')

        return render(request, 'suppliers/list.html', {
            "suppliers": suppliers,
            "products": products,
            "selected_product": selected_product,
            "countries": countries,
            "selected_country": selected_country,
            "search": search
        })


class SuppliersSourceCreateView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        products = Product.objects.all()
        regions = Regions.objects.all().order_by('country')
        fileform = FileForm()
        return render(request, 'suppliers/source/create.html', {
            "products": products,
            "regions": regions,
            "fileform": fileform
        })

    def post(self, request):
        data = request.POST
        
        supplier = Suppliers(
            product_id=data.get('product'),
            added_by=self.request.user,
            region_id=data.get('region'),

            company_name=data.get('company_name'),
            contact_name=data.get('contact_name'),
            landline=data.get('landline'),
            mobile=data.get('mobile'),
            email=data.get('email'),
            format=data.get('format'),
            comments=data.get('comments'),
            # certifications=data.get('certifications'),
            # specifications=data.get('specifications'),
            identifier=data.get('identifier'),
    
            departure_address_lat=data.get('departure_address_lat', None),
            departure_address_lng=data.get('departure_address_lng', None),
            destination_address_lat=data.get('destination_address_lat', None) if data.get('destination_address_lat', None) else None,
            destination_address_lng=data.get('destination_address_lng', None) if data.get('destination_address_lng', None) else None,
    
            weight_of_full_truck=data.get('weight_of_full_truck'),
            margin=data.get('margin'),
            price=data.get('price'),
        )

        price_data = calculate_price_from_source(data)

        supplier.price_exwb = price_data['exwb']
        supplier.price_exws = price_data['exws']

        supplier.save()

        SupplierPrices.objects.create(
            added_by=self.request.user,
            suppliers=supplier,
            price_exwb=supplier.price_exwb,
            price_exws=supplier.price_exws
        )

        for certification_document in request.FILES.getlist('certifications'):
            CertificationDocumentSuppliers.objects.create(
                supplier=supplier,
                file=certification_document
            )

        for specification_document in request.FILES.getlist('specifications'):
            SpecificationDocumentSuppliers.objects.create(
                supplier=supplier,
                file=specification_document
            )

        generate_offers_for_new_supplier(supplier)

        return redirect('suppliers:list')


class SuppliersSalesCreateView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        products = Product.objects.all()
        regions = Regions.objects.all().order_by('country')
        return render(request, 'suppliers/sales/create.html', {
            "products": products,
            "regions": regions
        })

    def post(self, request):
        data = request.POST
        
        supplier = Suppliers(
            product_id=data.get('product'),
            added_by=self.request.user,
            region_id=data.get('region'),

            company_name=data.get('company_name'),
            contact_name=data.get('contact_name'),
            landline=data.get('landline'),
            mobile=data.get('mobile'),
            email=data.get('email'),
            # certifications=data.get('certifications'),
            # specifications=data.get('specifications'),
            identifier=data.get('identifier'),
            format=data.get('format'),
            comments=data.get('comments'),
    
            departure_address_lat=data.get('departure_address_lat', None),
            departure_address_lng=data.get('departure_address_lng', None),
            destination_address_lat=data.get('destination_address_lat', None) if data.get('destination_address_lat', None) else None,
            destination_address_lng=data.get('destination_address_lng', None) if data.get('destination_address_lng', None) else None,
    
            weight_of_full_truck=data.get('weight_of_full_truck') if data.get('weight_of_full_truck') else None,
            price=data.get('price'),
        )

        price_data = calculate_price_from_sales(data)

        supplier.price_exwb = price_data['exwb']
        supplier.price_exws = price_data['exws']

        supplier.save()

        SupplierPrices.objects.create(
            added_by=self.request.user,
            suppliers=supplier,
            price_exwb=supplier.price_exwb,
            price_exws=supplier.price_exws
        )

        for certification_document in request.FILES.getlist('certifications'):
            CertificationDocumentSuppliers.objects.create(
                supplier=supplier,
                file=certification_document
            )

        for specification_document in request.FILES.getlist('specifications'):
            SpecificationDocumentSuppliers.objects.create(
                supplier=supplier,
                file=specification_document
            )

        generate_offers_for_new_supplier(supplier)

        return redirect('suppliers:list')


class SuppliereNewPriceCreateView(View):
    
    def get(self, request, pk):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        supplier = Suppliers.objects.get(id=pk)
        return render(request, "suppliers/source/price.html", {
            "supplier": supplier
        })

    def post(self, request, pk):
        print(request.POST)
        supplier = Suppliers.objects.get(id=pk)

        price_data = calculate_price_from_source({
            "price_type": request.POST.get("price_type"),
            "margin": supplier.product.default_margin,
            "departure_address_lat": supplier.departure_address_lat,
            "departure_address_lng": supplier.departure_address_lng,
            "destination_address_lat": request.POST.get('destination_address_lat', None),
            "destination_address_lng": request.POST.get('destination_address_lng', None),
            "price": int(request.POST.get('price')),
            "weight_of_full_truck": request.POST.get('weight_of_full_truck', None),
            "region": supplier.region.id,

        })

        supplier.price_exwb = price_data['exwb']
        supplier.price_exws = price_data['exws']

        supplier.save()

        SupplierPrices.objects.create(
            added_by=self.request.user,
            suppliers=supplier,
            price_exwb=price_data['exwb'],
            price_exws=price_data['exws']
        )

        generate_offers_for_supplier_new_price(supplier)

        return redirect("suppliers:list")


class SupplierUpdateView(View):
    
    def get(self, request, pk):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        supplier = Suppliers.objects.get(id=pk)
        supplier_prices = supplier.get_supplier_prices()
        return render(request, 'suppliers/update.html', {
            "supplier": supplier,
            "supplier_prices": supplier_prices
        })

    def post(self, request, pk):
        supplier = Suppliers.objects.get(id=pk)

        supplier.company_name = request.POST.get('company_name')
        supplier.contact_name = request.POST.get('contact_name')
        supplier.landline = request.POST.get('landline')
        supplier.mobile = request.POST.get('mobile')
        supplier.email = request.POST.get('email')
        supplier.identifier = request.POST.get('identifier')
        supplier.format = request.POST.get('format')
        supplier.comments = request.POST.get('comments')

        supplier.save()

        return redirect('suppliers:list')


class SupplierDeleteView(View):


    def get_object(self, pk):
        return Suppliers.objects.get(id=pk)

    def get(self, request, pk):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        supplier = self.get_object(pk)
        return render(request, 'suppliers/delete.html', {
            "supplier": supplier
        })

    def post(self, request, pk):
        supplier = self.get_object(pk)

        delete_offers_of_suppliers_on_supplier_delete(supplier)

        supplier.delete()


        return redirect("suppliers:list")