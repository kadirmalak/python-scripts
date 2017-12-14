import unittest
import inspect
import re

def run_tests(clazz):
    
    def is_test_method(name):
        return re.search('^test_*', name) is not None
    
    funcs = inspect.getmembers(clazz, predicate=inspect.isfunction)
    tests = [f for f in funcs if is_test_method(f[0])]
    problems = []

    for test in tests:
        instance = clazz(methodName=test[0])
        results = instance.run()
        
        if len(results.errors) == 0 and len(results.failures) == 0:
            print("%s passed..." % test[0])
        else:
            print("%s failed..." % test[0])
            problems.extend([f[1] for f in results.failures])
            problems.extend([e[1] for e in results.errors])
        
    if len(problems) > 0:
        print()
        for problem in problems:
            print(problem)
        raise Exception('%d test(s) failed...' % len(problems))
        
class SomeTests(unittest.TestCase):
    
    def __init__(self, *args, **kwargs):
        super(SomeTests, self).__init__(*args, **kwargs)
        
    def test1(self):
        self.assertEqual('foo', 'foo')
     
    def test2(self):
        self.assertEqual('foo', 'bar')

run_tests(SomeTests)

#test1 passed...
#test2 failed...

#Traceback (most recent call last):
#  File "<ipython-input-8-c2e141ec5648>", line 10, in test2
#    self.assertEqual('foo', 'bar')
#AssertionError: 'foo' != 'bar'
#- foo
#+ bar
