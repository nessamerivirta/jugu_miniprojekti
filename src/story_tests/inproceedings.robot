*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***
User can delete an inproceeding
    Create Inproceeding  robotdelete123  Test Author  Robot Test Inproceeding  2026  Test Book Title

    Get Text  body  *=  Robot Test Inproceeding

    Click  //tr[td[contains(text(), 'robotdelete123')]]//button[normalize-space()='Delete']
    Get Text  body  not contains  Robot Test Inproceeding

At the start there is add new inproceeding button
    Go To  ${HOME_URL}
    Get Text  body  *=  Add new inproceeding

After adding an inproceeding there is one inproceeding on the list
    Create Inproceeding  Test1  Tester  Add inproceeding  2026  Jess in paradise
    Get Text  body  *=  Number of references: 1
