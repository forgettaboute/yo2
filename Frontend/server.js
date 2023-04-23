// load the things we need
var express = require('express');
var app = express();
const bodyParser  = require('body-parser');

// required module to make calls to a REST API
const axios = require('axios');

app.use(bodyParser.urlencoded());

// set the view engine to ejs
app.set('view engine', 'ejs');

// index page 
app.get('/', function(req, res) {

    // use res.render to load up an ejs view file
    res.render('/Frontend/views/pages/index.ejs', {
    });
});

// carts page
app.get('/scheduledCargo', function(req, res) {
    // use res.render to load up an ejs view file
    axios.get('127.0.0.1:5000/api/cargo/all')
    .then((response)=>{
        var cartData = response.data.carts;
        carts = []
        console.log(cartData)

        // loops carts
        for (let i = 0; i < cartData.length; i++) {
            let total = 0;

            // calculates avg and appends to respectice cart
            for (let j = 0; j < cartData[i].products.length; j++) {
                total += cartData[i].products[j].total;
            }
            cartData[i].cartAverage = total / cartData[i].totalQuantity;
            carts.push({"id": cartData[i].id, "cartAverage": cartData[i].cartAverage});

            console.log(cartData[i].cartAverage);
        }

        console.log(carts)

        res.render('pages/carts', {
            cartData: cartData,
            carts: carts
        });
    });
});


app.listen(8080);
console.log('Front-End server running on port 8080! :D');
