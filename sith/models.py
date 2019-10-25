from django.db import models


def get_short_name(name, length=25):
    return name if len(str(name)) <= length else name[:length] + '...'


class Planet(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return get_short_name(self.name)


class Sith(models.Model):
    name = models.CharField(max_length=1000)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "sith"

    def __str__(self):
        return get_short_name(self.name)


class Recruit(models.Model):
    name = models.CharField(max_length=1000)
    planet = models.ForeignKey(Planet, on_delete=models.CASCADE)
    age = models.IntegerField()
    email = models.CharField(max_length=100)
    assigned_sith = models.ForeignKey(Sith, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return get_short_name(self.name)


class Question(models.Model):
    text = models.CharField(max_length=1000)

    def __str__(self):
        return get_short_name(self.text, 100)


class TestAssignment(models.Model):
    unique_code = models.CharField(max_length=1000)
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return get_short_name(self.unique_code, 100)


class CollectedResponse(models.Model):
    recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.BooleanField()

