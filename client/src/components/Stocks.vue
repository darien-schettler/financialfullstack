<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-sm-10">
        <h1>Stocks</h1>
        <hr><br><br>
        <button type="button" class="btn btn-success btn-sm">Add A Stock</button>
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
                  <button type="button" class="btn btn-warning btn-sm">Update</button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<!-- After the component is initialized, the getStocks() method is called via the created lifecycle hook, which fetches the stocks from the back-end endpoint we just set up. -->
<script>
import axios from 'axios';

export default {
  data() {
    return {
      stocks: [],
    };
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
  },
  created() {
    this.getStocks();
  },
};
</script>