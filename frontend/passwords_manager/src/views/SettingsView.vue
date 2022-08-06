<template>
  <div class="container">
    <div class="content settingscontainer">
      <div class="title">
        <h4>Vault</h4>
      </div>
      <div class="settings">
        <div class="setting">
          <router-link :to="{ name: 'master-edit' }" class="setting-content"
            ><i class="fal fa-key"></i> Change vault master
            password</router-link
          >
        </div>

        <div class="title">
          <h4>Account</h4>
        </div>
        <div class="setting">
          <router-link :to="{ name: 'password-change' }" class="setting-content"
            ><i class="fal fa-mobile"></i> Change Password</router-link
          >
        </div>
        <div class="setting">
          <router-link :to="{ name: 'email-change' }" class="setting-content"
            ><i class="fal fa-user-circle"></i> Change Email</router-link
          >
        </div>
        <div class="settings">
          <div class="setting">
            <router-link :to="{ name: 'logout' }" class="setting-content"
              ><i class="fal fa-sign-out"></i> Logout</router-link
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
