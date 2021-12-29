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
                    <input id="entrysite" v-model="entrysite" class="textinput textInput form-control" type="text" name="site" value="">
                </div>
                <div class="form-group">
                    <div><label for="masterpassword">Email or Username</label></div>
                    <input id="entryemail" v-model="entryemail" class="textinput textInput form-control" type="text" name="email" value="">
                </div>
                <div class="form-group">
                    <div><label for="masterpassword">Password</label></div>
                    <input id="entrypassword" v-model="entrypassword" class="textinput textInput form-control" type="text" name="password" value="">
                </div>
                <div><button class="cta cta1" type="submit" @click=addNewEntry>Save</button></div>
            </form>

            <form v-else v-html>
                <div class="form-group">
                    <div><label for="masterpassword">Master Password</label></div>
                    <input id="masterpassword" class="textinput textInput form-control" type="text" name="master" value="">
                </div>
                <div><button class="cta cta1" type="submit" @click=checkMasterPassword>Authenticate</button></div>
            </form>
        </div>`
    ,
    data() {
        return {
            authenticated: false,
            masterpassword: false,
            message: false,
            entrysite: "",
            entrypassword: "",
            entryemail: "",
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

        doAjaxPostMasterPassword: function(path, obj) {
            let data = JSON.stringify(obj)

            var state = this

            $.ajax({
                url: path,
                headers: {'X-CSRFToken': csrfToken},
                dataType: 'json',
                data: data,
                type: 'post',
                success: function(response) {
                    console.log(response)
                    if (response['is_masterpass_correct'] == "true") {
                        state.authenticated = true
                        state.masterpassword = obj['masterpass']
                        console.log(state.masterpassword)
                        state.show_alert(state, {message: "Successfully Authenticated", class: "alert alert-success"}, 10000)
                    } else {
                        state.show_alert(state, {message: "Your master password is wrong", class: "alert alert-danger"}, 10000)
                    }
                }})
        },

        doAjaxPostNewEntry: function(path, obj) {
            let data = JSON.stringify(obj)

            var state = this

            $.ajax({
                url: path,
                headers: {'X-CSRFToken': csrfToken},
                dataType: 'json',
                data: data,
                type: 'post',
                success: function(response) {
                    if (response['status'] == 'ok') {
                        state.show_alert(state, {message: "Entry Successfully Created", class: "alert alert-success"}, 10000)
                    } else {
                        state.show_alert(state, {message: "Ups,a problem ocurred. You entry may not have been saved", class: "alert alert-danger"}, 10000)
                    }
                }})
        },

        checkMasterPassword: function(e) {
            e.preventDefault()
            let masterpass = document.querySelector('#masterpassword')
            this.doAjaxPostMasterPassword('', {'masterpass': masterpass.value})
        },

        addNewEntry: function(e) {
            e.preventDefault()
            let postData = {
                entrysite: this.entrysite,
                entryemail: this.entryemail,
                entrypassword: this.entrypassword,
                masterpassword: this.masterpassword,
            }
            this.doAjaxPostNewEntry('/new/', postData)
            this.entrysite = ""
            this.entryemail = ""
            this.entrypassword = ""
        }
    },

    created() {
    }
}
