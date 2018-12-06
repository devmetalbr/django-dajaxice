var Dajaxice = {

    {% with module=dajaxice_config.modules top=True %}
    {% include "dajaxice/dajaxice_function_loop.js" %}
    {% endwith %}

    {% with top=False %}
    {% for name, module in dajaxice_config.modules.submodules.items %}
    {% include "dajaxice/dajaxice_module_loop.js" %},
    {% endfor %}
    {% endwith %}

    get_cookie: function(name)
    {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].toString().replace(/^\s+/, "").replace(/\s+$/, "");
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    call: function(dajaxice_function, method, dajaxice_callback, argv, custom_settings)
    {
        var custom_settings = custom_settings || {},
            error_callback = Dajaxice.get_setting('default_exception_callback');

        if('error_callback' in custom_settings && typeof(custom_settings['error_callback']) == 'function'){
            error_callback = custom_settings['error_callback'];
        }

        var send_data = 'argv='+encodeURIComponent(JSON.stringify(argv)),
            oXMLHttpRequest = new XMLHttpRequest,
            endpoint = '{% url 'dajaxice-endpoint' %}'+dajaxice_function+'/';

        if(method == 'GET'){
            endpoint = endpoint + '?' + send_data;
        }
        oXMLHttpRequest.open(method, endpoint);
        oXMLHttpRequest.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        oXMLHttpRequest.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        oXMLHttpRequest.setRequestHeader("X-CSRFToken", Dajaxice.get_cookie('{{ dajaxice_config.django_settings.CSRF_COOKIE_NAME }}'));
        oXMLHttpRequest.onreadystatechange = function() {
            if (this.readyState == XMLHttpRequest.DONE) {
                if(this.responseText == Dajaxice.EXCEPTION || !(this.status in Dajaxice.valid_http_responses())){
                    error_callback();
                }
                else{
                    var response;
                    try {
                        response = JSON.parse(this.responseText);
                    }
                    catch (exception) {
                        response = this.responseText;
                    }
                    dajaxice_callback(response);
                }
            }
        }
        if(method == 'POST'){
            oXMLHttpRequest.send(send_data);
        }
        else{
            oXMLHttpRequest.send();
        }
        return oXMLHttpRequest;
    },

    setup: function(settings)
    {
        this.settings = settings;
    },

    get_setting: function(key){
        if(this.settings == undefined || this.settings[key] == undefined){
            return Dajaxice.default_settings[key];
        }
        return this.settings[key];
    },

    valid_http_responses: function(){
        return {200: null, 301: null, 302: null, 304: null}
    },

    EXCEPTION: '{{ dajaxice_config.DAJAXICE_EXCEPTION }}',
    default_settings: {'default_exception_callback': function(){ console.log('Dajaxice: Something went wrong.')}}
};

window['Dajaxice'] = Dajaxice;
