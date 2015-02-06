var currentStash;
main();
function main()
{
    currentStash = "maxwell's stash";
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
            document.getElementById('stashName').currentStash = e.detail.name;
            //contentList.url = "../data/stashData" + contentList.stashId + ".json";
        }

        toggleDrawer();
}

function toggleDrawer()
{
    document.getElementById('drawerPanel').togglePanel();
}
