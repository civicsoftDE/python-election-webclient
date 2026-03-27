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


document.addEventListener('DOMContentLoaded', function() {
        if (typeof Choices !== 'undefined') {
            var choices = new Choices('.js-choice', {
                placeholderValue: 'Bitte wählen...',
                searchPlaceholderValue: 'Suchen...',
                shouldSort: false
            });
            console.log('Choices initialisiert');
        } else {
            console.error('Choices.js nicht geladen!');
        }
    });

function loadView(routeName, data = {}) {
    new QWebChannel(qt.webChannelTransport, function(channel) {
        channel.objects.bridge.load_view(routeName, data);
    });
}