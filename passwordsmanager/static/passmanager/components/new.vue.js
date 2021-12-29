var newpass = {
    template:
    `
        <div class="container">
            <form v-html>
                <h1>New Entry</h1>
                <div class="form-group">
                    <div><label for="masterpassword">Master Password</label></div>
                    <input id="" class="textinput textInput form-control" type="text" name="" value="">
                </div>
                <div class="form-group">
                    <div><label for="masterpassword">Master Password</label></div>
                    <input id="" class="textinput textInput form-control" type="text" name="" value="">
                </div>
                <div><button class="cta cta1" type="submit" @click=checkMasterPassword>Authenticate</button></div>
            </form>
        </div>`
    ,
    data() {
        return {
    }
    },

    delimiters: ['[[', ']]'],

    methods: {
        doAjaxPost: function(obj) {
            let data = JSON.stringify(obj)

            $.ajax({
                url: '/',
                headers: {'X-CSRFToken': csrfToken},
                dataType: 'json',
                data: data,
                type: 'post',
                success: function(response) {
                    console.log(response)
                    if (response['is_masterpass_correct'] == "true") {
                        this.router.go(1)
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
