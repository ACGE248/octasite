from django.shortcuts import render
from django.views.generic import ListView
from octapply.models import Professor, Program, University
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def home(request):
    allprog = Program.objects.all().count()
    alluni = University.objects.all().count()
    allprof = Professor.objects.all().count()
    return render(request, "octapply/home.html", {'programs': allprog ,'universities': alluni ,'professors': allprof ,})

def program(request , slug):
    program = Program.objects.get(slug=slug)
    return render(request,'octapply/program.html' , {'program': program ,})

def programs(request , slug):
    uni = University.objects.get(slug=slug)
    allprograms = Program.objects.all()
    programs = allprograms.filter(university = uni)
    return render(request,'octapply/programs.html' , {'programs': programs ,})

def professor(request , slug):
    professor = Professor.objects.get(slug=slug)
    return render(request,'octapply/professor.html' , {'professor': professor ,})

def professors(request , slug):
    uni = University.objects.get(slug=slug)
    allprofessors = Professor.objects.all()
    professors = allprofessors.filter(university = uni)
    return render(request,'octapply/professors.html' , {'professors': professors ,})

def university(request , slug):
    university = University.objects.get(slug=slug)
    return render(request,'octapply/university.html' , {'university': university ,})

class UniversityList(ListView):
    model = University

class ProgramList(ListView):
    model = Program
    
class ProfessorList(ListView):
    model = Professor    
    paginate_by=10
    def get_queryset(self):
        search=self.request.GET.get("search")
        university=self.request.GET.get("university")
        country=self.request.GET.get("country")
        department=self.request.GET.get("department")
        adsearch=Professor.objects.all()
        
        if search:
            adsearch=Professor.objects.filter(Q(name__icontains=search))
            #order=order.filter(Q(user=False) & Q(type='1')).order_by(order_by)
        elif search is None:
            adsearch=Professor.objects.all()
        else:
            adsearch=Professor.objects.filter(Q(university=university))

        return adsearch
POSTS_PER_PAGE = 2

def uni_list_view(request):
    universitylist, search = _search_posts(request)
    #countries = universitylist.filter().order_by('country').values('country').distinct()
    context = {"universitylist": universitylist, "search": search, "is_search_view": False}
    return render(request, "octapply/university_list.html", context)


def uni_list_search_view(request):
    universitylist, search = _search_posts(request)
    context = {"universitylist": universitylist, "search": search, "is_search_view": True}
    return render(request, "octapply/university_list_search_results.html", context)


def _search_posts(request):
    search = request.GET.get("search")
    country = request.GET.get("country")
    rank = request.GET.get("rank")
    page = request.GET.get("page")

    universitylist = University.objects.all()
    if search is None:
        universitylist    
    if search:
        universitylist = universitylist.filter(title__icontains=search)
    if country and country!="Choose Country":
        universitylist = universitylist.filter(country=country)
    if rank and rank!="Rank":
        universitylist = universitylist.filter(ranking__lte=rank)
    paginator = Paginator(universitylist, POSTS_PER_PAGE)
    try:
        universitylist = paginator.page(page)
    except PageNotAnInteger:
        universitylist = paginator.page(1)
    except EmptyPage:
        universitylist = paginator.page(paginator.num_pages)

    return universitylist, search or ""