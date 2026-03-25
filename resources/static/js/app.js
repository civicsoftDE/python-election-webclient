document.addEventListener('contextmenu', function(event) {
    event.preventDefault();
    event.stopPropagation();
    return false;
});

document.addEventListener('keydown', function(event) {
    if (event.key === 'F12') {
        event.preventDefault();
        return false;
    }
    if (event.ctrlKey && event.shiftKey && event.key === 'I') {
        event.preventDefault();
        return false;
    }
    if (event.ctrlKey && event.shiftKey && event.key === 'J') {
        event.preventDefault();
        return false;
    }
    if (event.ctrlKey && event.key === 'u') {
        event.preventDefault();
        return false;
    }
});

document.querySelector('.list-group-item-action').scrollIntoView({
    behavior: 'smooth',
    block: 'center'
});

function loadView(routeName, data = {}) {
    new QWebChannel(qt.webChannelTransport, function(channel) {
        var bridge = channel.objects.bridge;
        bridge.load_view(routeName, function(htmlContent) {
            document.open();
            document.write(htmlContent);
            document.close();
        });
    });
}