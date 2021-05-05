from django.shortcuts import render, redirect
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone, dateformat
from django.http import HttpResponse, JsonResponse
from .models import Verified_data
from datetime import datetime


# Create your views here.
def dashboard(request):
    city = [item['city'] for item in Verified_data.objects.order_by().values('city').distinct()]
    category = [item['category'] for item in Verified_data.objects.order_by().values('category').distinct()]
    if request.session.has_key('is_logged'):
        return render(request, 'report.html', {"cities": city, "categories": category})
    else:
        if request.user.is_authenticated:
            request.session['is_logged'] = True
            request.session['username'] = request.user.username
            request.session['first_name'] = request.user.first_name
            request.session['last_name'] = request.user.last_name
            return render(request, 'report.html', {"cities": city, "categories": category})
        else:
            return render(request, 'login.html')
        # return render(request, 'login.html')


class information_ret(BaseDatatableView):
    # The model we're going to show
    model = Verified_data

    # define the columns that will be returned

    # columns = ['name', 'poc', 'phone', 'address', 'email', 'notes', 'verified_status', 'verified_date', 'verified_by' , 'city', 'category']
    columns = ['name', 'poc', 'phone', 'address', 'pincode' ,'email', 'notes', 'verified_status', 'verified_date', 'verified_by',
               'Edit']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    # order_columns = ['id']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 50

    # TODO: Fix time going to column
    def render_column(self, row, column):
        if column == 'Edit':
            return """<button class='btn btn-primary' style="cursor:pointer;" data-toggle="modal" data-target="#info_modal" onclick="show_modal({})">View</button>""".format(
                row.id)
        if column == 'verified_date':
            # import pdb
            # pdb.set_trace()
            if row.verified_date: 
                return timezone.localtime(row.verified_date).strftime("%d %b, %H:%M")
                # return row.verified_date.strftime("%d %b, %H:%M")
        return super(information_ret, self).render_column(row, column)

    # TODO: Change istartswiths to icontains
    def filter_queryset(self, qs):
        search = self.request.GET.get('search[value]', None)
        if search:
            qs = qs.filter(Q(name__icontains=search) |
                           Q(poc__icontains=search) |
                           Q(phone__icontains=search) | Q(email__icontains=search) |
                           Q(notes__icontains=search) | Q(address__icontains=search) |
                           Q(pincode__icontains=search))

        # more advanced example using extra parameters
        city_opt = self.request.GET.get('city', None)
        category_opt = self.request.GET.get('category', None)

        if city_opt and category_opt:
            qs = qs.filter(Q(city=city_opt) & Q(category=category_opt))
        # print("In t")
        # import pdb
        # pdb.set_trace()
        print(len(qs))
        print(qs)
        print(type(qs))
        # import pdb; pdb.set_trace()
        return qs


@csrf_exempt
def get_details(request):
    resource_details = {}
    id = request.POST.get('pk', None)

    if id:
        resource_obj = Verified_data.objects.get(id=id)
        if resource_obj:
            if resource_obj.verified_date == None:
                verified_date = ''
            else:
                verified_date = timezone.localtime(resource_obj.verified_date).strftime("%d %b, %H:%M")

            resource_details = {
                "name": resource_obj.name.capitalize(),
                "poc": resource_obj.poc,
                "phone": resource_obj.phone,
                "email": resource_obj.email,
                "notes": resource_obj.notes,
                "status": resource_obj.verified_status,
                'verified_date': verified_date,
                'verified_by': resource_obj.verified_by,
                'address': resource_obj.address,
                'pincode': resource_obj.pincode
            }

    print(resource_details)
    return JsonResponse({'resource_details': resource_details}, safe=False)


@csrf_exempt
def update_database(request):
    msg = "Failed to update!"
    response = {}
    id = request.POST.get('pk', None)

    if id:
        user = request.POST.get('user', None)
        name = request.POST.get('name', None)
        poc = request.POST.get('poc', None)
        phone = request.POST.get('phone', None)
        email = request.POST.get('email', None)
        notes = request.POST.get('notes', None)
        status = request.POST.get('status', None)
        pincode = request.POST.get('pincode', None)
        address = request.POST.get('address', None)

        try:
            update_obj = Verified_data.objects.filter(id=id)
            update_obj.update(
                name=name,
                poc=poc,
                phone=phone,
                email=email,
                notes=notes,
                address=address,
                pincode=pincode,
                verified_status=status,
                verified_date=timezone.now(),
                verified_by=user,
            )
            msg = "Updated!"
        except:
            msg = "Update Failed!"

    return JsonResponse({"result": msg}, safe=False)


@csrf_exempt
def new_resource(request):
    msg = "Failed to create!"
    response = {}
    user = request.POST.get('user', None)

    if user:
        name = request.POST.get('name', None)
        poc = request.POST.get('poc', None)
        phone = request.POST.get('phone', None)
        email = request.POST.get('email', None)
        notes = request.POST.get('notes', None)
        status = request.POST.get('status', None)
        city = request.POST.get('city', None)
        category = request.POST.get('category', None)
        pincode = request.POST.get('pincode', None)
        address = request.POST.get('address', None)

        try:
            new_obj = Verified_data.objects.create(
                name=name,
                poc=poc,
                phone=phone,
                email=email,
                notes=notes,
                verified_status=status,
                verified_date=timezone.now(),
                verified_by=user,
                city=city,
                category=category,
                address=address,
                pincode=pincode
            )
            msg = "Created Entry!!"
        except:
            msg = "Insertion Failed!"

    return JsonResponse({"result": msg}, safe=False)
