from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from .models import Product, Units


class ProductsListView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        products = Product.objects.all()
        product_count = products.count()
        return render(request, 'products/list.html', {
            'products': products,
            'products_count': product_count
        })



class ProductsCreateView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        units = Units.objects.all().order_by('-id')
        return render(request, 'products/create.html', {
            "units": units
        })

    def post(self,request):
        Product.objects.create(
            name=request.POST.get('name'),
            default_unit_id=request.POST.get('unit'),
            default_margin=request.POST.get('margin'),
        )
        return redirect("products:list")

class ProductsUpdateView(View):

    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    def get(self, request, pk):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        product = self.get_object(pk)
        other_units = Units.objects.all().exclude(
            id=product.default_unit.id
        )

        return render(request, 'products/update.html', {
            "product": product,
            "other_units": other_units
        })

    def post(self, request, pk):
        product = self.get_object(pk)
        product.name = request.POST.get('name')
        product.default_unit_id = request.POST.get('unit')
        product.default_margin = request.POST.get('margin')
        product.save()

        return redirect("products:list")
        

class ProductsDeleteView(View):

    def get_object(self, pk):
        return get_object_or_404(Product, pk=pk)

    def get(self, request, pk):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        product = self.get_object(pk)
        return render(request, "products/delete.html", {
            "product": product
        })

    def post(self, request, pk):
        product = self.get_object(pk)
        product.delete()

        return redirect("products:list")


class UnitCreateView(View):

    def get(self, request):
        if not request.user.is_authenticated:
            print("Not Logged In")
            return redirect("accounts:login")

        return render(request, 'units/create.html', {
        })

    def post(self,request):
        Units.objects.create(
            name=request.POST.get('name'),
        )
        return redirect(request.GET.get('next'))
