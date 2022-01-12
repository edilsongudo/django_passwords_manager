var settings = {
    template:
    `
        <div class="container">
            <div class="content settingscontainer">

                <div class="title">
                    <h4>Vault</h4>
                </div>
                <div class="settings">
                    <div class="setting">
                        <a href="/master/" class="setting-content">
                            <i class="fal fa-key"></i> Change vault master password
                        </a>
                    </div>

                    <div class="title">
                        <h4>Account</h4>
                    </div>
                    <div class="setting">
                        <a href="/accounts/password/reset/" class="setting-content">
                            <i class="fal fa-mobile"></i> Password Reset
                        </a>
                    </div>
                    <div class="setting">
                        <a href="/accounts/email/" class="setting-content">
                            <i class="fal fa-user-circle"></i> Email Addresses
                        </a>
                    </div>
                    <div class="settings">
                        <div class="setting">
                            <a href="/accounts/logout/" class="setting-content">
                                <i class="fal fa-sign-out"></i> Logout
                            </a>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    `
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
