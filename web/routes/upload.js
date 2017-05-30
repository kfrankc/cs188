const express = require('express');
const router = express.Router();
const spawn = require('child_process').spawn;

/* /upload */
router.post('/', (req, res, next) => {
  res.json({
    'success': true,
    'data': 12345
  });

  const py_script = __dirname + '/' + '../../project/run.py'
  const dcm = __dirname + '/' + '../../project/2d_angiogram.dcm'
  const out_dir = __dirname + '/' + '../public/'
  const process_dicom = spawn('python', [py_script, dcm, out_dir]);

  process_dicom.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  process_dicom.stderr.on('data', (data) => {
    console.log(`stderr: ${data}`);
  });

  process_dicom.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
  });
});

module.exports = router;
