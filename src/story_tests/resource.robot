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

Open And Fill Reference Form
    [Arguments]  ${type}  ${citation_key}  ${author}  ${title}  ${publishing_year}
    Go To  ${HOME_URL}
    Click  text=Add new reference
    Select Options By  [name="type"]  value  ${type}
    Fill Text  [name="citation_key"]  ${citation_key}
    Fill Text  [name="author"]  ${author}
    Fill Text  [name="title"]  ${title}
    Fill Text  [name="publishing_year"]  ${publishing_year}

Create Book
    [Arguments]  ${citation_key}  ${author}  ${title}  ${publishing_year}  ${publisher}
    Open And Fill Reference Form  book  ${citation_key}  ${author}  ${title}  ${publishing_year}
    Fill Text  [name="publisher"]  ${publisher}
    Click  button >> text=Create

Create Article
    [Arguments]  ${citation_key}  ${author}  ${title}  ${publishing_year}  ${journal}  ${volume}  ${pages}
    Open And Fill Reference Form  article  ${citation_key}  ${author}  ${title}  ${publishing_year}
    Fill Text  [name="journal"]  ${journal}
    Fill Text  [name="volume"]  ${volume}
    Fill Text  [name="pages"]  ${pages}
    Click  button >> text=Create

Create Inproceeding
    [Arguments]  ${citation_key}  ${author}  ${title}  ${publishing_year}  ${booktitle}
    Open And Fill Reference Form  inproceedings  ${citation_key}  ${author}  ${title}  ${publishing_year}
    Fill Text  [name="booktitle"]  ${booktitle}
    Click  button >> text=Create

Delete Reference
    [Arguments]  ${citation_key}
    Click  //tr[td[contains(text(), '${citation_key}')]]//button[normalize-space()='Delete']
