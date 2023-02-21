<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const data = ref([]);
const inputRef = ref(null);
const outputRef = ref(null);
const formRef = ref(null);
const isWordClicked = ref([]);

// const message = ref("");
// const showMessage = ref(false);

// const getResponse = () => {
//   const path = "http://127.0.0.1:5000/test";
//   axios
//     .get(path)
//     .then((res) => {
//       // console.log(res.data);
//       data.value = res.data.data;
//     })
//     .catch((err) => {
//       console.error(err);
//     });
// };

const addData = (formData) => {
  const path = "/test";
  axios
    .post(path, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
      transformRequest: (formData) => formData,
    })
    .then((res) => {
      console.log(res.data);
      // getResponse();
      data.value = res.data.data;

      // message.value = res.data.message;
      // showMessage.value = true;
      // setTimeout(() => {
      //   showMessage.value = false
      // }, 2000)
    })
    .catch((err) => {
      console.error(err.message);
    });
};

const submitData = (e) => {
  // const payload = {
  //   1: "1",
  //   2: "2",
  //   3: "3",
  // };

  e.preventDefault();

  const payload = new FormData();
  payload.append("file", inputRef.value.files[0]);
  console.log(formRef.value);
  console.log(payload);

  addData(payload);

  const src = URL.createObjectURL(inputRef.value.files[0]);
  outputRef.value.src = src;

  // addData(payload);
  // inputs.value = [];
};

const submitForm = () => {
  formRef.value.submit();
};

const changeVisibility = (id) => {
  console.log(id)
  isWordClicked.value[id] = !isWordClicked.value[id]
}

// getResponse();
</script>

<template>
  <div>
    <div>
      <h1>Upload photo or take a picture</h1>
      <form ref="formRef" @submit.prevent="submitData">
        <input
          type="file"
          accept="image/jpeg, image/png, image/jpg"
          ref="inputRef"
          @change="submitData"
          capture="environment"
        />
        <!-- <button type="submit">Submit</button> -->
      </form>
      <img class="output" ref="outputRef" />
    </div>
    {{ data }}
    <div class="words-wrapper">
      <div v-for="word in data" :key="word['id']" :id="word['id']" @click="changeVisibility(word['id'])">
        <button class="word">{{ word["word"] }} </button>
        <p class="description" v-if="isWordClicked[word.id]">{{ word["description"] }}</p>
      </div>
    </div>

    <!-- <p v-if="showMessage">{{ message }}</p> -->
    <!-- <table>
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
    </table> -->

    <!-- <form @submit.prevent="submitData">
      <div v-for="i in 3" :key="i">
        <label :for="i">{{ i }}</label>
        <input :id="i" v-model="inputs[i]" />
      </div>
      <button type="submit">Submit</button>
    </form> -->

    <!-- <p v-for="input in inputs">{{ input }}</p> -->
  </div>
</template>

<style lang="scss" scoped>
img {
  max-width: 100%;
  max-height: 100%;
}

.words-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;

  .word {
    padding: 1rem;
    background-color: antiquewhite;
    border-radius: 999px;
  }
}
</style>
