var passwordGenerator = {
    template:
    `
        <div class="container">

            <div>
                <h3>Password Generator</h3>
                <div class="form-group">
                    <input v-model="password" autofocus id="masterpassword" class="textinput textInput form-control" type="text" name="master" autocomplete="off">
                </div>
                <div>
                    <button @click="getrandompassword" class="cta cta1" >
                        Generate <i class="fal fa-dice"></i>
                    </button>
                </div>
            </div>

        </div>`
    ,
    data() {
        return {
            password: ""
        }
    },

    delimiters: ['[[', ']]'],

    methods: {

        getrandompassword: function (e) {
            var state = this
            $.ajax({
                url: "/generate_password/",
                // headers: {'X-CSRFToken': csrfToken},
                // dataType: 'json',
                // data: {"request": "give me a password please"},
                // type: 'post',
                success: function(response) {
                    state.password = response['password']
                }})
        },

    },

    created() {
        this.getrandompassword()
    }
}
