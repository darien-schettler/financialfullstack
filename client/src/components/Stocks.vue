<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-sm-10">
        <h1>Stocks</h1>
        <hr><br><br>
        <alert :message=message :alertVariant=successStatus v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.stock-modal>Add A Stock</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Ticker</th>
              <th scope="col">Company</th>
              <th scope="col">Price</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(stock, index) in stocks" :key="index">
              <td>{{ stock.ticker }}</td>
              <td>{{ stock.company }}</td>
              <td>{{ stock.price }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm mx-1 px-2 rounded font-weight-bold" v-b-modal.stock-update-modal @click="editStock(stock)">Update</button>
                  <button type="button" class="btn btn-danger btn-sm mx-1 px-2 rounded font-weight-bold" @click="onDeleteStock(stock)">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addStockModal"
    id="stock-modal"
    title="Add a new stock"
    hide-footer>
    <!-- "<>.prevent" prevent's the button from causing the page to be reloaded when clicked -->
    <!--  Same as putting "evt.preventDefault();" at the top of the specified methods -->
    <b-form @submit.prevent="onSubmit" @reset.prevent="onReset" class="w-100">
      <b-form-group id="form-ticker-group"
      label="Ticker:"
      label-for="form-ticker-input">
      <b-form-input id="form-ticker-input"
      type="text"
      v-model="addStockForm.ticker"
      required
      placeholder="Enter ticker symbol">
    </b-form-input>
  </b-form-group>
  <b-form-group id="form-company-group"
  label="Company:"
  label-for="form-company-input">
  <b-form-input id="form-company-input"
  type="text"
  v-model="addStockForm.company"
  required
  placeholder="Enter company name">
</b-form-input>
</b-form-group>
<b-form-group id="form-price-group">
  <b-form-input id="form-price-input"
  type="text"
  v-model="addStockForm.price"
  required
  placeholder="Enter stock price">
</b-form-input>
</b-form-group>
<b-button-group>
  <b-button type="submit" variant="primary" class="mx-1 rounded">Submit</b-button>
  <b-button type="reset" variant="danger" class="mx-1 rounded">Quit</b-button>
</b-button-group>
</b-form>
</b-modal>
<b-modal ref="editStockModal"
id="stock-update-modal"
title="Update"
hide-footer>
<b-form @submit.prevent="onSubmitUpdate" @reset.prevent="onResetUpdate" class="w-100">
  <b-form-group id="form-ticker-edit-group"
  label="Ticker:"
  label-for="form-ticker-edit-input">
  <b-form-input id="form-ticker-edit-input"
  type="text"
  v-model="editForm.ticker"
  required
  placeholder="Enter ticker symbol">
</b-form-input>
</b-form-group>
<b-form-group id="form-company-edit-group"
label="Company:"
label-for="form-company-edit-input">
<b-form-input id="form-company-edit-input"
type="text"
v-model="editForm.company"
required
placeholder="Enter Company Name">
</b-form-input>
</b-form-group>
<b-form-group id="form-price-edit-group"
label="Price:"
label-for="form-price-edit-input">
<b-form-input id="form-price-edit-input"
type="text"
v-model="editForm.price"
required
placeholder="Enter Price">
</b-form-input>
</b-form-group>
<b-button-group>
  <b-button type="submit" variant="primary" class="mx-1 rounded">Update</b-button>
  <b-button type="reset" variant="danger" class="mx-1 rounded">Cancel</b-button>
</b-button-group>
</b-form>
</b-modal>
</div>
</template>

<!-- After the component is initialized, the getStocks() method is called via the created lifecycle hook, which fetches the stocks from the back-end endpoint we just set up. -->
<script>
  import axios from 'axios';
  import Alert from './Alert.vue';

  export default {

    data() {
      return {
        stocks: [],
        addStockForm: {
          ticker: '',
          company: '',
          price: '',
        },
        editForm: {
          id: '',
          title: '',
          author: '',
          read: [],
        },
        message: '',
        showMessage: false,
        successStatus: false,
      };
    },

    // By passing another component we are able to reference it in the template section above
    components: {
      alert: Alert,
    },

    methods: {
      getStocks() {
        const path = 'http://localhost:5000/stocks';
        axios.get(path)
        .then((response) => {
          this.stocks = response.data.stocks;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
      },

      editStock(stock) {
        this.editForm = stock;
      },

      // POST method that is called when a user submits the modal after information has been added to an array (payload)
      addStock(payload){
        const path = 'http://localhost:5000/stocks';
        // Pass the path and payload to the axios method POST
        // No matter what the response (so long as it isn't an error) we update the stocks from backend data
        // If there is an error we display the error and update stocks from backend data
        axios.post(path, payload)
        .then((response) => {
          this.getStocks();
          this.successStatus = "success";
          this.message = "Stock Added Successfully!  :)"
          this.showMessage = true;
        })
        .catch((error) => {
        // eslint-disable-next-line
        console.log(error);
        this.getStocks();
        this.successStatus = "danger";
        this.message = "Something Went Wrong!  :("
        this.showMessage = true;
        });
      },

      updateStock(payload, stockID) {
        // back tick allows us to pass javascript
        const path = `http://localhost:5000/stocks/${stockID}`;
        axios.put(path, payload)
        .then((response) => {
          this.getStocks();
          this.successStatus = "success";
          this.message = "Stock Edited Successfully!  :)"
          this.showMessage = true;
        })
        .catch((error) => {
        // eslint-disable-next-line
        console.error(error);
        this.getStocks();
        this.successStatus = "danger";
        this.message = "Something Went Wrong!  :("
        this.showMessage = true;
        });
      },

      // Simple method to erase anything entered into the forms of the modal
      initForm() {
        this.addStockForm.ticker = '';
        this.addStockForm.company = '';
        this.addStockForm.price = '';
        this.editForm.id = '';
        this.editForm.ticker = '';
        this.editForm.company = '';
        this.editForm.price = '';
      },

      // This method is run when the user opens the modal (fills out the information) and clicks SUBMIT
      onSubmit(evt) {
        // ref element is how we can access the dom element to hide it when we are done
        this.$refs.addStockModal.hide();

        // Create an array called payload from the information passed in the modal
        const payload = {
          ticker: this.addStockForm.ticker,
          company: this.addStockForm.company,
          price: this.addStockForm.price,
        };

        // Call the addStock method and pass the payload array 
        this.addStock(payload);

        // Reinitialize the forms in the modal to be blank by calling the initForm method
        this.initForm();
      },

      onSubmitUpdate(evt) {
        this.$refs.editStockModal.hide();

        const payload = {
          ticker: this.editForm.ticker,
          company: this.editForm.company,
          price: this.editForm.price,
        };
        this.updateStock(payload, this.editForm.id);
      },

      // Method to hide the modal and reset any of the forms
      onReset(evt) {
        this.$refs.addStockModal.hide();
        this.initForm();
      },

      onResetUpdate(evt) {
        this.$refs.editStockModal.hide();
        this.initForm();
        this.getStocks(); // why?
      },
      removeStock(stockID) {
        const path = `http://localhost:5000/stocks/${stockID}`;
        axios.delete(path)
          .then(() => {
            this.getStocks();
            this.successStatus = "success";
            this.message = 'Stock Removed!';
            this.showMessage = true;
          })
          .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
            this.getStocks();
            this.successStatus = "danger";
            this.message = "Something Went Wrong!  :("
            this.showMessage = true;
          });
      },
      onDeleteStock(stock) {
        this.removeStock(stock.id);
      },
    },

    // Whenever the page's Vue component is created we will fetch the stock prices stored on the backend
    created() {
      this.getStocks();
    },
  };
</script>