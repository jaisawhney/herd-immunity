import math
import random
import sys

from matplotlib import pyplot as plt

from person import Person
from logger import Logger
from virus import Virus

random.seed(42)


class Simulation(object):
    def __init__(self, virus, population_size, vaccination_percentage, initial_infected=1):
        self.population = []
        self.newly_infected = []

        # Simulation Variables
        self.virus = virus
        self.population_size = population_size
        self.vaccination_percentage = vaccination_percentage
        self.initial_infected = initial_infected

        # Logger
        self.folder_name = f"./results/{virus.name}_simulation_pop_{population_size}_vp_{vaccination_percentage}_infected_{initial_infected}"
        self.logger = Logger(self.folder_name)

        # Reset every timestep
        self.timestep_dead = 0
        self.timestep_infected = 0

        # Tallies for the simulation
        self.total_dead = 0
        self.total_infected = 0
        self.total_interactions = 0
        self.total_interactions_vaccinated = 0
        self.total_vaccinated = 0
        self.total_interactions_deaths = 0

        self.logger.write_metadata(self.population_size, self.vaccination_percentage, self.virus.name,
                                   self.virus.mortality_rate,
                                   self.virus.reproduction_rate)

    def _create_population(self, initial_infected):
        people = []
        people_infected = 0
        people_vaccinated = 0

        initial_vaccinated = math.floor(self.population_size * self.vaccination_percentage)
        self.total_vaccinated += initial_vaccinated

        while len(people) != self.population_size:
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
        infected_people = [person for person in self.population if person.virus and person.is_alive]
        if len(infected_people) == 0:
            return False
        return True

    def run(self):
        self.population = self._create_population(self.initial_infected)

        time_step_counter = 0
        should_continue = self._simulation_should_continue()
        while should_continue:
            time_step_counter += 1
            print(f"Running timestep {time_step_counter}")
            self.time_step()

            people_alive = len([person for person in self.population if person.is_alive])
            self.logger.log_time_step(time_step_counter, self.timestep_infected,
                                      self.timestep_dead, self.total_dead, people_alive,
                                      self.total_vaccinated)
            should_continue = self._simulation_should_continue()
        print(f"The simulation has ended after {time_step_counter} turns.")

        people_alive = len([person for person in self.population if person.is_alive])
        self.logger.append_end_results(self.population_size, people_alive, self.total_dead, self.total_vaccinated,
                                       self.total_interactions_vaccinated, self.total_interactions_deaths,
                                       self.total_interactions, self.total_infected)
        self._display_results()

    def time_step(self):
        # Reset current dead and infected for the timestep
        self.timestep_dead = 0
        self.timestep_infected = 0
        for person in self.population:
            if person.is_alive and person.virus:
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
                    self.total_interactions_vaccinated += 1
                self.total_vaccinated += 1
        self._infect_newly_infected()

    def interaction(self, person, random_person):
        assert person.is_alive == True
        assert random_person.is_alive == True

        if not random_person.is_vaccinated and not random_person.virus:
            self.total_interactions += 1
            if random.random() < self.virus.reproduction_rate:
                self.newly_infected.append(random_person.ID)

    def _infect_newly_infected(self):
        for sickPersonId in self.newly_infected:
            person = self.population[sickPersonId]
            person.virus = self.virus
            self.timestep_infected += 1
            self.total_infected += 1
        self.newly_infected = []

    def _display_results(self):
        # Display results
        alive_no_vaccine = len([person for person in self.population if person.is_alive and not person.is_vaccinated])

        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis("equal")
        slices = ["Non-immune Living", "Dead", "Vaccinated"]
        results = [alive_no_vaccine, self.total_dead, self.total_vaccinated]
        ax.pie(results, labels=slices, autopct="%1.2f%%")
        plt.savefig(f"{self.folder_name}/plot.png")
        plt.show()


if __name__ == "__main__":
    try:
        params = sys.argv[1:]
        virus_name = str(params[0])
        repro_num = float(params[1])
        mortality_rate = float(params[2])

        pop_size = int(params[3])
        vaccination_percentage = float(params[4])

        if len(params) == 6:
            initial_infected = int(params[5])
        else:
            initial_infected = 1

        virus = Virus(virus_name, repro_num, mortality_rate)
        sim = Simulation(virus, pop_size, vaccination_percentage, initial_infected)
        sim.run()
    except KeyboardInterrupt:
        pass
