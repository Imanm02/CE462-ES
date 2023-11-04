from enum import Enum
import random

class MainState(Enum):
    S1 = 1
    S2 = 2
    S3 = 3

class SubState(Enum):
    S1 = 1
    S2 = 2
    S3 = 3

class Encubator:
    def __init__(self):
        self.PS = MainState.S1
        self.S2_PS = SubState.S1
        self.S3_PS = SubState.S1

    def process_temperature(self, T: int):
        if self.PS == MainState.S1:
            if T > 35:
                self.PS = MainState.S2
            elif T < 15:
                self.PS = MainState.S3

        elif self.PS == MainState.S2:
            if T < 25:
                self.PS = MainState.S1
            else:
                if self.S2_PS == SubState.S1:
                    if T > 40:
                        self.S2_PS = SubState.S2
                elif self.S2_PS == SubState.S2:
                    if T > 45:
                        self.S2_PS = SubState.S3
                    elif T < 35:
                        self.S2_PS = SubState.S1
                elif self.S2_PS == SubState.S3:
                    if T < 40:
                        self.S2_PS = SubState.S2

        elif self.PS == MainState.S3:
            if T > 30:
                self.PS = MainState.S1
            else:
                if self.S3_PS == SubState.S1:
                    if T < 5:
                        self.S3_PS = SubState.S2
                elif self.S3_PS == SubState.S2:
                    if T < -5:
                        self.S3_PS = SubState.S3
                    elif T > 15:
                        self.S3_PS = SubState.S1
                elif self.S3_PS == SubState.S3:
                    if T > 5:
                        self.S3_PS = SubState.S2

        else:
            raise Exception("Invalid Main State")

    def simulate(self, T: int):
        while True:
            prev_PS = self.PS
            prev_S2_PS = self.S2_PS
            prev_S3_PS = self.S3_PS
            self.process_temperature(T)
            if prev_PS == self.PS and prev_S2_PS == self.S2_PS and prev_S3_PS == self.S3_PS:
                break
        print(f'Temperature: {T}')
        print('State:', self.PS.name)
        if self.PS == MainState.S2:
            print('S2 State:', self.S2_PS.name)
        elif self.PS == MainState.S3:
            print('S3 State:', self.S3_PS.name)

if __name__ == '__main__':
    encubator = Encubator()
    Ts = [random.randint(-10, 50) for _ in range(100)]
    for T in Ts:
        encubator.simulate(T)