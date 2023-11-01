<template>
  <v-card variant="outlined" :color="state.output ? 'green' : 'black'">
    <v-card class="mx-auto">
      <v-card-title
      
        ><v-row>
          <v-col>Channel {{ channel }}</v-col>
          <v-spacer></v-spacer>
          <v-col>
            <v-btn
              block
              size="small"
              flat
              :color="state.output ? 'green' : 'blue'"
              @click="toggleOutput()"
              disabled
            >
              {{ state.output ? "On" : "Off" }}
            </v-btn></v-col
          ></v-row
        >
      </v-card-title>
      <v-divider></v-divider>
      <v-card-item>
        <div>
          <v-row>
            <v-col></v-col>
            <v-col><b>Set</b></v-col>
            <v-col><b>Is</b></v-col>
          </v-row>
          <v-row>
            <v-col>Voltage</v-col>
            <v-col v-if="loading">{{ state.set.voltage.toFixed(3) }} V</v-col>
            <v-col v-else>
              <v-text-field
                v-model="state.set.voltage"
                :rules="voltageRules"
              ></v-text-field>
            </v-col>
            <v-col>{{ state.is.voltage.toFixed(3) }} V</v-col>
          </v-row>
          <v-row>
            <v-col>Current</v-col>
            <v-col v-if="loading">{{ state.set.current.toFixed(3) }} A</v-col>
            <v-col v-else
              ><v-slider
                v-model="state.set.current"
                class="align-center"
                :max="ps.max_current / ps.scaling"
                :min="ps.min_current / ps.scaling"
                thumb-label="always"
              ></v-slider
            ></v-col>
            <v-col>{{ state.is.current.toFixed(3) }} A</v-col>
          </v-row>
          <v-row>
            <v-col>Power</v-col>
            <v-col
              >{{
                loading
                  ? "-"
                  : (state.set.voltage * state.set.current).toFixed(3)
              }}
              W</v-col
            >
            <v-col>{{ state.is.power.toFixed(3) }} W</v-col>
          </v-row>
        </div>
      </v-card-item>

      <v-card-actions>
        <v-row>
          <v-col>
            <v-btn
              variant="outlined"
              :color="state.output ? 'blue' : 'green'"
              @click="toggleOutput()"
              block
            >
              {{ state.output ? "Disable" : "Enable" }}
            </v-btn>
          </v-col>
          <v-col>
            <v-btn
              variant="outlined"
              :color="state.sync ? 'green' : 'orange'"
              @click="updateOutput()"
              block
              :disabled="state.sync"
            >
              {{ state.sync ? "In Sync" : "Sync" }}
            </v-btn>
          </v-col>
        </v-row>
      </v-card-actions>
    </v-card>
    <v-card>
      <v-card-text> here comes the plot </v-card-text>
    </v-card>
  </v-card>
</template>

<script>
import axios from "axios";
export default {
  props: ["channel", "api", "ps"],
  data: () => ({
    channel_id: "",
    api_address: "",
    loading: true,
    voltageRules: [
      (value) => !!value || "Required",
      (value) =>
        value < this.ps.min_voltage / this.ps.scaling || "Setting too low",
      (value) =>
        value > this.ps.max_voltage / this.ps.scaling || "Setting too high",
    ],
    state:
      // per channel one object
      {
        set: {
          voltage: 0.0,
          current: 0.0,
        },
        is: {
          voltage: 0.0,
          current: 0.0,
          power: 0.0,
        },
        output: false,
        sync: true,
      },
    stateArchive: {
      // timestamp: state
    },
  }),
  methods: {
    toggleOutput() {
      this.state.output = !this.state.output;
    },
    updateOutput() {
      this.state.sync = !this.state.sync;
    },
    async read_state() {
      await axios
        .get(this.api_address + "channel/" + this.channel_id)
        .then((response) => {
          console.log(response.data);
          this.state.set.voltage = response.data.SET.VOLTAGE;
          this.state.set.current = response.data.SET.CURRENT;
          this.state.is.voltage = response.data.IS.VOLTAGE;
          this.state.is.current = response.data.IS.CURRENT;
          this.state.is.power = response.data.IS.POWER;
        })
        .catch((error) => {
          console.log(error);
          this.ip = "ERRROR";
          this.api = "ERROR";
        })
        .finally(() => (this.loading = false));
    },
  },
  async mounted() {
    this.channel_id = this.channel;
    this.api_address = this.api + "ps/";
    await this.read_state();
  },
};
</script>