import * as React from 'react';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './Title';

// Generate Order Data

export default function ManageTable(props) {
  const [newName, setNewName] = React.useState('Untitled');
  const [createDialogOpen, setcreateDialogOpen] = React.useState(false);;
  const handleCreateDialogClickOpen = () => {
    setcreateDialogOpen(true);
  };

  const handleCreateDialogClose = () => {
    setcreateDialogOpen(false);
  };

  const handleCreateDialogSubmit = () => {
    setcreateDialogOpen(false);
    props.create(newName);
  };

  const handleNewName = (e) => {
    setNewName(e.target.value);
  }
  return (
    <React.Fragment>
      <Title>{props.title}</Title>
      <Table size="small">
        <TableHead>
          <TableRow>
            {Object.keys(props.theads).map(
              key => <TableCell key={key}>{props.theads[key]}</TableCell>
            )}
            <TableCell key="control">Control</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {props.records.length ?
            props.records.map(record => (
              <TableRow key={record.id}>
                {Object.keys(props.theads).map(
                  key => <TableCell key={record.id + '-' + key}>{record[key]}</TableCell>
                )}
                <TableCell key={'control' + record.id}>{<props.control record={record} getRecords={props.getRecords} />}</TableCell>
              </TableRow>
            )) :
            <TableRow><TableCell colSpan={Object.keys(props.theads).length + 1}>No Recoeds.</TableCell></TableRow>}
        </TableBody>
      </Table>
      <p></p>
      {props.create?<Button variant="outlined" onClick={handleCreateDialogClickOpen}>Create a Record</Button>:''}
      <Dialog open={createDialogOpen} onClose={handleCreateDialogClose}>
        <DialogTitle>Create a record</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Please input the name of the new record
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
          <Button onClick={handleCreateDialogClose}>Cancel</Button>
          <Button onClick={handleCreateDialogSubmit}>Confirm</Button>
        </DialogActions>
      </Dialog>
    </React.Fragment>
  );
}
