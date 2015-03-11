main();
function main()
{
    var stashList = document.querySelector('stash-list');
    stashList.selectedStash = 1;

    document.querySelector('stash-list').addEventListener('loadStash', loadStash);
    Polymer.addEventListener(document.getElementById('addContentButton'), 'click', showDialog);
    Polymer.addEventListener(document.getElementById('newContent'), 'addNewContent', newContent);
    Polymer.addEventListener(document.getElementById('stashNameDecorator'), 'click', changeStashName);
    Polymer.addEventListener(document.getElementById('okayButton'), 'click', nameChange);
    Polymer.addEventListener(document.getElementById('cancelButton'), 'click', nameCancel);
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
        document.getElementById('stashName').value = e.detail.name;

        var dialog = document.getElementById('newContent');
        dialog.stashId = e.detail.id;
    }

    document.getElementById('drawerPanel').closeDrawer();
}

function newContent(e)
{
    document.querySelector('content-list').newContent = e.detail.content;
}

function showDialog()
{
    document.getElementById('newContent').toggle();
}

function toggleDrawer()
{
    document.getElementById('drawerPanel').togglePanel();
}

function changeStashName(e)
{
    var stashName = document.getElementById('stashName');
    stashName.disabled = false;
    stashName.oldValue = stashName.value;
    document.getElementById('okayButton').style.display = 'inline';
    document.getElementById('cancelButton').style.display = 'inline';
}

function nameChange(e)
{
    var stashName = document.getElementById('stashName');
    stashName.disabled = true;
    document.getElementById('okayButton').style.display = 'none';
    document.getElementById('cancelButton').style.display = 'none';
    document.getElementById('stashList').newStashName = stashName.value;
}

function nameCancel(e)
{
    var stashName = document.getElementById('stashName');
    stashName.value = stashName.oldValue;
    stashName.disabled = true;
    document.getElementById('okayButton').style.display = 'none';
    document.getElementById('cancelButton').style.display = 'none';
}
