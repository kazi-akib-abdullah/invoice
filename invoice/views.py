from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.template.loader import get_template
from django.http import HttpResponse
from django.views import View
from .models import LineItem, Invoice
from .forms import LineItemFormset, InvoiceForm

import pdfkit

class InvoiceListView(View):
    def get(self, *args, **kwargs):
        invoices = Invoice.objects.all()
        context = {
            "invoices":invoices,
        }

        return render(self.request, 'invoice/invoice-list.html', context)
    
    def post(self, request):        
        # import pdb;pdb.set_trace()
        invoice_ids = request.POST.getlist("invoice_id")
        invoice_ids = list(map(int, invoice_ids))

        update_status_for_invoices = int(request.POST['status'])
        invoices = Invoice.objects.filter(id__in=invoice_ids)
        # import pdb;pdb.set_trace()
        if update_status_for_invoices == 0:
            invoices.update(status=False)
        else:
            invoices.update(status=True)

        return redirect('invoice:invoice-list')

def createInvoice(request):
    """
    Invoice Generator page it will have Functionality to create new invoices, 
    this will be protected view, only admin has the authority to read and make
    changes here.
    """

    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = LineItemFormset(request.GET or None)
        form = InvoiceForm(request.GET or None)
    elif request.method == 'POST':
        formset = LineItemFormset(request.POST)
        form = InvoiceForm(request.POST)
        
        if form.is_valid():
            invoice = Invoice.objects.create(customer=form.data["customer"],
                    # customer_email=form.data["customer_email"],
                    phone=form.data['phone'],
                    area=form.data['area'],
                    billing_address = form.data["billing_address"],
                    # due_date=form.data["due_date"], 
                    message=form.data["message"],
                    )
            if invoice.area == 'BD-O*':
                delivery_fees = float(130)
            else:
                delivery_fees = float(80)
            # invoice.save()
            
        if formset.is_valid():
            # import pdb;pdb.set_trace()
            # extract name and other data from each form and save
            total = 0
            grand_total = 0
            for form in formset:
                # service = form.cleaned_data.get('service')
                product = form.cleaned_data.get('product')
                # description = form.cleaned_data.get('description')
                quantity = form.cleaned_data.get('quantity')
                rate = form.cleaned_data.get('rate')
                if product and quantity and rate:
                    amount = float(rate)*float(quantity)
                    total += amount
                    LineItem(customer=invoice,
                            product=product,
                            # description=description,
                            quantity=quantity,
                            rate=rate,
                            amount=amount).save()
            grand_total = total+delivery_fees

            invoice.total_amount = total
            invoice.grand_total = grand_total
            invoice.delivery_fees = delivery_fees
            invoice.save()
            print(grand_total)
            print(total)
            print(delivery_fees)
            try:
                generate_PDF(request, id=invoice.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect('/')
    context = {
        "title" : "Invoice Generator",
        "formset": formset,
        "form": form,
    }
    return render(request, 'invoice/invoice-create.html', context)


def view_PDF(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)
    lineitem = invoice.lineitem_set.all()

    context = {
        "company": {
            "name": "The Fashion Truck",
            "address" :"Malibagh, Dhaka 1217",
            "phone": "01832-198223",
            "email": "thefashiontruckbd@gmail.com",
        },
        "invoice_id": invoice.id,
        "invoice_total": invoice.total_amount,
        "delivery_fees": invoice.delivery_fees,
        "grand_total": invoice.grand_total,
        "customer": invoice.customer,

        # "customer_email": invoice.customer_email,
        "phone": invoice.phone,
        "area": invoice.area,
        "date": invoice.date,
        # "due_date": invoice.due_date,
        "billing_address": invoice.billing_address,
        "message": invoice.message,
        "lineitem": lineitem,

    }
    return render(request, 'invoice/pdf_template.html', context)

def generate_PDF(request, id):
    # Use False instead of output path to save pdf to a variable
    pdf = pdfkit.from_url(request.build_absolute_uri(reverse('invoice:invoice-detail', args=[id])), False)
    response = HttpResponse(pdf,content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    return response


def change_status(request):
    return redirect('invoice:invoice-list')

def view_404(request,  *args, **kwargs):

    return redirect('invoice:invoice-list')