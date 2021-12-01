import random

from virus import Virus

random.seed(42)


class Person(object):
    def __init__(self, _id, is_vaccinated=False, virus=None):
        self.ID = _id
        self.is_alive = True
        self.is_vaccinated = is_vaccinated
        self.virus = virus

    def check_survival(self):
        if random.random() < self.virus.mortality_rate:
            self.is_alive = False
            return False
        else:
            self.is_vaccinated = True
            self.virus = None
            return True


def test_vacc_person_instantiation():
    person = Person(1, True)
    assert person.ID == 1
    assert person.is_alive is True
    assert person.is_vaccinated is True
    assert person.virus is None


def test_not_vacc_person_instantiation():
    person = Person(2, False)
    assert person.ID == 2
    assert person.is_alive is True
    assert person.is_vaccinated is False
    assert person.virus is None


def test_sick_person_instantiation():
    virus = Virus("Flu", 0.9, 0.053)
    person = Person(3, False, virus)
    assert person.ID == 3
    assert person.is_alive is True
    assert person.is_vaccinated is False
    assert person.virus == virus


def test_did_survive_infection():
    virus = Virus("Flu", 0.9, 0.053)
    person = Person(4, False, virus)

    assert person.ID == 4
    assert person.is_alive is True
    assert person.is_vaccinated is False
    assert person.virus == virus

    survived = person.check_survival()
    if survived:
        assert person.is_alive is True
        assert person.is_vaccinated is True
    else:
        assert person.is_alive is False
        assert person.is_vaccinated is False
