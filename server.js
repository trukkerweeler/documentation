require("dotenv").config();

const exp = require("constants");
const cors = require("cors");
const express = require("express");
const app = express();
const port = 3000;

app.use(cors());

app.use(express.static('public'));
app.use(express.json());

app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  next();
});

const sysdocRoutes = require("./routes/sysdocs");
app.use("/sysdocs", sysdocRoutes);

const requestRoutes = require("./routes/requests");
app.use("/requests", requestRoutes);

const historyRoutes = require("./routes/history");
app.use("/history", historyRoutes);

const docsavailRoutes = require("./routes/docsavail");
app.use("/docsavail", docsavailRoutes);


app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});
