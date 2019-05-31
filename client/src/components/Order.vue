<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Ready to buy?</h1>
        <hr>
        <router-link to="/" class="btn btn-primary">
          Back Home
        </router-link>
        <br><br><br>
        <div class="row">
          <div class="col-sm-6">
            <div>
              <h4>You are buying:</h4>
              <ul>
                <li>Stock Ticker: <em>{{ stock.ticker }}</em></li>
                <li>Company Name: <em>{{ stock.company }}</em></li>
                <li>Amount: <em class="font-weight-bold">${{ stock.price }}</em></li>
              </ul>
            </div>
            <div>
              <h4>Use this info for testing:</h4>
              <ul>
                <li>Card Number: 4242424242424242</li>
                <li>CVC Code: any three digits</li>
                <li>Expiration: any date in the future</li>
              </ul>
            </div>
          </div>
          <div class="col-sm-6">
            <h3>One time payment</h3>
            <br>
            <form>
              <div class="form-group">
                <label>Credit Card Info</label>
                <input type="text"
                       class="form-control"
                       placeholder="XXXXXXXXXXXXXXXX"
                       v-model="card.number"
                       required>
              </div>
              <div class="form-group">
                <input type="text"
                       class="form-control"
                       placeholder="CVC"
                       v-model="card.cvc"
                       required>
              </div>
              <div class="form-group">
                <label>Card Expiration Date</label>
                <input type="text"
                       class="form-control"
                       placeholder="MM/YY"
                       v-model="card.exp"
                       required>
              </div>
              <button class="btn btn-primary btn-block" @click.prevent="validate">Submit</button>
            </form>
            <div v-show="errors">
              <br>
              <ol class="text-danger">
                <li v-for="(error, index) in errors" :key="index">
                  {{ error }}
                </li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      stock: {
        ticker: '',
        company: '',
        price: '',
      },
      card: {
        number: '',
        cvc: '',
        exp: '',
      },
      errors: [],
    };
  },
  methods: {
    getStock() {
      const path = `http://localhost:5000/stocks/${this.$route.params.id}`;
      axios.get(path)
        .then((response) => {
          this.stock = response.data.stock;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    validate() {
      this.errors = [];
      let valid = true;
      if (!this.card.number) {
        valid = false;
        this.errors.push('Card Number is required');
      }
      if (!this.card.cvc) {
        valid = false;
        this.errors.push('CVC is required');
      }
      if (!this.card.exp) {
        valid = false;
        this.errors.push('Expiration date is required');
      }
      if (valid) {
        this.createToken();
      }
    },
    createToken() {
      // eslint-disable-next-line
      console.log('The form is valid!');
    },
  },
  created() {
    this.getStock();
  },
};
</script>