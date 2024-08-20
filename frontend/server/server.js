var express = require("express");
var path = require("path");

var app = express();

app.use(express.static(path.join(__dirname, "..")));

app.listen(3000, (err) => {
    if (err) return console.log(err);
    console.log("The server is listening to port 3000");
});

app.get("/flastagram/posts", function (req, res) {
    res.sendFile(path.join(__dirname, "..", "post_list.html"));
});

app.get("flastagram/post-create", function (req, res) {
    res.sendFile(path.join(__dirname, "..", "post_create.html"));
});