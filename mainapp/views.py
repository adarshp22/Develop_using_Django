from django.shortcuts import render
from .models import Mainapp
from django.conf import settings  # to access the settings values
from .forms import MainappForm,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login
from .forms import SEOForm
from .models import SEOAnalysis
import textrazor
from collections import defaultdict
import json
import requests
import random
import nltk






def analyze_text(request):
    context = {}

    if request.method == "POST":
        form = SEOForm(request.POST)
        if form.is_valid():
            input_text = form.cleaned_data['input_text']

            # Setup TextRazor client
            client = textrazor.TextRazor(extractors=["entities", "topics", "words"])
            client.set_api_key(settings.TEXTRAZOR_API_KEY)
            response = client.analyze(input_text)

            # Extract all keywords: entities and topics
            topic_keywords = {t.label for t in response.topics() if t.score and t.score > 0.5}
            entity_keywords = {e.id for e in response.entities() if e.confidence_score and e.confidence_score > 2}
            all_keywords = topic_keywords | entity_keywords

            # Prepare for quick lookup - lowercase keywords
            all_keywords_lower = {kw.lower() for kw in all_keywords}

            # Suggested keywords excluding input text words
            input_words = set(w.lower() for w in input_text.split())
            suggested_keywords = list(all_keywords_lower - input_words)[:15]

            # Map each word to related keywords that contain or relate to it
            word_replacements = defaultdict(list)

            for word in response.words():
                token = word.token.lower()
                pos = word.part_of_speech

                # Only consider meaningful words (noun, verb, adjective) and length > 3
                if len(token) > 3 and pos.startswith(("NN", "JJ", "VB")):
                    related_suggestions = []

                    # Find keywords that include token as substring or vice versa
                    for kw in all_keywords:
                        kw_lower = kw.lower()
                        if (token in kw_lower or kw_lower in token) and kw_lower != token:
                            related_suggestions.append(kw)

                    # If no direct substring match, find keywords sharing any word with token
                    if not related_suggestions:
                        token_parts = set(token.split())
                        for kw in all_keywords:
                            kw_parts = set(kw.lower().split())
                            if token_parts & kw_parts and kw.lower() != token:
                                related_suggestions.append(kw)

                    # Take unique suggestions, limit to 5 to keep output clean
                    related_suggestions = list(dict.fromkeys(related_suggestions))[:5]

                    if related_suggestions:
                        word_replacements[token].extend(related_suggestions)

            # Build replacement prompts
            replacement_prompts = [
                f"Consider replacing **'{orig}'** with: {', '.join(candidates)}"
                for orig, candidates in word_replacements.items()
            ]

            if not replacement_prompts:
                replacement_prompts.append("No strong replacement suggestions detected — well done!")

            # Calculate readability
            sentence_count = len(response.sentences())
            word_count = len(list(response.words()))
            readability = round(word_count / sentence_count, 2) if sentence_count else 0

            # SEO heuristic tips
            seo_suggestions = []
            if readability > 25:
                seo_suggestions.append("Break long sentences for better readability.")
            if word_count < 100:
                seo_suggestions.append("Text is short. Aim for 300+ words.")
            if len(suggested_keywords) < 5:
                seo_suggestions.append("Include more SEO-relevant terms.")
            if len(suggested_keywords) > 12:
                seo_suggestions.append("Avoid overstuffing with keywords.")

            # Save analysis (optional)
            SEOAnalysis.objects.create(
                input_text=input_text,
                keywords=suggested_keywords,
                readability_score=readability,
                suggestions="\n".join(seo_suggestions + replacement_prompts)
            )

            context.update({
                'form': form,
                'keywords': suggested_keywords,
                'readability': readability,
                'suggestions': "\n".join(seo_suggestions + replacement_prompts),
                'original_text': input_text,
                'word_replacements': json.dumps(word_replacements)
            })

    else:
        form = SEOForm()

    context['form'] = form
    return render(request, 'seo.html', context)


def mainapp_list(request):
    mainapp = Mainapp.objects.all().order_by('-created_at')
    return render(request, 'mainapp_list.html', {'mainapps': mainapp})


@login_required
def mainapp_create(request):
    if request.method == 'POST':
        form = MainappForm(request.POST, request.FILES)
        if form.is_valid():
            mainapp = form.save(commit=False)
            mainapp.user = request.user
            mainapp.save()
            return redirect('mainapp_list')
    else:
        form = MainappForm()
    return render(request, 'mainapp_form.html', {'form': form})





def mainapp_list(request):
    mainapp=Mainapp.objects.all().order_by('-created_at')
    return render(request, 'mainapp_list.html',{'mainapps': mainapp})


@login_required
def mainapp_create(request):
    if request.method=='POST':
        form=MainappForm(request.POST, request.FILES)
        if form.is_valid():
            
            mainapp=form.save(commit=False)
            mainapp.user=request.user
            mainapp.save()
            return redirect('mainapp_list')
            
    
    else:
        form=MainappForm()
    return render(request,'mainapp_form.html',{'form':form})



@login_required
def mainapp_edit(request,mainapp_id):
    mainapp=get_object_or_404(Mainapp,pk=mainapp_id,user=request.user)
    if request.method=='POST':
         form=MainappForm(request.POST, request.FILES, instance=mainapp)
         
         
         if form.is_valid():   
          mainapp=form.save(commit=False)
          mainapp.user=request.user
          mainapp.save()
          return redirect('mainapp_list')
    
        
    else:
        form=MainappForm(instance=mainapp)
    return render(request,'mainapp_form.html',{'form':form})





@login_required
def mainapp_delete(request,mainapp_id):
    mainapp=get_object_or_404(Mainapp,pk=mainapp_id,user=request.user)
    if request.method =="POST":
        mainapp.delete()
        return redirect('mainapp_list')
    return render(request,'mainapp_confirm_delete.html',{'mainapp':mainapp})
    
    
def register(request):
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid:
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('mainapp_list')
    else:
        form=UserRegistrationForm()
    
    return render(request,'registration/register.html',{'form':form})
    