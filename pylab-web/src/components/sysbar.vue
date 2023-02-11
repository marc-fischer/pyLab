<template>
  <v-navigation-drawer model-value class="pt-4" color="grey-lighten-3" expand-on-hover>
    <v-avatar
      color="grey-darken-1"
      size="36"
      class="d-block text-center mx-auto mb-9"
      to="/"
    ><v-icon>mdi-home</v-icon></v-avatar>
    <v-list density="compact" nav>
      <v-list-item
        prepend-icon="mdi-gauge-low"
        title="Powersupply"
        value="powersupply"
        to="/powersupply"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-account"
        title="My Account"
        value="account"
      ></v-list-item>
      <v-list-item
        prepend-icon="mdi-account-group-outline"
        title="Users"
        value="users"
      ></v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>
    
<script>
export default {};
</script>