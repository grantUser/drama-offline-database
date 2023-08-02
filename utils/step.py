class Step:
    def __init__(self) -> None:
        """
        Initializes the Step class.
        """
        pass

    def get_step(self) -> str:
        """
        Read the contents of the 'step.txt' file and return the data as a string.

        Returns:
            str: The contents of the 'step.txt' file as a string.
        """
        with open("step.txt") as step:
            return step.read()

    def set_step(self, data: str) -> None:
        """
        Write the provided data to the 'step.txt' file.

        Args:
            data (str): The data to be written to the 'step.txt' file.
        """
        with open("step.txt", "w") as step:
            step.write(data)


step = Step()
