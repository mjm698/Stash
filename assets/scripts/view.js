main();
function main()
{
    var contentId = window.location.search.substring(1).split("=")[1];
    var el = document.getElementById('visible-content');
    el.contentId = contentId;
}
