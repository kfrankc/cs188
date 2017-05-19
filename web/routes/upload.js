let express = require('express');
let router = express.Router();

/* /upload */
router.post('/', (req, res, next) => {
  res.json({
    'success': true,
    'data': 12345
  });
});


module.exports = router;
