// ==================================================
// DOCUMENT HISTORY ROUTER

// Require express
require('dotenv').config();
// sequelize...

const express = require('express');
const router = express.Router();
const mysql = require('mysql');


// get records
router.get('/:id', (req, res) => {
    try {
        const db = mysql.createConnection({
            host: process.env.DB_HOST,
            user: process.env.DB_USER,
            password: process.env.DB_PASS,
            port: process.env.DB_PORT,
            database : 'quality'
        });

        db.connect(function(err) {
            if (err) {
                console.error('Error connecting: ' + err.stack);
                return;
            }
            
        let did = '';
        did = req.params.id;
        // console.log(did);
        const query = `select dcr.*, dcrt.REQUEST_TEXT from DOCM_CHNG_RQST dcr left join DOC_CHG_REQ_TXT dcrt on dcr.REQUEST_ID = dcrt.REQUEST_ID where dcr.DOCUMENT_ID = '${req.params.id}'`;
        // console.log(query);
        
        db.query(query, (err, rows, fields) => {
            if (err) {
                console.log('Failed to query for document history: ' + err);
                res.sendStatus(500);
                return;
            }
            res.json(rows);
        });

        db.end();
        });
    
    } catch (err) {
        console.log('Error connecting to Db');
        return;
    }

});

module.exports = router;
