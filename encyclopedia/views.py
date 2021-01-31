from django.shortcuts import render
import markdown2
from . import util
from django import forms
import random

# Class inheritance from django built-in forms
class SearchForm (forms.Form):
    search = forms.CharField(label="Search Encyclopedia")

# Class for submitting New Page
class NewPageForm (forms.Form):
    page_title = forms.CharField()
    md_content = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))

# Class for Editting Pages
class EditForm (forms.Form):
    md_content = forms.CharField(label="Markdown Content", widget=forms.Textarea(attrs={"rows":5, "cols":20}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def route(request, title):

    # Obtain file from entries folder
    md = util.get_entry(title)

    if md == None:
        error = "does not exist"
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "form": SearchForm(),
            "message": error
            })

    # Convert Markdown to HTML
    html = markdown2.markdown(md)

    return render(request, "encyclopedia/title.html", {
        "title": title,
        "html": html,
        "form": SearchForm()
    })



def search(request):
  
    if request.method == 'POST':

        # Get Search Entry and store in form
        form = SearchForm(request.POST)  

        # is_valid python function returning boolean expression (Ex. blank = False)
        if form.is_valid():

            # Cleaned_data used to avoid attacks, secure input
            search_entry = form.cleaned_data["search"]

            for item in util.list_entries():
                
                # If match return the HTML page
                if item.lower() == search_entry.lower():
                    md = util.get_entry(item)
                    html = markdown2.markdown(md) 
                    return render(request, "encyclopedia/title.html", {
                        "title": search_entry,
                        "html": html,
                        "form": SearchForm()
                    })

            # Encyclopedia entry does not match, Search List
            x = len(search_entry)
            matches = []
            found_match = False
            
            # Create list of matches
            for item in util.list_entries():
                if item[0:x] == search_entry:
                    matches.append(item)
                    found_match = True
                
            
            if found_match == True:
                # Pass matches list and search_entry to search.html
                return render(request, "encyclopedia/search.html", {
                        "matches": matches,
                        "form": SearchForm(),
                        "search": search_entry
                    })
            else:
                error = "does not exist"
                return render(request, "encyclopedia/error.html", {
                    "title": search_entry,
                    "form": SearchForm(),
                    "message": error
                })

    else:   
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })


def create(request):

    if request.method == 'POST':

        # Get Search Entry and store in form
        form = NewPageForm(request.POST)

        # is_valid python function returning boolean expression (Ex. blank = False)
        if form.is_valid():

            # Cleaned_data used to avoid attacks, secure input
            title = form.cleaned_data["page_title"]
            md = form.cleaned_data["md_content"]

            error = "already exists"

            # For Loop if encyclopedia entry exists, return error message
            for item in util.list_entries():
                if item == title:
                    return render(request, "encyclopedia/error.html", {
                    "title": title,
                    "form": SearchForm(),
                    "message": error
                    })

            # Save Entry
            util.save_entry(title, md)

            # Convert Markdown to HTML
            html = markdown2.markdown(md)

            return render(request, "encyclopedia/title.html", {
                "title": title,
                "html": html,
                "form": SearchForm()
    })
    else:
        return render(request, "encyclopedia/create.html", {
            "entries": util.list_entries(),
            "new_page_form": NewPageForm(),
            "form": SearchForm()
    })


def edit(request, title):
    if request.method == 'POST':

        # Same sequence as Create : POST
        form = EditForm(request.POST)

        if form.is_valid():

            md = form.cleaned_data["md_content"]
            util.save_entry(title, md)
            html = markdown2.markdown(md)
            return render(request, "encyclopedia/title.html", {
                "title": title,
                "html": html,
                "form": SearchForm()
            })          


    else:
        md = util.get_entry(title)

        # Initalize form value
        content = EditForm(initial={'md_content': md}, auto_id=False)

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "md": md,
            "form": SearchForm(),
            "content": content
        })

def random_page(request):

    # Generate random number, title
    entries = len(util.list_entries())
    n = random.randint(0, entries - 1)

    title = util.list_entries()[n]

    # Obtain HTML content
    md = util.get_entry(title)
    html = markdown2.markdown(md) 

    return render(request, "encyclopedia/title.html", {
                "title": title,
                "html": html,
                "form": SearchForm()
            })    
