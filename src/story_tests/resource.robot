*** Settings ***
Library  Browser

*** Variables ***
${SERVER}     localhost:5001
${DELAY}      500ms
${HOME_URL}   http://${SERVER}
${RESET_URL}  http://${SERVER}/reset_db
${BROWSER}    chromium
${HEADLESS}   false

*** Keywords ***
Open And Configure Browser
    IF  $HEADLESS == 'true'
        New Browser  browser=${BROWSER}  headless=True
    ELSE
        New Browser  browser=${BROWSER}  headless=False  slowMo=${DELAY}
    END
    New Context
    New Page  about:blank

Reset Database
    Go To  ${RESET_URL}

Create Book
    [Arguments]  ${citation_key}  ${author}  ${title}  ${publishing_year}  ${publisher}
    Go To  ${HOME_URL}/new_book
    Fill Text  [name="citation_key"]  ${citation_key}
    Fill Text  [name="author"]  ${author}
    Fill Text  [name="title"]  ${title}
    Fill Text  [name="publishing_year"]  ${publishing_year}
    Fill Text  [name="publisher"]  ${publisher}
    Click  button >> text=Create

Create Inproceeding
    [Arguments]  ${citation_key}  ${author}  ${title}  ${publishing_year}  ${booktitle}
    Go To  ${HOME_URL}/new_inproceeding
    Fill Text  [name="citation_key"]  ${citation_key}
    Fill Text  [name="author"]  ${author}
    Fill Text  [name="title"]  ${title}
    Fill Text  [name="publishing_year"]  ${publishing_year}
    Fill Text  [name="booktitle"]  ${booktitle}
    Click  button >> text=Create
