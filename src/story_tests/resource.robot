*** Settings ***
# Library  Browser
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser

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

Reset Todos
    Go To  ${RESET_URL}

*** Test Cases ***
At start there are no todos
    Go To  ${HOME_URL}
    # Go To  ${SERVER}
    Get Title  ==  Todo app
    Get Text  body  *=  things still unfinished: 0

