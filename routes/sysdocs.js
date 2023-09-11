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

        const query = 'select DOCUMENT_ID, NAME, TYPE, STATUS, REVISION_LEVEL, ISSUE_DATE, CREATE_BY, CREATE_DATE from DOCUMENTS order by REFERENCE';
        connection.query(query, (err, rows, fields) => {
            if (err) {
                console.log('Failed to query for corrective actions: ' + err);
                res.sendStatus(500);
                return;
            }
            res.json(rows);
        });

        connection.end();
        });
    

    // res.send('Hello Corrective!');
    } catch (err) {
        console.log('Error connecting to Db');
        return;
    }

});

// ==================================================
// Get a single record

// post new doc
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
        console.log('Connected to DB');

        const query = 'insert into DOCUMENTS (DOCUMENT_ID, NAME, TYPE, SUBJECT, REFERENCE, STATUS, REVISION_LEVEL, ISSUE_DATE, CHECKED_OUT, AUDIT_RESPONSIBLE, CREATE_BY, CREATE_DATE) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)';

        connection.query(query, [req.body.document_id, req.body.document_name, req.body.DOCUMENT_TYPE, req.body.document_name, req.body.reference, req.body.status, req.body.doc_rev, req.body.issue_date, req.body.CHECKED_OUT, req.body.AUDIT_RESPONSIBLE, req.body.CREATE_BY, req.body.CREATE_DATE], (err, rows, fields) => {
            if (err) {
                console.log('Failed to query for corrective actions: ' + err);
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