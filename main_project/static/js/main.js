let image = document.getElementById('memes');
let myPics = ["/static/images/memes/meme1.jpg", "/static/images/memes/meme2.jpg", "/static/images/memes/meme3.jpg", "/static/images/memes/meme4.jpg", "/static/images/memes/meme5.jpg", "/static/images/memes/meme6.jpg", "/static/images/memes/meme7.jpg", "/static/images/memes/meme8.jpg", "/static/images/memes/meme9.jpg", "/static/images/memes/meme10.jpg", "/static/images/memes/meme11.jpg", "/static/images/memes/meme12.jpg", "/static/images/memes/meme13.jpg", "/static/images/memes/meme14.jpg", "/static/images/memes/meme15.jpg"];
let res = () => {
  randomNum = Math.floor(Math.random() * myPics.length);
  image.src = myPics[randomNum];
  console.log(image.src);
}
res();

let img = document.getElementById('img');
    axios.get('https://dog.ceo/api/breeds/image/random')
    .then(res =>{
        img.src = res.data.message;
    }).catch(err =>{
        let pp = document.createElement("p");
        pp.textContent = 'wrong address';
})
console.log(img.src);
console.log(img);

            
var CREATE_PAYMENT_URL  = 'http://127.0.0.1:5000/payment';
var EXECUTE_PAYMENT_URL = 'http://127.0.0.1:5000/execute';

paypal.Button.render({

    env: 'sandbox', // Or 'sandbox'

    commit: true, // Show a 'Pay Now' button

    payment: function() {
        return paypal.request.post(CREATE_PAYMENT_URL).then(function(data) {
            return data.paymentID;
        });
    },

    onAuthorize: function(data) {
        return paypal.request.post(EXECUTE_PAYMENT_URL, {
            paymentID: data.paymentID,
            payerID:   data.payerID
        }).then(function(res) {

            console.log(res.success)
            // The payment is complete!
            // You can now show a confirmation message to the customer
        });
    }

}, '#paypal-button');
