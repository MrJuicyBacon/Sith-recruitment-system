from django.shortcuts import render, redirect, HttpResponse
from django.db import transaction
from django.http import JsonResponse, HttpResponseNotFound
from django.core.mail import send_mail
from .models import Planet, Recruit, TestAssignment, Question, CollectedResponse, Sith
import re
import threading


class EmailThread(threading.Thread):
    def __init__(self, subject, message, sender, recipients,  *args, **kwargs):
        self.recipients = recipients
        self.sender = sender
        self.message = message
        self.subject = subject
        super(EmailThread, self).__init__(*args, **kwargs)

    def run(self):
        send_mail(self.subject, self.message, self.sender, self.recipients, fail_silently=True)


def index(request):
    return render(request, 'sith/index.html')


# Recruit section
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


# Sith section
def sith(request):
    sith_objects = Sith.objects.all()
    return render(request, 'sith/sith/sith.html', {'sith': sith_objects})


def sith_recruit(request, recruit_id):
    try:
        current_sith = Sith.objects.select_related('planet').get(pk=recruit_id)
    except Sith.DoesNotExist:
        return redirect('sith')

    current_sith_recruits_count = len(Recruit.objects.filter(assigned_sith=current_sith))

    if request.method == 'POST':
        if 'recruit_id' in request.POST:
            try:
                current_recruit = Recruit.objects.get(pk=request.POST['recruit_id'], assigned_sith=None)
            except Recruit.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Невозможно завербовать данного рекрута. '
                               'Возможно его уже завербовал кто-то другой.'
                })
            if current_sith_recruits_count >= 3:
                return JsonResponse({
                    'success': False,
                    'message': 'Вы достигли лимита рекрутов.'
                })
            current_recruit.assigned_sith = current_sith
            current_recruit.save()
            EmailThread(
                'Вам назначен Ситх',
                f'Вы приняты Рукой Тени.\nВаш Ситх - {current_sith.name}',
                'admin@sithrecruitment.com',
                [current_recruit.email]
            ).start()
            return JsonResponse({'success': True})
        else:
            return HttpResponseNotFound()

    recruits = Recruit.objects.filter(planet=current_sith.planet, assigned_sith=None)
    responses = CollectedResponse.objects.filter(recruit__in=recruits).select_related('recruit')

    responses_dict = {}
    for response in responses:
        if response.recruit.id in responses_dict:
            responses_dict[response.recruit.id].append({'question': response.question, 'answer': response.answer})
        else:
            responses_dict[response.recruit.id] = [{'question': response.question, 'answer': response.answer}]

    return render(request, 'sith/sith/recruit.html', {
        'planet': current_sith.planet,
        'recruits': recruits,
        'responses': responses_dict,
        'sith': current_sith,
        'limit': True if current_sith_recruits_count >= 3 else False,
    })
