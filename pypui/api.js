var PYPUI = PYPUI || {};

var xxx = {};
var _ready;

PYPUI.event = {
    addListener: function(name, callback) {
        if(!xxx[name])
            xxx[name] = [];

        xxx[name].push(callback);
    },

    removeListener: function(el, type, fn) {
    },
}

PYPUI.log = function (msg) { console.log(msg) }

PYPUI.ready = function(callback) {
    _ready = callback;
}

PYPUI._send_response = function (jsondata) {
    var func = callbacks.shift();
    if (jsondata === "") {
        func();
    } else {
        func(JSON.parse(jsondata));
    }
}

var callbacks = new Array();

PYPUI.send = function (name, data, callback) {
    callbacks.push(callback);
    alert(JSON.stringify({"name": name, "data": data}));
}

document.addEventListener('DOMContentLoaded', function() {
    if(_ready)
        _ready();
}, false);
