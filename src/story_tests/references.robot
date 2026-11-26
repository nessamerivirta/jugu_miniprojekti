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
    Create Book  TestAddBook  Tester  Add book  2026  Jess
    Get Text  body  *=  Number of references: 1

After adding a book its information is displayed
    Create Book  TestDisplayInformation  Tester  Add book  2026  Jess
    Get Text  body  *=  TestDisplayInformation
    Get Text  body  *=  Tester
    Get Text  body  *=  Add book
    Get Text  body  *=  2026    

After adding two books there are two references
    Create Book  TestTwoBooks  Tester  First book  2026  Jess
    Create Book  Test2  Tester2  Second book  2025  Jess
    Get Text    body    *=    Number of references: 2

Add new book link opens the correct page
    Go To    ${HOME_URL}
    Click    text=Add new book
    Get Url    ==    ${HOME_URL}/new_book

User can open edit page
    Create Book  robotedit  Test Author  Robot Test Book  2026  Test Publisher

    Get Text  body  *=  Number of references: 1
    Get Text  body  *=  Robot Test Book

    Click    button >> text=Edit
    Get Url  *=  ${HOME_URL}/edit_reference/1
    Get Text  body  *=  Edit Robot Test Book
    Get Attribute  [name="citation_key"]  value  ==  robotedit
    Get Attribute  [name="author"]  value  ==  Test Author
    Get Attribute  [name="title"]  value  ==  Robot Test Book
    Get Attribute  [name="publishing_year"]  value  ==  2026
    Get Attribute  [name="publisher"]  value  ==  Test Publisher

User can open edit page and see book title
    Create Book  robotOpenEdit  Original Author  Original Book Title  2020  Original Publisher

    Click  button >> text=Edit
    Get Text  body  *=  Edit Original Book Title

User can edit book reference
    Create Book  roboteditbefore  Original Author  Original Book Title  2020  Original Publisher

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

User can edit article reference
    Go To  ${HOME_URL}
    Click  text=Add new article
    Fill Text  [name="citation_key"]  roboteditbefore
    Fill Text  [name="author"]  Original Author
    Fill Text  [name="title"]  Original Article Title
    Fill Text  [name="publishing_year"]  2020
    Fill Text  [name="journal"]  Original Journal
    Fill Text  [name="volume"]  Original Volume
    Fill Text  [name="pages"]  Original Pages


    Click  button >> text=Create

    Click  button >> text=Edit
    Fill Text  [name="citation_key"]  roboteditafter
    Fill Text  [name="author"]  Updated Author
    Fill Text  [name="title"]  Updated Article Title
    Fill Text  [name="publishing_year"]  2024
    Fill Text  [name="journal"]  Updated Journal
    Fill Text  [name="volume"]  Updated Volume
    Fill Text  [name="pages"]  Updated Pages
    Click  button >> text=Save changes

    Get Url  ==  ${HOME_URL}/view_references
    Get Text  body  *=  roboteditafter
    Get Text  body  *=  Updated Author
    Get Text  body  *=  Updated Article Title
    Get Text  body  *=  2024
    Get Text  body  *=  Updated Journal
    Get Text  body  *=  Updated Volume
    Get Text  body  not contains  roboteditbefore
    Get Text  body  not contains  Original Article Title

User can edit inproceeding reference
    Create Inproceeding  roboteditproceeding  Original Author  Original Proceedings Title  2020  Original Book Title

    Click  button >> text=Edit
    Get Attribute  [name="proc_year"]  value  ==  2020
    Get Attribute  [name="booktitle"]  value  ==  Original Book Title
    Fill Text  [name="citation_key"]  roboteditedproceeding
    Fill Text  [name="author"]  Updated Author
    Fill Text  [name="title"]  Updated Proceedings Title
    Fill Text  [name="publishing_year"]  2024
    Fill Text  [name="proc_year"]  2024
    Fill Text  [name="booktitle"]  Updated Book Title
    Click  button >> text=Save changes

    Get Url  ==  ${HOME_URL}/view_references
    Get Text  body  *=  roboteditedproceeding
    Get Text  body  *=  Updated Author
    Get Text  body  *=  Updated Proceedings Title
    Get Text  body  *=  Updated Book Title
    Get Text  body  *=  2024
    Get Text  body  not contains  roboteditproceeding
    Get Text  body  not contains  Original Proceedings Title
    Get Text  body  not contains  Original Book Title


User can delete a reference
    Create Book  robotdelete123  Test Author  Robot Test Book  2026  Test Publisher

    Get Text  body  *=  Number of references: 1
    Get Text  body  *=  Robot Test Book

    Click  //tr[td[contains(text(), 'robotdelete123')]]//button[normalize-space()='Delete']

    Get Text  body  not contains  Robot Test Book
    Get Text  body  *=  No references added yet.
