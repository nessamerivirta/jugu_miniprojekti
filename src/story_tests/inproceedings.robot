*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***
User can delete an inproceeding
    Create Inproceeding  robotdelete123  Test Author  Robot Test Inproceeding  2026  Test Book Title
    Get Text  body  *=  Robot Test Inproceeding

    Delete Reference  robotdelete123
    Get Text  body  not contains  Robot Test Inproceeding

After adding an inproceeding there is one inproceeding on the list
    Create Inproceeding  Test1  Tester  Add inproceeding  2026  Jess in paradise
    Get Text  body  *=  Number of references: 1
