require('dotenv/config')
const express = require('express')
const bodyParser = require('body-parser')
const twilio = require('twilio');
const ngrok = require('ngrok');
const colors = require('colors');
const readlineSync = require('readline-sync');
const { validatePhoneNumber } = require('./js/validator')
const { spawn } = require('child_process');

// Globals
let proxyNumber = process.env.PROXY_NUMBER
let userNumber

/** 
 * INITIALIZE TWILIO AND NGROK
 */

// Initialize Ngrok tunnel
(async function () {
    try {
        const url = await ngrok.connect({
            proto: 'http',
            addr: 8081, // port or network address, defaults to 8080
            subdomain: 'proxyblock', // my reserved tunnel name
            authtoken: process.env.NGROK_TOKEN, // Your ngrok tunnel url
            region: 'us', // region
        });
        console.log("SERVER IS LIVE AT ".yellow + url + "\n")

    } catch (error) {
        console.log('FAILED TO ESTABLISH TUNNEL'.red + error)
    }

})();

// initialize Twilio API
var accountSid = process.env.TWILIO_SID; // Your Account SID from www.twilio.com/console
var authToken = process.env.TWILIO_TOKEN;   // Your Auth Token from www.twilio.com/console
var client = new twilio(accountSid, authToken);

// initialize Express app
const app = express()
const port = 8081

// configs
app.use(bodyParser.urlencoded({ extended: false }))


/** 
 * USER INPUTS 
 */

// Prompt for getting users real number
console.log("\nWELCOME TO PROXYBLOCK\n".rainbow)

// User input
let input = readlineSync.question("Enter your phone number ex. 646-222-2222: ");

// validate phone number
while (!validatePhoneNumber(input)) {

    input = readlineSync.question("Invalid phone number try again: ");

}
// Set user number
userNumber = input
console.log("\nYOUR PROXY NUMBER IS " + proxyNumber.green + "\n")
console.log("YOUR MAY NOW USE YOUR PROXY NUMBER\nALL NON-SPAM MESSAGES WILL BE FOWARDED TO " + `${userNumber}`.green + "\n")


/** 
 * ROUTES
 */

// main route
app.get('/', (req, res) => { res.send("Hello this is a `ProxyBlock` Server") })

// test route
app.get('/test', (req, res) => { res.send("Test response") })

// Route for incoming messages.
app.post('/message', (req, res) => {

    let senderNumber = req.body.From;
    let message = req.body.Body;

    // log inbound message
    console.log("INBOUND SMS: ".green + `${senderNumber}` + " BODY: ".green + `${message}`)

    // Initialize Neural Net Prediction using (predict.py)
    const process = spawn('python3', ['./ml_model/predict.py', message]);

    // Process Neural Net output
    process.stdout.on('data', function (data) {

        let buffer = Buffer.from(data)
        let prediction = escape(buffer.toString());

        // If prediction is Not Spam foward to users actual phone number
        if (prediction == "NOT%20SPAM%0A") {

            console.log("MESSAGE NOT SPAM FOWARDING TO YOUR PHONE".yellow)

            // compose and relay message
            client.messages.create({
                body: message, // message 
                to: userNumber,  // recipient number
                from: proxyNumber // proxy number
            }).then((message) => {
                console.log("OUTBOUND SMS: ".green + userNumber + " BODY: ".green + `${message}`)
            })

            // If prediction is "Spam" foward to users actual phone number
        } else {
            console.log("MESSAGE IS SPAM BLOCKED".red)
        }

    });


})

app.listen(port, () => console.log("SERVER RUNNING ON PORT ".yellow + `${port}`))