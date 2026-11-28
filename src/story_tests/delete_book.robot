*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***
User can delete a book
    Create Book  robotdelete123  Test Author  Robot Test Book  2026  Test Publisher
    Get Text  body  *=  Robot Test Book

    Delete Reference  robotdelete123
    Get Text  body  not contains  Robot Test Book