import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import FileDownloadIcon from '@mui/icons-material/FileDownload';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import Link from '@mui/material/Link';
import axios from "axios";
import { API_URL } from '../../config.js';

function DatasetControl(props) {
  const [newName, setNewName] = React.useState(props.record.name);
  const [renameDialogOpen, setRenameDialogOpen] = React.useState(false);
  const [deleteDialogOpen, setDeleteDialogOpen] = React.useState(false);

  const handleRenameDialogClickOpen = () => {
    setRenameDialogOpen(true);
  };

  const handleRenameDialogClose = () => {
    setRenameDialogOpen(false);
    setNewName(props.record.name)
  };

  const handleRenameDialogSubmit = () => {
    setRenameDialogOpen(false);
    axios
      .post(API_URL + "dataset/rename", { "id": props.record.id, "name": newName })
      .then(response => {
        if (response.data) {
          props.getRecords();
        }
      }, error => {
        if (error.response.data.msg) alert(error.response.data.msg);
        props.getRecords();
      });
  };

  const handleNewName = (e) => {
    setNewName(e.target.value);
  }

  const handleDeleteDialogClickOpen = () => {
    setDeleteDialogOpen(true);
  };

  const handleDeleteDialogClose = () => {
    setDeleteDialogOpen(false);
  };

  const handleDeleteDialogSubmit = () => {
    setDeleteDialogOpen(false);
    axios
      .get(API_URL + "dataset/delete?id=" + props.record.id)
      .then(response => {
        if (response.data) {
          props.getRecords();
        }
      }, error => {
        if (error.response.data.msg) alert(error.response.data.msg);
        props.getRecords();
      });
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      let form = new FormData();
      form.append('id', props.record.id)
      form.append('file', e.target.files[0])
      axios
        .post(API_URL + "dataset/upload", form)
        .then(response => {
          if (response.data) {
            props.getRecords();
          }
        }, error => {
          if (error.response.data.msg) alert(error.response.data.msg);
          props.getRecords();
        });
    }
  };

  return (
    <>
      {
        props.record.upload_time ?
          <Button component={Link} size="small" variant="text" href={API_URL + props.record.file_path}><FileDownloadIcon /></Button>
          :
          <Button component="label" size="small" variant="text" to={"/project/" + props.record.id}>
            <input hidden accept="text/csv" multiple type="file" onChange={handleFileChange} />
            <CloudUploadIcon />
          </Button>
      }

      <Button size="small" variant="text" onClick={handleRenameDialogClickOpen}><EditIcon /></Button>
      
      <Button size="small" variant="text" onClick={handleDeleteDialogClickOpen}><DeleteIcon /></Button>

      <Dialog open={renameDialogOpen} onClose={handleRenameDialogClose}>
        <DialogTitle>Rename</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Please input the new name of this project
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            type="text"
            fullWidth
            variant="standard"
            value={newName}
            onChange={handleNewName}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleRenameDialogClose}>Cancel</Button>
          <Button onClick={handleRenameDialogSubmit}>Confirm</Button>
        </DialogActions>
      </Dialog>

      <Dialog
        open={deleteDialogOpen}
        onClose={handleDeleteDialogClose}
      >
        <DialogTitle>
          {"Do you really want to delete?"}
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            This app does not delete records physically. It only marks a delete_time and you may recover it by set the mark to null.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleDeleteDialogClose}>Cancel</Button>
          <Button onClick={handleDeleteDialogSubmit} autoFocus>Delete</Button>
        </DialogActions>
      </Dialog>

    </>
  );
}

export default DatasetControl;
