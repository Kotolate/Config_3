import unittest
import io
import sys
from contextlib import redirect_stdout
from translator import main
from translator import process_xml

class TestTranslator(unittest.TestCase):

    def test_constants(self):
        xml_input = """
        <config>
          <constant name="x">10</constant>
          <constant name="y">5.5</constant>
        </config>
        """
        expected_output = """x is 10.0
y is 5.5
"""
        self.assertEqual(process_xml(xml_input), expected_output)


    def test_dictionaries(self):
        xml_input = """
        <config>
          <dictionary name="myDict">
            <item key="a">100</item>
            <item key="b">200</item>
          </dictionary>
        </config>
        """
        expected_output = """{ myDict = {
  a = 100.0,
  b = 200.0,
}}
"""
        self.assertEqual(process_xml(xml_input), expected_output)


    def test_expressions(self):
        xml_input = """
        <config>
          <constant name="x">10</constant>
          <value>@[+ x 2]</value>
          <value>@[- x 3]</value>
          <value>@[+ x 2 pow(2)]</value>
        </config>
        """
        expected_output = """x is 10.0
12.0
7.0
144.0
"""
        self.assertEqual(process_xml(xml_input), expected_output)

    def test_comments(self):
        xml_input = """
        <config>
          /+ Это многострочный комментарий +/
          <constant name="x">10</constant>
          \ Это однострочный комментарий
        </config>
        """
        expected_output = """<# Это многострочный комментарий #>
<# Это однострочный комментарий #>
x is 10.0
"""
        self.assertEqual(process_xml(xml_input), expected_output)


    def test_invalid_name(self):
        xml_input = """
        <config>
          <constant name="123">10</constant> 
        </config>
        """
        with self.assertRaises(ValueError) as context:
            process_xml(xml_input)
        self.assertTrue("Некорректное имя константы" in str(context.exception))

if __name__ == '__main__':
    unittest.main()