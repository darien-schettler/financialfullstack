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
      stripePublishableKey: 'pk_test_6s3BrjbZqmKod7wBreLSswcF',
      stripeCheck: false,
    };
  },
  
  methods: {  

    // -------------------  Shipping to production?  ------------------- 
    // You'll want to use an environment variable to dynamically 
    // set the base server-side URL (which is currently http://localhost:5000) 
    // -----------------------------------------------------------------

    getStock() {
      const path = `http://127.0.0.1:5000/stocks/${this.$route.params.id}`;
      axios.get(path)
        .then((response) => {
          this.stock = response.data.stock;
          console.log(response.data.stock);
          console.log(this.stock);
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

    // If the form is valid, the createToken method is triggered...
    // This validates the credit card info (via Stripe.js)
    // It then either returns an error (if invalid) or a unique token (if valid)
    // If there are no errors, we send the token to the server
    // The serve side code will charge the card, and then send the user back to the main page
    createToken() {
      this.stripeCheck = true;
      window.Stripe.setPublishableKey(this.stripePublishableKey);
      window.Stripe.createToken(this.card, (status, response) => {
        
        if (response.error) {
          
          this.stripeCheck = false;
          this.errors.push(response.error.message);
          // eslint-disable-next-line
          console.error(response);

        } else {
            // Define the payload that will be sent to the backend (stock info & token from stripe)
            const payload = {
            stock: this.stock,
            token: response.id,
          
          };
          
          // Path to backend endpoint which will charge the card a certain amount based on the stock info and the token
          const path = 'http://127.0.0.1:5000/charge';
          
          axios.post(path, payload)
            .then((response) => {
              
              // Once successfull reroute to the success page passing the bought stocks id (from the returned payload)
              this.$router.push({ path: `/complete/${response.data.charge.id}` });
          
            })
            .catch((error) => {
          
              // eslint-disable-next-line
              console.error(error);
          
            });
        }
      });
        // Example Of Returned Stripe Response
          // - address_city: null
          // - address_country: null
          // - address_line1: null
          // - address_line1_check: null
          // - address_line2: null
          // - address_state: null
          // - address_zip: null
          // - address_zip_check: null
          // - brand: "Visa"
          // - country: "US"
          // - cvc_check: "unchecked"
          // - dynamic_last4: null
          // - exp_month: 12
          // - exp_year: 2022
          // - funding: "credit"
          // - id: "card_1EhI2PAvbek8DMNplqP7M2zn"
          // - last4: "4242"
    }
  },

  created() {
    this.getStock();
  },

};
</script>