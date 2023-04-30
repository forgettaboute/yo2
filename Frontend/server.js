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

//Randome stuffs
const headers = {
    'content-type': 'application/json'
}

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
    axios.get('/api/cargo/all')
    .then((response)=>{
        const cargoList = response.data;
        res.render('pages/scheduledCargo.ejs', { cargoList });
    })
    .catch((error) => {
        console.error(error);
        res.status(500).send('Error retrieving scheduled cargo data');
    })
});

app.post('/addCargo', function(req, res) {
    cargo = {
        'weight': req.body.weight,
        'cargotype': req.body.cargotype,
        'departure': req.body.departure,
        'arrival': req.body.arrival,
        'shipid': req.body.shipid
    }

    axios.post('/api/cargo/add', {cargo})
    .then(function(response) {

        res.render('pages/scheduledCargo.ejs', { });
    });
});

app.post('/updCargo', function(req, res) {
    var id = req.body.id

    res.render('pages/scheduledCargo.ejs', {});
});

app.post('/delCargo', function(req, res) {
    cargo = {
        'id': req.body.id
    }
    console.log(cargo)

    axios.post('/api/cargo/delete', {cargo: cargo}, )
    .then(function(response) {

        res.render('pages/scheduledCargo.ejs', { });
    });
});


app.listen(8080);
console.log('Front-End server running on port 8080! :D');
