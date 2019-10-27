from django.template.defaulttags import register


@register.filter(name='get_questions_by_recruit_id')
def get_questions_by_recruit_id(questions, id):
    return questions.get(id)
