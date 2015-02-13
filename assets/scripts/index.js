main();
function main()
{
    //todo: change these hardcoded things to use previous stash instead
    document.getElementById('stashName').innerHTML = "maxwell's stash";
    var stashList = document.querySelector('stash-list');
    stashList.selectedStash = 1;

    document.querySelector('stash-list').addEventListener('loadStash', loadStash);
    Polymer.addEventListener(document.getElementById('addContentButton'), 'click', showDialog);
    Polymer.addEventListener(document.getElementById('newContent'), 'addNewContent', newContent);
}

function loadStash(e)
{
    var contentList = document.querySelector('content-list');
    if(contentList.stashId !== e.detail.id)
    {
        var stashList = document.querySelector('stash-list');
        stashList.selectedStash = e.detail.id;

        contentList.stashId = e.detail.id;
        contentList.userId = e.detail.userId;
        document.getElementById('stashName').innerHTML = e.detail.name;

        var dialog = document.getElementById('newContent');
        dialog.stashId = e.detail.id;
    }

    toggleDrawer();
}

function newContent(e)
{
    document.querySelector('content-list').newContent = e.detail.content;
}

function showDialog(element)
{
    document.getElementById('newContent').toggle();
}

function toggleDrawer()
{
    document.getElementById('drawerPanel').togglePanel();
}
