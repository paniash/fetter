from elec.read import read_csv
from elec.fit import linear_fit as fit
import numpy as np
import matplotlib.pyplot as plt


class TwoDevice:
    r"""
    Class describing a two-terminal device.
    """

    def __init__(self, filename, terminal):
        r"""
        terminal - user specified (source or drain)
        """
        self.terminal = terminal
        if not (
            self.terminal == "source"
            or self.terminal == "Source"
            or self.terminal == "drain"
            or self.terminal == "Drain"
        ):
            raise NameError("Argument must be either 'source' or 'drain'!")

        file = read_csv(filename)
        volt = [sub[0] for sub in file]
        id = [sub[1] for sub in file]
        iss = [sub[2] for sub in file]

        volt = list(map(float, volt))
        id = list(map(abs, list(map(float, id))))
        iss = list(map(abs, list(map(float, iss))))

        # Remove negative entries from `volt` and corresponding elements from `id` and `iss`
        indices_left = []
        ileft = 0
        for index, v in enumerate(volt):
            if v < 0:
                indices_left.append(index)
            else:
                break

        ileft = max(indices_left)
        volt = volt[ileft + 1 :]
        id = id[ileft + 1 :]
        iss = iss[ileft + 1 :]

        indices_right = []
        iright = 0
        for index, v in enumerate(volt[::-1]):
            if v < 0:
                indices_right.append(index)
            else:
                break

        iright = max(indices_right)
        volt = volt[: -iright - 1]
        iss = iss[: -iright - 1]
        id = id[: -iright - 1]

        # Separate into forward and backward data
        for index, val in enumerate(volt):
            if volt[index - 1] <= volt[index]:
                count = index

        self.vForward = volt[:count]
        self.isForward = iss[:count]
        self.idForward = id[:count]

        vBackward = volt[count:]
        isBackward = iss[count:]
        idBackward = id[count:]

        # Correct for nonlinear behaviour of backward characteristics
        def backCorrection(current: list, voltage: list):
            for index, val in enumerate(current):
                if current[index - 1] >= current[index]:
                    maxIndex = index

            current = current[:maxIndex]
            voltage = voltage[:maxIndex]

            return current, voltage

        self.isBackward, self.vsBackward = backCorrection(isBackward, volt)
        self.idBackward, self.vdBackward = backCorrection(idBackward, volt)

    def slope(self, voltage, current):
        a = fit(voltage, current)[1]
        return a

    def conductivity(self, direction):
        if self.terminal == "source" or self.terminal == "Source":
            if direction == "forward" or direction == "Forward":
                return self.slope(self.vForward, self.isForward)

            elif direction == "backward" or direction == "Backward":
                return self.slope(self.vsBackward, self.isBackward)

            else:
                raise NameError(
                    "String argument should be either 'forward' or 'backward'!"
                )

        elif self.terminal == "drain" or self.terminal == "Drain":
            if direction == "forward" or direction == "Forward":
                return self.slope(self.vForward, self.idForward)

            elif direction == "backward" or direction == "Backward":
                return self.slope(self.vdBackward, self.idBackward)

            else:
                raise NameError(
                    "String argument should be either 'forward' or 'backward'!"
                )

        else:
            raise NameError("String argument should be either 'source' or 'drain'!")

    def hysteresis(self):
        return abs(self.conductivity("forward") - self.conductivity("backward"))

    def plotter(self, direction):
        if self.terminal == "source" or self.terminal == "Source":
            if direction == "forward" or direction == "Forward":
                a = fit(self.vForward, self.isForward)[0]
                b = fit(self.vForward, self.isForward)[1]
                x = np.linspace(self.vForward[0], self.vForward[-1], 1000)
                y = a + b * x
                plt.plot(
                    x,
                    y,
                    "g",
                    label="Slope = {} S/m".format(self.conductivity(direction)),
                )
                plt.scatter(self.vForward, self.isForward, s=5, label="Datapoints")
                plt.xlabel("$I$ (volts)")
                plt.ylabel("$I_s$ (Amp)")
                # plt.title("Forward conductivity for source")
                plt.legend()

            elif direction == "backward" or direction == "Backward":
                a = fit(self.vsBackward, self.isBackward)[0]
                b = fit(self.vsBackward, self.isBackward)[1]
                x = np.linspace(self.vsBackward[0], self.vsBackward[-1], 1000)
                y = a + b * x
                plt.plot(
                    x,
                    y,
                    "g",
                    label="Slope = {} S/m".format(self.conductivity(direction)),
                )
                plt.scatter(self.vsBackward, self.isBackward, s=5, label="Datapoints")
                plt.xlabel("$V$ (volts)")
                plt.ylabel("$I_s$ (Amp)")
                # plt.title("Backward conductivity for source")
                plt.legend()

            else:
                raise NameError(
                    "String argument should be either 'forward' or 'backward'!"
                )

        elif self.terminal == "drain" or self.terminal == "Drain":
            if direction == "forward" or direction == "Forward":
                a = fit(self.vForward, self.idForward)[0]
                b = fit(self.vForward, self.idForward)[1]
                x = np.linspace(self.vForward[0], self.vForward[-1], 1000)
                y = a + b * x
                plt.plot(
                    x,
                    y,
                    "g",
                    label="Slope = {} S/m".format(self.conductivity(direction)),
                )
                plt.scatter(self.vForward, self.idForward, s=5, label="Datapoints")
                plt.xlabel("$V$ (volts)")
                plt.ylabel("$I_d$ (Amp)")
                # plt.title("Forward conductivity for drain")
                plt.legend()

            elif direction == "backward" or direction == "Backward":
                a = fit(self.vdBackward, self.idBackward)[0]
                b = fit(self.vdBackward, self.idBackward)[1]
                x = np.linspace(self.vdBackward[0], self.vdBackward[-1], 1000)
                y = a + b * x
                plt.plot(
                    x,
                    y,
                    "g",
                    label="Slope = {} S/m".format(self.conductivity(direction)),
                )
                plt.scatter(self.vdBackward, self.idBackward, s=5, label="Datapoints")
                plt.xlabel("$V$ (volts)")
                plt.ylabel("$I_d$ (Amp)")
                # plt.title("Backward conductivity for drain")
                plt.legend()

            else:
                raise NameError(
                    "String argument should be either 'forward' or 'backward'!"
                )

        else:
            raise NameError("String argument should be either 'source' or 'drain'!")
