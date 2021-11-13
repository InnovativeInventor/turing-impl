import json
import typer

class Turing:
    def __init__(self, filename: str = "description.json"):
        with open(filename) as f:
            self.description = json.load(f)

        self.head = self.description["start"]
        self.halt = self.description["halt"]
        self.state = self.description["state"]

    def __str__(self):
        if not len(self.state[1]):
            self.state[1].append(0)
        return "".join(map(str, self.state[0])) + self.head + "".join(map(str, self.state[1]))

    def run(self):
        while self.head != self.halt:
            yield self.step()

    def step(self):
        if not len(self.state[1]):
            self.state[1].append(0)
        bit = self.state[1][0]

        instruction = self.description[self.head][bit]
        self.state[1][0] = instruction[1]

        if instruction[2] == "R":
            self.state[0].append(self.state[1].pop(0))
        elif instruction[2] == "L":
            if not len(self.state[0]):
                self.state[0].append(0)
            self.state[1].insert(0, self.state[0].pop())
        elif instruction[2] == "N":
            pass
        else:
            raise ValueError("Invalid move")

        self.head = instruction[3]
        return str(self)


def main(filename: str = "description.json"):
    machine = Turing(filename)
    print(str(machine))
    for step in machine.run():
        print("\item", "$"+step+"$")

if __name__== "__main__":
    typer.run(main)
