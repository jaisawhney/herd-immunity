from logger import Logger
from datetime import date
from shutil import rmtree


def test_metadata():
    file_path = "./results/test"
    logger = Logger(file_path)

    logger.write_metadata(10000, 0.5, "Some virus", 0.25, 0.1)
    file = open(f"{file_path}/results.txt", "r")
    file_content = file.read()
    assert file_content == (
        f'Running simulation for virus "Some virus" on {date.today()}'
        "\nPopulation: 10000, Vaccination Percentage: 0.5, "
        "Mortality Rate: 0.25, Reproduction Rate 0.1\n\n")
    rmtree(file_path)


def test_time_step():
    file_path = "./results/test"
    logger = Logger(file_path)
    logger.log_time_step(5, 2500, 200, 5231, 4769, 400)
    file = open(f"{file_path}/results.txt", "r")
    file_content = file.read()
    assert file_content == ("Time step 5 has ended:\n"
                            "•    # Infected: 2500\n"
                            "•    # Dead: 200\n"
                            "•    Population State:\n"
                            "     ◦    Total Living: 4769\n"
                            "     ◦    Total Dead: 5231\n"
                            "     ◦    Total Vaccinated: 400\n\n")
    rmtree(file_path)


def test_end_msg():
    file_path = "./results/test"
    logger = Logger(file_path)
    logger.append_end_results(10000, 2500, 7500, 2500, 2500,
                              7500, 80000, 10000)
    file = open(f"{file_path}/results.txt", "r")
    file_content = file.read()
    assert file_content == ("Simulation Ended\n"
                            "•    Total Living: 2500\n"
                            "•    Total Dead: 7500\n"
                            "•    Total infected: 10000\n"
                            "•    # Vaccinations: 2500\n"
                            "•    Interactions:\n"
                            "     ◦    Total: 80000\n"
                            "     ◦    # Resulted in death: 7500\n"
                            "     ◦    # Resulted in vaccinations: 2500\n"
                            "•    Reason for end: No infections remaining")
    rmtree(file_path)
