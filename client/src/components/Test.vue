<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const data = ref([]);
const inputRef = ref(null);
const outputRef = ref(null);
const formRef = ref(null);
const isWordClicked = ref([]);

const getData = () => {
  const path = "/test";
  axios
    .get(path)
    .then((res) => {
      console.log(res)
      data.value = res.data.data;
    })
    .catch((error) => {
      // eslint-disable-next-line
      console.error(error);
    });
};

const addData = (formData) => {
  const path = "/test";
  axios
    .post(path, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        "Access-Control-Allow-Origin": "*",
      },
    })
    .then((res) => {
      console.log(res);
      // data.value = res.data.data;
      getData();
    })
    .catch((err) => {
      console.error(err);
      getData();
    });
  // fetch(path, {
  //   method: "POST",
  //   body: formData,
  // })
  //   .then((response) => response.json())
  //   .then((result) => {
  //     console.log("Success:", result);
  //     data.value = result.data
  //   })
  //   .catch((error) => {
  //     console.error("Error:", error);
  //   });
};

const submitData = (e) => {
  e.preventDefault();

  const payload = new FormData();
  payload.append("file", inputRef.value.files[0]);

  addData(payload);

  const src = URL.createObjectURL(inputRef.value.files[0]);
  outputRef.value.src = src;
};

const submitForm = () => {
  formRef.value.submit();
};

const changeVisibility = (id) => {
  console.log(id);
  isWordClicked.value[id] = !isWordClicked.value[id];
};

getData();
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
      </form>
      <img class="output" ref="outputRef" />
    </div>
    {{ data }}
    <div class="words-wrapper">
      <div
        v-for="word in data"
        :key="word['id']"
        :id="word['id']"
        @click="changeVisibility(word['id'])"
      >
        <button class="word">{{ word["word"] }}</button>
        <p class="description" v-if="isWordClicked[word.id]">
          {{ word["description"] }}
        </p>
      </div>
    </div>
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
