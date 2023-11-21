

# TestMagic.py
import pytest
import os
from IPython.core.magic import (Magics, magics_class, register_line_magic, register_line_cell_magic)
from IPython import get_ipython

global TEST_COUNT
TEST_COUNT = 1


@magics_class
class TestMagic(Magics):

    @register_line_cell_magic
    def run_test(self, cell):
        print('Running tests ...')
        global TEST_COUNT
        test_file = OUTPUT_PATH + 'test_' + str(TEST_COUNT) + '.py'
        with open(test_file, 'w') as f:
            f.write(cell.format(**globals()))
            f.close()
        #pytest.main([test_file])
        #result = 'OK' if pytest.main(['--no-header','-vv', '-s', '-rA', '--color=yes', '--code-highlight=yes', test_file]) == 0 else 'FAIL'
        result = 'OK' if pytest.main(['--no-header','-q', '--color=yes', '--code-highlight=yes', test_file]) == 0 else 'FAIL'

        os.remove(test_file)
        # result test in file csv
        if not os.path.exists(OUTPUT_PATH + '../results_tests_' + str(TEST_COUNT) + '.csv'):
            with open(OUTPUT_PATH + '../results_tests_' + str(TEST_COUNT) + '.csv', 'w') as f:
                f.write('CARPETA,TEST\n')
                f.close()

        with open(OUTPUT_PATH + '../results_tests_' + str(TEST_COUNT) + '.csv', 'a') as f:
            f.write(CARPETA + ',' + result + '\n')
            f.close()

        print(f"Finish test: {result}")
        TEST_COUNT = TEST_COUNT + 1

    @register_line_cell_magic
    def save_test(self, cell):
        print('Saving tests ...')
        test_file = OUTPUT_PATH + 'test.py'
        with open(test_file, 'a') as f:
            f.write(cell.format(**globals()))
            f.close()
        print(f"Finish saving tests in {test_file}")

    @register_line_magic
    def run_all_tests(self):
        print('Running all tests ...')
        test_file = OUTPUT_PATH + 'test.py'
        pytest.main(['--no-header', '-vv', '-s', '-rA', '--color=yes', '--code-highlight=yes', test_file])
        print("Finish tests")
        os.remove(test_file)


def load_ipython_extension(ipython):
    ipython.register_magics(TestMagic)
