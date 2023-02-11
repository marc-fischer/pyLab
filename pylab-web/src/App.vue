<template>
  <v-app id="inspire">
    <sysbar />

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
import sysbar from "@/components/sysbar";
export default {
  components: { sysbar },
};
</script>