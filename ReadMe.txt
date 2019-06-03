<strong>Flask-Vue Web Application for Financial Watchlists And Stripe Integration</strong>

<strong>Things Done:</strong>
*	Basic CRUD application created utilizing FLASK & VUE
*	Use BOOTSTRAPVUE to make components and front-end simple
*	Hookup Stripe to allow for checkout web-flow

<strong>Things To Do:</strong>
*	Add client and server-side unit and integration tests.
*	Create a shopping cart so customers can purchase more than one book at a time.
*	Add Postgres to store the stocks/orders/etc.
*	Containerize Vue and Flask (and Postgres, if you add it) with Docker to simplify the development workflow.
*	Add profiles and let the main page be the 'watchlists' for individuals
*	Add images to the stocks (graphs maybe) and create a more robust product page.
*	Hook up the prices to a stock price api
*	Utilize ElasticSearch to find and add a stock to your 'Watchlist'
*	Capture emails and send email confirmations (review Sending Confirmation Emails with Flask, Redis Queue, and Amazon SES).
*	Deploy the client-side static files to AWS S3 and the server-side app to an EC2 instance.
*	Going into production? Think about the best way to update the Stripe keys so they are dynamic based on the environment.
*	Create a separate component for checking out.
*	Improve everything to do with checking out and verification