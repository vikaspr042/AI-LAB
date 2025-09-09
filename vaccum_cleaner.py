class ReflexVacuumCleaner:
    def __init__(self, location, environment):
        self.location = location
        self.environment = environment

    def display(self):
        print(f"Vacuum at {self.location} | Rooms: {self.environment}")

    def reflex_agent(self):
        if self.environment[self.location] == "Dirty":
            return "Suck"
        return "Right" if self.location == "A" else "Left"

    def execute(self, action):
        if action == "Suck":
            print(f"Suck at {self.location}")
            self.environment[self.location] = "Clean"
        else:
            new_location = "B" if action == "Right" else "A"
            print(f"Move {action} to {new_location}")
            self.location = new_location

    def run(self, steps=6):
        for _ in range(steps):
            self.display()
            action = self.reflex_agent()
            self.execute(action)
        self.display()
        print("Finished.")


def get_input(prompt, valid_options):
    while True:
        response = input(prompt).strip().upper()
        if response in valid_options:
            return response
        print(f"Invalid input. Please enter one of {valid_options}.")


def main():
    print("Reflex Vacuum Cleaner Simulation")

    location = get_input("Enter initial location (A or B): ", {"A", "B"})
    env = {}
    for room in ["A", "B"]:
        env[room] = get_input(f"Is room {room} Dirty or Clean? ", {"DIRTY", "CLEAN"}).capitalize()

    vacuum = ReflexVacuumCleaner(location, env)
    steps = int(input("Enter number of steps to run the simulation: "))
    vacuum.run(steps)


if __name__ == "__main__":
    main()

