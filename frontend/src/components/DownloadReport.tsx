import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import {
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
  FormControl,
} from '@mui/material';
import DownloadIcon from '@mui/icons-material/Download';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';
import { saveAs } from 'file-saver';


function DownloadReport(props: {
  invoiceName: String;
  currentReport: any;
  inputDiv: any;
}) {
  const [open, setOpen] = React.useState(false);
  const [downloadFormat, setDownloadFormat] = React.useState('');
  const { invoiceName, currentReport, inputDiv } = props;

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleChange = (event: SelectChangeEvent) => {
    setDownloadFormat(event.target.value);
  };

  const handleDownloadJSON = () => {
    const dataStr = JSON.stringify(currentReport, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });

    const formatName = invoiceName.replace(/\.[^/.]+$/, '');

    saveAs(blob, `${formatName}-validation-report.json`);
  };

  const handleDownloadPDF = async () => {
    const inputDiv = document.getElementById('report-content');
    if (inputDiv) {
      const pdf = new jsPDF();
      const margin = 10;
      const pdfWidth = pdf.internal.pageSize.getWidth() - margin * 2;
      const pdfHeight = pdf.internal.pageSize.getHeight() - margin * 2;
      const canvas = await html2canvas(inputDiv);

      let imgData = canvas.toDataURL('image/png');
      let imgHeight = (canvas.height * pdfWidth) / canvas.width;

      let heightLeft = imgHeight;
      let position = margin;

      pdf.addImage(imgData, 'PNG', margin, position, pdfWidth, imgHeight);
      heightLeft -= pdfHeight;

      while (heightLeft >= 0) {
        position = heightLeft - imgHeight;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', margin, position, pdfWidth, imgHeight);
        heightLeft -= pdfHeight;
      }

      const formatName = invoiceName.replace(/\.[^/.]+$/, '');
      pdf.save(`${formatName}-validation-report.pdf`);
    }
  };

  return (
    <>
      <Button
        onClick={handleClickOpen}
        startIcon={<DownloadIcon />}
        variant='contained'
        sx={{
          padding: '15px',
        }}
      >
        Download Report
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}
        PaperProps={{
          component: 'form',
          onSubmit: (event: React.FormEvent<HTMLFormElement>) => {
            event.preventDefault();
            if (downloadFormat == 'JSON') {
              handleDownloadJSON();
            } else {
              handleDownloadPDF();
            }
          },
        }}
      >
        <DialogTitle>Download report for {invoiceName}?</DialogTitle>
        <DialogContent>
          <DialogContentText>Select a download format below.</DialogContentText>

          <FormControl
            fullWidth
            variant='outlined'
            margin='normal'
            required
            sx={{ mt: 2, mb: -1 }}
          >
            <InputLabel id='select-format'>Download Format</InputLabel>
            <Select
              labelId='select-format'
              id='select-format'
              value={downloadFormat}
              label='Download Format'
              onChange={handleChange}
              required
              fullWidth
            >
              <MenuItem value={'JSON'}>JSON</MenuItem>
              <MenuItem value={'PDF'}>PDF</MenuItem>
            </Select>
          </FormControl>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button type='submit'>Download</Button>
        </DialogActions>
      </Dialog>
    </>
  );
}

export default DownloadReport;
