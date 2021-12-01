import os

from datetime import date


class Logger(object):
    def __init__(self, folder_name):
        self.folder_name = folder_name

        try:
            os.mkdir(self.folder_name)
        except OSError as error:
            # Folder already exists - ignore
            pass

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate,
                       reproduction_rate):
        with open(f"{self.folder_name}/results.txt", "w") as file:
            file.write(
                f'Running simulation for virus "{virus_name}" on {date.today()}'
                f"\nPopulation: {pop_size}, Vaccination Percentage: {vacc_percentage}, "
                f"Mortality Rate: {mortality_rate}, Reproduction Rate {reproduction_rate}\n\n")

    def log_time_step(self, time_step_number, num_infected, num_dead, total_dead, total_living, total_vaccinated):
        with open(f"{self.folder_name}/results.txt", "a") as file:
            file.write(f"Time step {time_step_number} has ended:\n"
                       f"•    # Infected: {num_infected}\n"
                       f"•    # Dead: {num_dead}\n"
                       f"•    Population State:\n"
                       f"     ◦    Total Living: {total_living}\n"
                       f"     ◦    Total Dead: {total_dead}\n"
                       f"     ◦    Total Vaccinated: {total_vaccinated}\n\n")

    def append_end_results(self, pop_size, total_alive, total_dead, total_vaccinated, interactions_vaccinated,
                           interactions_deaths,
                           total_interactions, total_infected):
        with open(f"{self.folder_name}/results.txt", "a") as file:
            reason = "Population Dead" if pop_size == total_dead else "No infections remaining"

            file.write(f"Simulation Ended\n"
                       f"•    Total Living: {total_alive}\n"
                       f"•    Total Dead: {total_dead}\n"
                       f"•    Total infected: {total_infected}\n"
                       f"•    # Vaccinations: {total_vaccinated}\n"
                       f"•    Interactions:\n"
                       f"     ◦    Total: {total_interactions}\n"
                       f"     ◦    # Resulted in death: {interactions_deaths}\n"
                       f"     ◦    # Resulted in vaccinations: {interactions_vaccinated}\n"
                       f"•    Reason for end: {reason}")
