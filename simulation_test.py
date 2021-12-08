from simulation import Simulation
from virus import Virus
from shutil import rmtree


def test_init():
    virus = Virus("Flu", 0.9, 0.053)
    sim = Simulation(virus, 50000, 0.2, 10)

    assert sim.virus == virus
    assert sim.population_size == 50000
    assert sim.vaccination_percentage == 0.2
    assert sim.initial_infected == 10

    assert sim.folder_name == "./results/Flu_simulation_pop_50000_vp_0.2_infected_10"
    rmtree(sim.folder_name)


def test_population():
    virus = Virus("Flu", 0.9, 0.053)
    sim = Simulation(virus, 50000, 0.2, 10)
    population = sim._create_population(10)

    assert len(population) == 50000
    assert sim.initial_infected == 10
    assert sim.total_vaccinated == 10000
    rmtree(sim.folder_name)
