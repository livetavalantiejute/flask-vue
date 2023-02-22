<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const data = ref([]);
const inputRef = ref(null);
const outputRef = ref(null);
const formRef = ref(null);
const isWordClicked = ref([]);

const addData = (formData) => {
  const path = "/test";
  axios
    .post(path, formData, {
      headers: formData.getHeaders ? formData.getHeaders() : { 'Content-Type': 'multipart/form-data' },
    })
    .then((res) => {
      console.log(res.data);
      data.value = res.data.data;
    })
    .catch((err) => {
      console.error(err);
    });
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
