var home = {
    template:
    `
        <div class="container">
            <form v-html>
                <div><label for="masterpassword">Master Password</label></div>
                <input id="masterpassword" class="textinput textInput form-control" type="text" name="master" value="">
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
                        window.location = "/#/new"
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
