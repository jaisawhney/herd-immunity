class Virus(object):
    def __init__(self, name, repro_rate, mortality_rate):
        self.name = name
        self.repro_rate = repro_rate
        self.mortality_rate = mortality_rate


def test_virus_instantiation():
    virus = Virus("Flu", 0.9, 0.053)
    assert virus.name == "Flu"
    assert virus.repro_rate == 0.9
    assert virus.mortality_rate == 0.053
