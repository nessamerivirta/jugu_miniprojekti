*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***
User can delete an inproceeding
    Go To  ${HOME_URL}/new_inproceeding
    Fill Text  [name="citation_key"]  robotdelete123
    Fill Text  [name="author"]  Test Author
    Fill Text  [name="title"]  Robot Test Inproceeding
    Fill Text  [name="publishing_year"]  2026
    Fill Text  [name="booktitle"]  Test Book Title
    Click  button >> text=Create

    Get Text  body  *=  Robot Test Inproceeding

    Click  //tr[td[contains(text(), 'robotdelete123')]]//button[normalize-space()='Delete']
    Get Text  body  not contains  Robot Test Inproceeding

At the start there is add new inproceeding button
    Go To  ${HOME_URL}
    Get Text  body  *=  Add new inproceeding

After adding an inproceeding there is one inproceeding on the list
    Go To  ${HOME_URL}
    Click    text=Add new inproceeding
    Fill Text  [name="citation_key"]  Test1
    Fill Text  [name="author"]  Tester
    Fill Text  [name="title"]  Add inproceeding
    Fill Text  [name="publishing_year"]  2026
    Fill Text  [name="booktitle"]  Jess in paradise
    Click  button >> text=Create
    Get Text  body  *=  Number of references: 1
