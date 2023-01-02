## Minimal juni xml creation based on the output of qtest:

```
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
```

For now, the properties are not possible to construct.
Python 3.9 is required to have reliable working xml formatting.

For usage, see run_unittest().
