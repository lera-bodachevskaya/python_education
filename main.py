# import cProfile
import numpy as np

from pyinstrument import Profiler

import detector_factory
# from detector import Detector

if __name__ == '__main__':
    # text = 'Hello how are You 1-3 444-95 :) bye \u0364 \u1C00'
    # text = 'Otec matka      msyn @gmail.com'

    f = open("example.txt", "r")
    text = f.read()
    res_list = []

    for i in range(1000):
        profiler = Profiler()
        profiler.start()

        result = detector_factory.detect_langs(text)
        # print(result)

        profiler.stop()
        # print(profiler.output_text(unicode=True, color=True, show_all=True))

        s = profiler.frame_records
        sum = 0
        for item in s:
            sum += item[1]
        res_list.append(sum)

    del res_list[0]
    res = np.sum(res_list) / len(res_list)
    print(res)
    # python -m cProfile -o myLog.profile main.py
    # a = 1
