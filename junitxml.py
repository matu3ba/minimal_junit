#!/bin/python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import sys

"""
Minimal juni xml creation based on the output of qtest:

<testsuite errors="0" failures="0" tests="6" name="SomeMessageUT">
  <properties>
    <property value="val" name="test system version"/>
    <property value="val" name="build system version"/>
  </properties>
  <testcase result="pass" name="initTestCase"/>
  <testcase result="pass" name="TestRequest"/>
  <testcase result="pass" name="TestResponse"/>
  <testcase result="pass" name="TestRestore"/>
  <testcase result="pass" name="TestRestoreAndCreateResponse"/>
  <testcase result="pass" name="cleanupTestCase"/>
  <system-err/>
</testsuite>

For now, the properties are not possible to construct.
Python 3.9 is required to have reliable working xml formatting.
"""

class Junit:
    """Class holding the xml and the counting data."""
    count: int = 0
    passed: int = 0
    failed: int = 0
    errors: int = 0
    skipped: int = 0
    tree: object # xml tree

    ## Note: Must use final() to write the errors, failures and test number tags on root.
    ## Then use writeFile() or use getXml().
    def __init__(self, testsuite_name: str):
        root_in = ET.Element(testsuite_name)
        self.tree = ET.ElementTree(root_in)
        root = self.tree.getroot()

    ## adds necessary tags for errors, failure and test sum to xml tree
    def final(self: object):
        root = self.tree.getroot()
        # assert root.tag == "testsuite", "Invalid root tag"
        testcases_query = root.findall("./testcase")

        if len(testcases_query) == 0:
            print("No test case executed, exiting..")
            sys.exit(1)
        for testcase in testcases_query:
            if testcase.attrib["result"] == "pass":
                self.passed += 1
                self.count += 1
                print("testcase passed")
            elif testcase.attrib["result"] == "failed":
                self.failed += 1
                self.count += 1
                print("testcase failed")
            if testcase.attrib["result"] == "error":
                self.errors += 1
                self.count += 1
                print("testcase errored")
            if testcase.attrib["result"] == "skip":
                self.errors += 1
                self.count += 1
                print("testcase skipped")

            # if testcase.attrib["skipped"]:
            #     self.skipped += 1
        root.set("errors", str(self.errors))
        root.set("failures", str(self.failed))
        root.set("tests", str(self.count))
        root.set("skipped", str(self.skipped))

    ## writes xml to file with optionally correct xml version flag
    def writeFile(self: object, filepath: str, use_bom: bool):
        with open(filepath, 'wb') as file:
            if (True == use_bom):
                file.write('<?xml version="1.0" encoding="UTF-8"?>\n\n'.encode('utf-8'))
            tree.write(file, encoding='utf-8')

    def getXml(self) -> object:
        return self.tree

    def getXmlRoot(self) -> object:
        return self.tree.getroot()

def addResultByReturnCode(root: object, name: str, return_code: int):
    result: str = "pass"
    if return_code != 0:
        result = "failure"
    if return_code == 128:
        result = "skip"
    addResult(root, name, result)

## result must be pass or failure
def addResult(root: object, name: str, result: str):
    assert result != "pass" or result != "failure" or result != "error", "Failure on result interpretation, exiting.."
    # assert root.tag == "testsuite", "Invalid root tag"
    attributes = {}
    attributes["name"] = name
    attributes["result"] = result
    subel = ET.SubElement(root, "testcase", attributes)

# def addProperty(value: str, name: str):
#     pass

def run_unittest():
    junit = Junit("testsuite_a")
    tree_root = junit.getXmlRoot()
    addResult(tree_root, "name1", "failed")
    addResult(tree_root, "name2", "pass")
    addResult(tree_root, "name3", "error")
    junit.final()
    tree_str = ET.tostring(tree_root, encoding='utf-8')
    print("tree_dump: ", tree_str)

# run_unittest()
