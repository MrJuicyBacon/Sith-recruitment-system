from django.shortcuts import render, redirect, HttpResponse
from django.db import transaction
from .models import Planet, Recruit, TestAssignment, Question, CollectedResponse
import re


def index(request):
    return render(request, 'sith/index.html')


def recruit_signup(request):
    errors = None
    params = None
    if request.method == 'POST':
        email = request.POST.get('email', None)
        name = request.POST.get('name', None)
        planet_id = request.POST.get('planet', None)
        age = request.POST.get('age', None)
        if len(Recruit.objects.filter(email=str(email))):
            errors = ['Данный email уже зарегистрирован']
            params = {'email': email, 'name': name, 'planet_id': int(planet_id), 'age': age}
        elif name and planet_id and age and email:
            planet_object = Planet.objects.get(pk=int(planet_id))
            new_recruit = Recruit(
                name=str(name),
                planet=planet_object,
                age=int(age),
                email=str(email),
            )
            new_recruit.save()
            return redirect('recruit_trial', new_recruit.id)

    planets = Planet.objects.all()
    return render(request, 'sith/recruit/signup.html', {'planets': planets, 'errors': errors, 'params': params})


def recruit(request):
    return redirect('recruit_signup')


def recruit_trial(request, recruit_id):
    try:
        current_recruit = Recruit.objects.get(pk=recruit_id)
    except Recruit.DoesNotExist:
        return redirect('recruit_signup')

    if request.method == 'POST':
        question_ids = []
        responses = []
        for param in request.POST:
            match = re.match(r'radioResponseId(\d+)', param)
            if match:
                question_ids.append(int(match.group(1)))
                responses.append(True if request.POST[param] == '1' else False)
        questions = Question.objects.filter(id__in=question_ids)
        collected_responses = CollectedResponse.objects.filter(recruit=current_recruit,
                                                               question__in=questions).select_related('question')

        with transaction.atomic():
            for i, question in enumerate(questions):
                new_collected_response = None
                for collected_response in collected_responses:
                    if collected_response.question == question:
                        new_collected_response = collected_response
                        new_collected_response.answer = responses[i]
                        break
                if not new_collected_response:
                    new_collected_response = CollectedResponse(
                        recruit=current_recruit,
                        question=question,
                        answer=responses[i],
                    )
                new_collected_response.save()
        request.session['recruit_success'] = True
        return redirect('recruit_success')

    test_assignment = TestAssignment.objects.prefetch_related('questions').last()
    questions = test_assignment.questions.all()

    return render(request, 'sith/recruit/trial.html', {'recruit_name': str(current_recruit), 'questions': questions})


def recruit_success(request):
    if 'recruit_success' in request.session and request.session['recruit_success']:
        del request.session['recruit_success']
        return render(request, 'sith/recruit/success.html')
    else:
        return redirect('recruit_signup')
