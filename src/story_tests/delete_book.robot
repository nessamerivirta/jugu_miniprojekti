*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser

*** Test Cases ***
User can delete a book
    Create Book  robotdelete123  Test Author  Robot Test Book  2026  Test Publisher

    Get Text  body  *=  Robot Test Book

    Click  //tr[td[contains(text(), 'robotdelete123')]]//button[normalize-space()='Delete']
    Get Text  body  not contains  Robot Test Book