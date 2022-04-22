from fetter.read import read_csv
from fetter.fit import linear_fit as fit
import numpy as np
import matplotlib.pyplot as plt


class TwoDevice:
    r"""
    string - user specified (source or drain)
    """

    def __init__(self, filename, string):
        self.string = string
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

    def conductivity(self, forORback):
        if self.string == "source" or self.string == "Source":
            if forORback == "forward" or forORback == "Forward":
                return self.slope(self.vForward, self.isForward)

            elif forORback == "backward" or forORback == "Backward":
                return self.slope(self.vsBackward, self.isBackward)

            else:
                raise NameError(
                    "String argument should be either 'forward' or 'backward'!"
                )

        elif self.string == "drain" or self.string == "Drain":
            if forORback == "forward" or forORback == "Forward":
                return self.slope(self.vForward, self.idForward)

            elif forORback == "backward" or forORback == "Backward":
                return self.slope(self.vdBackward, self.idBackward)

            else:
                raise NameError(
                    "String argument should be either 'forward' or 'backward'!"
                )

        else:
            raise NameError("String argument should be either 'source' or 'drain'!")

    def hysteresis(self):
        return abs(self.conductivity("forward") - self.conductivity("backward"))

    def plotter(self, forORback):
        if self.string == "source" or self.string == "Source":
            if forORback == "forward" or forORback == "Forward":
                a = fit(self.vForward, self.isForward)[0]
                b = fit(self.vForward, self.isForward)[1]
                x = np.linspace(self.vForward[0], self.vForward[-1], 1000)
                y = a + b * x
                plt.plot(
                    x,
                    y,
                    "g",
                    label="Slope = {} S/m".format(self.conductivity(forORback)),
                )
                plt.scatter(self.vForward, self.isForward, s=5, label="Datapoints")
                plt.xlabel("Forward voltage (volts)")
                plt.ylabel("Forward source current (Amp)")
                plt.legend()

            elif forORback == "backward" or forORback == "Backward":
                a = fit(self.vsBackward, self.isBackward)[0]
                b = fit(self.vsBackward, self.isBackward)[1]
                x = np.linspace(self.vsBackward[0], self.vsBackward[-1], 1000)
                y = a + b * x
                plt.plot(
                    x,
                    y,
                    "g",
                    label="Slope = {} S/m".format(self.conductivity(forORback)),
                )
                plt.scatter(self.vsBackward, self.isBackward, s=5, label="Datapoints")
                plt.xlabel("Backward voltage (volts)")
                plt.ylabel("Backward source current (Amp)")
                plt.legend()

            else:
                raise NameError(
                    "String argument should be either 'forward' or 'backward'!"
                )

        elif self.string == "drain" or self.string == "Drain":
            if forORback == "forward" or forORback == "Forward":
                a = fit(self.vForward, self.idForward)[0]
                b = fit(self.vForward, self.idForward)[1]
                x = np.linspace(self.vForward[0], self.vForward[-1], 1000)
                y = a + b * x
                plt.plot(
                    x,
                    y,
                    "g",
                    label="Slope = {} S/m".format(self.conductivity(forORback)),
                )
                plt.scatter(self.vForward, self.idForward, s=5, label="Datapoints")
                plt.xlabel("Forward voltage (volts)")
                plt.ylabel("Forward drain current (Amp)")
                plt.legend()

            elif forORback == "backward" or forORback == "Backward":
                a = fit(self.vdBackward, self.idBackward)[0]
                b = fit(self.vdBackward, self.idBackward)[1]
                x = np.linspace(self.vdBackward[0], self.vdBackward[-1], 1000)
                y = a + b * x
                plt.plot(
                    x,
                    y,
                    "g",
                    label="Slope = {} S/m".format(self.conductivity(forORback)),
                )
                plt.scatter(self.vdBackward, self.isBackward, s=5, label="Datapoints")
                plt.xlabel("Backward voltage (volts)")
                plt.ylabel("Backward drain current (Amp)")
                plt.legend()

            else:
                raise NameError(
                    "String argument should be either 'forward' or 'backward'!"
                )

        else:
            raise NameError("String argument should be either 'source' or 'drain'!")


# # read file
# file = read_csv("p2.txt")
# x1 = [sub[0] for sub in file]  # store columns in lists
# x2 = [sub[1] for sub in file]
# x3 = [sub[2] for sub in file]

# # convert string elements into float
# vDv = list(map(float, x1))
# iD = list(map(abs, list(map(float, x2))))
# iS = list(map(abs, list(map(float, x3))))

# # Remove negative entries of vDv and corresponding elements from iD and iS
# indices_left = []
# ileft = 0
# for index, v in enumerate(vDv):
#     if v < 0:
#         indices_left.append(index)
#     else:
#         break

# ileft = max(indices_left)
# vDv = vDv[ileft + 1 :]
# iD = iD[ileft + 1 :]
# iS = iS[ileft + 1 :]

# indices_right = []
# iright = 0
# for index, v in enumerate(vDv[::-1]):
#     if v < 0:
#         indices_right.append(index)
#     else:
#         break

# iright = max(indices_right)
# vDv = vDv[: -iright - 1]
# iS = iS[: -iright - 1]
# iD = iD[: -iright - 1]

# # Separate into forward and backward data
# for i in range(len(vDv)):
#     if vDv[i - 1] <= vDv[i]:
#         count = i

# vForward = vDv[:count]
# iSForward = iS[:count]
# iDForward = iD[:count]

# vBackward = vDv[count:]
# iSBackward = iS[count:]
# iDBackward = iD[count:]

# # Correct for nonlinear behaviour of backward characteristics
# def backCorrection(current: list, voltage: list):
#     for i in range(len(current)):
#         if current[i - 1] >= current[i]:
#             maxIndex = i

#     current = current[:maxIndex]
#     voltage = voltage[:maxIndex]

#     return current, voltage


# iSBackward, vSBack = backCorrection(iSBackward, vBackward)
# iDBackward, vDBack = backCorrection(iDBackward, vBackward)


# #%%
# a, b, delA2, delB2 = fit(vDBack, iDBackward)
# x = np.linspace(vDBack[0], vDBack[-1], 1000)
# y = a + b * x
# plt.plot(x, y, label="fit")
# plt.scatter(vDBack, iDBackward, s=5, label="data")
# plt.legend()
# plt.show()

# a, b, delA2, delB2 = fit(vForward, iDForward)
# x = np.linspace(vForward[0], vForward[-1], 1000)
# y = a + b * x
# plt.plot(x, y, label="fit")
# plt.scatter(vForward, iDForward, s=5, label="data")
# plt.legend()
# plt.show()
