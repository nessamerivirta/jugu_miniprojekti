*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Todos

*** Test Cases ***
At start there are no todos
    Go To  ${HOME_URL}
    Get Title  ==  Todo app
    Get Text  body  *=  things still unfinished: 0

After adding a todo, there is one
    Go To  ${HOME_URL}
    Click  text=Create new todo
    Fill Text  [name="content"]  Buy milk
    Click  button >> text=Create
    Get Text  body  *=  things still unfinished: 1
    Get Text  body  *=  Buy milk

After adding two todos and marking one done, there is one unfinished
    Go To  ${HOME_URL}
    Click  text=Create new todo
    Fill Text  [name="content"]  Buy milk
    Click  button >> text=Create
    Click  text=Create new todo
    Fill Text  [name="content"]  Clean house
    Click  button >> text=Create
    Click  //li[div[contains(text(), 'Buy milk')]]/form/button
    Get Text  body  *=  things still unfinished: 1
    Get Text  body  *=  Buy milk, done
