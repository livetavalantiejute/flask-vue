<script setup>
import { RouterLink, RouterView } from "vue-router";
import { ref } from "vue";
import axios from "axios";

import HelloWorld from "./components/HelloWorld.vue";
import Test from "./components/Test.vue";

// const inputRef = ref(null);
// const outputRef = ref(null);

// const data = ref([]);

// const getResponse = () => {
//   const path = "http://localhost:5000/test";
//   axios
//     .get(path)
//     .then((res) => {
//       console.log(res.data);
//       data.value = res.data.data;
//     })
//     .catch((err) => {
//       console.error(err);
//     });
// };

// const addData = (payload) => {
//   const path = "http://localhost:5000/test";
//   axios
//     .post(path, payload)
//     .then((res) => {
//       getResponse();
//       // message.value = res.data.message;
//       // showMessage.value = true;
//       // setTimeout(() => {
//       //   showMessage.value = false
//       // }, 2000)
//     })
//     .catch((err) => {
//       console.error(err);
//       getResponse();
//     });
// };


// const getUploadPic = () => {
//   outputRef.value.src = URL.createObjectURL(inputRef.value.files[0])
//   addData(outputRef.value.src)
// }
</script>

<template>
  testass
  <RouterView />
</template>

<style scoped>

</style>
