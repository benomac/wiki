from django.shortcuts import render
import markdown2
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util

# class to create form on "create page"
class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry title")
    description = forms.CharField(widget=forms.Textarea())
    
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def rtrv_entry(request, entry):
    if not util.get_entry(entry):
        result = "ERROR 404: PAGE NOT FOUND"
    else:
        result = markdown2.markdown(util.get_entry(entry))
    return render(request, "encyclopedia/rtrv_entry.html", {
        "entry": result, "title":entry
    })

def search(request):
    if request.method == "POST":
        
        # Get search term from form
        form = request.POST.get('q')
        results = []
        
        for entry in util.list_entries():
            # Check to see if the search term matches a list entry completely. Will take user to that page if it does.
            if form.lower() == entry.lower():
                return HttpResponseRedirect(reverse('encyclopedia:rtrv_entry', args=[form]))
            # Check to see if the search term matches part of a list entry. 
            else:
                if form.lower() in entry.lower():
                    results.append(entry)
        # Returns a warning saying therte is no match at all if there isn't.
        if not results:
            return render(request, "encyclopedia/search.html", {
                                    "none":"No results for that search. "
                            })
        # Return a list of pages that contain search in the title.
        else:
            return render(request, "encyclopedia/search.html", {
                "results":results
        })   

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title in util.list_entries():
                return render(request, "encyclopedia/create.html", {
        "warning":"An entry with that title already exists."
    })
            description = form.cleaned_data["description"]
            util.save_entry(title, description)
            return HttpResponseRedirect(reverse('encyclopedia:rtrv_entry', args=[title]))
    return render(request, "encyclopedia/create.html", {
        "form":NewEntryForm()
    }) 

        
        


