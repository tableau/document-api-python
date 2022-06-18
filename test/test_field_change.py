import unittest
import os.path

from tableaudocumentapi import Datasource
from lxml import etree as ET


TEST_ASSET_DIR = os.path.join(
    os.path.dirname(__file__),
    'assets'
)
TEST_TDS_FILE = os.path.join(
    TEST_ASSET_DIR,
    'field_change_test.tds'
)
TEST_TDS_FILE_OUTPUT = os.path.join(
    TEST_ASSET_DIR,
    'field_change_test_output.tds'
)

MESSAGES = {
    'test_change_values1': 'Value has not changed when altering values for {}.',
    'test_change_values2': 'XML-Structure has not changed when altering values for {}.',
    'test_change_valuesFail1': 'Value has changed when submitting the wrong value for {}.',
    'test_change_valuesFail2': 'XML-Structure has changed when submitting the wrong value for {}.',
    'test_change_aliases1': 'XML-Structure has not changed when altering aliases for {}.',
    'test_change_aliases2': 'Values have not changed when altering aliases for {}.'

}

NEW_VALUES = {
    'caption': 'testcaption',
    'alias': 'testalias',
    'datatype': 'boolean',
    'role': 'measure',
    'type': 'ordinal'
}

WRONG_VALUES = {
    'datatype': 'boolani',
    'role': 'messhure',
    'type': 'gordinol'
}

ALIASES = {
    'one': 'two',
    'three': 'four',
    'five': 'six'
}


class TestFieldChange(unittest.TestCase):

    def setUp(self):
        self.tds = Datasource.from_file(TEST_TDS_FILE)

    def current_hash(self):
        """ Return a hash of the current state of the XML.

        Allows us to easily identify whether the underlying XML-structure
        of a TDS-file has actually changed. Avoids false positives if,
        for example, a fields value has changed but the XML hasn't.
        """
        return hash(ET.tostring(self.tds._datasourceTree.getroot()))

    def check_state_change(self, should_change, msg, field_name):
        """ Check whether the XML has changed and update the current state.

            Args:
                should_change: Whether the XML is supposed to have changed or not. Boolean.
                msg: The message to be displayed in an error case, as key for the MESSAGES dict. String.
                field_name: The field name that will be displayed in the error message. String.

            Returns:
                Nothing.
        """
        new_state = self.current_hash()
        compare_func = self.assertNotEqual if should_change else self.assertEqual
        compare_func(
            self.state,
            new_state,
            msg=MESSAGES[msg].format(field_name)
        )
        self.state = new_state

    def test_change_values(self):
        """ Test if the value changes of a field are reflected in the object and in the underlying XML structure.
        """
        field_to_test = "[amount]"
        self.state = self.current_hash()
        # change all fields
        for key, value in NEW_VALUES.items():
            setattr(self.tds.fields[field_to_test], key, value)
            # the new value must be reflected in the object
            self.assertEqual(
                getattr(self.tds.fields[field_to_test], key),
                value,
                msg=MESSAGES['test_change_values1'].format(key)
            )
            # the new value must be reflected in the xml
            self.check_state_change(True, 'test_change_values2', key)

    def test_change_values_fail(self):
        """ Test if the value changes of a field are rejected if the wrong arguments are passed.
        """
        field_to_test = "[amount]"
        self.state = self.current_hash()
        # change all fields
        for key, value in WRONG_VALUES.items():

            with self.assertRaises(ValueError):
                # this must fail
                setattr(self.tds.fields[field_to_test], key, value)

            # the new value must NOT be reflected in the object
            self.assertNotEqual(
                getattr(self.tds.fields[field_to_test], key),
                value,
                msg=MESSAGES['test_change_valuesFail1'].format(key)
            )
            # the new value must NOT be reflected in the xml
            self.check_state_change(False, 'test_change_valuesFail2', key)

    def test_remove_field(self):
        """ Test if a Field can be removed.
        """
        field_to_test = "[amount]"
        self.state = self.current_hash()
        # change all fields
        field = self.tds.fields["[amount]"]
        self.tds.remove_field(field)
        self.assertNotEqual(self.state, self.current_hash())

    def test_change_aliases(self):
        """ Test if the alias changes of a field are reflected in the object and in the underlying XML structure.
        """
        field_to_test = "[amount]"
        self.state = self.current_hash()
        # change all fields
        for key, value in ALIASES.items():
            self.tds.fields[field_to_test].add_alias(key, value)
            # the new value must be reflected in the xml
            self.check_state_change(True, 'test_change_aliases1', field_to_test)

        # check whether all fields of ALIASES have been applied
        self.assertEqual(
            set(self.tds.fields[field_to_test].aliases),
            set(ALIASES),
            msg=MESSAGES['test_change_aliases2'].format(field_to_test)
        )

    def test_calculation_base(self):
        """ Test if the initial state of calculated fields is correct.
        """
        # Demo data has 2 calculated fields at the start
        original_len = len(self.tds.calculations)

        # Can't write to calculation for not-calculated fields!
        self.tds.fields['[name]'].calculation = '1 * 2'
        self.assertEqual(len(self.tds.calculations), original_len + 1)
        self.tds.fields['[name]'].calculation = '2 * 3'
        self.assertEqual(len(self.tds.calculations), original_len + 1)
        self.tds.fields['[price]'].calculation = '2 * 3'
        self.assertEqual(len(self.tds.calculations), original_len + 2)

    def test_calculation_change(self):
        """ Test whether changing calculations of a field works.
        """
        self.state = self.current_hash()
        new_calc = '33 * 44'
        fld_name = '[Calculation_357754699576291328]'
        self.tds.calculations[fld_name].calculation = new_calc

        # Check object representation
        self.assertEqual(self.tds.calculations[fld_name].calculation, new_calc)

        # Check XML representation
        new_state = self.current_hash()
        self.assertNotEqual(self.state, new_state)

    def test_calculation_new(self):
        """ Test if creating a new calculation works.
        """
        args = 'TestCalc', '12*34', 'integer', 'measure', 'quantitative', 'False'
        original_len = len(self.tds.calculations)
        self.tds.add_calculation(*args)
        self.assertEqual(len(self.tds.calculations), original_len + 1)

    def test_calculation_remove(self):
        """ Test if deleting a calculation works.
        """
        args = 'TestCalc2', '12*34', 'integer', 'measure', 'quantitative', 'True'

        original_len = len(self.tds.calculations)
        calc = self.tds.add_calculation(*args)
        self.assertEqual(len(self.tds.calculations), original_len + 1)

        self.tds.remove_field(calc)
        self.assertEqual(len(self.tds.calculations), original_len)

    def tearDown(self):
        """ Test if the file can be saved.
        Output file will be ignored by git, but can be used to verify the results.
        """
        self.tds.save_as(TEST_TDS_FILE_OUTPUT)


if __name__ == '__main__':
    unittest.main()
