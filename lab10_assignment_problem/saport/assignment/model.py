from __future__ import annotations
from dataclasses import dataclass
from typing import List
import numpy as np
import os
import copy


@dataclass
class Assignment:
    """
    Basic class to represent a solution to an assignment problem

    Attributes:
    -----------
    assigned_tasks: List[int]
        list with assigned tasks;
        assigned_tasks[2] == 1 means that worker with index 2 has been assigned to task 1
        value -1 means  that the worked has no task assigned
    objective: int
        total cost of the assignment
    """
    assigned_tasks: List[int]
    objective: int


@dataclass
class AssignmentProblem:
    """
    Basic class to represent an assignment problem

    Attributes:
    -----------
    name: string
        name of the problem
    costs: np.array
        cost array specific to the problem
    objective_is_min: bool
        whether we are looking to minimize costs or maximize profit

    Methods:
    --------
    n_tasks() -> int:
        number of tasks involved in the problem
    n_workers() -> int:
        number of workers involved in the problem

    Static Methods:
    ---------------
    from_file(path: str) -> AssignmentProblem:
        creates an instance based on the contents of a file at the given path;
        the format of the file is simple:

        <objective min/max> <n_workers> <m_tasks>
        <m costs separated by whitespace for the first worker>
        <m costs separated by whitespace for the second worker>
        ....
        <m costs separated by whitespace for the n'th worker>
    """
    name: str
    costs: np.array
    objective_is_min: bool

    def n_tasks(self):
        return self.costs.shape[1]

    def n_workers(self):
        return self.costs.shape[0]

    @staticmethod
    def from_file(path: str) -> AssignmentProblem:
        name = os.path.splitext(os.path.basename(path))[0]
        costs = None
        objective_min = True

        with open(path) as f:
            header = f.readline().split()
            objective_min = header[0] == "min"
            n_workers, n_tasks = tuple([int(v) for v in header[1:]])
            costs = np.zeros((n_workers, n_tasks), int)
            for (i, costs_row) in enumerate(f.readlines()):
                for (j, cost) in enumerate([int(v) for v in costs_row.split()]):
                    costs[i, j] = cost
        return AssignmentProblem(name, costs, objective_min)


@dataclass
class NormalizedAssignmentProblem:
    """
    Basic class to represent an assignment problem with a min objective and square cost matrix.
    It can be created from the normal max non-square problem

    Attributes:
    -----------
    costs: np.array
        a sqaure cost array specific to the problem
    original_problem: AssignmentProblem
        the original problem that has been used to create the instance

    Methods:
    --------
    size() -> int:
        size of the problem (number of workers/tasks)

    Static Methods:
    ---------------
    from_problem(problem: AssignmentProblem) -> NormalizedAssignmentProblem:
        creates an instance based on the possibly non-square, non-min assignment problem
    """
    costs: np.Array
    original_problem: AssignmentProblem

    def size(self) -> int:
        return self.costs.shape[0]

    @staticmethod
    def from_problem(problem: AssignmentProblem) -> NormalizedAssignmentProblem:

        # 1) create a square matrix capable to fit the orignal square matrix
        # 2) copy the original matrix into new one, inverting the costs if the original problem was a maximization problem
        # 3) extra rows and cols should always be filled with 0s
        # tip: inverting the costs means that you should subtract the original cost from the maximal cost in the matrix

        problem_copy = copy.deepcopy(problem)

        ilosc_wierszy = len(problem_copy.costs)
        ilosc_kolumn = len(problem_copy.costs[0])
        max_value = np.max(problem_copy.costs)

        if ilosc_wierszy > ilosc_kolumn:
            new_column = np.zeros((ilosc_wierszy, ilosc_wierszy - ilosc_kolumn))
            problem_copy.costs = np.append(problem_copy.costs, new_column, axis=1)
        elif ilosc_wierszy < ilosc_kolumn:
            new_row = np.zeros((ilosc_kolumn - ilosc_wierszy, ilosc_kolumn))
            problem_copy.costs = np.append(problem_copy.costs, new_row, axis=0)

        ilosc_wierszy = len(problem_copy.costs)
        ilosc_kolumn = len(problem_copy.costs[0])
        if not problem_copy.objective_is_min:
            for i in range(ilosc_wierszy):
                for j in range(ilosc_kolumn):
                    problem_copy.costs[i][j] = max_value - problem_copy.costs[i][j]

        return NormalizedAssignmentProblem(problem_copy.costs, problem)
