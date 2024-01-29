from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util

import markdown2
import random

class new_form(forms.Form) :
    title = forms.CharField(
        initial="",
        widget=forms.TextInput(attrs={'placeholder': 'Enter Page title'}), 
        label=''
        )
    text = forms.CharField(
        initial="",
        widget=forms.Textarea(attrs={
        "placeholder" : "Enter text here" , 
        # "rows":5, "cols":5,
        }),
        label="",
        ) 

all_entries = util.list_entries(True) 
# Home page
def index(request) :
    return render(request, "encyclopedia/index.html")

# Listing entire pages
def all_pages(request):
    want_all_entries = True
    return render(request, "encyclopedia/all_pages.html", {
        "entries": util.list_entries(want_all_entries),
        "want_all_entries" : want_all_entries 
    })


# page url
def return_by_title(request, route, return_webpage=True):
    # page_exists is a bool
    page_exists = None
    # Return by exact title
    if util.get_entry(route):
        if return_webpage :
            page_exists = True
            return render(request, "encyclopedia/page.html", {
                "content" : markdown2.markdown(util.get_entry(route)), "title" : route, "page_exists" : page_exists, "entries" : all_entries 
            })
        else :
            return util.get_entry(route)

# Display warning page
def warning(request) :
    return render(request, "encyclopedia/warningpage.html", {
        "entries" : all_entries 
    })

# Creating Page
def create_page(request, save_page_ifExists = None) :
    form = new_form(request.POST)
    if "title-body" not in request.session :
        request.session["title-body"] = []
    if "content-body" not in request.session :
        request.session["content-body"] = []
    if request.method == "GET" and save_page_ifExists != "yes" and save_page_ifExists !="no":
        page_exists = True
        return render(request, "encyclopedia/newpage.html", {
            "form" : form , "entries" : all_entries 
        })
    elif request.method == "POST" and save_page_ifExists != "yes":
        if form.is_valid():
            title = form.cleaned_data["title"]
            title = title.strip()
            content = form.cleaned_data["text"]
            request.session["title-body"] = title
            request.session["content-body"] = content
            if util.get_entry(title) and save_page_ifExists!= "ignore" :
                # to ask user if they want to replace the page with identitcal title
                return HttpResponseRedirect(reverse('warning'))
            else :
                util.save_entry(request.session["title-body"],request.session["content-body"])
                return HttpResponseRedirect(reverse('page',args=[title]))
    
    # yes, replace page with identitcal title
    elif save_page_ifExists =="yes" :
        util.save_entry(request.session["title-body"],request.session["content-body"])
        return HttpResponseRedirect(reverse('page',args=[request.session["title-body"]]))
    
    # no, don't replace page with identitcal title
    elif save_page_ifExists =="no" :
        # return HttpResponse(f'{request.session["title-body"]}')
        form.fields['title'].initial = request.session["title-body"]
        form.fields['text'].initial = request.session["content-body"]
        return render(request, "encyclopedia/newpage.html", {
            "form" : form , "entries" : all_entries 
        })
    else:
        form = new_form()
    return render(request, "encyclopedia/newpage.html", {
        "form": form, "entries" : all_entries 
        })

# Editing a page
def edit_page(request, route) :
    return_webpage = False
    edit_form  = new_form()
    edit_form.fields['title'].initial = route
    edit_form.fields['text'].initial = return_by_title(request, route, return_webpage)
    return render(request, "encyclopedia/newpage.html", {
            "form" : edit_form , "entries" : all_entries , "ignoreWarning" : True
    })

# Searching for a page
def search(request) :
    title = request.GET.get("q","")
    title = title.strip()
    exact_entry = title if util.get_entry(title) else None
    if request.method == "GET" :
        want_all_entries = False
        page_exists = False
        return render(request, "encyclopedia/all_pages.html", {
            "search_entries" : util.list_entries(want_all_entries, title) , 
            "exact_entry" : exact_entry,
            "title" : title, 
            "page_exists" : page_exists, 
            "entries" : all_entries,
            "want_all_entries" : want_all_entries
        })

# Random Page
def random_page(request) :
    all_pages = util.list_entries(True)
    number_of_pages = len(all_pages)
    random_num = random.randint(0, number_of_pages -1)
    return HttpResponseRedirect(reverse('page',args=[all_pages[random_num]])) 