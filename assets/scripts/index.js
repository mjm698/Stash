var currentStash;
main();
function main()
{
    document.getElementById('stashName').innerHTML = "maxwell's stash";
    document.querySelector('stash-list').addEventListener('loadStash', loadStash);
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
        }

        toggleDrawer();
}

function toggleDrawer()
{
    document.getElementById('drawerPanel').togglePanel();
}
