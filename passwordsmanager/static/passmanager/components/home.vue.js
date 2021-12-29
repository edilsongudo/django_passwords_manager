var home = {
    template:
    `
        <div class="container">

            <div v-if="message" :class="message.class">
                [[ message.message ]]
            </div>

            <form v-if="authenticated" v-html>
                <h1>New Entry</h1>
                <div class="form-group">
                    <div><label for="masterpassword">Site</label></div>
                    <input id="" class="textinput textInput form-control" type="text" name="site" value="">
                </div>
                <div class="form-group">
                    <div><label for="masterpassword">Password</label></div>
                    <input id="" class="textinput textInput form-control" type="text" name="password" value="">
                </div>
                <div><button class="cta cta1" type="submit" @click=checkMasterPassword>Authenticate</button></div>
            </form>

            <form v-else v-html>
                <div><label for="masterpassword">Master Password</label></div>
                <input id="masterpassword" class="textinput textInput form-control" type="text" name="master" value="">
                <div><button class="cta cta1" type="submit" @click=checkMasterPassword>Authenticate</button></div>
            </form>
        </div>`
    ,
    data() {
        return {
            authenticated: false,
            message: false
    }
    },

    delimiters: ['[[', ']]'],

    methods: {

        show_alert: function (state, obj, timeout) {
            state.message = obj
            setTimeout(function () {
                state.message = false
            }, timeout)
        },

        doAjaxPost: function(obj) {
            let data = JSON.stringify(obj)

            var state = this

            $.ajax({
                url: '/',
                headers: {'X-CSRFToken': csrfToken},
                dataType: 'json',
                data: data,
                type: 'post',
                success: function(response) {
                    console.log(response)
                    if (response['is_masterpass_correct'] == "true") {
                        state.authenticated = true
                        state.show_alert(state, {message: "Successfully Authenticated", class: "alert alert-success"}, 3000)
                    } else {
                        state.show_alert(state, {message: "Your master password is wrong", class: "alert alert-danger"}, 3000)
                    }
                }})
        },

        checkMasterPassword: function(e) {
            e.preventDefault()
            let masterpass = document.querySelector('#masterpassword')
            this.doAjaxPost({'masterpass': masterpass.value})
        }
    },

    created() {
    }
}
