import random, sys
import math

random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, virus, pop_size, vacc_percentage, initial_infected=1):
        self.population = []
        self.pop_size = pop_size
        self.virus = virus
        self.initial_infected = initial_infected
        self.vacc_percentage = vacc_percentage
        self.file_name = f"{virus_name}_simulation_pop_{pop_size}_vp_{vacc_percentage}_infected_{initial_infected}.txt"
        self.logger = Logger(self.file_name)
        self.newly_infected = []

        # Reset every timestep
        self.timestep_dead = 0
        self.timestep_infected = 0

        # Tallies for the simulation
        self.total_dead = 0
        self.total_infected = 0
        self.total_interactions = 0
        self.total_interactions_vacc = 0
        self.total_interactions_deaths = 0

        self.logger.write_metadata(self.pop_size, self.vacc_percentage, self.virus.name, self.virus.mortality_rate,
                                   self.virus.repro_rate)

    def _create_population(self, initial_infected):
        people = []
        people_infected = 0
        people_vaccinated = 0

        initial_vaccinated = math.floor(self.pop_size * self.vacc_percentage)
        self.total_interactions_vacc += initial_vaccinated
        while len(people) != self.pop_size:
            if people_infected != initial_infected:
                person = Person(len(people), False, self.virus)
                self.newly_infected.append(person.ID)
                people_infected += 1
            else:
                if initial_vaccinated != people_vaccinated:
                    person = Person(len(people), True)
                    people_vaccinated += 1
                else:
                    person = Person(len(people), False)
            people.append(person)
        return people

    def _simulation_should_continue(self):

        # Stop the simulation if there are no infected people left or everyone is dead
        infected_people = [person for person in self.population if person.infection and person.is_alive]
        if len(infected_people) == 0:
            return False
        return True

    def run(self):
        self.population = self._create_population(self.initial_infected)

        time_step_counter = 0
        should_continue = self._simulation_should_continue()
        while should_continue:
            time_step_counter += 1
            self.time_step()

            people_alive = len([person for person in self.population if person.is_alive])
            self.logger.log_time_step(time_step_counter, self.timestep_infected,
                                      self.timestep_dead, self.total_dead, people_alive, self.total_interactions_vacc)
            should_continue = self._simulation_should_continue()
        print(f"The simulation has ended after {time_step_counter} turns.")

        people_alive = len([person for person in self.population if person.is_alive])
        self.logger.append_end_results(self.pop_size, people_alive, self.total_dead, self.total_interactions_vacc,
                                       self.total_interactions_deaths, self.total_interactions)

    def time_step(self):
        # Reset current dead and infected for the timestep
        self.timestep_dead = 0
        self.timestep_infected = 0

        for person in self.population:
            if not person.is_alive or not person.infection:
                continue
            i = 0
            while i < 100:
                random_person = random.choice(self.population)
                if not random_person.is_alive:
                    continue
                self.interaction(person, random_person)
                i += 1

            # Check if the person has died after all interactions
            survival = person.check_survival()
            if not survival:
                self.timestep_dead += 1
                self.total_dead += 1
                self.total_interactions_deaths += 1
            else:
                self.total_interactions_vacc += 1
        self._infect_newly_infected()

    def interaction(self, person, random_person):
        assert person.is_alive == True
        assert random_person.is_alive == True

        if not random_person.is_vaccinated and not random_person.infection:
            self.total_interactions += 1
            if random.random() < self.virus.repro_rate:
                self.newly_infected.append(random_person.ID)

    def _infect_newly_infected(self):
        for sickPersonId in self.newly_infected:
            person = self.population[sickPersonId]
            person.infection = self.virus
            self.timestep_infected += 1
            self.total_infected += 1
        self.newly_infected = []


if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_num = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(virus, pop_size, vacc_percentage, initial_infected)
    sim.run()
