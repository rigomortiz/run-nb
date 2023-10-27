

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
        pytest.main(['--no-header','-vv', '-s', '-rA', '--color=yes', '--code-highlight=yes', test_file])
        print("Finish tests")
        os.remove(test_file)
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
