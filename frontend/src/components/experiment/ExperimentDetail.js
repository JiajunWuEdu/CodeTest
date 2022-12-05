import * as React from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import Paper from '@mui/material/Paper';
import Divider from '@mui/material/Divider';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import CloseIcon from '@mui/icons-material/Close';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import axios from "axios";
import { API_URL } from '../../config.js';

function ExperimentDetail(props) {
  const [currentDataset, setCurrentDataset] = React.useState(props.experiment.dataset);
  const [currentResult, setCurrentResult] = React.useState(props.experiment.result);
  const [currentDatasetVisualizationPath, setCurrentDatasetVisualizationPath] = React.useState(props.experiment.dataset ? props.experiment.dataset.visualization_path : null);
  const [datasets, SetDatasets] = React.useState([]);
  
  const handleDatasetVisualize = () => {
    return axios
      .get(API_URL + "dataset/visualize?id=" + currentDataset.id)
      .then(response => {
        if (response.data) {
          setCurrentDatasetVisualizationPath(response.data.visualization_path);
        }
      }, error => {
        if (error.response.data.msg) alert(error.response.data.msg);
      });
  };

  const handleFitLinear = () => {
    return axios
      .post(API_URL + "result/create", {
        'experiment_id': props.experiment.id,
        'dataset_id': currentDataset.id,
        'model': 'linear'
      })
      .then(response => {
        if (response.data) {
          setCurrentResult(response.data);
          setTimeout(refreshResult, 1000, response.data.id);
        }
      }, error => {
        if (error.response.data.msg) alert(error.response.data.msg);
        setCurrentResult(null);
      });
  };

  const refreshResult = result_id => {
    if (!result_id) return;
    return axios
      .get(API_URL + "result/info?id=" + result_id)
      .then(response => {
        if (response.data && response.data.finish_time) {
          setCurrentResult(response.data);
        } else {
          setTimeout(refreshResult, 1000, result_id);
        }
      }, error => {
        if (error.response.data.msg) alert(error.response.data.msg);
        setCurrentResult(null);
      });
  };

  const handleResultVisualize = () => {
    return axios
      .get(API_URL + "result/visualize?id=" + currentResult.id)
      .then(response => {
        if (response.data) {
          setCurrentResult(response.data);
        }
      }, error => {
        if (error.response.data.msg) alert(error.response.data.msg);
      });
  };

  const handleSave = () => {
    return axios
      .post(API_URL + "experiment/save", {
        'id': props.experiment.id,
        'dataset_id': currentDataset ? currentDataset.id : null,
        'result_id': currentResult ? currentResult.id : null,
        'model': 'linear'
      })
      .then(response => {
        if (response.data) {
          props.refreshExperiments();
          handleDetailDialogClose();
        }
      }, error => {
        if (error.response.data.msg) alert(error.response.data.msg);
      });
  };

  React.useEffect(() => {
    const getDatasets = () => {
      return axios
        .get(API_URL + "project/datasets?id=" + props.experiment.project.id)
        .then(response => {
          if (response.data) {
            SetDatasets(response.data);
          }
        }, error => {
          if (error.response.data.msg) alert(error.response.data.msg);
          SetDatasets([]);
        });
    };
    getDatasets();
  }, [props.experiment.project.id]);

  const handleDetailDialogClose = () => {
    props.onClose();
  };

  const handleDatasetChange = (e) => {
    const record = datasets.find((item) => {
      return item.id === e.target.value
    });
    setCurrentDataset(record);
    setCurrentDatasetVisualizationPath(record.visualization_path);
    setCurrentResult(null);
  };

  return (
    <>
      <Dialog
        fullScreen
        open={true}
        onClose={handleDetailDialogClose}
      >
        <AppBar sx={{ position: 'relative' }}>
          <Toolbar>
            <IconButton
              edge="start"
              color="inherit"
              onClick={handleDetailDialogClose}
              aria-label="close"
            >
              <CloseIcon />
            </IconButton>
            <Typography sx={{ ml: 2, flex: 1 }} variant="h6" component="div">
              {props.experiment.name}
            </Typography>
            <Button autoFocus color="inherit" onClick={handleSave}>
              Save
            </Button>
          </Toolbar>
        </AppBar>

        <Paper elevation={0} key="step1" style={{ margin: '1rem' }}>
          <Typography component="p" variant="h6" color="primary" gutterBottom>
            Step 1. Select a dataset
          </Typography>
          <FormControl variant="standard" sx={{ m: 1, minWidth: 120 }}>
            <InputLabel id="dataset-select-label">Dataset</InputLabel>
            <Select
              labelId="dataset-select-label"
              value={currentDataset ? currentDataset.id : ''}
              onChange={handleDatasetChange}
              label="Select a dataset"
            >
              {
                datasets.map(record => (record.upload_time && (record.row_count > 0)) ?
                  <MenuItem key={record.id} value={record.id}>{record.id + '. ' + record.name + '(' + record.row_count + ' rows)'}</MenuItem>
                  :
                  null)
              }
            </Select>
          </FormControl>
        </Paper>

        <Divider />

        <Paper elevation={0} key="step2" style={{ margin: '1rem' }}>
          <Typography component="p" variant="h6" color="primary" gutterBottom>
            Step 2. Visualize the dataset
          </Typography>
          {
            currentDataset ?
              (
                currentDatasetVisualizationPath ?
                  <img alt="visualization" style={{ height: '20rem' }} src={API_URL + currentDatasetVisualizationPath} />
                  :
                  <Button variant="contained" onClick={handleDatasetVisualize}>Visualize</Button>
              )
              :
              <Typography component="p" variant="p" color="secondary">Please finish the previous step.</Typography>
          }
        </Paper>
        <Divider />
        <Paper elevation={0} key="step3" style={{ margin: '1rem' }}>
          <Typography component="p" variant="h6" color="primary" gutterBottom>
            Step 3. Fit a linear model
          </Typography>
          {
            currentDatasetVisualizationPath ?
              (
                currentResult ?
                  (
                    currentResult.finish_time ?
                      (
                        <Typography component="p" variant="p" color="secondary">
                          {'Computation started at ' + currentResult.create_time}<br />
                          {'Computation finished at ' + currentResult.finish_time}<br />
                          {'Computation result: ' + currentResult.result_text}<br />
                          To simulate huge datasets, I used multithreading technology and placed a "sleep(5)" in the computation function, so you see a 5-second delay .
                        </Typography>
                      )
                      :
                      (
                        <Typography component="p" variant="p" color="secondary">
                          {'Computation started at ' + currentResult.create_time}<br />
                          To simulate huge datasets, I used multithreading technology and placed a "sleep(5)" in the computation function. Please wait 5 seconds for the app to fetch the result asynchronously.
                        </Typography>
                      )
                  )
                  :
                  <Button variant="contained" onClick={handleFitLinear}>Fit</Button>
              )
              :
              <Typography component="p" variant="p" color="secondary">Please finish the previous step.</Typography>
          }
        </Paper>

        <Divider />

        <Paper elevation={0} key="step4" style={{ margin: '1rem' }}>
          <Typography component="p" variant="h6" color="primary" gutterBottom>
            Step 4. Visualize the result
          </Typography>
          {
            currentResult && currentResult.finish_time ?
              (
                currentResult.visualization_path ?
                  <img alt="visualization" style={{ height: '20rem' }} src={API_URL + currentResult.visualization_path} />
                  :
                  <Button variant="contained" onClick={handleResultVisualize}>Visualize</Button>
              )
              :
              <Typography component="p" variant="p" color="secondary">Please finish the previous step.</Typography>
          }
        </Paper>

        <Divider />

        <Paper elevation={0} key="step5" style={{ margin: '1rem' }}>
          <Button variant="contained" onClick={handleSave}>Save</Button>
        </Paper>

      </Dialog>
    </>
  );
}

export default ExperimentDetail;
