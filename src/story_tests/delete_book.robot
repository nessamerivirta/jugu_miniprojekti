*** Settings ***
Resource         resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser

*** Test Cases ***
User can delete a book
    Go To  ${HOME_URL}/new_reference
    Select Options By  [name="type"]   value  book
    Fill Text  [name="citation_key"]  robotdelete123
    Fill Text  [name="author"]  Test Author
    Fill Text  [name="title"]  Robot Test Book
    Fill Text  [name="publishing_year"]  2026
    Fill Text  [name="publisher"]  Test Publisher
    Click  button >> text=Create

    Get Text  body  *=  Robot Test Book

    Click  //tr[td[contains(text(), 'robotdelete123')]]//button[normalize-space()='Delete']
    Get Text  body  not contains  Robot Test Book