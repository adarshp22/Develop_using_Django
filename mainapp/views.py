from django.shortcuts import render
from .models import Mainapp
from .forms import MainappForm,UserRegistrationForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login
from .forms import TextInputForm
from .models import SEOAnalysis

# Simulated SEO API response (if no real API available)
def mock_seo_api(text):
    return {
        "readability_score": 72.5,
        "keywords": ["optimization", "search", "content", "ranking"]
    }

# Simple logic to insert a keyword at a natural break
def insert_keyword(text, keyword):
    sentences = text.split('.')
    if len(sentences) > 1:
        sentences[0] += f" {keyword}"
        return '.'.join(sentences)
    else:
        return text + f" {keyword}"

def analyze_text(request):
    form = TextInputForm()
    context = {'form': form}

    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            user_text = form.cleaned_data['text']

            # 🔄 Call external SEO API (replace with real API if needed)
            try:
                # Example using Twinword or mock API
                # response = requests.post("https://api.twinword.com/api/seo-analyzer/", headers={...}, data={"text": user_text})
                # result = response.json()
                result = mock_seo_api(user_text)
            except:
                result = {"readability_score": None, "keywords": []}

            keywords = result.get("keywords", [])
            readability = result.get("readability_score", None)

            # Save to DB (optional)
            SEOAnalysis.objects.create(
                original_text=user_text,
                readability_score=readability,
                keywords=keywords
            )

            context.update({
                "original_text": user_text,
                "readability_score": readability,
                "keywords": keywords,
                "form": form
            })

            # If keyword insertion requested
            if 'insert_keyword' in request.POST:
                keyword_to_insert = request.POST.get('insert_keyword')
                updated_text = insert_keyword(user_text, keyword_to_insert)
                context["updated_text"] = updated_text
                context["inserted_keyword"] = keyword_to_insert

    return render(request, 'analyzer/index.html', context)

def index(request): 
    return render(request,'index.html')

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
    