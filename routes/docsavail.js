require('dotenv').config();
// sequelize...

const express = require('express');
const router = express.Router();
const mysql = require('mysql');

// post doc to docsavail
router.post('/', (req, res) => {
    try {
        const connection = mysql.createConnection({
            host: process.env.DB_HOST,
            user: process.env.DB_USER,
            password: process.env.DB_PASS,
            port: 3306,
            database: 'quality'
        });
        connection.connect(function(err) {
            if (err) {
                console.error('Error connecting: ' + err.stack);
                return;
            }
        // console.log('Connected to DB');

        const query = 'insert into DOCS_AVAIL (DOCUMENT_ID) values (?)';

        connection.query(query, [req.body.document_id], (err, rows, fields) => {
            if (err) {
                console.log('Failed to query for docs avail insert: ' + err);
                res.sendStatus(500)
                return;
            }
            res.json(rows);
        });

        connection.end();
        });

    } catch (err) {
        console.log('Error connecting to Db');
        return;
    }

});

module.exports = router;