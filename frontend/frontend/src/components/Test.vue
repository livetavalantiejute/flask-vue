<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const data = ref([]);
const inputs = ref([]);
const message = ref("");
const showMessage = ref(false);

const getResponse = () => {
  const path = "http://localhost:5000/test";
  axios
    .get(path)
    .then((res) => {
      console.log(res.data);
      data.value = res.data.data;
    })
    .catch((err) => {
      console.error(err);
    });
};

const addData = (payload) => {
  const path = "http://localhost:5000/test";
  axios
    .post(path, payload)
    .then((res) => {
      getResponse();
      message.value = res.data.message;
      showMessage.value = true;
      setTimeout(() => {
        showMessage.value = false
      }, 2000)
    })
    .catch((err) => {
      console.error(err);
      getResponse();
    });
};

const submitData = () => {
  const payload = {
    1: inputs.value[1],
    2: inputs.value[2],
    3: inputs.value[3],
  };

  addData(payload);
  inputs.value = [];
};

getResponse();
</script>

<template>
  <div>
    <p v-if="showMessage">{{ message }}</p>
    <table>
      <thead>
        <tr>
          <th v-for="i in 3" :key="i">{{ i }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in data" :key="index">
          <td v-for="(column, idx) in row" :key="idx">{{ column }}</td>
        </tr>
      </tbody>
    </table>

    <form @submit.prevent="submitData">
      <div v-for="i in 3" :key="i">
        <label :for="i">{{ i }}</label>
        <input :id="i" v-model="inputs[i]" />
      </div>
      <button type="submit">Submit</button>
    </form>

    <p v-for="input in inputs">{{ input }}</p>
  </div>
</template>
