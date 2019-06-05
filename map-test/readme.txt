Must replace chromedriver.exe with chrome driver corresponding to your version of chrome.

Must specify environment variable when running test pointing to the chrome driver: -ea -Dwebdriver.chrome.driver=/Users/benjamindcosta/schooldir/cmpe280-final-project/map-test/chromedriver

Run MapTest.java as junit test

May have to manually delete following user to get tests to run if user already exists:
user: TestUser
password: pass