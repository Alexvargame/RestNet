from django.db import models
from django.shortcuts import reverse

from users.models import User

from random import randint
from decimal import Decimal

from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
import io
import xhtml2pdf.pisa as pisa

class Printer(models.Model):
    key=randint(1,100)
    name=models.CharField(max_length=100)
    api_key=models.CharField(max_length=20,unique=True,default=key)
    check_type=models.CharField(choices=[('kitchen','kitchen'),('client','client')],max_length=10)
    point_id=models.IntegerField()

    class Meta:
        verbose_name='Принтер'
        verbose_name_plural='Принтеры'

    def __str__(self):
        return self.name

    def print_check(self,query_check):
        for ch in query_check:
            ch.status = 'printed'
            print('PDF', ch.pdf_file, 'напечатан на принтере', self)
            ch.save()
        return query_check


def get_check_file_path(instance,filename):
    date_str=instance.order['date_created'].strftime("%Y%m%d")
    return os.path.join('checks/files/'+f'{date_str}',filename)
class Check(models.Model):
    printer_id=models.ForeignKey(Printer,related_name='printer',on_delete=models.DO_NOTHING)
    type=models.CharField(choices=[('kitchen','kitchen'),('client','client')],max_length=10)
    order=models.JSONField(blank=True,null=True)
    order_created=models.ForeignKey(User,related_name='order_created',on_delete=models.DO_NOTHING,default=1)
    status=models.CharField(choices=[('new','new'),('rendered','rendered'),('printed','printed')],max_length=10)
    pdf_file=models.FileField(default='default.pdf',upload_to=get_check_file_path,blank=True,null=True)

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    def __str__(self):
        return self.order['order_id']

    def get_creator(self):
        return User.objects.get(id=self.order['creator'])

    def get_absolute_url(self):
        return reverse('check_detail_url',kwargs={'pk':self.id})

    def get_order_list(self):
        list_order_dict={}
        for key,value in self.order['order'].items():
            list_order_dict[Product.objects.get(id=key).name]=value
        return list_order_dict

    def get_order_summa(self):
        total_price=Decimal(0)
        for key,value in self.order['order'].items():
            total_price+=Decimal(value['quantity'])*Decimal(value['price'])
        return total_price

    def render_to_pdf(self,template_src, filename='contract.pdf'):
        template = get_template(template_src)
        #context = Context(self.order)
        html = template.render(self.order)
        result = io.StringIO()

        pdf = pisa.pisaDocument(
            #io.BytesIO(html.encode('utf-8')),
            result,
            encoding='UTF-8',
            show_error_as_pdf=True
        )
        if not pdf.err:

            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename

            return response
        return HttpResponse(u'We had some errors!')


class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    in_stock=models.FloatField()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail_url',kwargs={'product_id':self.id})

    def get_update_url(self):
        return reverse('product_update_url',kwargs={'product_id':self.id})
    def get_delete_url(self):
        return reverse('product_delete_url',kwargs={'product_id':self.id})