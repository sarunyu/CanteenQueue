
/**
 * Module dependencies.
 */

var express = require('express');
var routes = require('./routes');
var user = require('./routes/user');
var http = require('http');
var path = require('path');
var io = require('socket.io').listen(81);
var aq = 0;
var cq = 0;
var queue =[];


var app = express();

// all environments
app.set('port', process.env.PORT || 80);
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');
app.use(express.favicon());
app.use(express.logger('dev'));
app.use(express.json());
app.use(express.urlencoded());
app.use(express.methodOverride());
app.use(express.cookieParser('your secret here'));
app.use(express.session());
app.use(app.router);
app.use(require('stylus').middleware(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'public')));

// development only
if ('development' == app.get('env')) {
  app.use(express.errorHandler());
}

app.get('/', function (req, res) {
  res.sendfile(__dirname + '/index.html');
});

app.get('/cq', function (req, res) {
  res.sendfile(__dirname + '/cq.html');
});

app.get('/jquery-2.1.0.min.js', function (req, res) {
  res.sendfile(__dirname + '/jquery-2.1.0.min.js');
});

app.get('/socket.io.js', function (req, res) {
  res.sendfile(__dirname + '/socket.io.js');
});


app.get('/api',function(req, response){
 response.end("Welcome to the API!");
});
app.post('/api', function(req, response) {
  response.end("Welcome to the API!");

var cmd = req.param('cmd');
var orderid = req.param('orderid');
var menu = req.param('menu');
var quantity = req.param('quantity');
var custom = req.param('custom');


console.log(cmd);
console.log(orderid);
console.log(menu);
console.log(quantity);
console.log(custom);

if (cmd==1){
aq+=1
//queue[orderid].push(cmd,orderid,menu,quantity,custom)
console.log(queue);
}
if (cmd==0 & aq >0){
aq-=1
cq+=1
orderid=cq
}

io.sockets.emit('data', [cmd,orderid,menu,quantity,custom,aq,cq]);


});


http.createServer(app).listen(app.get('port'), function(){
  console.log('Express server listening on port ' + app.get('port'));
});


io.sockets.on('connection', function (socket) {



io.sockets.emit('data', [-1,-1,-1,-1,-1,aq,cq]);



});

