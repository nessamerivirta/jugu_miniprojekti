*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Database

*** Test Cases ***
At the start there are no references
    Go To  ${HOME_URL}
    Get Text  body  *=  No references added yet.

At the start there is add new book button
    Go To  ${HOME_URL}
    Get Text  body  *=  Add new book

After adding a book there is one book on the list
    Go To  ${HOME_URL}
    Click    text=Add new book
    Fill Text  [name="citation_key"]  TestAddBook
    Fill Text  [name="author"]  Tester
    Fill Text  [name="title"]  Add book
    Fill Text  [name="publishing_year"]  2026
    Fill Text  [name="publisher"]  Jess
    Click  button >> text=Create
    Get Text  body  *=  Number of references: 1

After adding a book its information is displayed
    Go To  ${HOME_URL}
    Click  text=Add new book
    Fill Text  [name="citation_key"]  TestDisplayInformation
    Fill Text  [name="author"]  Tester
    Fill Text  [name="title"]  Add book
    Fill Text  [name="publishing_year"]  2026
    Fill Text  [name="publisher"]  Jess
    Click    button >> text=Create
    Get Text  body  *=  TestDisplayInformation
    Get Text  body  *=  Tester
    Get Text  body  *=  Add book
    Get Text  body  *=  2026    

After adding two books there are two references
    Go To    ${HOME_URL}
    Click    text=Add new book
    Fill Text    [name="citation_key"]    TestTwoBooks
    Fill Text    [name="author"]    Tester
    Fill Text    [name="title"]    First book
    Fill Text    [name="publishing_year"]    2026
    Fill Text    [name="publisher"]    Jess
    Click    button >> text=Create

    Go To    ${HOME_URL}
    Click    text=Add new book
    Fill Text    [name="citation_key"]    Test2
    Fill Text    [name="author"]    Tester2
    Fill Text    [name="title"]    Second book
    Fill Text    [name="publishing_year"]    2025
    Fill Text    [name="publisher"]    Jess
    Click    button >> text=Create
    Get Text    body    *=    Number of references: 2

Add new book link opens the correct page
    Go To    ${HOME_URL}
    Click    text=Add new book
    Get Url    ==    ${HOME_URL}/new_book

User can open edit page
    Go To  ${HOME_URL}
    Click  text=Add new book
    Fill Text  [name="citation_key"]  robotedit
    Fill Text  [name="author"]  Test Author
    Fill Text  [name="title"]  Robot Test Book
    Fill Text  [name="publishing_year"]  2026
    Fill Text  [name="publisher"]  Test Publisher
    Click  button >> text=Create

    Get Text  body  *=  Number of references: 1
    Get Text  body  *=  Robot Test Book

    Click    button >> text=Edit
    Get Url  *=  ${HOME_URL}/edit_reference/1
    Get Text  body  *=  Edit reference
    Get Attribute  [name="citation_key"]  value  ==  robotedit
    Get Attribute  [name="author"]  value  ==  Test Author
    Get Attribute  [name="title"]  value  ==  Robot Test Book
    Get Attribute  [name="publishing_year"]  value  ==  2026
    Get Attribute  [name="publisher"]  value  ==  Test Publisher

User can edit reference
    Go To  ${HOME_URL}
    Click  text=Add new book
    Fill Text  [name="citation_key"]  roboteditbefore
    Fill Text  [name="author"]  Original Author
    Fill Text  [name="title"]  Original Book Title
    Fill Text  [name="publishing_year"]  2020
    Fill Text  [name="publisher"]  Original Publisher
    Click  button >> text=Create

    Click  button >> text=Edit
    Fill Text  [name="citation_key"]  roboteditafter
    Fill Text  [name="author"]  Updated Author
    Fill Text  [name="title"]  Updated Book Title
    Fill Text  [name="publishing_year"]  2024
    Fill Text  [name="publisher"]  Updated Publisher
    Click  button >> text=Save changes

    Get Url  ==  ${HOME_URL}/view_references
    Get Text  body  *=  roboteditafter
    Get Text  body  *=  Updated Author
    Get Text  body  *=  Updated Book Title
    Get Text  body  *=  2024
    Get Text  body  *=  Updated Publisher
    Get Text  body  not contains  roboteditbefore
    Get Text  body  not contains  Original Book Title

User can delete a reference
    Go To  ${HOME_URL}
    Click  text=Add new book
    Fill Text  [name="citation_key"]  robotdelete123
    Fill Text  [name="author"]  Test Author
    Fill Text  [name="title"]  Robot Test Book
    Fill Text  [name="publishing_year"]  2026
    Fill Text  [name="publisher"]  Test Publisher
    Click  button >> text=Create

    Get Text  body  *=  Number of references: 1
    Get Text  body  *=  Robot Test Book

    Click  //tr[td[contains(text(), 'robotdelete123')]]//button[normalize-space()='Delete']

    Get Text  body  not contains  Robot Test Book
    Get Text  body  *=  No references added yet.
