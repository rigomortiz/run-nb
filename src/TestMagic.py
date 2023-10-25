

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
    def test(self, cell):
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


def load_ipython_extension(ipython):
    ipython.register_magics(TestMagic)
