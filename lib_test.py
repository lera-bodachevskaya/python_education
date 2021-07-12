import numpy as np

from langdetect import detect_langs
from pyinstrument import Profiler


if __name__ == '__main__':
    # text = 'Hello how are You 1-3 444-95 :) bye \u0364 \u1C00'
    # text = 'Otec matka      msyn @gmail.com'

    f = open("example.txt", "r")
    text = f.read()
    res_list = []

    for i in range(1000):
        profiler = Profiler()
        profiler.start()

        result = detect_langs(text)
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

# 0.0304 -> 0.279
