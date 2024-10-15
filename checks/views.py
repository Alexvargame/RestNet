import os
import asyncio
import json

from django.shortcuts import render,get_object_or_404, redirect
from django.shortcuts import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.files.base import ContentFile
from django.core.files import File

from decimal import Decimal
from datetime import datetime
from random import randint

from .forms import OrderForm,CheckForm,ProductForm
from .models import Check,Product,Printer
from cart.forms import CartAddProductForm
from cart.cart import Cart

from .services import get_files#,print_files

from threading import Thread

#import aspose.words
def main_page(request):
    return render(request,'checks/main_page.html')


# class CheckCreateView(LoginRequiredMixin,View):
#
#
#     def get(self,request):
#         cart=Cart(request)
#         #form_order=OrderForm()
#         form_check=CheckForm()
#         return render(request, 'checks/check_create.html', {'form_check':form_check,'cart':cart})#'form_order': form_order,
#
#     def post(self,request):
#         order_dict={}
#         cart=Cart(request)
#         #bound_form_order=OrderForm(request.POST)
#         bound_form_check=CheckForm(request.POST)
#         print(request.POST)
#         print(bound_form_check['printer_id'].value())
#         if bound_form_check.is_valid():# and bound_form_order.is_valid():
#             new_check=bound_form_check.save(commit=False)
#             order_dict['order_id'] = str(randint(1, 100)) + datetime.now().strftime("%Y%m%d%H%M%S")
#             order_dict['creator']=request.user.id
#             order_dict['date_created']=datetime.now().strftime("%Y %m %d %H:%M:%S")
#             # product=Product.objects.get(id=bound_form_order['name'].value())
#             order_dict['order']={}
#             # order_dict[bound_form_order['name'].value()]['count']=bound_form_order['count'].value()
#             # order_dict[bound_form_order['name'].value()]['price'] = str(product.price)
#             # order_dict[bound_form_order['name'].value()]['summa'] = str(Decimal(bound_form_order['count'].value())*product.price)
#             for item in cart:
#                 order_dict['order'][item['product'].id]= {'quantity':item['quantity'],'product':item['product'].name,'price':item['price'],'total_price':item['total_price']}
#             new_check.order=order_dict
#             new_check.save()
#             cart.clear()
#             for product in Product.objects.filter(id__in=new_check.order['order'].keys()):
#                 product.in_stock-=float(new_check.order['order'][product.id]['quantity'])
#                 product.save()
#             return redirect(new_check)
#         else:
#             return render(request, 'checks/check_create.html', {'form_check': bound_form_check})#'form_order': bound_form_order,

class CheckDetailView(LoginRequiredMixin,View):

    def get(self,request,pk):
        check=Check.objects.get(id=pk)
        return render(request,'checks/check_detail.html',{'check':check})

class ChecksListView(LoginRequiredMixin,View):
    def get(self,request):
        checks=Check.objects.all()
        return render(request,'checks/checks_list.html',{'checks':checks,'summary':sum([c.get_order_summa() for c in checks]),
                                                         'length':len(checks)})


class ProductListView(LoginRequiredMixin,View):
    def get(self,request):
        products=Product.objects.all()
        return render(request,'checks/products_list.html',{'products':products})

class ProductDetailView(LoginRequiredMixin,View):
    def get(self,request,product_id):
        product=Product.objects.get(id=product_id)
        cart_add_form=CartAddProductForm()
        return render(request,'checks/product_detail.html',{'product':product,'cart_add_form':cart_add_form})

class ProductCreateView(LoginRequiredMixin,View):
    def get(self,request):
        form=ProductForm(initial={'in_stock':0.00})
        return render(request,'checks/product_create.html',{'form':form})
    def post(self,request):
        bound_form=ProductForm(request.POST)
        if bound_form.is_valid():
            new_product=bound_form.save()
            return redirect(new_product)
        else:
            return render(request, 'checks/product_create.html', {'form': bound_form})

