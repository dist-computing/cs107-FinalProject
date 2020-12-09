def run_tests():
    '''
    RUNS ALL TESTS IN THE TEST DIRECTORY
    '''
    exec(open('test_main.py').read())
    exec(open('test_utils.py').read())
    exec(open('test_function.py').read())
    exec(open('test_graddesc.py').read())
    exec(open('test_gmres.py').read())
    exec(open('test_newton.py').read())
run_tests()