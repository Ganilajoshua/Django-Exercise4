import csv
import io
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from .models import Contact
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .forms import ContactForm

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
@login_required(login_url='/login/')
def contactList(request):
    contacts = Contact.objects.filter(
            creator = request.user)
    return render(
            request, 'contact/contact_home.html'
            ,{'contacts':contacts})
@login_required(login_url='/login/')
def new_contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.creator = request.user
            contact.save()
            return redirect('/contacts', pk=contact.pk)
    else:
        form = ContactForm()
    return render(
            request
            ,'contact/contact_new.html'
            ,{'form': form})
@login_required(login_url='/login/')
def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.creator = request.user
            contact.save()
            return redirect('/contacts', pk=contact.pk)
    else:
        form = ContactForm(instance=contact)
        contacts = Contact.objects.filter(id=pk)
    return render(
            request, 'contact/contact_edit.html'
            , {'form': form,'contacts':contacts})
@login_required(login_url='/login/')
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    return render(
            request, 'contact/contact_delete.html'
            ,{'contact': contact})
@login_required(login_url='/login/')
def confirm_delete_contact(request,pk):
    contact = get_object_or_404(Contact,pk=pk)
    if request.user:
        contact.delete()
    else:
        print(request.user)
    return redirect('/contacts')
@login_required(login_url='/login/')
def contact_upload(request):
    template = "contact_upload.html"
    prompt = {
        'order':'Order of the CSV should be Last name,First name,Contact Number, Address'
    }
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        prompt = {
            'order':'Please upload .csv file only'
        }
        return render(request, template, prompt)
    date_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(date_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Contact.objects.update_or_create(
            creator = request.user,
            LastName=column[0],
            FirstName=column[1],
            ContactNo=column[2],
            Address=column[3],

        )
    contacts = Contact.objects.filter(creator = request.user)
    return render(
            request,'contact/contact_home.html'
            ,{'contacts':contacts})
@login_required(login_url='/login/')
def contact_download(request):
    contacts = Contact.objects.filter(creator = request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="contact.csv"'
    writer = csv.writer(response, delimiter=',')
    writer.writerow([
        'Last Name'
        ,'First Name'
        ,'Contact No.'
        ,'Address'])
    for contact in contacts:
        writer.writerow([
            contact.LastName
            ,contact.FirstName
            ,contact.ContactNo
            ,contact.Address])
    return response