class ProductUpdateView(LoginRequiredMixin,View):
    def get(self,request,product_id):
        product=Product.objects.get(id=product_id)
        form=ProductForm(instance=product)
        return render(request,'checks/product_update.html',{'form':form})
    def post(self,request,product_id):
        product = Product.objects.get(id=product_id)
        in_stock = product.in_stock
        bound_form=ProductForm(request.POST,instance=product)
        if bound_form.is_valid():
            product=bound_form.save(commit=False)
            product.in_stock=in_stock+float(bound_form['in_stock'].value())
            product.save()
            return redirect(product)
        else:
            return render(request, 'checks/product_update.html', {'form': bound_form})


class ProductDeleteView(LoginRequiredMixin, View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)
        return render(request, 'checks/product_delete.html', context={'product': product})


    def post(self, request, product_id):
        product = Product.objects.get(id=product_id)
        product.delete()
        return redirect(reverse('products_list_url'))

class ChecksMultiCreateView(LoginRequiredMixin,View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'checks/check_create.html',{'cart': cart,
                                'message':f"Если в чеке все верно, сохраниет и отправьте на печать"})
    def post(self,request):
        cart=Cart(request)
        order_dict={}
        checks_list=[]
        order_dict['order_id'] = str(randint(1, 100)) + datetime.now().strftime("%Y%m%d%H%M%S")
        order_dict['creator'] = request.user.id
        order_dict['date_created'] = datetime.now().strftime("%Y %m %d %H:%M:%S")
        order_dict['order'] = {}
        for item in cart:
            order_dict['order'][item['product'].id] = {'quantity': item['quantity'], 'product': item['product'].name,
                                                       'price': item['price'], 'total_price': item['total_price']}
        if not os.path.isdir(os.path.join(os.getcwd(), 'checks_files')):
            os.mkdir(os.path.join(os.getcwd(), 'checks_files'))
        os.chdir(os.path.join(os.getcwd(), 'checks_files'))
        path = os.path.join(os.getcwd(),order_dict['order_id'][-14:-6])
        if not os.path.isdir(path):
            os.mkdir(path)
        os.chdir(path)
        for printer in Printer.objects.filter(point_id=1):
            filename=order_dict['order_id']+'_'+printer.check_type+'.pdf'
            new_check=Check.objects.create(printer_id=printer,status='new',order=order_dict,pdf_file=filename)
            new_check.type=printer.check_type
            # file=aw.Document()
            # builder=aw.DocumentBuilder(file)
            # builder.writeln(new_check.order)
            # doc.save(new_check.pdf_file)
            with open(filename,'w') as f:

               # f.write(new_check.render_to_pdf('checks/check_detail.html',new_check.pdf_file))
                for key,value in new_check.__dict__.items():
                    f.write("{}-{}".format(key,value)+'\n')


            r=new_check.render_to_pdf('checks/check_detail.html',new_check.pdf_file)
            print(r)


            new_check.save()

            checks_list.append(new_check)
        cart.clear()
        os.chdir(r'C:\Python39\django\RestNet')
        for product in Product.objects.filter(id__in=new_check.order['order'].keys()):
            product.in_stock-=float(new_check.order['order'][product.id]['quantity'])
            product.save()

        return render(request,'checks/new_checks_list.html',{'checks':checks_list})

class FilesToRenderView(LoginRequiredMixin,View):
    def get(self,request):
        print_query=[]
        print_dict={}
        query=[check for check in Check.objects.filter(status='new')]
        if query:
            query=asyncio.run(get_files(query))
            for q in query:
                q.save()
        print_query=[check for check in Check.objects.filter(status='rendered')]
        if print_query:
            for check in Check.objects.filter(status='rendered'):
                key,value=check.printer_id,check
                l=print_dict.get(key,[])
                if value.printer_id==key:
                    l.append(value)
                print_dict[key]=l
            main_thread = list(print_dict.keys())[0]
            if len(print_dict.keys())>1:
                for key in list(print_dict.keys())[1:]:
                    Thread(target=key.print_check,args=(print_dict[key],)).start()
            main_thread.print_check(print_dict[main_thread])

        return render(request,'checks/files.html',{'query':print_query})