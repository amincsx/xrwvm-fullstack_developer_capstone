const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const port = 3030;

// Middleware
app.use(cors());
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Load JSON data
const reviews_data = JSON.parse(fs.readFileSync("data/reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("data/dealerships.json", 'utf8'));

// Connect to MongoDB with error handling
mongoose.connect("mongodb://localhost:27017/", { dbName: 'dealershipsDB' })
  .then(() => {
    console.log('Connected to MongoDB');
    // Import Mongoose models
    const Reviews = require('./review');
    const Dealerships = require('./dealership');
    
    // Seed the database
    try {
      Reviews.deleteMany({}).then(() => {
        Reviews.insertMany(reviews_data['reviews']);
      });
      Dealerships.deleteMany({}).then(() => {
        Dealerships.insertMany(dealerships_data['dealerships']);
      });
    } catch (error) {
      console.error('Error seeding database:', error);
    }
  })
  .catch((err) => {
    console.log('MongoDB not available, using JSON data directly:', err.message);
  });

// ----------------------
// ROUTES
// ----------------------

// Home route
app.get('/', (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const Reviews = require('./review');
    const documents = await Reviews.find();
    res.json(documents);
  } catch (error) {
    res.json(reviews_data['reviews']);
  }
});

// Fetch reviews by dealer id
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const Reviews = require('./review');
    const documents = await Reviews.find({ dealership: req.params.id });
    res.json(documents);
  } catch (error) {
    const filtered = reviews_data['reviews'].filter(r => r.dealership == req.params.id);
    res.json(filtered);
  }
});

// Fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    const Dealerships = require('./dealership');
    const dealerships = await Dealerships.find();
    res.json(dealerships);
  } catch (error) {
    // Fallback to JSON data if MongoDB is not available
    res.json(dealerships_data['dealerships']);
  }
});

// Fetch dealerships by state
app.get('/fetchDealers/:state', async (req, res) => {
  try {
    const state = req.params.state;
    const Dealerships = require('./dealership');
    const dealerships = await Dealerships.find({ state: state });
    res.json(dealerships);
  } catch (error) {
    // Fallback to JSON data if MongoDB is not available
    const filtered = dealerships_data['dealerships'].filter(d => d.state === req.params.state);
    res.json(filtered);
  }
});

// Fetch dealer by id
app.get('/fetchDealer/:id', async (req, res) => {
  try {
    const id = parseInt(req.params.id);
    const Dealerships = require('./dealership');
    const dealership = await Dealerships.findOne({ id: id });
    if (!dealership) {
      return res.status(404).json({ error: 'Dealer not found' });
    }
    res.json(dealership);
  } catch (error) {
    const dealer = dealerships_data['dealerships'].find(d => d.id == req.params.id);
    if (dealer) {
      res.json(dealer);
    } else {
      res.status(404).json({ error: 'Dealer not found' });
    }
  }
});

// Insert a new review
app.post('/insert_review', express.raw({ type: '*/*' }), async (req, res) => {
  try {
    const data = JSON.parse(req.body);

    const documents = await Reviews.find().sort({ id: -1 });
    const new_id = documents.length > 0 ? documents[0].id + 1 : 1;

    const review = new Reviews({
      id: new_id,
      name: data.name,
      dealership: data.dealership,
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year,
    });

    const savedReview = await review.save();
    res.json(savedReview);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
