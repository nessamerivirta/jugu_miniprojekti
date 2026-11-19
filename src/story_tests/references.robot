*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***
At the start there are no references
    Go To  ${HOME_URL}
    Get Title  ==  References
    Get Text  body  *=  No references added yet.

At the start there is add new book button
    Go To  ${HOME_URL}
    Get Text  body  *=  Add new book

After adding a book there is one book on the list
    Go To  ${HOME_URL}
    Click    text=Add new book
    Fill Text  [name="citation_key"]  Test1
    Fill Text  [name="author"]  Tester
    Fill Text  [name="title"]  Add book
    Fill Text  [name="publishing_year"]  2026
    Fill Text  [name="publisher"]  Jess
    Click  button >> text=Create





    