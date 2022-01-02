var home = {
    template:
    `
        <div class="container">

            <div class="l">

                <div v-if="message" :class="message.class">
                    [[ message.message ]]
                </div>

                <form v-if="authenticated && !show_list" v-html>
                    <div class="quick-action"><button @click="listentries" class="cta cta1"><i class="fas fa-list"></i> list</button></div>
                    <h4>New Entry</h4>
                    <div class="form-group">
                        <div><label for="masterpassword">Site</label></div>
                        <input id="entrysite" v-model="entrysite" class="textinput textInput form-control" type="text" name="site" value="" autocomplete="off">
                    </div>
                    <div class="form-group">
                        <div><label for="masterpassword">Email or Username</label></div>
                        <input id="entryemail" v-model="entryemail" class="textinput textInput form-control" type="text" name="email" value="" autocomplete="off">
                    </div>
                    <div class="form-group">
                        <div><label for="masterpassword">Password</label></div>
                        <input id="entrypassword" v-model="entrypassword" class="textinput textInput form-control" type="text" name="password" value="" autocomplete="off">
                    </div>
                    <div><button class="cta cta1" type="submit" @click=addNewEntry>Save</button></div>
                </form>

                <div v-else-if="authenticated && show_list">
                    <form v-html>
                        <div class="quick-action"><button @click="listentries" class="cta cta1"><i class="fas fa-plus"></i> Add</button></div>
                        <h4>Your Passwords</h4>
                        <div class="entriescontainer">
                            <div class="entrycontainer" v-for="entry in entries">
                                <div>
                                    <div class="entry-site textinput textInput form-control">Site: [[ entry.site ]]</div>
                                    <div class="entry-email textinput textInput form-control">User: [[ entry.email ]]</div>
                                    <div class="entry-password textinput textInput form-control">Password: [[ entry.decrypted_password ]]</div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>

                <form v-else v-html>
                    <div class="form-group">
                        <div><label for="masterpassword">Master Password</label></div>
                        <input id="masterpassword" class="textinput textInput form-control" type="text" name="master" value="" autocomplete="off">
                    </div>
                    <div><button class="cta cta1" type="submit" @click=checkMasterPassword>Authenticate</button></div>
                </form>

            </div>

        </div>`
    ,
    data() {
        return {
            authenticated: false,
            masterpassword: false,
            message: false,
            show_list: false,
            entrysite: "",
            entrypassword: "",
            entryemail: "",
            entries: [],
        }
    },

    delimiters: ['[[', ']]'],

    methods: {

        checkinativity: function() {
            var idleTime = 0;
            var state = this
            $(document).ready(function () {
                // Increment the idle time counter every minute.
                var idleInterval = setInterval(timerIncrement, 1000); // 1 second

                // Zero the idle timer on mouse movement.
                $(this).mousemove(function (e) {
                    idleTime = 0;
                });
                $(this).keypress(function (e) {
                    idleTime = 0;
                });
            });

            function timerIncrement() {
                idleTime = idleTime + 1;
                if (idleTime > 300) { // 300 seconds
                    state.masterpassword = false
                    state.authenticated = false
                    console.log('idle')
                    idleTime = 0 //line added by me. It is optional
                }
            }
        },

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
                        state.entries = response['response']
                        state.authenticated = true
                        state.masterpassword = obj['masterpassword']
                        state.checkinativity()
                        console.log(state.masterpassword)
                        state.show_alert(state, {message: "Successfully Authenticated", class: "alert alert-success"}, 3000)
                    } else {
                        state.show_alert(state, {message: "Your master password is wrong", class: "alert alert-danger"}, 3000)
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
                        state.show_alert(state, {message: "Entry Successfully Created", class: "alert alert-success"}, 3000)
                    } else {
                        state.show_alert(state, {message: "Ups,a problem ocurred. You entry may not have been saved", class: "alert alert-danger"}, 3000)
                    }
                }})
        },

        doAjaxPostrequestEntries: function(path, obj) {
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
                    state.entries = response['response']
                }})
        },

        checkMasterPassword: function(e) {
            e.preventDefault()
            let masterpass = document.querySelector('#masterpassword')
            this.doAjaxPostMasterPassword('', {'masterpassword': masterpass.value.trim()})
        },

        listentries: function () {
            if (this.show_list) {
                this.show_list = false
            } else {
                this.show_list = true
                this.doAjaxPostrequestEntries('', {'masterpassword': this.masterpassword.trim()})
            }
        },

        addNewEntry: function(e) {
            e.preventDefault()
            if (this.entrysite.trim() != "" && this.entryemail.trim() !="" && this.entrypassword.trim() !="") {
                let postData = {
                    entrysite: this.entrysite.trim(),
                    entryemail: this.entryemail.trim(),
                    entrypassword: this.entrypassword.trim(),
                    masterpassword: this.masterpassword.trim(),
                }
                this.doAjaxPostNewEntry('/new/', postData)
                this.entrysite = ""
                this.entryemail = ""
                this.entrypassword = ""
            } else {
                this.show_alert(this, {message: "Plese, fill all the fields", class: "alert alert-danger"}, 3000)
            }
        }
    },

    created() {
        console.log('created')
    }
}
