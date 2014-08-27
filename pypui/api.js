var PYPUI = {"py": {}};

PYPUI.getApp = function () {
    return PYPUI;
}

PYPUI.log = function (msg) {
    console.log(msg)
}

PYPUI.ready = function(callback) {
    PYPUI._ready = callback;
}

PYPUI.register = function(name, func) {
    PYPUI._funcs[name] = func;
}

// private

PYPUI._funcs = {};


PYPUI._call_func = function (name, data) {
    var func = PYPUI._funcs[name];
    func(JSON.parse(data));
}


PYPUI._send = function (name, data, callback) {
    PYPUI._callbacks.push(callback);
    alert(JSON.stringify({"name": name, "data": data}));
}


PYPUI._register_function = function (name) {
    PYPUI.py[name] = function () {
        var args = [name];
        for (var i=0; i < arguments.length; i++) {
            args.push(arguments[i]);
        }
        return PYPUI._send.apply(null, args);
    };
}

PYPUI._callbacks = [];

PYPUI._send_response = function (jsondata) {
    var func = PYPUI._callbacks.pop();
    if (func !== undefined) {
        if (jsondata === "") {
            func();
        } else {
            func(JSON.parse(jsondata));
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    if(PYPUI._ready)
        PYPUI._ready();
}, false);
