$(document).ready(async function (){
    var filePaths
    var fileUpload = $('<div/>').addClass('fileBrowser').append($('<div/>').addClass('input-group input-group-sm mb-3')
                .append($('<input/>').addClass('form-control').attr({'type':'text', 'id':'worklistFilePath'}).prop('disabled', true))
                .append($('<span/>').addClass('input-group-text').attr('id', 'choosePathButton').html('Choose File')));
    var submitButton = $('<button/>').attr({'id':'submitFiles', 'type':'button'}).addClass('btn btn-primary').html('Submit')
    $('#main').append(fileUpload).append(submitButton)
    $('#choosePathButton').css('cursor', 'pointer').on('click', async function(){
        var worklistInfo = await eel.filePathRetrieve()();
        $('#worklistFilePath').val(worklistInfo.length + ' Files Choosen');
        filePaths = worklistInfo
    });
    $('#submitFiles').on('click', async function(){
        var concordanceData = await eel.concordanceSubmit(filePaths)();
        console.log(concordanceData)
    });
});