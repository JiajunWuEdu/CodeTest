import * as React from 'react';
import axios from "axios";
import ManageTable from '../tool/ManageTable';
import {API_URL} from '../../config.js';
import ExperimentControl from './ExperimentControl';

function ExperimentTable({projectId}) {
    const [records,SetRescords] = React.useState([]);
    const theads = {'id' : 'ID', 'name' : 'Name', 'update_time' : 'Update Time'};
    const getRecords = React.useCallback(() => {
        axios
        .get(API_URL + "project/experiments?id="+projectId)
        .then(response => {
            if (response.data) {
                SetRescords(response.data);
            }
        },error=>{
            if(error.response.data.msg) alert(error.response.data.msg);
            SetRescords([]);
        });
    },[projectId]);

    React.useEffect(()=>{
        getRecords();
    },[getRecords]);

    const handleCreate = newName => {
        axios
            .post(API_URL + "experiment/create", { "name": newName, "project_id": projectId })
            .then(response => {
                if (response.data) {
                    getRecords();
                }
            }, error => {
                if (error.response.data.msg) alert(error.response.data.msg);
                getRecords();
            });
    };
  
  return (
    <>
    <ManageTable title="Experiments" theads={theads} records={records} getRecords={getRecords} control={ExperimentControl} create={handleCreate}/>
    </>
  );
}


export default ExperimentTable;
