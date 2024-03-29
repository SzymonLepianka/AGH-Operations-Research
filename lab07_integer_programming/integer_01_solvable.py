import logging
from saport.integer.model import Model


def run():
    model = Model("integer_01_solvable")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")

    model.add_constraint(x1 + x2 <= 6)
    model.add_constraint(5*x1 + 9*x2 <= 45)
    model.maximize(5 * x1 + 8 * x2)

    try:
        solution = model.solve()
    except:
        raise AssertionError(
            "This problem has a solution and your algorithm hasn't found it!")

    logging.info(solution)

    assert (solution.assignment == [
            0, 5]), "Your algorithm found an incorrect solution!"

    logging.info("Congratulations! This solution seems to be alright :)")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()
