from time import time
from queue import Queue


def enter_state(statE):

    def inp():
        for g in range(3):

            line_of_cube = list(input())

            for h in range(2):
                for element in line_of_cube:

                    if element == " " or element == ",":
                        line_of_cube.remove(element)

            for element in line_of_cube:
                state.append(int(element))

    state = []

    if statE == "start":
        print("Enter start state:")
        inp()

    elif statE == "goal":
        state = [1, 2, 3,
                 4, 5, 6,
                 7, 8, 0]

        print("Goal state is:")
        a = 0

        for x in range(3):

            for y in range(3):
                print(state[a], end="  ")
                a += 1
            print()

        print()

        change = input("Would you like to change it? (y/n) ")
        change = change.lower()

        if change == "y" or change == "yes":
            print("Enter goal state:")
            state.clear()
            inp()

        else:
            print("Default goal being used!")

    else:
        print("Wrong state!!")

    return state


class Puzzle:

    goal = enter_state("goal")
    num_of_instances = 0

    def __init__(self, state, parent, action):
        self.parent = parent
        self.state = state
        self.action = action

        Puzzle.num_of_instances += 1

    def goal_test(self):
        if self.state == self.goal:
            return True

        return False

    @staticmethod
    def find_legal_actions(i, j):
        legal_action = ["U", "D", "L", "R"]

        if i == 0:
            legal_action.remove("U")

        elif i == 2:
            legal_action.remove("D")

        if j == 0:
            legal_action.remove("L")

        elif j == 2:
            legal_action.remove("R")

        return legal_action

    def generate_child(self):
        children = []
        x = self.state.index(0)
        i = int(x / 3)
        j = int(x % 3)
        legal_actions = self.find_legal_actions(i, j)

        for action in legal_actions:
            new_state = self.state.copy()

            if action == "U":
                new_state[x], new_state[x - 3] = new_state[x - 3], new_state[x]

            elif action == "D":
                new_state[x], new_state[x + 3] = new_state[x + 3], new_state[x]

            elif action == "L":
                new_state[x], new_state[x - 1] = new_state[x - 1], new_state[x]

            elif action == "R":
                new_state[x], new_state[x + 1] = new_state[x + 1], new_state[x]

            children.append(Puzzle(new_state, self, action))

        return children

    def find_solution(self):

        solution = []
        solution.append(self.action)
        path = self

        while path.parent is not None:
            path = path.parent
            solution.append(path.action)

        solution = solution[:-1]
        solution.reverse()

        return solution


def breadth_first_search(initial_state):

    print("solving...")
    start_node = Puzzle(initial_state, None, None)

    if start_node.goal_test():
        return start_node.find_solution()

    q = Queue()
    q.put(start_node)
    explored = set()

    while not (q.empty()):
        node = q.get()
        explored.add(str(node.state))
        children = node.generate_child()

        for child in children:

            if str(child.state) not in explored:

                if child.goal_test():
                    return child.find_solution()

                q.put(child)

    return False


state = enter_state("start")
Puzzle.num_of_instances = 0
t0 = time()
bfs = breadth_first_search(state)

if not bfs:
    print("Not solvable!!")

else:
    t1 = time() - t0
    print("BFS                  :", bfs)
    print("Instances generated  :", Puzzle.num_of_instances)
    print("Time                 :", int(t1), "s")
    print("Exactly              :", t1, "s")
    print("Nodes                :", len(bfs))

print("something")
