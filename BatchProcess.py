from mininet.net import Mininet
from mininet.util import dumpNodeConnections
import numpy as np

import time
import random

class BatchProcessing:
    @staticmethod
    def smallestLoad(carga):
        multiplier = 1000
        if(carga[-1] == 'M'):
            multiplier *= 1000
        elif(carga[-1] == 'G'):
            multiplier *= 1000 * 1000
        return int(carga[:-1]) * multiplier

    @staticmethod
    def largestLoad(carga):
        multiplier = 1000
        if(carga[-1] == 'M'):
            multiplier *= 1000
        elif(carga[-1] == 'G'):
            multiplier *= 1000 * 1000
        return 1/(int(carga[:-1]) * multiplier)


    @classmethod
    def sjf(cls, cargas):
        cargas.sort(key = cls.smallestLoad)

    @classmethod
    def ljf(cls, cargas):
        cargas.sort(key = cls.largestLoad)
