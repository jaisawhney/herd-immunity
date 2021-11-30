import random
# random.seed(42)
from virus import Virus


class Person(object):
    def __init__(self, _id, is_vaccinated=False, infection=None):
        self.ID = _id  # int
        self.is_alive = True  # boolean
        self.is_vaccinated = is_vaccinated  # boolean
        self.infection = infection  # Virus object or None

    def check_survival(self):
        if random.random() < self.infection.mortality_rate:
            self.is_alive = False
            return False
        else:
            self.is_vaccinated = True
            self.infection = None
            return True


def test_vacc_person_instantiation():
    # create some people to test if our init method works as expected
    person = Person(1, True)
    assert person.ID == 1
    assert person.is_alive is True
    assert person.is_vaccinated is True
    assert person.infection is None


def test_not_vacc_person_instantiation():
    person = Person(2, False)
    assert person.ID == 2
    assert person.is_alive is True
    assert person.is_vaccinated is False
    assert person.infection is None


def test_sick_person_instantiation():
    virus = Virus("Flu", 0.9, 0.053)
    person = Person(3, False, virus)
    assert person.ID == 3
    assert person.is_alive is True
    assert person.is_vaccinated is False
    assert person.infection == virus


def test_did_survive_infection():
    virus = Virus("Flu", 0.9, 0.053)
    person = Person(4, False, virus)

    assert person.ID == 4
    assert person.is_alive is True
    assert person.is_vaccinated is False
    assert person.infection == virus

    survived = person.check_survival()
    if survived:
        assert person.is_alive is True
        assert person.is_vaccinated is True
    else:
        assert person.is_alive is False
        assert person.is_vaccinated is False
