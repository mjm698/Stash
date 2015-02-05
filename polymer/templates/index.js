main();
function main()
{
    document.querySelector('stash-list').addEventListener('loadStash', loadStash);
}

function loadStash(e)
{
        var contentList = document.querySelector('content-list');
        if(contentList.stashId !== e.detail.msg)
        {
            var stashList = document.querySelector('stash-list');
            stashList.selectedStash = e.detail.id;
            contentList.stashId = e.detail.id;
            document.getElementById('stashName').currentStash = e.detail.name;
            contentList.url = "../data/stashData" + contentList.stashId + ".json";
        }

        toggleDrawer();
}

function toggleDrawer()
{
    document.getElementById('drawerPanel').togglePanel();
}
