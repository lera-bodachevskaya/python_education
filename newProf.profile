
  _     ._   __/__   _ _  _  _ _/_   Recorded: 11:39:47  Samples:  285
 /_//_/// /_\ / //_// / //_'/ //     Duration: 0.354     CPU time: 0.828
/   _/                      v3.2.0

Program: main.py

0.353 <module>  main.py:1
├─ 0.283 detect_langs  detector_factory.py:136
│  ├─ 0.255 init_factory  detector_factory.py:122
│  │  └─ 0.255 load_profile  detector_factory.py:36
│  │     ├─ 0.184 add_profile  detector_factory.py:81
│  │     │  ├─ 0.176 [self]  
│  │     │  ├─ 0.004 len  <built-in>:0
│  │     │  └─ 0.004 defaultdict.get  <built-in>:0
│  │     ├─ 0.064 load  json/__init__.py:274
│  │     │     [6 frames hidden]  json, codecs
│  │     │        0.005 decode  codecs.py:319
│  │     │        └─ 0.005 utf_8_decode  <built-in>:0
│  │     └─ 0.005 [self]  
│  └─ 0.027 get_probabilities  detector.py:143
│     └─ 0.027 _detect_block  detector.py:148
│        └─ 0.022 _extract_ngrams  detector.py:185
│           ├─ 0.012 add_char  utils/ngram.py:31
│           │  ├─ 0.006 [self]  
│           │  └─ 0.004 normalize  utils/ngram.py:64
│           └─ 0.009 [self]  
├─ 0.064 <module>  numpy/__init__.py:1
│     [105 frames hidden]  numpy, pathlib, urllib, ntpath, pickl...
└─ 0.006 <module>  detector_factory.py:1
   └─ 0.005 <module>  detector.py:1

