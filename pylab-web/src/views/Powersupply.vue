<template>
  <v-card class="mx-auto">
    <v-card-text>
      <p class="text-h6 text--primary">Siglent SPD3303X-E</p>
      <v-row>
        <v-col cols="6">
          <channel channel="1" :api="api_address" :ps="powersupply"/>
        </v-col>
        <v-col cols="6">
          <channel channel="2" :api="api_address" :ps="powersupply"/>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-btn
        variant="outlined"
        color="primary"
        @click="supplySettings = !supplySettings"
      >
        API Details
      </v-btn>
    </v-card-actions>

    <v-dialog v-model="supplySettings" width="64rem">
      <v-card>
        <v-card-title>API Details</v-card-title>
        <v-card-text class="pb-0">
          <p>
            Backend Version: {{ api }}
            <v-btn
              variant="outlined"
              color="grey"
              :href="api_address + 'docs'"
              size="x-small"
              >Read Docs</v-btn
            >
          </p>
          <br />
          <p>Parameters</p>
          <v-list lines="one">
            <v-list-item
              v-for="(payload, prop) in powersupply"
              :key="'ps-' + prop"
              :title="prop"
              :subtitle="payload"
            >
            </v-list-item>
          </v-list>
          <br />
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="pt-0">
          <v-btn color="primary" block @click="supplySettings = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
import axios from "axios";
import channel from "@/components/supply/channel.vue";
export default {
  components: { channel },
  data: () => ({
    supplySettings: false,
    loading: true,
    api: "loading",
    api_address: "http://127.0.0.1:8000/",
    powersupply: {}, // empty object, details from API
  }),
  mounted() {
    axios
      .get(this.api_address)
      .then((response) => {
        console.log(response.data);
        this.powersupply = response.data.ps;
        this.api = response.data.version;
      })
      .catch((error) => {
        console.log(error);
        this.ip = "ERRROR";
        this.api = "ERROR";
      })
      .finally(() => (this.loading = false));
  },
};
</script>
