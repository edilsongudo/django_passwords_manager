var passwordGenerator = {
    template:
    `
        <div class="container">

            <form>
                <h3>Password Generator</h3>
                <div class="form-group">
                    <input autofocus id="masterpassword" class="textinput textInput form-control" type="text" name="master" value="" autocomplete="off">
                </div>
                <div>
                    <button class="cta cta1" >
                        Generate <i class="fas fa-dice"></i>
                    </button>
                </div>
            </form>

        </div>`
    ,
    data() {
        return {
        }
    },

    delimiters: ['[[', ']]'],

    methods: {
    },

    created() {
    }
}
