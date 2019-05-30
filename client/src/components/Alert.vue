<template>
  <div>
    <b-alert :variant="this.alertVariant" show dismissible fade>{{ message }}</b-alert>
    <br>
  </div>
</template>

<script>

export default {
  props: {
  message : String,
  alertVariant: String
  },
};

</script>