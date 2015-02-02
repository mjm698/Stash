var userData = { "user": { 
                "name" : "maxwell",
                "id" : "maxwell.mosley@gmail.com",
                "previousStash" : "1",
                "stashes" : [
                    { "name" : "My Stash", 
                      "id" : "1", 
                      "users" : [
                        { "name" : "maxwell",
                          "id" : "maxwell.mosley@gmail.com" }
                      ]
                    },
                    { "name" : "Our Stash", 
                      "id" : "2", 
                      "users" : [
                        { "name" : "maxwell",
                          "id" : "maxwell.mosley@gmail.com" },
                        { "name" : "ishita",
                          "id" : "ishitaaloni@gmail.com" }
                      ]
                    },
                    { "name" : "Poopy Stash", 
                      "id" : "3", 
                      "users" : [
                        { "name" : "maxwell",
                          "id" : "maxwell.mosley@gmail.com" },
                        { "name" : "ishita",
                          "id" : "ishitaaloni@gmail.com" },
                        { "name" : "morgan",
                          "id" : "morganneiman@gmail.com" }
                      ]
                    }
                ] } };

var fakeStashData = { "stashList" : [
    { "name" : "My Stash",
      "id" : "1",
      "content" : [
        {"link" : "http://i.imgur.com/kOGWKFw.jpg",
         "user" : { "name" : "maxwell", "id" : "maxwell.mosley@gmail.com" },
         "time" : "2015-01-31T18:47:13.839Z",
         "status" : "viewed",
         "comments" : [ 
            { "user" : { "name" : "maxwell", "id" : "maxwell.mosley@gmail.com" },
              "text" : "This is so funny",
              "time" : "2015-01-31T18:47:13.839Z" 
            }
         ] 
        },
        {"link" : "http://i.imgur.com/dR3XRDr.jpg",
         "user" : { "name" : "maxwell", "id" : "maxwell.mosley@gmail.com" },
         "time" : "2015-01-31T18:52:34.695Z",
         "status" : "viewed",
         "comments" : [ 
            { "user" : { "name" : "maxwell", "id" : "maxwell.mosley@gmail.com" },
              "text" : "This is so cute...",
              "time" : "2015-01-31T18:52:34.695Z"
            }
         ]
        }
      ] },
    { "name" : "Our Stash",
      "id" : "2",
      "content" : [
        {"link" : "http://i.imgur.com/kOGWKFw.jpg",
         "user" : { "name" : "ishita", "id" : "ishitaaloni@gmail.com" },
         "time" : "2015-01-31T18:47:13.839Z",
         "status" : "viewed",
         "comments" : [ 
            { "user" : { "name" : "maxwell", "id" : "maxwell.mosley@gmail.com" },
              "text" : "This is so funny",
              "time" : "2015-01-31T18:47:13.839Z" 
            }
         ] 
        },
        {"link" : "http://i.imgur.com/dR3XRDr.jpg",
         "user" : { "name" : "maxwell", "id" : "maxwell.mosley@gmail.com" },
         "time" : "2015-01-31T18:52:34.695Z",
         "status" : "viewed",
         "comments" : [ 
            { "user" : { "name" : "maxwell", "id" : "maxwell.mosley@gmail.com" },
              "text" : "This is so cute...",
              "time" : "2015-01-31T18:52:34.695Z"
            }
         ]
        }
      ] },
    { "name" : "Poopy Stash",
      "id" : "3",
      "content" : [
        {"link" : "http://i.imgur.com/kOGWKFw.jpg",
         "user" : { "name" : "morgan", "id" : "poopy.pi@gmail.com" },
         "time" : "2015-01-31T18:47:13.839Z",
         "status" : "viewed",
         "comments" : [ 
            { "user" : { "name" : "maxwell", "id" : "maxwell.mosley@gmail.com" },
              "text" : "This is so funny",
              "time" : "2015-01-31T18:47:13.839Z" 
            }
         ] 
        },
        {"link" : "http://i.imgur.com/dR3XRDr.jpg",
         "user" : { "name" : "maxwell", "id" : "maxwell.mosley@gmail.com" },
         "time" : "2015-01-31T18:52:34.695Z",
         "status" : "viewed",
         "comments" : [ 
            { "user" : { "name" : "maxwell", "id" : "maxwell.mosley@gmail.com" },
              "text" : "This is so cute...",
              "time" : "2015-01-31T18:52:34.695Z"
            }
         ]
        }
      ] }
    ] };

var currentStash = { id: 0,
                     name: '',
                     content: []
                   };
main();
function main()
{
    //createStashList(userData.user.stashes);
}

function createStashList(stashes) 
{
    var index;
    for(index = 0; index < stashes.length; ++index)
    {
        addStash(stashes[index]);
    }

    if(index != 0)
    {
        loadStash();
    }
}

function addStash(stashData)
{
    var myStashDiv = document.getElementById("divMyStash");
    var div = document.createElement('div');

    div.id = "stash_" + stashData.id;
    div.className = "myStash";
    div.onclick = function() { loadStash(stashData.id); };
    div.innerHTML = stashData.name;

    myStashDiv.appendChild(div);
}

function loadStash(id)
{
    var stashDiv;
    var thisStashDiv;
    if(!id)
    {
        id = userData.user.previousStash;
    }
    
    unselectStash();

    currentStash = loadStashData(id);
    if(currentStash !== null) 
    {
        selectStash(id);
        updateStashDiv();
    }
}

function unselectStash()
{
    var div;

    if(!currentStash.id)
    {
        return;
    }

    div = document.getElementById('stash_' + currentStash.id);
    div.classList.remove('selectedStash');
}

function selectStash(id)
{
    var div;
    div = document.getElementById("stash_" + id);
    div.classList.add('selectedStash');
}

function loadStashData(id)
{
    //todo majix
    var index;
    for(index = 0; index < fakeStashData.stashList.length; index++)
    {
        if(fakeStashData.stashList[index].id === id) return fakeStashData.stashList[index];
    }
    return null;
}

function stashObserver(changes)
{
    changes.forEach(function(change, i)
    {
        updateStashDiv();
        console.log('what property changed? ' + change.name);
        console.log(change);
    });
}

function updateStashDiv()
{
    var index;
    var stashDiv = document.getElementById('divThisStash');
    var list = document.createElement('ul');

    emptyDiv(stashDiv);

    stashDiv.innerHTML = currentStash.name;
    
    for(index = 0; index < currentStash.content.length; index++)
    {
        list.appendChild(createContent(index));
    }

    stashDiv.appendChild(list);
}

function emptyDiv(divToEmpty)
{
    while(divToEmpty.lastChild) 
    {
        divToEmpty.removeChild(divToEmpty.lastChild);
    }
    divToEmpty.innerHTML = '';
}

function createContent(index)
{
   var item = document.createElement('li');

   item.appendChild(document.createTextNode(currentStash.content[index].user.name));
   item.appendChild(document.createTextNode(currentStash.content[index].link));

   return item;
}

