// Loading the things we need! :)
var express = require('express'); // Serves our pages to a specified port
var app = express();
const axios = require('axios').create({baseURL: "http://127.0.0.1:5000"}); // Makes external API calls into our frontend server
const bodyParser  = require('body-parser');

app.use(bodyParser.urlencoded());
app.use(express.static('Frontend'));

// Set the view engine to ejs & defines views directory
app.set('views', './Frontend/views');
app.set('view engine', 'ejs');

// Index page 
app.get('/', function(req, res) {

    // Using res.render to load respective ejs viewpage file
    res.render('pages/index.ejs', {
    });
});

// Login page
app.get('/login', function(req, res) {

    res.render('pages/login.ejs', {
    });
});

// login verification
app.post('/processlogin', function(req, res) {
    var usernameInput = request.data.username;
    var passwordInput = request.data.password;
    var data = {
        username: usernameInput,
        password: passwordInput
    }
    const headers = {
        'content-type': 'text/json'
    }

    axios.get('/api/login', data, headers)
    .then((response)=>{
        console.log("RESPONSE RECEIVED: ", res);
    })
    .catch((err) => {
        console.log("AXIOS ERROR: ", err);
    })
});

// Scheduled Cargo Overview page
app.get('/scheduledCargo', function(req, res) {
    axios.get('api/cargo/all')
    .then((response)=>{
        const cargoList = response.data;
        res.render('pages/scheduledCargo.ejs', { cargoList });
    })
    .catch((error) => {
        console.error(error);
        res.status(500).send('Error retrieving scheduled cargo data');
    })
});

app.get('/manageCargo', async (req, res) => {
    
    res.render('pages/scheduledCargo.ejs', { cargoList });

    }
);

// Carts page (FOR TESTING)
//app.get('/carts', function(req, res) {
//    axios.get('https://dummyjson.com/carts')
//   .then((response)=>{
//        var cartData = response.data.carts;
//        carts = [];
//        console.log(cartData);
//
//        // loops carts
//        for (let i = 0; i < cartData.length; i++) {
//            let total = 0;
//
//            // calculates avg and appends to respectice cart
//            for (let j = 0; j < cartData[i].products.length; j++) {
//                total += cartData[i].products[j].total;
//            }
//            cartData[i].cartAverage = total / cartData[i].totalQuantity;
//            carts.push({"id": cartData[i].id, "cartAverage": cartData[i].cartAverage});
//
//            console.log(cartData[i].cartAverage);
//        }
//
//       console.log(carts)
//
//        res.render('pages/carts', {
//            cartData: cartData,
//            carts: carts
//        });
//    });
//});


app.listen(8080);
console.log('Front-End server running on port 8080! :D');
