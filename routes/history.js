// ==================================================
// DOCUMENT HISTORY ROUTER

const url = 'http://localhost:3000/history';

require('dotenv').config();
// sequelize...

const express = require('express');
const router = express.Router();
const mysql = require('mysql');


// ==================================================
// Get all records
router.get('/', (req, res) => {
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
        console.log('Connected to DB');

        const query = "select dcr.DOCUMENT_ID, dcr.DECISION, dcr.DECISION_DATE, d.NAME, dcr.REQUEST_ID, dcr.CHANGE_REASON from DOCM_CHNG_RQST dcr inner join DOCUMENTS d on dcr.DOCUMENT_ID = d.DOCUMENT_ID where dcr.DOCUMENT_ID = 'CI-QSP-7150'";
        connection.query(query, (err, rows, fields) => {
            if (err) {
                console.log('Failed to query for DOCM_CHNG_RQST: ' + err);
                res.sendStatus(500);
                return;
            }
            res.json(rows);
        });

        connection.end();
        });
    
    } catch (err) {
        console.log('Error connecting to Db history 44');
        return;
    }

});

module.exports = router;
