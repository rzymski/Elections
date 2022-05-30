from django.http import HttpResponse
from django.shortcuts import render, redirect
from wybory.models import *
from .forms import VoteForm
from .decorator import login_required
from django.utils import timezone


@login_required
def index(request):
    user = Osoba.objects.filter(pesel=request.session['UserID'])[0]
    elections = OsobaWybory.objects.order_by('wyboryId_id').filter(OsobaId_id=user.pk)[:10]
    return render(request, "index.html", {'user': user, 'elections': elections})


@login_required
def vote(request, election_id):
    election = Wybory.objects.get(pk=election_id)
    if timezone.now() < election.poczatekWyborow or election.koniecWyborow < timezone.now():
        return HttpResponse("To nie czas na glosowanie")

    # wszystkie osoby zwiazane z konkretnymi wyborami
    elections_people = OsobaWybory.objects.filter(wyboryId_id=election_id)

    # użytkownik
    user = elections_people.filter(OsobaId__pesel=request.session['UserID'])

    # jeśli użytkownika nie ma w wborach
    if not user:
        return HttpResponse("Nie masz prawa glosować w tych wyborach")

    if user[0].czyOddalGlos:
        return HttpResponse("Już zaglosowaleś w tych wyborach")

    candidates_in_elections = elections_people.filter(czyKandydat__exact=True)

    # krotka z id kandydata i jego nazwa do formularza glosowania
    candidates = [(k.OsobaId.id, f'{k.OsobaId.imie} {k.OsobaId.nazwisko}') for k in candidates_in_elections]

    if request.method == 'POST':
        form = VoteForm(candidates, request.POST)
        if form.is_valid():
            # utworzenie glosu i go zapisanie w bazei
            glos = Glos(wyboryId_id=election_id, kandydatOsobaID_id=form.cleaned_data['kandydaci'])
            glos.save()

            # oznaczenie ze urzytkownik oddal glos i zapisanie w bazie
            user[0].czyOddalGlos = True
            user[0].save()
            return redirect('index')
    else:
        form = VoteForm(candidates)

    return render(request, 'vote.html', {'form': form, 'election': election})


def election_results(request, election_id):
    election = Wybory.objects.get(pk=election_id)

    if election.koniecWyborow > timezone.now():
        return HttpResponse("Wybory sie jeszcze nie skonczyly")

    # liczba wszystkich glosow
    total_vote_count = Glos.objects.filter(wyboryId=election_id).count()

    #kandydaci
    candidates = OsobaWybory.objects.filter(wyboryId_id=election_id).filter(czyKandydat__exact=True)

    # lista slownikow z nazwa kanydata liczba glosow i procentem glosow
    candidates_and_votes = []
    for candidat in candidates:
        # liczba glosow na kandydata
        candidate_total_vote = Glos.objects.filter(kandydatOsobaID=candidat.OsobaId).count()

        candidates_and_votes.append({
            'name': f'{candidat.OsobaId.imie} {candidat.OsobaId.nazwisko}',
            'count': candidate_total_vote,
            'percent': candidate_total_vote / total_vote_count * 100
        })

    return render(request, 'electionResults.html', {
        'election': election,
        'candidates_vote_count': candidates_and_votes,
        'total_vote_count': total_vote_count
    })
