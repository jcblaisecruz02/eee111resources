import ast, inspect

def print_header(fn):
    print("###\n### Running tests on {}\n###".format(fn.__name__))
    
def print_exp(out, expected, a, *b, end='\n'):
    args = str(a)
    if len(b) > 0: 
        for arg in b: args += (' ' + str(arg))
    print("Input:", args, "| Expected:", expected, "| Output:", out, end=end)

def test_has_return(fn, a, *b):
    try:
        out = fn(a, *b)
        assert out is not None
        print('The function', fn.__name__, 'returns a value.')
        return True
    except:
        print("RETURN FAIL. The function",  fn.__name__, "did not have a return value.")
        return False
    finally:
        pass

def test_nocall_1arg(fn, a):
    try:
        out = fn(a)
        call_names = [c.func.id for c in ast.walk(ast.parse(inspect.getsource(fn))) if isinstance(c, ast.Call)]
        assert len(call_names) == 0
        print('The function', fn.__name__, 'does not use any imported or external functions.')
        return True
    except:
        print('EXTERNAL FUNCTION CHECK FAIL. The function', fn.__name__, 'uses an externally written function (possibly from a library).')
        return False
    finally:
        pass

def test_is_type(fn, expected, a, *b):
    try:
        out = fn(a, *b)
        assert type(out) is expected
        print('The function', fn.__name__, 'has the correct return data type.', end=' | ')
        return True
    except:
        print("RETURN TYPE CHECK FAIL. The function does not output the expected type.", end=' | ')
        return False
    finally:
        print_exp(type(out), expected, type(a))

def test_fn_1arg(fn, expected, a):
    try:
        out = fn(a)
        assert out == expected
        print('Test case passed.', end=' | ')
        return True
    except:
        print('TEST CASE FAILED.', end=' | ')
        return False
    finally:
        print_exp(out, expected, a)

def test_fn_2arg(fn, expected, a, b):
    try:
        out = fn(a, b)
        assert out == expected
        print('Test case passed.', end=' | ')
        return True
    except:
        print('TEST FAILED.', end=' | ')
        return False
    finally:
        print_exp(out, expected, a, b)

def test_precision_1arg(fn, expected, a):
    try:
        out = fn(a)
        assert abs(out - expected) <= 10**(-10)
        print('Precision test case passed.', end=' | ')
        return True
    except:
        print('PRECISION TEST CASE FAILED.', end=' | ')
        return False
    finally:
        print_exp(out, expected, a)

def run_tests(tests, point=1):
    award = point

    # If one of the test cases failed
    if False in tests: 
        award = 0
        print('One or more test cases have failed. Zero points awarded.\n')

    else:
        print('All test cases passed. Awarded {} point(s)\n'.format(point))

    return award

def score_workbook_week2(is_divisible_by_4, collatz, num_factors, factorial, is_prime, greatest_common_factor, square_root):
    points = 0

    # Is Divisible by 4
    print_header(is_divisible_by_4)
    tests = [
        test_has_return(is_divisible_by_4, 4),
        test_is_type(is_divisible_by_4, bool, 4),
        test_fn_1arg(is_divisible_by_4, True, 4),
        test_fn_1arg(is_divisible_by_4, False, 5)
    ]
    points += run_tests(tests, point=1)

    # Collatz
    print_header(collatz)
    tests = [
        test_has_return(collatz, 24),
        test_is_type(collatz, int,  4),
        test_fn_1arg(collatz, 12, 24),
        test_fn_1arg(collatz, 40, 13),
        test_fn_1arg(collatz, 406, 135)
    ]
    points += run_tests(tests, point=1)

    # Num Factors
    print_header(num_factors)
    tests = [
        test_has_return(num_factors, 1),
        test_is_type(num_factors, int,  1),
        test_fn_1arg(num_factors, 5, 16),
        test_fn_1arg(num_factors, 8, 88),
        test_fn_1arg(num_factors, 4, 91)
    ]
    points += run_tests(tests, point=1)

    # Factorial
    print_header(factorial)
    tests = [
        test_has_return(factorial, 1),
        test_is_type(factorial, int,  1),
        test_fn_1arg(factorial, 1, 0),
        test_fn_1arg(factorial, 1, 1),
        test_fn_1arg(factorial, 720, 6),
        test_fn_1arg(factorial, 3628800, 10)
    ]
    points += run_tests(tests, point=1)

    # Is Prime
    print_header(is_prime)
    tests = [
        test_has_return(is_prime, 1),
        test_is_type(is_prime, bool, 1),
        test_fn_1arg(is_prime, False, 0),
        test_fn_1arg(is_prime, False, 1),
        test_fn_1arg(is_prime, False, -1),
        test_fn_1arg(is_prime, False, -16),
        test_fn_1arg(is_prime, True, -13),
        test_fn_1arg(is_prime, False, 16),
        test_fn_1arg(is_prime, True, 13),
        test_fn_1arg(is_prime, False, 19836)
    ]
    points += run_tests(tests, point=3)

    # Greatest Common Factor
    print_header(greatest_common_factor)
    tests = [
        test_has_return(greatest_common_factor, 1, 1),
        test_is_type(greatest_common_factor, int, 1, 1),
        test_fn_2arg(greatest_common_factor, 12, 24, 36),
        test_fn_2arg(greatest_common_factor, 1, 26, 55),
        test_fn_2arg(greatest_common_factor, 26, 182, 52),
    ]
    points += run_tests(tests, point=3)

    # Square Root
    from math import sqrt as test_sqrt
    print_header(square_root)
    tests = [
        test_has_return(square_root, 1),
        test_nocall_1arg(square_root, 1),
        test_is_type(square_root, float, 1),
        test_is_type(square_root, float, 1),
        test_fn_1arg(square_root, 5.0, 25),
        test_fn_1arg(square_root, 6.0, 36),
    ]
    tests += [test_precision_1arg(square_root, test_sqrt(i), i) for i in range(10, 101, 7)]
    del test_sqrt

    points += run_tests(tests, point=5)

    print('Your final score is {} point(s)'.format(points))
