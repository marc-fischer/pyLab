<template>
  <v-navigation-drawer
    v-model="drawer"
    :rail="rail"
    permanent
    @click="rail = false"
  >
    <v-list-item
      title="Marcs pyLab"
      nav
    >
      <template v-slot:append>
        <v-btn
          variant="text"
          icon="mdi-chevron-left"
          @click.stop="rail = !rail"
        ></v-btn>
      </template>
    </v-list-item>

    <v-divider></v-divider>
    <v-list density="compact" nav>
      <v-list-item
        v-for="n in items"
        :key="n.title"
        :prepend-icon="n.icon"
        :title="n.title"
        link
        :to="n.link"
      ></v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>
    
<script>
export default {
  data() {
    return {
      drawer: true,
      items: [
        { title: "Home", icon: "mdi-home-city", link: "/" },
        { title: "Powersupply", icon: "mdi-gauge-low", link: "/powersupply" },
        { title: "Scope", icon: "mdi-graph", link: "/scope" },
      ],
      rail: true,
    };
  },
};
</script>