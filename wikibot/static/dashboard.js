document.addEventListener('DOMContentLoaded', function() {
    get_alpha();

    $(".my-list").on("click", function() {
        var id = this.id;
        document.getElementById('singlepagehead').innerHTML = '';
        if (id == 'alpha') {
            $('#singlepagehead').append('<div id="category-list"></div><div id="singlepage" category=""></div>');
            get_alpha();
        } else if (id == 'beta')
            get_beta();
        else
            coming_soon();
    })

    function coming_soon() {
        $('#singlepagehead').append('<h5>This and many more features coming soon !</h5>');
    }

    function get_beta() {
        var temp = '<div id="singlepage"></div>';
        $('#singlepagehead').append(temp);

        temp = '<h5><b>Note </b>: This feature is view-only currently, you can use with bot, but can not edit here.</h5><br>\
        <h5>Messasges with only prefix (no sub message)(ex. +help)</h5>';
        $('#singlepage').append(temp);

        var url = "/api/dashboard/beta";
        send_request('GET', url, '', callback);

        function callback(response) {

            for (i = 0; i < response.length; i++) {
                var new_item = '<div class="row beta-row" id="beta-row{beta_id}"> <div class="col-lg-2 my-col"> \
                <input type="text" class="form-control-plaintext beta-keyword" id="beta-keyword{beta_id}" value="+{beta_keyword}" disabled> </div>\
                <div class="col-lg-6 my-col"> <textarea id="beta-resp{beta_id}" spellcheck="false" class="form-control my-response" rows="5" \
                data="{beta_response}" disabled>{beta_response}</textarea> </div> \
                <div class="col-lg-2 align-self-center my-col"> <button type="button" class="btn btn-primary row-buttons" \
                name="beta-edit" id ="beta-edit{beta_id}">Edit</button> <br> \
                <button type="button" class="btn btn-light row-buttons" name="beta-delete" id="beta-delete{beta_id}">Delete</button>\
                </div></div>'
                new_item = new_item.replace(/{beta_id}/g, response[i].beta_id);
                new_item = new_item.replace(/{beta_keyword}/g, response[i].beta_keyword);
                new_item = new_item.replace(/{beta_response}/g, response[i].beta_response);
                $('#singlepage').append(new_item);
            }
        }
    }

    function get_alpha() {
        get_data('main');
        get_categories();
    }

    function get_data(category) {
        var temp = document.getElementById('singlepage');
        if (temp != null)
            temp.innerHTML = '';

        temp = '<h5>Messages with prefix <b>+</b>' + category + ' goes here</h5>';
        if (category == 'main')
            temp = '<h5>This is the main category (messages without any prefix)</h5>';
        $('#singlepage').append(temp);

        document.getElementById('singlepage').setAttribute('category', category);
        temp = '<button type="button" class="btn btn-primary" id="new-entry">Add Entry</button>\
        <div id="new-entry-row"></div><div id="entry-row"></div>';
        $('#singlepage').append(temp);

        var url = "/api/dashboard/alpha/" + category;
        send_request('GET', url, '', callback);

        function callback(response) {

            for (var i = 0; i < response.length; i++) {
                var new_item = '<div class="row my-row" id="row{response_id}"><div class="col-lg-4 my-col"> \
                <input type="text" value="{keywords}" data="{keywords}" class="my-keyword" data-role="tagsinput" id="key{response_id}" disabled> </div>\
                <div class="col-lg-5 my-col"> <textarea spellcheck="false" class="form-control my-response" rows="5" id ="resp{response_id}" data="{message}" disabled>{message}\
                </textarea> </div> <div class="col-lg-1 align-self-center my-col"> \
                <button type="button" class="btn btn-primary row-buttons" name="edit" id ="esave{response_id}">Edit</button> <br>\
                <button type="button" class="btn btn-light row-buttons" name="delete" id="del{response_id}">Delete</button> </div> </div>'
                new_item = new_item.replace(/{response_id}/g, response[i].response_id);
                new_item = new_item.replace(/{keywords}/g, response[i].questions);
                new_item = new_item.replace(/{message}/g, response[i].response);

                $('#entry-row').append(new_item);
            }
            $('.my-keyword').tagsinput('refresh');
        }
    }

    function get_categories() {
        var url = '/api/dashboard/category/list';
        send_request('GET', url, '', callback);

        function callback(response) {

            var temp = document.getElementById('category-list');
            if (temp != null)
                temp.innerHTML = '';

            temp = 'Choose Category :<br><button type="button" class="btn btn-light float-right" id="delete-category" name="manage-category">Delete</button>\
            <button type="button" class="btn btn-primary float-right" id="add-category" name="manage-category">Add</button>';
            $("#category-list").append(temp);

            for (var i = 0; i < response.length; i++) {
                if (response[i].category != 'main')
                    temp = '+ '+response[i].category;
                else
                    temp = response[i].category;
                var new_item = '<button type="button" name="category" id="category' + response[i].category + '" \
                class="btn btn-secondary my-category">' + temp + '</button>';
                $("#category-list").append(new_item);
            }
        }
    }

    function send_request(type, url, data, callback) {
        var request = new XMLHttpRequest();
        request.open(type, url, true);
        if (type == 'GET')
            request.send();
        else if (type == 'POST') {
            var payload = JSON.stringify(data);
            request.send(payload);
        }
        request.onload = () => {
            var response = JSON.parse(request.responseText);
            callback(response);
        };
    }

    function fade_out() {
        document.getElementById('my-alert').style.visibility = "hidden";
    }

    $(".main-page").on("click", "[name='category']", function() {
        var id = (this.id).replace('category','');
        get_data(id);
    })

    $(".main-page").on("click", "[name='manage-category']", function() {
        $('#categoryModal').modal();
        var id = this.id;
        document.getElementById('category-input').value = '';
        var button = document.getElementById('category-action');
        var title = document.getElementById('category-title');
        var message = document.getElementById('category-message');
        var action = document.getElementById('category-action');
        
        if (id == 'add-category') {
            button.setAttribute('class', 'btn btn-success');
            title.innerHTML = "Create New Category";
            message.innerHTML = "Please enter the name for the new category to be created";
            action.innerHTML = 'Create';
        } 
        else if (id == 'delete-category') {
            button.setAttribute('class', 'btn btn-danger');
            title.innerHTML = "Delete Category";
            message.innerHTML = "Please enter the name for the category to be deleted<br>WARNING ! This action can't be undone";
            action.innerHTML = 'Delete';
        }
    })

    $(".main-page").on("click", "[name='action']", function() {

        var category = document.getElementById('category-input').value;
        var id = document.getElementById('category-action').innerHTML;
        $('#categoryModal').modal('hide');
        
        var data = {
            "action": id,
            "category-name": category
        };
        var url = '/api/dashboard/category/action'
        send_request('POST', url, data, callback)

        function callback(response){
            get_categories();
            document.getElementById('singlepage').innerHTML = '';
            if (id == 'Delete')
                get_data('main');
            else if (id == 'Create')
                get_data(category);
        }
    })


    $(".main-page").on("click", "[name='edit'],[name='save']", function() {
        var value = (this.id).replace('esave', '');

        if (this.name == 'edit') {
            this.innerHTML = 'Save';
            this.name = 'save';
            document.getElementById('del' + value).innerHTML = 'Cancel';
            document.getElementById('del' + value).name = "cancel";
            document.getElementById('key' + value).disabled = false;
            document.getElementById('resp' + value).disabled = false;
        } 
        else{
            var response = document.getElementById('resp' + value).value;
            var keys = $('#key' + value).tagsinput('items');

            document.getElementById('key' + value).setAttribute('data', keys);

            var data = {
                "id": value,
                "response": response,
                "keys": keys
            };
            var url = '/api/alpha/update';
            send_request('POST', url, data, callback)

            function callback(data) {
                var status = data['status'];
                
                if (status == true) {
                    var temp = document.getElementById('key' + value).getAttribute('data');
                    temp = temp.split(',');
                    
                    $('#key' + value).tagsinput('removeAll');
                    
                    for (var i = 0; i < temp.length; i++) {
                        $('#key' + value).tagsinput('add', temp[i]);
                    }
                    var key = document.getElementById('key' + value);
                    key.disabled = true;

                    var resp = document.getElementById('resp' + value);
                    resp.setAttribute("data", response);
                    resp.setAttribute("value", response);
                    resp.disabled = true;

                    var btn = document.getElementById('esave' + value);
                    btn.innerHTML = 'Edit';
                    btn.name = 'edit';

                    var btn = document.getElementById('del' + value);
                    btn.innerHTML = 'Delete';
                    btn.name = 'delete';
                } 
                else{
                    var alert = document.getElementById('my-alert');
                    alert.innerHTML = data['alert_message'];
                    alert.style.visibility = "visible";

                    setTimeout(fade_out, 5000);
                }
            }
        }
    });


    $(".main-page").on("click", "[name='delete'],[name='cancel']", function() {
        var value = (this.id).replace('del', '');

        if (this.name == 'cancel'){

            this.innerHTML = 'Delete';
            this.name = 'delete';

            document.getElementById('esave' + value).innerHTML = 'Edit';
            document.getElementById('esave' + value).name = 'edit';
            
            $('#key' + value).tagsinput('removeAll');
            
            var temp = document.getElementById('key' + value).getAttribute('data');
            temp = temp.split(',');
 
            for (var i = 0; i < temp.length; i++) {
                $('#key' + value).tagsinput('add', temp[i]);

            }

            document.getElementById('key' + value).disabled = true;

            var resp = document.getElementById('resp' + value);
            var temp = resp.getAttribute('data');
            resp.value = temp;
            resp.disabled = true;

        }
        else {
            $('#deleteModal').modal()

            document.getElementById('delete-entry').onclick = function() {
                $('#deleteModal').modal('hide')

                var data = {
                    "id": value
                };
                var url = '/api/alpha/delete';
                send_request('POST', url, data, callback);

                function callback(data) {
                    var row = document.getElementById('row' + value);
                    row.remove();
                }
            };
        };
    });

    $(".main-page").on("click", "[id='new-entry']", function() {
        var random = Math.random().toString(36);

        var new_item = '<div class="row my-row" id="row{id}">\
        <div class="col-lg-4 my-col" id="col{id}"> <input type="text" value="" class="my-keyword" data-role="tagsinput" id="key{id}"> </div> \
        <div class="col-lg-5 my-col"> <textarea spellcheck="false" class="form-control my-response" rows="5" id ="resp{id}"></textarea> </div> \
        <div class="col-lg-1 align-self-center my-col"><button type="button" class="btn btn-success row-buttons" name="create" id ="create{id}">Create</button>\
        <button type="button" class="btn btn-light row-buttons" name="remove" id ="remove{id}">Remove</button></div>'
        new_item = new_item.replace(/{id}/g, random);

        $("#new-entry-row").prepend(new_item);
        $('.my-keyword').tagsinput("refresh");

    });

    $(".main-page").on("click", "[name='remove']", function() {
        var temp = (this.id).replace('remove', '')
        row = document.getElementById('row' + temp);
        row.remove();
    });


    $(".main-page").on("click", "[name='create']", function() {
        var value = (this.id).replace('create', '');

        var btn = document.getElementById('create' + value);
        btn.innerHTML = 'Creating';
        btn.disabled = true;

        var response = document.getElementById('resp' + value).value;
        
        var temp = document.getElementById('col' + value).getElementsByClassName('tag label label-info');
        var keywords = [];

        for (var i = 0; i < temp.length; i++) {
            keywords.push(temp[i].textContent);
        }

        var category = document.getElementById('singlepage').getAttribute('category');
        var data = {
            "response": response,
            "keywords": keywords,
            "category": category
        };
        var url = '/api/alpha/create';
        send_request('POST', url, data, callback);

        function callback(data) {
            if (data['status']) {
                var id = data['response_id'];

                var new_item = '<div class="row my-row" id="row{id}">\
                <div class="col-lg-4 my-col" id="col{id}"> <input type="text" value="{keywords}" class="my-keyword" data-role="tagsinput" data="{keywords}" id="key{id}" disabled> </div> \
                <div class="col-lg-5 my-col"> <textarea spellcheck="false" value="{response}" data="{response}" class="form-control my-response" rows="5" id ="resp{id}" disabled>{response}</textarea> </div> \
                <div class="col-lg-1 align-self-center my-col"> \
                <button type="button" class="btn btn-primary row-buttons" name="edit" id ="esave{id}">Edit</button>\
                <button type="button" class="btn btn-light row-buttons" name="delete" id ="del{id}">Delete</button></div>'
                
                new_item = new_item.replace(/{id}/g, id);
                new_item = new_item.replace(/{response}/g, response);
                new_item = new_item.replace(/{keywords}/g, keywords);

                $("#entry-row").prepend(new_item);
                $('.my-keyword').tagsinput("refresh");

                var r = document.getElementById('row' + value); 
                r.remove();
            } 
            else{
                var alert = document.getElementById('my-alert');
                alert.innerHTML = data['alert_message'];
                var btn = document.getElementById('create' + value);
                btn.innerHTML = ' Create';
                btn.disabled = false;
                alert.style.visibility = 'visible';

                setTimeout(fade_out, 5000);
            }
        }
    });
});