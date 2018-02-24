import pickle
import datetime

with open('test_pick', 'wb') as testpic:
    pickle.dump([str(datetime.datetime.now()), 0, 3], testpic)

with open('test_pick', 'rb') as testpic2:
    t = pickle.load(testpic2)

# t.extend(['cool', 24, 23])

with open('test_pick', '+ab') as testpic3:
    pickle.dump(['cool', 24, 23], testpic3)

with open('test_pick', 'rb') as re:
    t1 = pickle.load(re)

print(t1)
