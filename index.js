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
var fakeStashData = { "name" : "My Stash",
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
                  ] };

var currentStash = { id: 0,
                     name: '',
                     content: []
                   };

main();

function main()
{
    createStashList(userData.user.stashes);
    Object.observe(currentStash, stashObserver, ['update']);
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

    selectStash(id);
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
    currentStash.id = id;
    return fakeStashData;
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
}

